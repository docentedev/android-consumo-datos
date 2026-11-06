package com.rojas.consumodatos.di

import com.rojas.consumodatos.data.remote.Config
import com.rojas.consumodatos.data.remote.NoticeApiService
import com.rojas.consumodatos.data.remote.NoticeRemoteDataSource
import com.rojas.consumodatos.data.remote.NoticeRemoteDataSourceImpl
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor { chain ->
                val request = chain.request().newBuilder()
                    .addHeader("authorization", "ApiKey " + Config.PRODUCTION.key)
                    .addHeader("Content-Type", "application/json")
                    .build()
                chain.proceed(request)
            }
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            })
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        val baseUrl = if (Config.PRODUCTION.url.endsWith("/")) {
            Config.PRODUCTION.url
        } else {
            "${Config.PRODUCTION.url}/"
        }

        return Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideNoticeApiService(retrofit: Retrofit): NoticeApiService {
        return retrofit.create(NoticeApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideNoticeRemoteDataSource(impl: NoticeRemoteDataSourceImpl): NoticeRemoteDataSource = impl
}
