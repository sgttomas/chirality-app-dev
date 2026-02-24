import {
  asNonEmptyString,
  parseAgentClass,
  parseAgentType,
  parseCommaSeparatedList,
  parseFrontmatter,
  readAgentInstruction,
  tryReadAgentInstruction
} from './agent-instruction';

export type GovernanceGateId =
  | 'ENVIRONMENT'
  | 'PERSONA_ALLOWLIST'
  | 'METADATA_PRESENCE'
  | 'CONTEXT_SEALED'
  | 'PIPELINE_RUN_APPROVED'
  | 'APPROVAL_REF'
  | 'INTERNAL_ERROR'
  | 'ALLOW';

export type SubagentGovernanceDecision = {
  allowed: boolean;
  gate: GovernanceGateId;
  reason: string;
  allowlistedSubagents: string[];
  delegatedSubagents: string[];
  approvalRef?: string;
  approvedBy?: string;
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function normalizeSubagentList(rawSubagents: unknown): string[] {
  const parsed = parseCommaSeparatedList(rawSubagents);
  const unique = new Set<string>();

  for (const candidate of parsed) {
    const normalized = candidate.trim();
    if (normalized.length > 0) {
      unique.add(normalized);
    }
  }

  return [...unique];
}

function deny(
  gate: Exclude<GovernanceGateId, 'ALLOW'>,
  reason: string,
  allowlistedSubagents: string[]
): SubagentGovernanceDecision {
  return {
    allowed: false,
    gate,
    reason,
    allowlistedSubagents,
    delegatedSubagents: []
  };
}

function logDecision(persona: string, decision: SubagentGovernanceDecision): void {
  if (decision.allowed) {
    const subagentSummary =
      decision.delegatedSubagents.length > 0 ? decision.delegatedSubagents.join(',') : 'none';
    const approvedByPart = decision.approvedBy ? ` approvedBy=${decision.approvedBy}` : '';
    console.info(
      `[harness/subagent-governance] ALLOW persona=${persona} gate=${decision.gate} delegated=${subagentSummary} approvalRef=${decision.approvalRef ?? ''}${approvedByPart}`
    );
    return;
  }

  console.info(
    `[harness/subagent-governance] DENY persona=${persona} gate=${decision.gate} reason=${decision.reason}`
  );
}

function formatAgentType(agentType: number | undefined): string {
  if (typeof agentType === 'number') {
    return `TYPE ${agentType}`;
  }
  return 'missing';
}

async function resolveDelegatedSubagents(
  subagents: string[],
  instructionRoot: string
): Promise<string[]> {
  const delegated: string[] = [];

  for (const subagentName of subagents) {
    const instruction = await tryReadAgentInstruction(subagentName, instructionRoot);
    if (!instruction) {
      console.error(
        `[harness/subagent-governance] Candidate subagent rejected: ${subagentName} instruction file not found.`
      );
      continue;
    }

    const agentType = parseAgentType(instruction.content);
    if (agentType !== 2) {
      console.error(
        `[harness/subagent-governance] Candidate subagent rejected: ${subagentName} declares AGENT_TYPE=${formatAgentType(
          agentType
        )}; expected TYPE 2.`
      );
      continue;
    }

    const agentClass = parseAgentClass(instruction.content);
    if (agentClass !== 'TASK') {
      const renderedClass = agentClass ?? 'missing';
      console.warn(
        `[harness/subagent-governance] Candidate subagent warning: ${subagentName} declares AGENT_CLASS=${renderedClass}; TASK is preferred.`
      );
    }

    delegated.push(subagentName);
  }

  return delegated;
}

export async function evaluateSubagentGovernance(
  persona: string,
  subagentGovernance: unknown,
  env: NodeJS.ProcessEnv = process.env
): Promise<SubagentGovernanceDecision> {
  let allowlistedSubagents: string[] = [];

  try {
    const personaInstruction = await readAgentInstruction(persona);
    const frontmatter = parseFrontmatter(personaInstruction.content, {
      warnPrefix: '[harness/subagent-governance]'
    });
    allowlistedSubagents = normalizeSubagentList(frontmatter.subagents);

    if (env.CHIRALITY_ENABLE_SUBAGENTS !== 'true') {
      const denied = deny(
        'ENVIRONMENT',
        'CHIRALITY_ENABLE_SUBAGENTS is not set to "true".',
        allowlistedSubagents
      );
      logDecision(persona, denied);
      return denied;
    }

    if (allowlistedSubagents.length === 0) {
      const denied = deny(
        'PERSONA_ALLOWLIST',
        'Active persona is not allowlisted for subagents.',
        allowlistedSubagents
      );
      logDecision(persona, denied);
      return denied;
    }

    if (!isRecord(subagentGovernance)) {
      const denied = deny(
        'METADATA_PRESENCE',
        'opts.subagentGovernance is missing or invalid.',
        allowlistedSubagents
      );
      logDecision(persona, denied);
      return denied;
    }

    if (subagentGovernance.contextSealed !== true) {
      const denied = deny(
        'CONTEXT_SEALED',
        'contextSealed must be strictly true.',
        allowlistedSubagents
      );
      logDecision(persona, denied);
      return denied;
    }

    if (subagentGovernance.pipelineRunApproved !== true) {
      const denied = deny(
        'PIPELINE_RUN_APPROVED',
        'pipelineRunApproved must be strictly true.',
        allowlistedSubagents
      );
      logDecision(persona, denied);
      return denied;
    }

    const approvalRef = asNonEmptyString(subagentGovernance.approvalRef);
    if (!approvalRef) {
      const denied = deny(
        'APPROVAL_REF',
        'approvalRef must be a non-empty string.',
        allowlistedSubagents
      );
      logDecision(persona, denied);
      return denied;
    }

    const approvedBy = asNonEmptyString(subagentGovernance.approvedBy);
    const delegatedSubagents = await resolveDelegatedSubagents(
      allowlistedSubagents,
      personaInstruction.instructionRoot
    );
    const allowed: SubagentGovernanceDecision = {
      allowed: true,
      gate: 'ALLOW',
      reason: 'All delegation governance gates passed.',
      allowlistedSubagents,
      delegatedSubagents,
      approvalRef,
      approvedBy
    };

    logDecision(persona, allowed);
    return allowed;
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown gate evaluation failure.';
    const denied = deny('INTERNAL_ERROR', message, allowlistedSubagents);
    logDecision(persona, denied);
    return denied;
  }
}
