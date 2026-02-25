'use client';

import { useCallback, useEffect, useState } from 'react';

type ApiKeyStatus = {
  hasKey: boolean;
  encryptionAvailable: boolean;
  source: 'ui' | 'env' | 'none';
};

type ApiKeyStoreResult = {
  ok: boolean;
  error?: string;
};

type ChiralityApiKeyBridge = {
  store: (key: string) => Promise<ApiKeyStoreResult>;
  remove: () => Promise<ApiKeyStoreResult>;
  status: () => Promise<ApiKeyStatus>;
};

type ChiralityWindow = typeof window & {
  chirality?: {
    apiKey?: ChiralityApiKeyBridge;
  };
};

function getApiKeyBridge(): ChiralityApiKeyBridge | undefined {
  if (typeof window === 'undefined') {
    return undefined;
  }
  return (window as ChiralityWindow).chirality?.apiKey;
}

export function ApiKeySettings(): JSX.Element {
  const [keyInput, setKeyInput] = useState('');
  const [revealed, setRevealed] = useState(false);
  const [status, setStatus] = useState<ApiKeyStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [bridgeAvailable, setBridgeAvailable] = useState(false);

  const refreshStatus = useCallback(async () => {
    const bridge = getApiKeyBridge();
    if (!bridge) {
      setBridgeAvailable(false);
      return;
    }

    setBridgeAvailable(true);
    try {
      const result = await bridge.status();
      setStatus(result);
    } catch {
      setStatus(null);
    }
  }, []);

  useEffect(() => {
    void refreshStatus();
  }, [refreshStatus]);

  async function handleSave(): Promise<void> {
    const bridge = getApiKeyBridge();
    if (!bridge) {
      setError('Secure storage is not available (not running in Electron)');
      return;
    }

    const trimmed = keyInput.trim();
    if (!trimmed) {
      setError('Please enter an API key');
      return;
    }

    setSaving(true);
    setError(null);

    try {
      const result = await bridge.store(trimmed);
      if (!result.ok) {
        setError(result.error ?? 'Failed to save key');
        return;
      }

      setKeyInput('');
      setRevealed(false);
      await refreshStatus();
    } catch {
      setError('Failed to save key. Check system storage availability.');
    } finally {
      setSaving(false);
    }
  }

  async function handleRemove(): Promise<void> {
    const bridge = getApiKeyBridge();
    if (!bridge) {
      return;
    }

    setError(null);

    try {
      const result = await bridge.remove();
      if (!result.ok) {
        setError(result.error ?? 'Failed to remove key');
        return;
      }

      await refreshStatus();
    } catch {
      setError('Failed to remove key');
    }
  }

  const sourceLabel =
    status?.source === 'ui'
      ? 'Key configured (stored in secure storage)'
      : status?.source === 'env'
        ? 'Key configured (from environment variable)'
        : 'No API key configured';

  const encryptionWarning =
    status && !status.encryptionAvailable
      ? 'Secure storage is not available on this platform. Use the ANTHROPIC_API_KEY environment variable instead.'
      : null;

  return (
    <div className="api-key-settings">
      <h3 className="api-key-settings-title">Anthropic API Key</h3>

      <p className="api-key-status" data-source={status?.source ?? 'unknown'}>
        {status ? sourceLabel : 'Checking...'}
      </p>

      {encryptionWarning ? (
        <p className="api-key-warning">{encryptionWarning}</p>
      ) : null}

      {bridgeAvailable && status?.encryptionAvailable !== false ? (
        <>
          <div className="api-key-input-row">
            <input
              type={revealed ? 'text' : 'password'}
              className="api-key-input"
              value={keyInput}
              onChange={(e) => {
                setKeyInput(e.target.value);
                if (error) {
                  setError(null);
                }
              }}
              placeholder="sk-ant-..."
              autoComplete="off"
              autoCorrect="off"
              autoCapitalize="off"
              spellCheck={false}
              data-lpignore="true"
              data-1p-ignore="true"
            />
            <button
              type="button"
              className="button-muted"
              onClick={() => {
                setRevealed(!revealed);
              }}
            >
              {revealed ? 'Hide' : 'Reveal'}
            </button>
            <button
              type="button"
              onClick={() => void handleSave()}
              disabled={saving || !keyInput.trim()}
            >
              {saving ? 'Saving...' : 'Save Key'}
            </button>
          </div>

          {status?.source === 'ui' ? (
            <button
              type="button"
              className="button-muted api-key-remove"
              onClick={() => void handleRemove()}
            >
              Remove Stored Key
            </button>
          ) : null}
        </>
      ) : null}

      {!bridgeAvailable ? (
        <p className="api-key-hint">
          Running outside Electron. Set the <code>ANTHROPIC_API_KEY</code> environment variable
          to configure the API key.
        </p>
      ) : null}

      {error ? <p className="api-key-error">{error}</p> : null}
    </div>
  );
}
