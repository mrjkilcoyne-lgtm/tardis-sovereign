# THE PLAN: TARDIS Sovereign Ecosystem
## A First-Principles Bootstrapper's Guide for the Majestic Fool
### Matthew Kilcoyne — April 2026

---

## PART 1: WHAT YOU'RE ACTUALLY BUILDING

You're not building one app. You're building an **ecosystem** — a self-reinforcing network of tools, platforms, and revenue streams that feed each other. Here's the honest map of what's across your 34 repos and 30 starred projects:

### The Stack (Bottom to Top)

```
LAYER 4: REVENUE STREAMS (Apps that make money)
  InventorForge    — invention-to-patent pipeline (SaaS)
  Hex Inventions   — daily viral teardowns (audience + ads)
  COMBOT           — competition entries + Qubic mining (crypto)
  Vex-Lang         — crypto trading DSL (tool licensing)
  BAKK Online      — CANZUK social platform (community/subscriptions)
  ClaimourLife     — digital rights toolkit (freemium)
  FutureSpeak      — language learning (ed-tech)
  TheBrunelEngine  — frustration-to-insight interviews (B2B consulting tool)
  nssLocalWebBuilder — drag-and-drop website builder (SaaS)

LAYER 3: AI & INTELLIGENCE
  LGM              — Large Grammar Model (your custom AI brain)
  Block Prophet     — MCTS inference reasoning engine
  The Luggage       — autonomous AI agent platform (MCP-native)
  + SakanaAI AI-Scientist-v2 (starred — automated research)
  + LangChain (starred — agent engineering)
  + oh-my-claudecode (starred — multi-agent Claude orchestration)

LAYER 2: INFRASTRUCTURE
  TARDIS Sovereign  — THIS REPO — K3s on Civo Cloud (LON1)
  + Tailscale (starred — secure networking/VPN)
  + NixOS (starred — reproducible deployments)
  + Immich (starred — self-hosted media)
  + changedetection.io (starred — monitoring)

LAYER 1: SECURITY & IDENTITY
  MKAngel           — Android incident tracking/security
  Sentinel          — "the good stuff"
  KilcoyneWatcher   — monitoring
  Digital ID Holder — identity management
  + Sherlock (starred — OSINT)
  + TruffleHog (starred — credential scanning)
  + Security awesome-lists (starred)
```

### The Secret Weapon: The IGOR Protocol (Hex Inventions Agent Swarm)

This isn't just a blog. It's a **7-agent AI swarm** themed on Discworld characters, running a structured reverse-engineering methodology:

| Agent | Role | Discworld Reference |
|-------|------|-------------------|
| **Igor** | Orchestrator — picks target, routes swarm | The loyal servant |
| **Tiffany** | Observer — "First Sight," sees what's really there | Tiffany Aching |
| **Vimes** | Forensics — follows the money | Sam Vimes |
| **Death** | Classifier — SEES THE TRUTH OF THINGS | Death himself |
| **Nanny** | Cross-Reference — connects dots across domains | Nanny Ogg |
| **Granny** | Transformer — "I can't be having with this" | Granny Weatherwax |
| **Ridcully** | Verifier — blunt, direct, tests everything | Archchancellor Ridcully |

**The IGOR Protocol (6 phases):** OBSERVE → DECOMPOSE → MAP → HYPOTHESIZE → VERIFY → TRANSCEND

Each cycle produces: a full case study, reverse-engineering findings, a new invention design, AND a UK IPO patent draft. **This pipeline feeds directly into InventorForge.**

First invention: **GRANNY** — an edge-AI food sovereignty system that replaces Samsung's $3,500 cloud-dependent smart fridge with on-device inference, 5 sensor modalities, zero ads, open protocol. Additional BOM cost: ~$14. Estimated food waste savings: $230-305/year per household. Payback: 17 days.

*Every file ends with `X-Clacks-Overhead: GNU Terry Pratchett`*

### The Thesis

Everything connects. The TARDIS (this K3s cluster) hosts the services. LGM provides the AI. The Luggage orchestrates agents. Hex Inventions runs the IGOR Protocol swarm to generate inventions. InventorForge turns those into patents. The revenue apps run on top. Security tools protect the lot. **One person, one cluster, many products.**

---

## PART 2: THE PHYSICAL ENVIRONMENT

### Option A: Cloud-Only (Recommended to START)

**Civo Cloud — Your current setup. Smart choice.**

| What | Spec | Monthly Cost |
|------|------|-------------|
| K3s Small node (g4s.kube.small) | 1 CPU, 2GB RAM, 40GB NVMe | **$10.86** |
| K3s Medium node (upgrade path) | 2 CPU, 4GB RAM, 50GB NVMe | **$21.73** |
| K3s Large node (when revenue hits) | 4 CPU, 8GB RAM, 60GB NVMe | **$43.45** |

**CLEVER FIX #1:** Civo gives **$250 free credit** to new accounts. That's ~23 months of a Small node FOR FREE. Sign up, add a card, claim it. If you burn through it, make a second account for a different project.

**CLEVER FIX #2:** Run your non-production workloads (dev, staging, testing) on a **free Oracle Cloud ARM instance** (4 OCPU, 24GB RAM, always free tier). Use Civo only for production.

### Option B: Home Server (When You're Ready)

**The Raspberry Pi 5 K3s Cluster**

| Item | Cost (UK) | Notes |
|------|-----------|-------|
| Raspberry Pi 5 8GB | ~£80 | The brain |
| 256GB NVMe SSD + HAT | ~£35 | MANDATORY — SD cards will die under K3s etcd writes |
| 27W USB-C PSU | ~£12 | Official Pi PSU |
| Cat6 Ethernet cable | ~£3 | Don't use WiFi for K3s |
| Case with cooling | ~£15 | Active cooling recommended |
| **TOTAL** | **~£145** | One node. Add more later. |

**CLEVER FIX #3:** Buy a **refurbished mini PC** instead. A Lenovo ThinkCentre M720q Tiny or Dell OptiPlex Micro with an i5, 16GB RAM goes for **£80-120 on eBay**. More power than a Pi 5, x86 compatibility (no ARM headaches), and it runs K3s beautifully. This is the bootstrapper's secret weapon.

**CLEVER FIX #4:** Check **Facebook Marketplace** and **Gumtree** for old office clear-outs. Companies dump perfectly good i5/i7 SFF PCs for £30-50. Slap in an NVMe and you're golden.

### Option C: The Hybrid (Best of Both)

Run Civo for public-facing production. Run a home mini PC for:
- LGM model training/inference (private, no cloud GPU costs)
- COMBOT Qubic mining (24/7, free electricity at home vs cloud costs)
- Development/staging K3s cluster
- Immich photo backup (self-hosted, starred repo)
- changedetection.io monitoring (starred repo)

Connect them with **Tailscale** (your starred repo) — zero-config VPN mesh. Home cluster and Civo cluster talk to each other as if on the same network. Free for personal use.

---

## PART 3: THE NETWORKING & SECURITY SETUP

### Domain & DNS

| Item | Cost | Clever Fix |
|------|------|-----------|
| Domain name (claimour.com etc) | ~£10/yr | You already have these |
| Cloudflare DNS | **FREE** | Free tier handles DNS + DDoS protection + CDN |
| SSL/TLS certs | **FREE** | cert-manager + Let's Encrypt on K3s |

### VPN & Secure Access

| Tool | Cost | Why |
|------|------|-----|
| Tailscale | **FREE** (personal) | Mesh VPN, connects all your devices/servers |
| WireGuard | **FREE** | If you want raw VPN without Tailscale |

### Security Stack (From Your Starred Repos)

- **TruffleHog** — scan your repos for leaked credentials (FREE, run in CI)
- **Sherlock** — OSINT reconnaissance (FREE)
- **MKAngel** — your own incident tracking app
- **changedetection.io** — monitor your deployed sites for tampering (self-hosted, FREE)

---

## PART 4: THE SOFTWARE STACK ON K3S

What actually runs in the TARDIS cluster:

### Core Platform Services (Deploy First)

```yaml
# Priority order for deployment
1. Traefik         — already included with K3s (ingress/routing) — FREE
2. cert-manager    — auto SSL from Let's Encrypt — FREE
3. PostgreSQL      — single shared DB for all apps — FREE (self-hosted)
   OR Civo Managed DB — $15/mo (if you want managed)
4. Redis           — caching/queues — FREE (self-hosted)
5. Longhorn        — distributed storage for K3s — FREE
```

### AI Services (Layer 3)

```yaml
6. LGM API         — your Large Grammar Model, containerised
7. The Luggage     — agent orchestration platform
8. Block Prophet   — MCTS reasoning engine
```

### Revenue Apps (Layer 4 — deploy as each is ready)

```yaml
9.  ClaimourLife    — Astro static site + API
10. InventorForge   — TypeScript app
11. BAKK Online     — TypeScript app
12. nssLocalWebBuilder — TypeScript app
13. Hex Inventions  — content publishing pipeline
14. TheBrunelEngine — HTML/interview tool
15. FutureSpeak     — TypeScript ed-tech app
```

### Monitoring & Ops

```yaml
16. Grafana + Prometheus — monitoring — FREE (self-hosted)
17. Loki            — log aggregation — FREE
18. changedetection.io — uptime/change monitoring — FREE
```

---

## PART 5: COST BREAKDOWN — THE HONEST NUMBERS

### Phase 1: RIGHT NOW (Month 1-6) — "The Free Ride"

| Item | Monthly Cost |
|------|-------------|
| Civo K3s Small (covered by $250 credit) | **$0** |
| Cloudflare DNS/CDN | **$0** |
| Let's Encrypt SSL | **$0** |
| Tailscale personal | **$0** |
| GitHub free tier (public repos) | **$0** |
| Claude Code (you're already paying this) | *existing cost* |
| Google Workspace (matt@claimour.com) | *existing cost* |
| **TOTAL NEW COSTS** | **$0/month** |

Hardware (one-time, if going hybrid):
| Item | Cost |
|------|------|
| Refurb mini PC from eBay | £80-120 |
| NVMe SSD 500GB | £30 |
| **TOTAL** | **£110-150** |

### Phase 2: GROWING (Month 6-12)

| Item | Monthly Cost |
|------|-------------|
| Civo K3s Medium node | **$21.73** |
| Domain renewals (amortised) | ~$2 |
| **TOTAL** | **~$24/month** |

### Phase 3: REVENUE (Month 12+)

| Item | Monthly Cost |
|------|-------------|
| Civo K3s Large node | **$43.45** |
| Civo Managed DB (optional) | **$15** |
| Extra storage | ~$5 |
| **TOTAL** | **~$63/month** |

By this point, if even ONE of your revenue apps is generating income, this is covered.

---

## PART 6: REVENUE STRATEGY — WHAT PAYS FIRST

Ranked by **speed to first dollar** and **effort required**:

### Tier 1: Quick Wins (Weeks)

1. **Hex Inventions** — Content plays pay fast. Daily invention teardowns build audience. Monetise with affiliate links, sponsored posts, newsletter. The IGOR Protocol is your publishing engine. Cost: $0 (just your time + Claude).

2. **COMBOT + Qubic Mining** — Qubic just transitioned to Dogecoin mining (April 2026). CPU/GPU resources now go to AI training. Run COMBOT on your phone AND home server 24/7. Passive income while you sleep. The hummingbot starred repo suggests you're already thinking about automated trading.

3. **ClaimourLife / Claimour** — "1300+ magic spells for reclaiming your digital life." Already built AND deployed (ClaimourLife on Eleventy/Netlify, Claimour on Astro/Vercel). Already running on free hosting. Add a donation button or premium tier. UK consumer rights is an underserved niche.

### Tier 2: Medium-term (1-3 Months)

4. **nssLocalWebBuilder** — In-browser website builder. SaaS model. Freemium + paid templates. Real demand exists.

5. **TheBrunelEngine** — "Turn frustrations into actionable insights." B2B consulting tool. Charge per assessment or monthly.

6. **InventorForge** — "Gripe to granted patent." Huge value prop if it works. Charge per patent application generated.

### Tier 3: Long Game (3-6 Months)

7. **BAKK Online** — CANZUK social platform (Next.js/Tailwind). Already has a premium tier designed at **£10/month** (verified badge, priority matching, job board, settlement guides). Community play. Needs critical mass but the revenue model is already baked in.

8. **Vex-Lang** — Crypto trading DSL. Niche but high-value users.

9. **FutureSpeak** — Ed-tech. Slow burn but scalable.

---

## PART 7: THE 90-DAY EXECUTION PLAN

### Week 1-2: FOUNDATION
- [ ] Claim Civo $250 free credit (if not already done)
- [ ] Deploy TARDIS K3s cluster with Terraform (this repo — already done)
- [ ] Set up Tailscale on phone + any computers you have
- [ ] Install Traefik ingress + cert-manager on the cluster
- [ ] Deploy PostgreSQL on K3s
- [ ] Set up GitHub Actions CI/CD for all active repos
- [ ] Run TruffleHog across all your repos (credential scan)

### Week 3-4: FIRST DEPLOYS
- [ ] Containerise and deploy ClaimourLife (Astro static — simplest)
- [ ] Containerise and deploy Hex Inventions publishing pipeline
- [ ] Set up COMBOT on phone for Qubic/Dogecoin mining
- [ ] Deploy changedetection.io for monitoring
- [ ] Set up Grafana + Prometheus for cluster observability

### Week 5-8: REVENUE PUSH
- [ ] Launch Hex Inventions daily content (build audience)
- [ ] Add monetisation to ClaimourLife (donations/premium)
- [ ] Containerise and deploy nssLocalWebBuilder
- [ ] Containerise and deploy TheBrunelEngine
- [ ] Begin InventorForge MVP deployment

### Week 9-12: AI LAYER
- [ ] Deploy LGM API on the cluster
- [ ] Integrate The Luggage agent platform
- [ ] Connect Block Prophet reasoning to LGM
- [ ] Wire AI into InventorForge (patent generation)
- [ ] Wire AI into Hex Inventions (automated teardowns)
- [ ] If revenue > $50/mo, upgrade Civo node to Medium

### ONGOING
- [ ] Buy refurb mini PC for home hybrid node when budget allows
- [ ] Expand BAKK Online when CANZUK community grows
- [ ] Develop Vex-Lang trading strategies
- [ ] Scale node count as traffic grows

---

## PART 8: CLEVER FIXES FOR THE CASH-STRAPPED

### Free Compute You're Not Using Yet

| Service | What You Get Free | How to Use It |
|---------|------------------|---------------|
| **Civo** | $250 credit | Your main K3s cluster |
| **Oracle Cloud** | 4 OCPU, 24GB ARM VM forever | Dev/staging K3s node |
| **Cloudflare Pages** | Unlimited static sites | Host Claimour, portfolio, etc. |
| **Cloudflare Workers** | 100K requests/day | API endpoints, edge functions |
| **Fly.io** | 3 shared VMs, 160GB bandwidth | Overflow services |
| **Railway** | $5/mo free credit | Quick app deploys |
| **Render** | Static sites free | Landing pages |
| **Vercel** | Hobby tier free | Next.js/static deploys |
| **PlanetScale** | Hobby DB free | MySQL if needed |
| **Supabase** | 500MB Postgres free | Auth + DB |
| **GitHub Actions** | 2000 min/mo free | CI/CD (already using) |

### Phone as a Server

Your phone is a computer. You already know this (COMBOT Android, MKAngel). Here's what it can do:

- **Qubic mining** — COMBOT, 24/7 background process
- **Tailscale node** — your phone joins the mesh VPN
- **Termux** — full Linux terminal on Android, can run lightweight services
- **Tasker** — Android automation for monitoring and alerts

### AI on the Cheap

- **Claude Code** — you're already here. Use it to build everything.
- **Google AI Studio** (via your Google Ultra account) — free Gemini API calls, use for batch processing
- **Ollama** — run local LLMs on your home mini PC for free (when you get one)
- **ROCm** (starred) — if you get an AMD GPU, use it for AI inference without NVIDIA tax

### The Android Arsenal

Your phone runs these repos already or can:
- COMBOT — mining + competitions
- MKAngel — security monitoring
- Termux — dev environment
- Brave Browser — privacy + BAT rewards (you mentioned Brave)

---

## PART 9: WHAT YOUR STARRED REPOS TELL US TO BUILD

| Starred Repo | What It Tells Us | Action |
|-------------|-----------------|--------|
| **oh-my-claudecode** | Multi-agent orchestration | Wire this into The Luggage |
| **AI-Scientist-v2** | Automated research | Feed this into InventorForge |
| **hummingbot** | Crypto trading bots | Integrate with Vex-Lang |
| **supervision (roboflow)** | Computer vision | Future MKAngel camera features |
| **sktime** | Time series ML | Market prediction for Vex-Lang/COMBOT |
| **PostHog** | Product analytics | Deploy on K3s, track all your apps |
| **novu** | Notification infra | Shared notification service across all apps |
| **immich** | Self-hosted photos | Deploy on home server |
| **yt-dlp** | Media downloading | Content pipeline for Hex Inventions |
| **MudBlazor** | Blazor components | If you pivot any app to .NET |
| **ROCm** | AMD GPU compute | Home server AI inference |
| **NixOS** | Reproducible systems | Lock down home server config |
| **engine262** | JS engine internals | FutureSpeak language engine? |

---

## PART 10: THE NAMING TELLS THE STORY

You've got a theme and it matters:

- **TARDIS** — bigger on the inside. One small cluster, infinite services.
- **The Luggage** — Discworld. Follows you everywhere. Opens for anything. Indestructible.
- **Hex** — the Unseen University's computer. AI that thinks for itself.
- **IGOR** — the protocol. Loyal, useful, gets things done without ego.
- **Doctor** — several repos use "Doctor" as the default branch. The Doctor fixes things.
- **Sentinel** — watching, protecting.
- **Brunel** — the great engineer. Building things that last.
- **Sovereign** — you own it. Nobody else controls it.

This isn't random. This is a **self-sovereign AI infrastructure** with a personality. That's your brand.

---

## APPENDIX: EQUIPMENT SHOPPING LIST

### Minimum Viable Setup (You Have This Now)
- [x] Android phone
- [x] Claude Code subscription
- [x] Google Workspace account (matt@claimour.com)
- [x] GitHub account with 34 repos
- [x] Civo account
- [ ] Claim Civo $250 credit

### Next Purchase (£110-150)
- [ ] Refurb mini PC (eBay: Lenovo M720q / Dell OptiPlex Micro, i5, 16GB)
- [ ] 500GB NVMe SSD
- [ ] Ethernet cable

### Nice to Have Later (£200-400)
- [ ] Second mini PC (high availability)
- [ ] AMD GPU (RX 6600 or similar, ~£120 used) for local AI inference via ROCm
- [ ] UPS battery backup (~£50) for the home server
- [ ] Managed switch (~£20) if running multiple nodes

### Skip These (Waste of Money Right Now)
- ~~Cloud GPUs~~ — too expensive for bootstrapping, use Google AI Studio free tier
- ~~Raspberry Pi cluster~~ — mini PCs are cheaper per compute
- ~~Dedicated server hosting~~ — Civo + home hybrid beats it on cost
- ~~Premium monitoring tools~~ — Grafana + Prometheus are free and better

---

*"The future is ours to see. Que sera by me."*

*Built from first principles. For the majestic fool who builds empires from a phone.*
