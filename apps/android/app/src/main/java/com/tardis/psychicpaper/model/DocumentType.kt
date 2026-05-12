package com.tardis.psychicpaper.model

import androidx.compose.ui.graphics.Color

/**
 * Layout styles that control how the document card renders.
 */
enum class DocumentLayout {
    CARD,
    TICKET,
    BADGE,
    FULL,
}

/**
 * All 10 credential types that Psychic Paper can morph into.
 * Each carries its own colour scheme, layout, keyword triggers, and field templates.
 * Colours matched to the iOS version.
 */
enum class DocumentType(
    val displayName: String,
    val issuer: String,
    val icon: String,
    val layout: DocumentLayout,
    val primaryColor: Color,
    val accentColor: Color,
    val backgroundColor: Color,
    val textPrimary: Color = Color.White,
    val textSecondary: Color = Color.White.copy(alpha = 0.7f),
    val keywords: List<String>,
    val fields: List<String>,
) {
    PRESS_PASS(
        displayName = "Press Pass",
        issuer = "PRESS CREDENTIALS",
        icon = "\uD83D\uDCF0",
        layout = DocumentLayout.BADGE,
        primaryColor = Color(0xFFD91F1F),
        accentColor = Color(0xFFFFD900),
        backgroundColor = Color(0xFF261414),
        keywords = listOf(
            "press", "media", "journalist", "reporter", "interview", "news",
            "coverage", "newspaper", "broadcast", "photography", "press conference"
        ),
        fields = listOf("NAME", "OUTLET", "PRESS ID", "VALID THROUGH", "ACCESS LEVEL"),
    ),
    EVENT_TICKET(
        displayName = "Event Ticket",
        issuer = "ADMIT ONE",
        icon = "\uD83C\uDFAB",
        layout = DocumentLayout.TICKET,
        primaryColor = Color(0xFF8F00D9),
        accentColor = Color(0xFFFF66B3),
        backgroundColor = Color(0xFF1F0D2E),
        keywords = listOf(
            "concert", "show", "gig", "festival", "performance", "music",
            "event", "arena", "stadium", "theatre", "theater", "live"
        ),
        fields = listOf("EVENT", "ATTENDEE", "DATE", "VENUE", "SEAT", "REF"),
    ),
    BOARDING_PASS(
        displayName = "Boarding Pass",
        issuer = "BOARDING PASS",
        icon = "\u2708\uFE0F",
        layout = DocumentLayout.TICKET,
        primaryColor = Color(0xFF0073D9),
        accentColor = Color(0xFF00CCFF),
        backgroundColor = Color(0xFF0D1A33),
        keywords = listOf(
            "flight", "airport", "plane", "fly", "airline", "boarding",
            "departure", "arrival", "terminal", "gate", "aviation"
        ),
        fields = listOf("PASSENGER", "FLIGHT", "FROM", "TO", "DATE", "GATE", "SEAT", "BOARDING"),
    ),
    DRIVING_LICENCE(
        displayName = "Driving Licence",
        issuer = "DRIVER AND VEHICLE LICENSING",
        icon = "\uD83D\uDE97",
        layout = DocumentLayout.CARD,
        primaryColor = Color(0xFF008C73),
        accentColor = Color(0xFF99E6CC),
        backgroundColor = Color(0xFF0D261F),
        keywords = listOf(
            "drive", "car", "vehicle", "road", "licence", "license",
            "traffic", "rental", "driving", "automobile", "motor"
        ),
        fields = listOf("NAME", "DATE OF BIRTH", "LICENCE NO.", "ISSUED", "EXPIRES", "CLASS"),
    ),
    MEMBERSHIP(
        displayName = "Membership Card",
        issuer = "MEMBER SINCE 2019",
        icon = "\uD83D\uDCB3",
        layout = DocumentLayout.CARD,
        primaryColor = Color(0xFFBF9933),
        accentColor = Color(0xFFFFE680),
        backgroundColor = Color(0xFF261F0D),
        keywords = listOf(
            "member", "club", "gym", "library", "subscribe", "loyalty",
            "vip", "exclusive", "premium", "society", "association"
        ),
        fields = listOf("MEMBER", "ORGANISATION", "MEMBER NO.", "SINCE", "TIER", "EXPIRES"),
    ),
    SECURITY_BADGE(
        displayName = "Security Badge",
        issuer = "SECURITY CLEARANCE",
        icon = "\uD83D\uDD12",
        layout = DocumentLayout.BADGE,
        primaryColor = Color(0xFF1A1A1A),
        accentColor = Color(0xFFE62626),
        backgroundColor = Color(0xFF141414),
        textPrimary = Color.White,
        textSecondary = Color(0xFFB3B3B3),
        keywords = listOf(
            "security", "restricted", "classified", "clearance", "access",
            "facility", "government", "military", "authorized", "badge"
        ),
        fields = listOf("NAME", "TITLE", "CLEARANCE", "BADGE NO.", "FACILITY", "EXPIRES"),
    ),
    TRANSPORT_PASS(
        displayName = "Transport Pass",
        issuer = "TRANSIT AUTHORITY",
        icon = "\uD83D\uDE87",
        layout = DocumentLayout.CARD,
        primaryColor = Color(0xFF009959),
        accentColor = Color(0xFF33E680),
        backgroundColor = Color(0xFF0D1F14),
        keywords = listOf(
            "bus", "train", "metro", "subway", "tram", "transit",
            "transport", "commute", "rail", "tube", "travel"
        ),
        fields = listOf("HOLDER", "PASS TYPE", "ZONE", "VALID FROM", "VALID TO", "SERIAL"),
    ),
    CONFERENCE_BADGE(
        displayName = "Conference Badge",
        issuer = "CONFERENCE ATTENDEE",
        icon = "\uD83C\uDFA4",
        layout = DocumentLayout.BADGE,
        primaryColor = Color(0xFF334DD9),
        accentColor = Color(0xFF80CCFF),
        backgroundColor = Color(0xFF0F142E),
        keywords = listOf(
            "conference", "summit", "convention", "seminar", "workshop",
            "expo", "symposium", "meetup", "keynote", "tech", "developer"
        ),
        fields = listOf("NAME", "TITLE", "COMPANY", "CONFERENCE", "DATE", "BADGE NO."),
    ),
    PERMIT(
        displayName = "Permit",
        issuer = "OFFICIAL PERMIT",
        icon = "\uD83D\uDCCB",
        layout = DocumentLayout.FULL,
        primaryColor = Color(0xFF66594D),
        accentColor = Color(0xFFB39966),
        backgroundColor = Color(0xFF1F1A14),
        keywords = listOf(
            "permit", "permission", "authorized", "construction", "parking",
            "filming", "work", "building", "official", "council", "license"
        ),
        fields = listOf("HOLDER", "PERMIT TYPE", "PERMIT NO.", "ISSUED BY", "ISSUED", "EXPIRES", "CONDITIONS"),
    ),
    INVITATION(
        displayName = "Invitation",
        issuer = "YOU ARE INVITED",
        icon = "\u2709\uFE0F",
        layout = DocumentLayout.FULL,
        primaryColor = Color(0xFFB33380),
        accentColor = Color(0xFFFFB3D9),
        backgroundColor = Color(0xFF260F1A),
        keywords = listOf(
            "invited", "invitation", "party", "wedding", "gala", "reception",
            "dinner", "celebration", "ceremony", "ball", "gathering", "soiree"
        ),
        fields = listOf("GUEST", "EVENT", "HOST", "DATE", "TIME", "VENUE", "DRESS CODE"),
    );

    companion object {
        /** Fallback when no keywords match. */
        val DEFAULT = PRESS_PASS
    }
}
