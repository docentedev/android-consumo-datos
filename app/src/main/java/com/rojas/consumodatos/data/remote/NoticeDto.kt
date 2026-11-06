package com.rojas.consumodatos.data.remote

import com.google.gson.annotations.SerializedName

data class NoticeDto(
    @SerializedName("id") val id: String? = null,
    @SerializedName("user_id") val userId: String? = null,
    @SerializedName("email") val email: String? = null,
    @SerializedName("text") val text: String? = null,
    @SerializedName("created_at") val createdAt: String? = null
)
