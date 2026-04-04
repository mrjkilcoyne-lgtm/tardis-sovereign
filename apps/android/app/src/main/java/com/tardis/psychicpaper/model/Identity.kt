package com.tardis.psychicpaper.model

import android.content.Context
import android.content.SharedPreferences

/**
 * Holds the user's base identity, persisted in SharedPreferences.
 * Psychic Paper stamps these details onto every generated credential.
 */
data class Identity(
    val name: String = "",
    val organisation: String = "",
    val title: String = "",
) {
    val isComplete: Boolean
        get() = name.isNotBlank()

    companion object {
        private const val PREFS_NAME = "psychic_paper_identity"
        private const val KEY_NAME = "name"
        private const val KEY_ORG = "organisation"
        private const val KEY_TITLE = "title"
        private const val KEY_SETUP_DONE = "setup_complete"

        fun load(context: Context): Identity {
            val prefs = prefs(context)
            return Identity(
                name = prefs.getString(KEY_NAME, "") ?: "",
                organisation = prefs.getString(KEY_ORG, "") ?: "",
                title = prefs.getString(KEY_TITLE, "") ?: "",
            )
        }

        fun save(context: Context, identity: Identity) {
            prefs(context).edit()
                .putString(KEY_NAME, identity.name)
                .putString(KEY_ORG, identity.organisation)
                .putString(KEY_TITLE, identity.title)
                .putBoolean(KEY_SETUP_DONE, true)
                .apply()
        }

        fun hasCompletedSetup(context: Context): Boolean =
            prefs(context).getBoolean(KEY_SETUP_DONE, false)

        private fun prefs(context: Context): SharedPreferences =
            context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    }
}
