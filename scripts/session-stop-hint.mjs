#!/usr/bin/env node
// Passive Stop hint. Do not block the session.
// If the session produced eval output or a claim about AI behaviour,
// remind the operator that a signed card is evidence, a score is not approval.
process.stderr.write(
  "[council-of-ai] If this session made a behaviour claim, verify or sign it. Empty cells stay empty. https://councilof.ai/verify\n"
);
process.exit(0);
