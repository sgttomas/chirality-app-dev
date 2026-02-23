#!/usr/bin/env node

import { execSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdir, readdir, readFile, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';

const REQUIRED_ROOT_FILES = [
  'AGENTS.md',
  'README.md',
  'WHAT-IS-AN-AGENT.md',
  'PROFESSIONAL_ENGINEERING.md'
];

const REQUIRED_DOC_FILES = ['DIRECTIVE.md', 'CONTRACT.md', 'SPEC.md', 'TYPES.md', 'PLAN.md'];

function toPosix(relativePath) {
  return relativePath.split(path.sep).join('/');
}

function nowIso() {
  return new Date().toISOString();
}

function printUsage() {
  console.log(`Usage: node ./scripts/verify-instruction-root-integrity.mjs [options]

Options:
  --source-root <path>   Source instruction-root root (default: ../)
  --bundle-root <path>   Packaged Resources root (default: dist/mac-arm64/Chirality.app/Contents/Resources)
  --output-root <path>   Output directory for manifest + summary (default: artifacts/harness/instruction-root-integrity/latest)
  --help                 Show this message
`);
}

function readArgValue(argv, index, flagName) {
  const value = argv[index];
  if (!value || value.startsWith('--')) {
    throw new Error(`Missing value for ${flagName}`);
  }
  return value;
}

function parseArgs(argv) {
  const options = {};

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (token === '--help') {
      options.help = true;
      continue;
    }

    if (token === '--source-root') {
      options.sourceRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--bundle-root') {
      options.bundleRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--output-root') {
      options.outputRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    throw new Error(`Unknown argument: ${token}`);
  }

  return options;
}

async function sha256ForFile(absolutePath) {
  const fileBuffer = await readFile(absolutePath);
  const fileStat = await stat(absolutePath);
  if (!fileStat.isFile()) {
    throw new Error(`Expected a file but found non-file entry: ${absolutePath}`);
  }
  return {
    sha256: createHash('sha256').update(fileBuffer).digest('hex'),
    sizeBytes: fileStat.size
  };
}

function readGitSha(sourceRoot) {
  try {
    return execSync('git rev-parse HEAD', {
      cwd: sourceRoot,
      stdio: ['ignore', 'pipe', 'ignore']
    })
      .toString('utf8')
      .trim();
  } catch {
    return null;
  }
}

async function listSourceAgentFiles(sourceRoot) {
  const agentsDirectory = path.join(sourceRoot, 'agents');
  const entries = await readdir(agentsDirectory, { withFileTypes: true });

  const agentFiles = entries
    .filter((entry) => entry.isFile() && /^AGENT_.*\.md$/.test(entry.name))
    .map((entry) => toPosix(path.join('agents', entry.name)))
    .sort();

  if (agentFiles.length === 0) {
    throw new Error(`No AGENT_*.md files were found in ${agentsDirectory}`);
  }

  return agentFiles;
}

async function listBundleAgentFiles(bundleRoot) {
  const agentsDirectory = path.join(bundleRoot, 'agents');
  let entries = [];
  try {
    entries = await readdir(agentsDirectory, { withFileTypes: true });
  } catch {
    return [];
  }

  return entries
    .filter((entry) => entry.isFile() && /^AGENT_.*\.md$/.test(entry.name))
    .map((entry) => toPosix(path.join('agents', entry.name)))
    .sort();
}

async function buildSourceManifest(sourceRoot) {
  const sourceAgentFiles = await listSourceAgentFiles(sourceRoot);
  const relativePaths = [
    ...REQUIRED_ROOT_FILES,
    ...REQUIRED_DOC_FILES.map((fileName) => toPosix(path.join('docs', fileName))),
    ...sourceAgentFiles
  ];

  const entries = [];
  for (const relativePath of relativePaths) {
    const absolutePath = path.join(sourceRoot, relativePath);
    const digest = await sha256ForFile(absolutePath);
    entries.push({
      path: relativePath,
      sha256: digest.sha256,
      sizeBytes: digest.sizeBytes
    });
  }

  return entries;
}

async function verifyManifestAgainstBundle({ manifestEntries, bundleRoot }) {
  const missingInBundle = [];
  const mismatchedFiles = [];
  const comparisons = [];

  for (const entry of manifestEntries) {
    const bundleFilePath = path.join(bundleRoot, entry.path);
    try {
      const bundleDigest = await sha256ForFile(bundleFilePath);
      const hashesMatch = bundleDigest.sha256 === entry.sha256;

      comparisons.push({
        path: entry.path,
        sourceSha256: entry.sha256,
        bundleSha256: bundleDigest.sha256,
        sourceSizeBytes: entry.sizeBytes,
        bundleSizeBytes: bundleDigest.sizeBytes,
        match: hashesMatch
      });

      if (!hashesMatch) {
        mismatchedFiles.push({
          path: entry.path,
          sourceSha256: entry.sha256,
          bundleSha256: bundleDigest.sha256
        });
      }
    } catch {
      missingInBundle.push(entry.path);
    }
  }

  const sourceAgentSet = new Set(
    manifestEntries.filter((entry) => entry.path.startsWith('agents/')).map((entry) => entry.path)
  );
  const bundleAgentFiles = await listBundleAgentFiles(bundleRoot);
  const unexpectedBundleAgentFiles = bundleAgentFiles.filter((entry) => !sourceAgentSet.has(entry));

  return {
    missingInBundle,
    mismatchedFiles,
    unexpectedBundleAgentFiles,
    comparisons
  };
}

async function writeJson(filePath, value) {
  await writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printUsage();
    return;
  }

  const sourceRoot = path.resolve(args.sourceRoot ?? path.resolve(process.cwd(), '..'));
  const bundleRoot = path.resolve(
    args.bundleRoot ?? path.join(process.cwd(), 'dist', 'mac-arm64', 'Chirality.app', 'Contents', 'Resources')
  );
  const outputRoot = path.resolve(
    args.outputRoot ??
      path.join(process.cwd(), 'artifacts', 'harness', 'instruction-root-integrity', 'latest')
  );

  await mkdir(outputRoot, { recursive: true });

  const manifestEntries = await buildSourceManifest(sourceRoot);
  const verification = await verifyManifestAgainstBundle({
    manifestEntries,
    bundleRoot
  });

  const status =
    verification.missingInBundle.length === 0 &&
    verification.mismatchedFiles.length === 0 &&
    verification.unexpectedBundleAgentFiles.length === 0
      ? 'pass'
      : 'fail';

  const gitSha = readGitSha(sourceRoot);
  const manifest = {
    generatedAt: nowIso(),
    gitSha,
    sourceRoot,
    files: manifestEntries
  };

  const summary = {
    generatedAt: nowIso(),
    gitSha,
    sourceRoot,
    bundleRoot,
    checkedFileCount: manifestEntries.length,
    status,
    missingInBundle: verification.missingInBundle,
    mismatchedFiles: verification.mismatchedFiles,
    unexpectedBundleAgentFiles: verification.unexpectedBundleAgentFiles,
    comparisons: verification.comparisons
  };

  await writeJson(path.join(outputRoot, 'manifest.json'), manifest);
  await writeJson(path.join(outputRoot, 'summary.json'), summary);

  console.log(`instruction-root integrity status: ${status}`);
  console.log(`checked files: ${manifestEntries.length}`);
  if (gitSha) {
    console.log(`git sha: ${gitSha}`);
  } else {
    console.log('git sha: unavailable');
  }
  console.log(`manifest: ${path.join(outputRoot, 'manifest.json')}`);
  console.log(`summary: ${path.join(outputRoot, 'summary.json')}`);

  if (status !== 'pass') {
    if (verification.missingInBundle.length > 0) {
      console.error(`Missing in bundle (${verification.missingInBundle.length}):`);
      for (const filePath of verification.missingInBundle) {
        console.error(`  - ${filePath}`);
      }
    }
    if (verification.mismatchedFiles.length > 0) {
      console.error(`Hash mismatches (${verification.mismatchedFiles.length}):`);
      for (const entry of verification.mismatchedFiles) {
        console.error(`  - ${entry.path}`);
      }
    }
    if (verification.unexpectedBundleAgentFiles.length > 0) {
      console.error(`Unexpected bundled agent files (${verification.unexpectedBundleAgentFiles.length}):`);
      for (const filePath of verification.unexpectedBundleAgentFiles) {
        console.error(`  - ${filePath}`);
      }
    }

    process.exitCode = 1;
  }
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`instruction-root integrity verification failed: ${message}`);
  process.exitCode = 1;
});
