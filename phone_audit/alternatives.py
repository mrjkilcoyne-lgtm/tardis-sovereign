"""Privacy-respecting alternatives and power combinations.

Every app in here is either:
- Open source and audited
- Privacy-respecting by design
- More capable than what it replaces
- Or all three

The aesthetics aren't Claude. They're TARDIS.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class AppProfile:
    name: str
    category: str
    privacy_score: int      # 1-10, 10 = fully private
    snooping_level: str     # none, low, moderate, aggressive, hostile
    data_collected: list[str] = field(default_factory=list)
    essential_function: str = ""  # what it actually does for you
    replaceable: bool = True


@dataclass
class Alternative:
    name: str
    replaces: list[str]     # app names it can replace
    category: str
    privacy_score: int
    open_source: bool
    cost: str               # free, freemium, £X/month
    platforms: list[str] = field(default_factory=list)
    power_features: list[str] = field(default_factory=list)
    install_url: str = ""
    notes: str = ""


# ── KNOWN SNOOPS ──
KNOWN_SNOOPS: dict[str, AppProfile] = {
    "facebook": AppProfile("Facebook", "social", 1, "hostile",
        ["contacts", "location", "browsing", "calls", "messages", "photos", "microphone"],
        "Social networking"),
    "instagram": AppProfile("Instagram", "social", 2, "hostile",
        ["contacts", "location", "browsing", "photos", "camera", "microphone"],
        "Photo sharing"),
    "tiktok": AppProfile("TikTok", "social", 1, "hostile",
        ["clipboard", "contacts", "location", "browsing", "device_info", "keystroke_patterns"],
        "Short video"),
    "whatsapp": AppProfile("WhatsApp", "messaging", 4, "moderate",
        ["contacts", "metadata", "location_if_shared"],
        "Messaging (E2E encrypted but Meta-owned)"),
    "google_maps": AppProfile("Google Maps", "navigation", 2, "aggressive",
        ["location_always", "search_history", "places_visited", "travel_patterns"],
        "Navigation"),
    "chrome": AppProfile("Chrome", "browser", 2, "aggressive",
        ["browsing_history", "passwords", "autofill", "location"],
        "Web browsing"),
    "gmail": AppProfile("Gmail", "email", 3, "aggressive",
        ["email_content", "contacts", "purchase_history"],
        "Email"),
    "google_photos": AppProfile("Google Photos", "photos", 3, "aggressive",
        ["all_photos", "location_from_exif", "face_recognition"],
        "Photo backup and management"),
    "alexa": AppProfile("Alexa", "assistant", 1, "hostile",
        ["voice_recordings", "smart_home", "purchase_history", "contacts"],
        "Voice assistant"),
    "twitter": AppProfile("Twitter/X", "social", 3, "moderate",
        ["browsing", "contacts_optional", "location_optional"],
        "Microblogging"),
    "linkedin": AppProfile("LinkedIn", "professional", 3, "moderate",
        ["contacts", "email", "browsing", "employment_history"],
        "Professional networking"),
    "uber": AppProfile("Uber", "transport", 3, "moderate",
        ["location", "contacts", "payment_info"],
        "Ride hailing"),
    "deliveroo": AppProfile("Deliveroo", "food", 4, "moderate",
        ["location", "payment_info", "order_history"],
        "Food delivery"),
}


# ── REPLACEMENTS ──
REPLACEMENTS: list[Alternative] = [

    # ── Messaging ──
    Alternative(
        name="Signal",
        replaces=["whatsapp", "facebook_messenger", "telegram"],
        category="messaging",
        privacy_score=10,
        open_source=True,
        cost="free",
        platforms=["iOS", "Android", "Desktop"],
        power_features=["E2E encrypted", "No metadata collection", "Disappearing messages",
                        "Note to self", "Group calls", "Stories"],
        notes="The gold standard. Swiss non-profit. Signal protocol is what WhatsApp copied.",
    ),

    # ── Browser ──
    Alternative(
        name="Firefox Focus",
        replaces=["chrome", "safari"],
        category="browser",
        privacy_score=9,
        open_source=True,
        cost="free",
        platforms=["iOS", "Android"],
        power_features=["Auto-delete history", "Tracking protection", "Ad blocking",
                        "Fast", "Minimal"],
        notes="For quick private browsing. Use Brave or Firefox for full sessions.",
    ),
    Alternative(
        name="Brave",
        replaces=["chrome"],
        category="browser",
        privacy_score=8,
        open_source=True,
        cost="free",
        platforms=["iOS", "Android", "Desktop"],
        power_features=["Built-in ad blocking", "Tor mode", "BAT rewards",
                        "Chromium-based (compatible)", "Brave Search"],
        notes="Chrome compatibility without Google surveillance. Built-in crypto wallet.",
    ),

    # ── Email ──
    Alternative(
        name="Proton Mail",
        replaces=["gmail", "outlook"],
        category="email",
        privacy_score=10,
        open_source=True,
        cost="free (1GB) / £4/month",
        platforms=["iOS", "Android", "Web"],
        power_features=["E2E encrypted", "Swiss jurisdiction", "No ads",
                        "Calendar", "Drive", "VPN included in paid"],
        notes="Swiss privacy law. Can import from Gmail. Proton suite replaces Google suite.",
    ),

    # ── Navigation ──
    Alternative(
        name="OsmAnd",
        replaces=["google_maps"],
        category="navigation",
        privacy_score=10,
        open_source=True,
        cost="free",
        platforms=["iOS", "Android"],
        power_features=["Fully offline maps", "No tracking", "Hiking/cycling routes",
                        "OpenStreetMap data", "Offline search"],
        notes="Download UK maps once, navigate forever without data or tracking.",
    ),
    Alternative(
        name="Organic Maps",
        replaces=["google_maps"],
        category="navigation",
        privacy_score=10,
        open_source=True,
        cost="free",
        platforms=["iOS", "Android"],
        power_features=["Offline-first", "No ads", "No tracking", "Fast", "Hiking trails"],
        notes="Fork of Maps.me without the tracking. Beautiful and fast.",
    ),

    # ── Photos ──
    Alternative(
        name="Ente",
        replaces=["google_photos", "icloud_photos"],
        category="photos",
        privacy_score=10,
        open_source=True,
        cost="free (5GB) / £3/month",
        platforms=["iOS", "Android", "Web", "Desktop"],
        power_features=["E2E encrypted", "Auto backup", "Sharing", "Face recognition (on-device)",
                        "Map view", "Import from Google Photos"],
        notes="Indian company, fully encrypted. Your photos, actually yours.",
    ),

    # ── Notes ──
    Alternative(
        name="Obsidian",
        replaces=["notion", "evernote", "apple_notes", "google_keep"],
        category="notes",
        privacy_score=9,
        open_source=False,
        cost="free (local) / £4/month sync",
        platforms=["iOS", "Android", "Desktop"],
        power_features=["Local-first", "Markdown", "Graph view", "Plugin ecosystem",
                        "Daily notes", "Templates", "Canvas", "Community plugins"],
        notes="Files stored locally as Markdown. You own them forever. Massive plugin ecosystem.",
    ),

    # ── Password Manager ──
    Alternative(
        name="Bitwarden",
        replaces=["1password", "lastpass", "chrome_passwords"],
        category="security",
        privacy_score=10,
        open_source=True,
        cost="free / £10/year premium",
        platforms=["iOS", "Android", "Desktop", "Browser"],
        power_features=["E2E encrypted", "Self-hostable", "TOTP built-in",
                        "Password sharing", "Breach reports"],
        notes="Open source, audited, and the free tier is genuinely excellent.",
    ),

    # ── VPN ──
    Alternative(
        name="Proton VPN",
        replaces=["nordvpn", "expressvpn", "no_vpn"],
        category="privacy",
        privacy_score=10,
        open_source=True,
        cost="free (limited) / included with Proton paid",
        platforms=["iOS", "Android", "Desktop"],
        power_features=["No-logs verified", "Swiss jurisdiction", "Secure Core",
                        "P2P support", "Kill switch"],
        notes="Free tier has no data cap. Paid tier comes with Proton Mail bundle.",
    ),

    # ── Social ──
    Alternative(
        name="Mastodon / Fediverse",
        replaces=["twitter", "facebook"],
        category="social",
        privacy_score=8,
        open_source=True,
        cost="free",
        platforms=["iOS", "Android", "Web"],
        power_features=["Decentralised", "No algorithm", "Chronological feed",
                        "No ads", "Choose your server"],
        notes="techhub.social or similar UK-adjacent instance. Your data, your rules.",
    ),

    # ── File Sync ──
    Alternative(
        name="Syncthing",
        replaces=["dropbox", "google_drive", "onedrive"],
        category="file_sync",
        privacy_score=10,
        open_source=True,
        cost="free",
        platforms=["Android", "Desktop (Linux/Mac/Win)"],
        power_features=["P2P sync", "No cloud", "Encrypted", "Versioning",
                        "Selective sync", "Ignore patterns"],
        notes="Files go directly between your devices. No server in the middle.",
    ),

    # ── 2FA ──
    Alternative(
        name="Aegis Authenticator",
        replaces=["google_authenticator", "authy"],
        category="security",
        privacy_score=10,
        open_source=True,
        cost="free",
        platforms=["Android"],
        power_features=["Encrypted vault", "Biometric unlock", "Import from Google Auth",
                        "Export/backup", "Organise by groups"],
        notes="Android only. For iOS use Raivo OTP (also open source).",
    ),
]


# ── POWER COMBINATIONS ──
# Apps that together are more powerful than the sum of their parts

COMBINATIONS: list[dict] = [
    {
        "name": "The Proton Suite",
        "apps": ["Proton Mail", "Proton VPN", "Proton Drive", "Proton Calendar"],
        "replaces": ["Gmail", "Google Drive", "Google Calendar", "any VPN"],
        "cost": "£4/month for everything",
        "why": "One account, Swiss privacy law, replaces entire Google ecosystem.",
    },
    {
        "name": "The Local-First Stack",
        "apps": ["Obsidian", "Syncthing", "Bitwarden"],
        "replaces": ["Notion", "Dropbox", "Chrome passwords"],
        "cost": "Free",
        "why": "Everything stored locally, synced P2P. You own all your data. Forever.",
    },
    {
        "name": "The Communication Shield",
        "apps": ["Signal", "Proton Mail", "Firefox Focus"],
        "replaces": ["WhatsApp", "Gmail", "Chrome"],
        "cost": "Free",
        "why": "Every message, email, and browsing session is encrypted and private.",
    },
    {
        "name": "The TARDIS Stack",
        "apps": ["Brave", "Obsidian", "Signal", "Ente", "Bitwarden", "Proton VPN"],
        "replaces": ["Chrome", "Notes", "WhatsApp", "Google Photos", "Passwords", "No VPN"],
        "cost": "£3/month (Ente only)",
        "why": "Complete digital sovereignty. Nothing phones home. Everything is yours.",
    },
]
