package com.rojas.consumodatos.data.remote

enum class Config (val url: String, val key: String) {
    STAGING("https://app.claudioviajando.com/api/saas", "crr_c16cb5041aeaad8849b565e746e6da7d79b39a98e769bc0a"),
    PRODUCTION("https://app.claudioviajando.com/api/saas", "crr_c16cb5041aeaad8849b565e746e6da7d79b39a98e769bc0a")
}

enum class Enpoints(val url: String) {
    SAVE_NOTICE("/notices"),
    GET_NOTICE("/notices")
}