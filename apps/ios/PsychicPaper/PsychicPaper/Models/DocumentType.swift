import SwiftUI

// MARK: - Layout Style

enum DocumentLayout: String, Codable {
    case card
    case ticket
    case badge
    case full
}

// MARK: - Document Color Scheme

struct DocumentColors: Equatable {
    let primary: Color
    let accent: Color
    let background: Color
    let textPrimary: Color
    let textSecondary: Color

    init(primary: Color, accent: Color, background: Color,
         textPrimary: Color = .white, textSecondary: Color = .white.opacity(0.7)) {
        self.primary = primary
        self.accent = accent
        self.background = background
        self.textPrimary = textPrimary
        self.textSecondary = textSecondary
    }
}

// MARK: - Document Field

struct DocumentField: Identifiable, Equatable {
    let id = UUID()
    let label: String
    var value: String
    let isLarge: Bool

    init(label: String, value: String = "", isLarge: Bool = false) {
        self.label = label
        self.value = value
        self.isLarge = isLarge
    }

    static func == (lhs: DocumentField, rhs: DocumentField) -> Bool {
        lhs.label == rhs.label && lhs.value == rhs.value && lhs.isLarge == rhs.isLarge
    }
}

// MARK: - Document Type

enum DocumentType: String, CaseIterable, Codable, Identifiable {
    case press_pass
    case event_ticket
    case boarding_pass
    case driving_licence
    case membership
    case security_badge
    case transport_pass
    case conference_badge
    case permit
    case invitation

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .press_pass:       return "Press Pass"
        case .event_ticket:     return "Event Ticket"
        case .boarding_pass:    return "Boarding Pass"
        case .driving_licence:  return "Driving Licence"
        case .membership:       return "Membership Card"
        case .security_badge:   return "Security Badge"
        case .transport_pass:   return "Transport Pass"
        case .conference_badge: return "Conference Badge"
        case .permit:           return "Permit"
        case .invitation:       return "Invitation"
        }
    }

    var issuer: String {
        switch self {
        case .press_pass:       return "PRESS CREDENTIALS"
        case .event_ticket:     return "ADMIT ONE"
        case .boarding_pass:    return "BOARDING PASS"
        case .driving_licence:  return "DRIVER AND VEHICLE LICENSING"
        case .membership:       return "MEMBER SINCE 2019"
        case .security_badge:   return "SECURITY CLEARANCE"
        case .transport_pass:   return "TRANSIT AUTHORITY"
        case .conference_badge: return "CONFERENCE ATTENDEE"
        case .permit:           return "OFFICIAL PERMIT"
        case .invitation:       return "YOU ARE INVITED"
        }
    }

    var icon: String {
        switch self {
        case .press_pass:       return "newspaper"
        case .event_ticket:     return "ticket"
        case .boarding_pass:    return "airplane"
        case .driving_licence:  return "car"
        case .membership:       return "person.crop.rectangle"
        case .security_badge:   return "lock.shield"
        case .transport_pass:   return "tram"
        case .conference_badge: return "person.badge.key"
        case .permit:           return "doc.text"
        case .invitation:       return "envelope.open"
        }
    }

    var layout: DocumentLayout {
        switch self {
        case .press_pass:       return .badge
        case .event_ticket:     return .ticket
        case .boarding_pass:    return .ticket
        case .driving_licence:  return .card
        case .membership:       return .card
        case .security_badge:   return .badge
        case .transport_pass:   return .card
        case .conference_badge: return .badge
        case .permit:           return .full
        case .invitation:       return .full
        }
    }

    var colors: DocumentColors {
        switch self {
        case .press_pass:
            return DocumentColors(
                primary: Color(red: 0.85, green: 0.12, blue: 0.12),
                accent: Color(red: 1.0, green: 0.85, blue: 0.0),
                background: Color(red: 0.15, green: 0.08, blue: 0.08)
            )
        case .event_ticket:
            return DocumentColors(
                primary: Color(red: 0.56, green: 0.0, blue: 0.85),
                accent: Color(red: 1.0, green: 0.4, blue: 0.7),
                background: Color(red: 0.12, green: 0.05, blue: 0.18)
            )
        case .boarding_pass:
            return DocumentColors(
                primary: Color(red: 0.0, green: 0.45, blue: 0.85),
                accent: Color(red: 0.0, green: 0.8, blue: 1.0),
                background: Color(red: 0.05, green: 0.1, blue: 0.2)
            )
        case .driving_licence:
            return DocumentColors(
                primary: Color(red: 0.0, green: 0.55, blue: 0.45),
                accent: Color(red: 0.6, green: 0.9, blue: 0.8),
                background: Color(red: 0.05, green: 0.15, blue: 0.12)
            )
        case .membership:
            return DocumentColors(
                primary: Color(red: 0.75, green: 0.6, blue: 0.2),
                accent: Color(red: 1.0, green: 0.9, blue: 0.5),
                background: Color(red: 0.15, green: 0.12, blue: 0.05)
            )
        case .security_badge:
            return DocumentColors(
                primary: Color(red: 0.1, green: 0.1, blue: 0.1),
                accent: Color(red: 0.9, green: 0.15, blue: 0.15),
                background: Color(red: 0.08, green: 0.08, blue: 0.08),
                textPrimary: .white,
                textSecondary: Color(red: 0.7, green: 0.7, blue: 0.7)
            )
        case .transport_pass:
            return DocumentColors(
                primary: Color(red: 0.0, green: 0.6, blue: 0.35),
                accent: Color(red: 0.2, green: 0.9, blue: 0.5),
                background: Color(red: 0.05, green: 0.12, blue: 0.08)
            )
        case .conference_badge:
            return DocumentColors(
                primary: Color(red: 0.2, green: 0.3, blue: 0.85),
                accent: Color(red: 0.5, green: 0.8, blue: 1.0),
                background: Color(red: 0.06, green: 0.08, blue: 0.18)
            )
        case .permit:
            return DocumentColors(
                primary: Color(red: 0.4, green: 0.35, blue: 0.3),
                accent: Color(red: 0.7, green: 0.6, blue: 0.4),
                background: Color(red: 0.12, green: 0.1, blue: 0.08)
            )
        case .invitation:
            return DocumentColors(
                primary: Color(red: 0.7, green: 0.2, blue: 0.5),
                accent: Color(red: 1.0, green: 0.7, blue: 0.85),
                background: Color(red: 0.15, green: 0.06, blue: 0.1)
            )
        }
    }

    var fieldTemplates: [String] {
        switch self {
        case .press_pass:
            return ["NAME", "OUTLET", "PRESS ID", "VALID THROUGH", "ACCESS LEVEL"]
        case .event_ticket:
            return ["EVENT", "ATTENDEE", "DATE", "VENUE", "SEAT", "REF"]
        case .boarding_pass:
            return ["PASSENGER", "FLIGHT", "FROM", "TO", "DATE", "GATE", "SEAT", "BOARDING"]
        case .driving_licence:
            return ["NAME", "DATE OF BIRTH", "LICENCE NO.", "ISSUED", "EXPIRES", "CLASS"]
        case .membership:
            return ["MEMBER", "ORGANISATION", "MEMBER NO.", "SINCE", "TIER", "EXPIRES"]
        case .security_badge:
            return ["NAME", "TITLE", "CLEARANCE", "BADGE NO.", "FACILITY", "EXPIRES"]
        case .transport_pass:
            return ["HOLDER", "PASS TYPE", "ZONE", "VALID FROM", "VALID TO", "SERIAL"]
        case .conference_badge:
            return ["NAME", "TITLE", "COMPANY", "CONFERENCE", "DATE", "BADGE NO."]
        case .permit:
            return ["HOLDER", "PERMIT TYPE", "PERMIT NO.", "ISSUED BY", "ISSUED", "EXPIRES", "CONDITIONS"]
        case .invitation:
            return ["GUEST", "EVENT", "HOST", "DATE", "TIME", "VENUE", "DRESS CODE"]
        }
    }

    var contextKeywords: [String] {
        switch self {
        case .press_pass:
            return ["press", "media", "journalist", "reporter", "interview", "news",
                    "coverage", "newspaper", "broadcast", "photography", "press conference"]
        case .event_ticket:
            return ["concert", "show", "gig", "festival", "performance", "music",
                    "event", "arena", "stadium", "theatre", "theater", "live"]
        case .boarding_pass:
            return ["flight", "airport", "plane", "fly", "airline", "boarding",
                    "departure", "arrival", "terminal", "gate", "aviation"]
        case .driving_licence:
            return ["drive", "car", "vehicle", "road", "licence", "license",
                    "traffic", "rental", "driving", "automobile", "motor"]
        case .membership:
            return ["member", "club", "gym", "library", "subscribe", "loyalty",
                    "vip", "exclusive", "premium", "society", "association"]
        case .security_badge:
            return ["security", "restricted", "classified", "clearance", "access",
                    "facility", "government", "military", "authorized", "badge"]
        case .transport_pass:
            return ["bus", "train", "metro", "subway", "tram", "transit",
                    "transport", "commute", "rail", "tube", "travel"]
        case .conference_badge:
            return ["conference", "summit", "convention", "seminar", "workshop",
                    "expo", "symposium", "meetup", "keynote", "tech", "developer"]
        case .permit:
            return ["permit", "permission", "authorized", "construction", "parking",
                    "filming", "work", "building", "official", "council", "license"]
        case .invitation:
            return ["invited", "invitation", "party", "wedding", "gala", "reception",
                    "dinner", "celebration", "ceremony", "ball", "gathering", "soiree"]
        }
    }
}
