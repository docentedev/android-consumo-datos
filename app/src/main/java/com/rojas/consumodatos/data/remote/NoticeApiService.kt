package com.rojas.consumodatos.data.remote

import retrofit2.http.GET

interface NoticeApiService {
    @GET("notices")
    suspend fun getNotices(): NoticeResponseDto
}
