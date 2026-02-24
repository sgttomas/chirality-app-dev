'use client';

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode
} from 'react';
import type { HarnessOpts } from '../../lib/harness/types';
import {
  buildHarnessOptsFromToolkit,
  createToolkitPreset,
  defaultToolkitState,
  defaultToolkitValues,
  sanitizeToolkitState,
  TOOLKIT_STORAGE_KEY,
  upsertToolkitPreset,
  type ToolkitPreset,
  type ToolkitValues
} from '../../lib/harness/toolkit';

type ToolkitContextValue = {
  hydrated: boolean;
  isToolkitVisible: boolean;
  setToolkitVisible: (visible: boolean) => void;
  values: ToolkitValues;
  updateValues: (patch: Partial<ToolkitValues>) => void;
  resetValues: () => void;
  optsPayload: HarnessOpts | undefined;
  presets: ToolkitPreset[];
  selectedPresetId: string | null;
  selectPreset: (presetId: string) => void;
  applySelectedPreset: () => void;
  savePreset: (name: string) => boolean;
  deleteSelectedPreset: () => void;
};

const ToolkitContext = createContext<ToolkitContextValue | null>(null);

export function ToolkitProvider({ children }: { children: ReactNode }): JSX.Element {
  const [state, setState] = useState(defaultToolkitState());
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }

    try {
      const raw = window.localStorage.getItem(TOOLKIT_STORAGE_KEY);
      if (raw) {
        setState(sanitizeToolkitState(JSON.parse(raw)));
      }
    } catch {
      setState(defaultToolkitState());
    } finally {
      setHydrated(true);
    }
  }, []);

  useEffect(() => {
    if (!hydrated || typeof window === 'undefined') {
      return;
    }

    window.localStorage.setItem(TOOLKIT_STORAGE_KEY, JSON.stringify(state));
  }, [state, hydrated]);

  const optsPayload = useMemo(() => buildHarnessOptsFromToolkit(state.values), [state.values]);

  useEffect(() => {
    if (!hydrated) {
      return;
    }
    const payload = optsPayload ? JSON.stringify(optsPayload) : '(empty)';
    console.info(`[toolkit] opts changed: ${payload}`);
  }, [optsPayload, hydrated]);

  const setToolkitVisible = useCallback((visible: boolean) => {
    setState((existing) => ({
      ...existing,
      visible
    }));
  }, []);

  const updateValues = useCallback((patch: Partial<ToolkitValues>) => {
    setState((existing) => ({
      ...existing,
      values: {
        ...existing.values,
        ...patch
      }
    }));
  }, []);

  const resetValues = useCallback(() => {
    setState((existing) => ({
      ...existing,
      values: defaultToolkitValues()
    }));
  }, []);

  const selectPreset = useCallback((presetId: string) => {
    setState((existing) => ({
      ...existing,
      selectedPresetId: presetId || null
    }));
  }, []);

  const applySelectedPreset = useCallback(() => {
    setState((existing) => {
      if (!existing.selectedPresetId) {
        return existing;
      }

      const selected = existing.presets.find((preset) => preset.id === existing.selectedPresetId);
      if (!selected) {
        return {
          ...existing,
          selectedPresetId: null
        };
      }

      return {
        ...existing,
        values: selected.values
      };
    });
  }, []);

  const savePreset = useCallback((name: string): boolean => {
    const normalizedName = name.trim();
    if (!normalizedName) {
      return false;
    }

    const nextPreset = createToolkitPreset(normalizedName, state.values);
    setState((existing) => ({
      ...existing,
      presets: upsertToolkitPreset(existing.presets, nextPreset),
      selectedPresetId: nextPreset.id
    }));
    return true;
  }, [state.values]);

  const deleteSelectedPreset = useCallback(() => {
    setState((existing) => {
      if (!existing.selectedPresetId) {
        return existing;
      }

      return {
        ...existing,
        presets: existing.presets.filter((preset) => preset.id !== existing.selectedPresetId),
        selectedPresetId: null
      };
    });
  }, []);

  const value = useMemo<ToolkitContextValue>(
    () => ({
      hydrated,
      isToolkitVisible: state.visible,
      setToolkitVisible,
      values: state.values,
      updateValues,
      resetValues,
      optsPayload,
      presets: state.presets,
      selectedPresetId: state.selectedPresetId,
      selectPreset,
      applySelectedPreset,
      savePreset,
      deleteSelectedPreset
    }),
    [
      hydrated,
      state.visible,
      state.values,
      state.presets,
      state.selectedPresetId,
      setToolkitVisible,
      updateValues,
      resetValues,
      optsPayload,
      selectPreset,
      applySelectedPreset,
      savePreset,
      deleteSelectedPreset
    ]
  );

  return <ToolkitContext.Provider value={value}>{children}</ToolkitContext.Provider>;
}

export function useToolkit(): ToolkitContextValue {
  const value = useContext(ToolkitContext);
  if (!value) {
    throw new Error('useToolkit must be used inside ToolkitProvider');
  }
  return value;
}
