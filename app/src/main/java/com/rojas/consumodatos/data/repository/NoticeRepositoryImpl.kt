package com.rojas.consumodatos.data.repository

import com.rojas.consumodatos.data.remote.NoticeRemoteDataSource
import com.rojas.consumodatos.domain.model.Notice
import com.rojas.consumodatos.domain.repository.NoticeRepository
import javax.inject.Inject

class NoticeRepositoryImpl @Inject constructor(
    private val remoteDataSource: NoticeRemoteDataSource
) : NoticeRepository {

    override suspend fun getNotices(): Result<List<Notice>> {
        return runCatching {
            val response = remoteDataSource.getNotices()
            response.items.map { dto ->
                Notice(
                    id = dto.id.orEmpty(),
                    userId = dto.userId.orEmpty(),
                    email = dto.email.orEmpty(),
                    text = dto.text.orEmpty(),
                    createdAt = dto.createdAt.orEmpty()
                )
            }
        }
    }
}
