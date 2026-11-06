package com.rojas.consumodatos.data.remote

import javax.inject.Inject

interface NoticeRemoteDataSource {
    suspend fun getNotices(): NoticeResponseDto
}

class NoticeRemoteDataSourceImpl @Inject constructor(
    private val apiService: NoticeApiService
) : NoticeRemoteDataSource {
    override suspend fun getNotices(): NoticeResponseDto = apiService.getNotices()
}
