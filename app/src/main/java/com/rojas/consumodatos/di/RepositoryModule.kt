package com.rojas.consumodatos.di

import com.rojas.consumodatos.data.repository.NoticeRepositoryImpl
import com.rojas.consumodatos.domain.repository.NoticeRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
interface RepositoryModule {

    @Binds
    @Singleton
    fun bindNoticeRepository(
        impl: NoticeRepositoryImpl
    ): NoticeRepository
}
