import Foundation

struct Identity: Codable, Equatable {
    var name: String
    var organisation: String
    var title: String

    static let empty = Identity(name: "", organisation: "", title: "")

    var isValid: Bool {
        !name.trimmingCharacters(in: .whitespaces).isEmpty
    }

    // MARK: - UserDefaults Persistence

    private static let storageKey = "psychicPaper.identity"

    func save() {
        if let data = try? JSONEncoder().encode(self) {
            UserDefaults.standard.set(data, forKey: Self.storageKey)
        }
    }

    static func load() -> Identity {
        guard let data = UserDefaults.standard.data(forKey: storageKey),
              let identity = try? JSONDecoder().decode(Identity.self, from: data)
        else {
            return .empty
        }
        return identity
    }

    static func clear() {
        UserDefaults.standard.removeObject(forKey: storageKey)
    }
}
