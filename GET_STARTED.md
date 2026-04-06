# GET STARTED: The Idiot-Proof Guide
## For Matt, On His Phone, Right Now

No jargon. No assumptions. Just steps. If a step says "tap", you tap. If it says "type", you type exactly what's written.

---

## STEP 0: WHAT YOU HAVE RIGHT NOW

You have:
- This phone
- A GitHub account (mrjkilcoyne-lgtm)
- A Google account (matt@claimour.com)
- Claude Code (you're reading this)
- 34 repos full of ideas and code
- A brain full of inventions

You need to turn all of that into running websites and services that people can actually visit and pay you money through. This guide gets you there.

---

## STEP 1: GET YOUR FREE CLOUD SERVER ($0)

Civo is where your server lives. They give you $250 free credit. That's about 2 years of a small server for free.

1. Open your browser
2. Go to: **https://dashboard.civo.com/signup**
3. Sign up with matt@claimour.com
4. **Add a payment card** — they won't charge you, but you need it to unlock the $250 credit
5. You'll see "$250.00 credit" on your dashboard — that's your free server money

**If you already have a Civo account**, log in and check your credit balance at the top of the dashboard.

---

## STEP 2: GET YOUR CIVO API TOKEN

This is like a password that lets your code talk to Civo.

1. Log into https://dashboard.civo.com
2. Click your **profile icon** (top right)
3. Click **"Security"**
4. You'll see **"API Keys"** — there should be one already, or click **"Create"**
5. **Copy the long string of letters and numbers** — that's your token
6. **Save it somewhere safe** (Notes app, password manager — NOT in a public GitHub repo)

---

## STEP 3: TELL GITHUB YOUR CIVO TOKEN

GitHub needs to know your Civo token so it can build your server automatically.

1. Go to: **https://github.com/mrjkilcoyne-lgtm/tardis-sovereign/settings**
2. In the left sidebar, click **"Environments"**
3. If there's no environment called **"production"**, click **"New environment"** and name it `production`
4. Click on the **production** environment
5. Under **"Environment secrets"**, click **"Add secret"**
6. Name: `CIVO_TOKEN`
7. Value: **paste your Civo API token from Step 2**
8. Click **"Add secret"**

---

## STEP 4: MERGE THE CODE TO BUILD YOUR SERVER

Right now all the infrastructure code is on a branch. Merging it to "main" tells GitHub to actually build the server.

**Before you do this**, understand: this will create a real server on Civo Cloud. It costs ~$10.86/month BUT you have $250 free credit, so it's free for ages.

1. Go to: **https://github.com/mrjkilcoyne-lgtm/tardis-sovereign**
2. You should see a yellow banner saying the branch `claude/add-claude-documentation-w61Sw` had recent pushes
3. Click **"Compare & pull request"**
4. Title it something like: `Set up TARDIS infrastructure`
5. Click **"Create pull request"**
6. Wait for the checks to run (green tick = good, red X = problem)
7. If green, click **"Merge pull request"**
8. Click **"Confirm merge"**

**What happens next**: GitHub Actions will automatically run `terraform apply`, which creates your K3s Kubernetes cluster on Civo. This takes about 2-5 minutes.

---

## STEP 5: CHECK YOUR SERVER EXISTS

1. Go to: **https://dashboard.civo.com**
2. Click **"Kubernetes"** in the left sidebar
3. You should see a cluster called **"tardis-sovereign"**
4. Status should be **"ACTIVE"** (green)
5. Click on it — you'll see your node, its IP address, and a download button for the kubeconfig

**If you see it: congratulations. You have a server.**

---

## STEP 6: GET YOUR KUBECONFIG (The Key to Your Server)

The kubeconfig is like a key that lets you control your server.

1. On the Civo Kubernetes page, click your **tardis-sovereign** cluster
2. Click the **"Download Config"** button
3. Save the file — it'll be called something like `civo-tardis-sovereign-kubeconfig`

Now you need to give this to GitHub so the deployment pipeline can use it:

4. Open the file in a text editor and **copy ALL the text**
5. Go to: **https://github.com/mrjkilcoyne-lgtm/tardis-sovereign/settings**
6. Click **"Environments"** → **"production"**
7. Under **"Environment secrets"**, click **"Add secret"**
8. Name: `KUBECONFIG`
9. Value: **paste the entire kubeconfig file contents**
10. Click **"Add secret"**

---

## STEP 7: GET A FREE DOMAIN POINTED AT YOUR SERVER

You probably already own domains (claimour.com, etc). If not:

### Option A: Use a domain you already own
1. Go to wherever you bought the domain (Namecheap, GoDaddy, Google Domains, etc)
2. Change the **nameservers** to Cloudflare (free):
   - `ns1.cloudflare.com`
   - `ns2.cloudflare.com`

### Option B: Get a free subdomain
- Skip this for now — your apps will work on the cluster IP address first

### Set up Cloudflare (FREE — this protects and speeds up your sites)

1. Go to: **https://dash.cloudflare.com/sign-up**
2. Sign up (free account)
3. Click **"Add a site"**
4. Type your domain name
5. Choose the **Free** plan
6. Cloudflare will scan your DNS records — click **"Continue"**
7. It'll tell you to change your nameservers — do what it says at your domain registrar
8. Once the nameservers propagate (can take up to 24 hours, usually faster), your domain is on Cloudflare

### Point your domain at your server

1. In Cloudflare, go to **DNS** → **Records**
2. Click **"Add record"**
3. Type: **A**
4. Name: **@** (or your subdomain like `hex` or `bakk`)
5. IPv4 address: **your cluster's IP** (from Step 5, visible on the Civo dashboard)
6. Proxy status: **Proxied** (orange cloud)
7. Click **"Save"**

Repeat for each subdomain you want (e.g., `hex.yourdomain.com`, `bakk.yourdomain.com`, `grafana.yourdomain.com`).

---

## STEP 8: DEPLOY YOUR FIRST APP

Let's get ClaimourLife running — it's the simplest (static site).

But first, ClaimourLife needs a container image (a packaged version of the app). This is done in the ClaimourLife repo, not here. Here's the cheat:

### Quick way: use the existing Netlify/Vercel deployments

Your apps are ALREADY deployed:
- **ClaimourLife** → already on Netlify
- **Claimour** → already on Vercel at https://claimour.vercel.app
- **BAKK Online** → check if it's deployed

**You don't need the K3s cluster to start making money.** The cluster is for when you want everything under one roof, running on your own infrastructure.

### When you're ready for K3s deployment

Each app needs a Dockerfile (a recipe for packaging it). I've created templates in this repo:
- `Dockerfile.static` → for ClaimourLife (Eleventy static site)
- `Dockerfile.template` → for BAKK Online, Hex Inventions (Node.js apps)
- `Dockerfile.python` → for LGM, The Luggage (Python services)

Copy the right template into each app's repo, build the image, push it. Then the K8s manifests in this repo will pick it up.

---

## STEP 9: SET UP TAILSCALE (Connect Everything)

Tailscale makes your phone, your server, and (eventually) your home computer all talk to each other securely. Free for personal use.

### On your phone:
1. Install **Tailscale** from the Play Store
2. Sign in with your Google account (matt@claimour.com)
3. Tap **"Connect"** — your phone is now on your private network

### On your Civo cluster (later):
- The script `k8s/scripts/tailscale-join.sh` does this for you
- You'll need a Tailscale auth key from https://login.tailscale.com/admin/settings/keys

### On a home computer (when you get one):
1. Install Tailscale: https://tailscale.com/download
2. Sign in with the same Google account
3. It auto-connects to the same network as your phone and server

**Result**: your phone, server, and computer can all talk to each other on a private encrypted network. No port forwarding, no firewall headaches.

---

## STEP 10: START MAKING MONEY

In order of "fastest to first pound":

### 1. Hex Inventions (content = audience = money)
- You already have the first invention (GRANNY fridge teardown)
- Publish one per day using the IGOR Protocol
- Set up a Substack or newsletter — link from the GitHub repo
- Affiliate links in teardowns (Amazon Associates is easy to join)
- This costs you nothing but time

### 2. ClaimourLife (already live on Netlify)
- Add a **"Buy me a coffee"** link: https://www.buymeacoffee.com
- Or add **Stripe** donation button (takes 5 minutes)
- The 1300+ spells are the product — people will pay for a premium version

### 3. BAKK Online (premium at £10/month)
- You've already designed the premium tier
- You need **Stripe** to take payments: https://dashboard.stripe.com/register
- Sign up, get your API keys, add them as secrets to the repo
- The K8s manifest already has Stripe env vars wired up

### 4. COMBOT (mining while you sleep)
- If COMBOT is ready, run it on your phone
- Qubic mining is now tied to Dogecoin (as of April 2026)
- This is passive income — small amounts but zero effort once running

---

## WHAT EACH FILE IN THIS REPO DOES

| File | What it does | Do you need to touch it? |
|------|-------------|-------------------------|
| `main.tf` | Creates your server on Civo | No (unless changing server size) |
| `variables.tf` | Settings like server name, region | No |
| `outputs.tf` | Makes kubeconfig available | No |
| `terraform.tf` | Version requirements | No |
| `THE_PLAN.md` | Your full ecosystem strategy | Read it. It's your map. |
| `CLAUDE.md` | Instructions for AI assistants | No |
| `GET_STARTED.md` | This file | You're reading it |
| `k8s/core/*` | Database, cache, SSL setup | Only to change passwords |
| `k8s/apps/*` | Your app deployments | Update domain names |
| `k8s/monitoring/*` | Prometheus + Grafana | Only to change passwords |
| `k8s/scripts/*` | Helper scripts | Run them, don't edit them |
| `Dockerfile.*` | Templates for packaging apps | Copy to app repos |
| `.github/workflows/*` | Automation pipelines | No |

---

## GLOSSARY (What The Words Mean)

| Word | What it actually means |
|------|----------------------|
| **Kubernetes (K8s)** | Software that runs your apps on a server and keeps them alive |
| **K3s** | A lighter, simpler version of Kubernetes. Same thing, less bloat. |
| **Cluster** | Your server(s). Right now it's one server, but can grow. |
| **Node** | One computer in your cluster. You have 1. |
| **Pod** | One running copy of an app. Like one worker doing one job. |
| **Namespace** | A folder inside your cluster to keep things organized |
| **Deployment** | Instructions that say "run this app with these settings" |
| **Service** | A phone number for your app inside the cluster |
| **Ingress** | The front door — routes internet traffic to the right app |
| **Terraform** | Code that creates cloud servers. You write what you want, it builds it. |
| **Docker/Container** | Your app packaged into a box that runs the same everywhere |
| **GHCR** | GitHub's storage for container images (free) |
| **Helm** | An app store for Kubernetes. Install tools with one command. |
| **cert-manager** | Auto-gets free SSL certificates (the padlock in browsers) |
| **Traefik** | Traffic cop. Routes visitors to the right app. Comes free with K3s. |
| **Tailscale** | Private VPN that connects all your devices. Free. Magic. |
| **CI/CD** | Robots that build and deploy your code when you push to GitHub |
| **Kubeconfig** | A key file that lets you control your cluster |
| **Secret** | A password stored securely in GitHub or Kubernetes |
| **PVC** | Persistent storage — your database data survives restarts |

---

## IF SOMETHING GOES WRONG

### "The GitHub Action failed" (red X)
1. Go to the repo → **"Actions"** tab
2. Click the failed run
3. Read the red error text
4. Screenshot it and paste it into a Claude Code session — I'll fix it

### "My cluster isn't showing on Civo"
- Check that `CIVO_TOKEN` is set correctly in GitHub Secrets
- Check the Actions tab for errors
- Log into Civo dashboard directly to see if anything is there

### "I can't access my app"
- Check your domain DNS is pointing to the right IP
- DNS changes can take up to 24 hours (usually minutes)
- Check the pod is running: the Grafana dashboard will show you

### "I'm confused and overwhelmed"
- Start with Step 1. Do only Step 1 today.
- Tomorrow, do Step 2.
- One step per day is fine. This is a marathon, not a sprint.
- You have $250 in free credit. There is no rush.

---

## THE ORDER OF OPERATIONS (What To Do Today)

**Today**: Steps 1-3 (Civo account, API token, GitHub secret). 15 minutes.

**Tomorrow**: Step 4 (merge the PR). 2 minutes. Then check Step 5.

**This week**: Step 7 (Cloudflare DNS). Step 9 (Tailscale on phone).

**When ready**: Step 10 (start publishing Hex Inventions, add donate button to ClaimourLife).

**When you have £100 spare**: Buy a refurb mini PC from eBay for your home server.

---

*You've got this. One step at a time. The TARDIS is bigger on the inside.*
