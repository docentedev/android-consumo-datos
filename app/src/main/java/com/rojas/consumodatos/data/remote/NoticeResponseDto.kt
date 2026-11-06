package com.rojas.consumodatos.data.remote

import com.google.gson.annotations.SerializedName

data class NoticeResponseDto(
    @SerializedName("items") val items: List<NoticeDto> = emptyList(),
    @SerializedName("total") val total: Int = 0,
    @SerializedName("page") val page: Int = 1,
    @SerializedName("limit") val limit: Int = 50,
    @SerializedName("pages") val pages: Int = 1
)
