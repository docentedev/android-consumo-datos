package com.rojas.consumodatos.domain.repository

import com.rojas.consumodatos.domain.model.Notice

interface NoticeRepository {
    suspend fun getNotices(): Result<List<Notice>>
}
