package com.tardis.psychicpaper.model

/**
 * Matches free-text situation descriptions to the best [DocumentType].
 *
 * Scoring: each keyword hit in the input adds one point to that document
 * type's score. Highest score wins; ties break in enum-declaration order.
 * If nothing matches at all, [DocumentType.DEFAULT] is returned.
 */
object ContextDetector {

    fun detect(situation: String): DocumentType {
        if (situation.isBlank()) return DocumentType.DEFAULT

        val words = situation.lowercase().split(Regex("[\\s,.:;!?]+"))

        var bestType = DocumentType.DEFAULT
        var bestScore = 0

        for (type in DocumentType.entries) {
            val score = type.keywords.sumOf { keyword ->
                words.count { it.contains(keyword) }
            }
            if (score > bestScore) {
                bestScore = score
                bestType = type
            }
        }

        return bestType
    }
}
