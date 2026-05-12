import Foundation

struct GeneratedDocument: Equatable {
    let documentType: DocumentType
    let fields: [DocumentField]
    let qrPayload: String
}

struct DocumentGenerator {

    static func generate(identity: Identity, documentType: DocumentType) -> GeneratedDocument {
        let fields = populateFields(identity: identity, documentType: documentType)
        let qrPayload = buildQRPayload(documentType: documentType, fields: fields)
        return GeneratedDocument(documentType: documentType, fields: fields, qrPayload: qrPayload)
    }

    // MARK: - Field Population

    private static func populateFields(identity: Identity, documentType: DocumentType) -> [DocumentField] {
        let templates = documentType.fieldTemplates
        return templates.map { label in
            DocumentField(label: label, value: valueFor(label: label, identity: identity, documentType: documentType))
        }
    }

    private static func valueFor(label: String, identity: Identity, documentType: DocumentType) -> String {
        let upper = label.uppercased()

        // Identity-based fields
        switch upper {
        case "NAME", "PASSENGER", "HOLDER", "MEMBER", "ATTENDEE", "GUEST":
            return identity.name.uppercased()
        case "TITLE":
            return identity.title.isEmpty ? "General" : identity.title
        case "ORGANISATION", "COMPANY", "OUTLET":
            return identity.organisation.isEmpty ? "Independent" : identity.organisation
        default:
            break
        }

        // Document-specific generation
        switch upper {
        case "PRESS ID", "BADGE NO.", "MEMBER NO.", "LICENCE NO.", "SERIAL", "PERMIT NO.":
            return generateID(prefix: prefixFor(documentType))
        case "REF":
            return generateRef()
        case "FLIGHT":
            return generateFlight()
        case "FROM":
            return "LHR LONDON"
        case "TO":
            return "JFK NEW YORK"
        case "GATE":
            return "\(["A", "B", "C", "D"].randomElement()!)\(Int.random(in: 1...42))"
        case "SEAT":
            return "\(Int.random(in: 1...38))\(["A","B","C","D","E","F"].randomElement()!)"
        case "BOARDING":
            return generateTime()
        case "DATE":
            return generateDate()
        case "TIME":
            return generateTime()
        case "ISSUED", "VALID FROM", "SINCE":
            return generatePastDate()
        case "EXPIRES", "VALID THROUGH", "VALID TO":
            return generateFutureDate()
        case "ACCESS LEVEL":
            return ["ALL AREAS", "BACKSTAGE", "PRESS POOL", "LEVEL 3"].randomElement()!
        case "CLEARANCE":
            return ["LEVEL 5", "TOP SECRET", "ALPHA", "RESTRICTED"].randomElement()!
        case "FACILITY":
            return identity.organisation.isEmpty ? "CENTRAL OPERATIONS" : identity.organisation.uppercased()
        case "EVENT":
            return documentType == .event_ticket ? "LIVE PERFORMANCE" : "ANNUAL SUMMIT 2026"
        case "CONFERENCE":
            return "\(identity.organisation.isEmpty ? "TECH" : identity.organisation.uppercased()) CONF 2026"
        case "VENUE":
            return ["GRAND HALL", "ALEXANDRA PALACE", "CONVENTION CENTRE", "THE RITZ"].randomElement()!
        case "PASS TYPE":
            return ["MONTHLY", "ANNUAL", "DAY PASS", "WEEKLY"].randomElement()!
        case "ZONE":
            return "ZONES 1-\(Int.random(in: 3...6))"
        case "TIER":
            return ["GOLD", "PLATINUM", "BLACK", "ELITE"].randomElement()!
        case "PERMIT TYPE":
            return ["GENERAL ACCESS", "FILMING", "CONSTRUCTION", "SPECIAL EVENT"].randomElement()!
        case "ISSUED BY":
            return "METROPOLITAN AUTHORITY"
        case "CONDITIONS":
            return "VALID WITH PHOTO ID"
        case "HOST":
            return ["The Director", "Management", "The Committee"].randomElement()!
        case "DRESS CODE":
            return ["BLACK TIE", "SMART CASUAL", "FORMAL", "COCKTAIL"].randomElement()!
        case "CLASS":
            return ["A", "B", "C", "A B"].randomElement()!
        case "DATE OF BIRTH":
            return generateDOB()
        default:
            return "---"
        }
    }

    // MARK: - Generators

    private static func prefixFor(_ type: DocumentType) -> String {
        switch type {
        case .press_pass:       return "PR"
        case .event_ticket:     return "TK"
        case .boarding_pass:    return "BP"
        case .driving_licence:  return "DL"
        case .membership:       return "MB"
        case .security_badge:   return "SC"
        case .transport_pass:   return "TP"
        case .conference_badge: return "CB"
        case .permit:           return "PM"
        case .invitation:       return "IV"
        }
    }

    private static func generateID(prefix: String) -> String {
        let num = Int.random(in: 100000...999999)
        return "\(prefix)-\(num)"
    }

    private static func generateRef() -> String {
        let chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return String((0..<8).map { _ in chars.randomElement()! })
    }

    private static func generateFlight() -> String {
        let airlines = ["BA", "VS", "AA", "UA", "DL", "LH"]
        let airline = airlines.randomElement()!
        return "\(airline)\(Int.random(in: 100...999))"
    }

    private static func generateDate() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "dd MMM yyyy"
        let future = Date().addingTimeInterval(Double.random(in: 86400...604800))
        return formatter.string(from: future).uppercased()
    }

    private static func generatePastDate() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "dd MMM yyyy"
        let past = Date().addingTimeInterval(-Double.random(in: 2592000...63072000))
        return formatter.string(from: past).uppercased()
    }

    private static func generateFutureDate() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "dd MMM yyyy"
        let future = Date().addingTimeInterval(Double.random(in: 2592000...31536000))
        return formatter.string(from: future).uppercased()
    }

    private static func generateDOB() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "dd/MM/yyyy"
        let dob = Date().addingTimeInterval(-Double.random(in: 662688000...1261440000))
        return formatter.string(from: dob)
    }

    private static func generateTime() -> String {
        let hour = Int.random(in: 6...22)
        let minute = [0, 15, 30, 45].randomElement()!
        return String(format: "%02d:%02d", hour, minute)
    }

    // MARK: - QR Payload

    private static func buildQRPayload(documentType: DocumentType, fields: [DocumentField]) -> String {
        var parts = [documentType.displayName]
        for field in fields.prefix(4) {
            parts.append("\(field.label): \(field.value)")
        }
        return parts.joined(separator: " | ")
    }
}
