package com.rojas.consumodatos.domain.model

data class Notice(
    val id: String,
    val userId: String,
    val email: String,
    val text: String,
    val createdAt: String
)
