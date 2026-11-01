---
name: idea-factory
description: >
  Synthesize, score, and validate profitable B2B SaaS and AI-Native Service product
  ideas grounded in Claude_Skills_Project and Business_Analyzer_Project. Use when
  the user asks to generate product ideas, run the 5-hour autonomous idea loop,
  score a startup concept with Israelsen risk-adjusted ROI and Weibull survival math,
  or answer the 14 investor diligence questions across Product, Market, Business Model,
  Financials, and Team.
argument-hint: "[seed | generate-one | run --hours 5.0 | verify]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(python3 -m idea_factory *)
---

# Idea Factory Skill

Generate, score, and validate startup and product ideas using the actuarial survival
models from `Business_Analyzer_Project` and the engineering primitives from `Claude_Skills_Project`.

## Workflow

1. **Seed & Synchronize Catalog:**
   ```bash
   python3 -m idea_factory seed
   ```
2. **Generate a New Product Idea On Demand:**
   ```bash
   python3 -m idea_factory generate-one
   ```
3. **Run the 5-Hour Continuous Credit-Window Loop:**
   ```bash
   python3 -m idea_factory run --hours 5.0 --interval 45
   ```
4. **Mandatory Self-Verification Gate:**
   Every run must close with deterministic verification of all 14 diligence questions and
   actuarial invariants:
   ```bash
   python3 -m idea_factory verify
   ```
   Confirm the output ends with `RESULT: PASS`.

