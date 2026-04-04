import Foundation

struct ContextDetector {

    struct ScoredResult: Comparable {
        let documentType: DocumentType
        let score: Double

        static func < (lhs: ScoredResult, rhs: ScoredResult) -> Bool {
            lhs.score < rhs.score
        }
    }

    /// Analyse a free-text situation description and return the best-matching document type.
    /// Falls back to `.press_pass` when nothing matches well enough.
    static func detect(situation: String) -> DocumentType {
        let results = scoreAll(situation: situation)
        return results.first?.documentType ?? .press_pass
    }

    /// Return all document types ranked by relevance to the given situation.
    static func scoreAll(situation: String) -> [ScoredResult] {
        let tokens = tokenise(situation)
        guard !tokens.isEmpty else {
            return DocumentType.allCases.map { ScoredResult(documentType: $0, score: 0) }
        }

        var results: [ScoredResult] = []

        for docType in DocumentType.allCases {
            let keywords = docType.contextKeywords
            var score: Double = 0

            for token in tokens {
                for keyword in keywords {
                    if token == keyword {
                        // Exact match
                        score += 1.0
                    } else if keyword.contains(token) || token.contains(keyword) {
                        // Partial / substring match
                        score += 0.5
                    }
                }
            }

            // Normalise by keyword count to avoid bias toward types with more keywords
            let normalised = keywords.isEmpty ? 0 : score / Double(keywords.count)
            results.append(ScoredResult(documentType: docType, score: normalised))
        }

        return results.sorted(by: >)
    }

    // MARK: - Private

    private static func tokenise(_ input: String) -> [String] {
        input
            .lowercased()
            .components(separatedBy: CharacterSet.alphanumerics.inverted)
            .filter { $0.count > 1 }
    }
}
