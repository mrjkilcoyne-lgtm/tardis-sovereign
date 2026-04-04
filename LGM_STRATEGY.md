# LGM: The Sovereign Swarm Strategy

## Project Overview
A **Locally Hosted Large Grammar Model (LGM)** framework designed for "British Sovereign AI." This project leverages local compute (Android/Desktop) to provide a private, culturally grounded, and linguistically precise AI experience.

## Core Pillars
1. **Sovereign Knowledge:** Grounded in the `TardAI` "British Source Code" graph.
2. **Grammar Constraints:** Using GBNF-style constraints to enforce regional dialects (Welsh, Scots, Scouse) and structured logic (UK Law, Consumer Rights).
3. **Agentic Swarm:** A multi-agent orchestration layer where specialized agents handle Intent, Research, and Drafting.

## Architecture
- **Engine (Kotlin/MediaPipe):** Runs GGUF models on-device with custom `GrammarConstraint` masking.
- **Knowledge Base (React/TypeScript Graph):** Exported as a vector/graph DB for local RAG.
- **Orchestration:**
    - **Registrar Agent:** Uses a "Dialect Grammar" to detect and respond in the user's regional style.
    - **Surveyor Agent:** Queries the `cultureGraph` nodes for grounding.
    - **Drafter Agent:** Uses a "Sovereign Grammar" to ensure outputs are legally and culturally compliant.

## Inspirations
- **GB1.ai:** British-first, regional language support, eco-conscious (local compute).
- **mrjkilcoyne-lgtm (GitHub):** Local-first, survival tech, consumer empowerment (`CLAIMOUR`).

## Roadmap
- [ ] Export `cultureGraph.ts` to JSONL for local RAG.
- [ ] Implement `RegionalGrammar.kt` for dialect enforcement.
- [ ] Build the `SwarmOrchestrator` in Kotlin.
- [ ] Integrate `TardAI` UI as the "Command Center" for the swarm.
