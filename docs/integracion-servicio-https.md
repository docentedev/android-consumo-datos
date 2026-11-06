# Guía Educativa: Integración de Servicios Web HTTPS con Retrofit, OkHttp y Hilt en Android

Esta guía tutorial está diseñada para estudiantes de desarrollo Android. Explica paso a paso cómo consumir un servicio web seguro (**HTTPS**) utilizando el patrón de arquitectura recomendado por Google: **Clean Architecture**, **MVVM**, **Retrofit**, **OkHttp**, **Corrutinas / Flow**, **Hilt** y **Jetpack Compose**.

---

## 🎯 Objetivo de la Guía

Al finalizar este tutorial, aprenderás a:
1. Configurar una URL base y autenticación mediante llaves de API (**ApiKey**).
2. Crear un **Interceptor de OkHttp** para adjuntar automáticamente encabezados de autenticación HTTP (`Authorization: ApiKey <TOKEN>`).
3. Modelar respuestas JSON complejas y paginadas utilizando objetos **DTO** (Data Transfer Objects).
4. Implementar una arquitectura por capas desacopladas (Data, Domain, Presentation).
5. Renderizar los datos en tiempo real en la interfaz de usuario con **Jetpack Compose**.

---

## 📐 1. Arquitectura y Flujo de Datos

El flujo de información para consumir el servicio HTTPS sigue una dirección unidireccional:

```text
[Servidor REST HTTPS]
         ▲
         │ (HTTP Request + Header "authorization: ApiKey <KEY>")
    [OkHttp Client]
         │ (HTTP Response JSON)
   [Retrofit API Service]
         │ (NoticeResponseDto)
 [NoticeRemoteDataSource]
         │ (DTOs)
   [NoticeRepository] ──► (Transforma DTOs a Modelos de Dominio: Notice)
         │ (Result<List<Notice>>)
   [NoticeViewModel] ──► (Actualiza StateFlow: NoticeUiState)
         │ (Estado de la UI)
  [NoticeScreen (Compose)]
```

---

## 🔐 2. Paso 1: Configuración de la API y Endpoints (`Config.kt`)

En lugar de escribir URLs y llaves de acceso "hardcodeadas" en múltiples archivos, creamos un archivo central de configuración utilizando `enum class`:

```kotlin
package com.rojas.consumodatos.data.remote

enum class Config(val url: String, val key: String) {
    STAGING(
        url = "https://app.claudioviajando.com/api/saas",
        key = "crr_c16cb5041aeaad8849b565e746e6da7d79b39a98e769bc0a"
    ),
    PRODUCTION(
        url = "https://app.claudioviajando.com/api/saas",
        key = "crr_c16cb5041aeaad8849b565e746e6da7d79b39a98e769bc0a"
    )
}

enum class Enpoints(val url: String) {
    SAVE_NOTICE("/notices"),
    GET_NOTICE("/notices")
}
```

> 💡 **Explicación para Estudiantes**:
> - `Config.PRODUCTION.url`: Es el dominio base HTTPS del servidor REST.
> - `Config.PRODUCTION.key`: Es la credencial privada/ApiKey necesaria para autenticar las peticiones.
> - `Enpoints`: Define las rutas relativas de cada endpoint de la API.

---

## 📦 3. Paso 2: Modelado del JSON / DTOs (`data/remote`)

El servidor HTTPS devuelve un objeto JSON paginado con la siguiente estructura:

```json
{
    "items": [
        {
            "id": "64",
            "user_id": "1",
            "email": "claudio.dcv@gmail.com",
            "text": "Informe $89.990 (stock 40)",
            "created_at": "2026-10-13T16:40:28.175Z"
        }
    ],
    "total": 7,
    "page": 1,
    "limit": 50,
    "pages": 1
}
```

Para recibir este JSON en Kotlin, creamos dos clases DTO usando la anotación `@SerializedName` de Gson:

### A. Objeto por Cada Elemento (`NoticeDto.kt`)
```kotlin
package com.rojas.consumodatos.data.remote

import com.google.gson.annotations.SerializedName

data class NoticeDto(
    @SerializedName("id") val id: String? = null,
    @SerializedName("user_id") val userId: String? = null,
    @SerializedName("email") val email: String? = null,
    @SerializedName("text") val text: String? = null,
    @SerializedName("created_at") val createdAt: String? = null
)
```

### B. Objeto Envoltura de Respuesta (`NoticeResponseDto.kt`)
```kotlin
package com.rojas.consumodatos.data.remote

import com.google.gson.annotations.SerializedName

data class NoticeResponseDto(
    @SerializedName("items") val items: List<NoticeDto> = emptyList(),
    @SerializedName("total") val total: Int = 0,
    @SerializedName("page") val page: Int = 1,
    @SerializedName("limit") val limit: Int = 50,
    @SerializedName("pages") val pages: Int = 1
)
```

---

## 🌐 4. Paso 3: Interfaz Retrofit (`data/remote/NoticeApiService.kt`)

Definimos la llamada HTTP asíncrona mediante la anotación `@GET`:

```kotlin
package com.rojas.consumodatos.data.remote

import retrofit2.http.GET

interface NoticeApiService {
    @GET("notices")
    suspend fun getNotices(): NoticeResponseDto
}
```

> 💡 **Explicación para Estudiantes**:
> La función se marca como `suspend` para ser ejecutada dentro de una Corrutina en segundo plano sin bloquear el hilo principal de la interfaz de usuario.

---

## ⚡ 5. Paso 4: Capa de Red e Interceptores OkHttp con Hilt (`di/NetworkModule.kt`)

Para autenticar las peticiones en el servidor HTTPS sin repetir código en cada llamada, utilizamos un **Interceptor de OkHttp**.

```kotlin
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
            // Interceptor que adjunta la cabecera de autenticación "authorization"
            .addInterceptor { chain ->
                val request = chain.request().newBuilder()
                    .addHeader("authorization", "ApiKey " + Config.PRODUCTION.key)
                    .addHeader("Content-Type", "application/json")
                    .build()
                chain.proceed(request)
            }
            // Interceptor para ver las peticiones/respuestas en el Logcat
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
```

---

## 🏛️ 6. Paso 5: Modelo de Dominio y Repositorio (`domain` y `data/repository`)

### A. Modelo de Dominio Limpio (`domain/model/Notice.kt`)
Representa la entidad que utilizará nuestra lógica de negocio y pantalla, sin depender de Retrofit ni de librerías externas:

```kotlin
package com.rojas.consumodatos.domain.model

data class Notice(
    val id: String,
    val userId: String,
    val email: String,
    val text: String,
    val createdAt: String
)
```

### B. Interfaz del Repositorio (`domain/repository/NoticeRepository.kt`)
```kotlin
package com.rojas.consumodatos.domain.repository

import com.rojas.consumodatos.domain.model.Notice

interface NoticeRepository {
    suspend fun getNotices(): Result<List<Notice>>
}
```

### C. Implementación del Repositorio (`data/repository/NoticeRepositoryImpl.kt`)
Convierte los DTOs de red recibidos en objetos del modelo de dominio limpiando valores nulos:

```kotlin
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
```

---

## 🎨 7. Paso 6: ViewModel y Estado de UI (`ui/notice`)

### A. Estado de UI Inmutable (`NoticeUiState.kt`)
```kotlin
package com.rojas.consumodatos.ui.notice

import com.rojas.consumodatos.domain.model.Notice

data class NoticeUiState(
    val notices: List<Notice> = emptyList(),
    val isLoading: Boolean = false,
    val errorMessage: String? = null
)
```

### B. ViewModel (`NoticeViewModel.kt`)
Gestiona el estado y realiza la llamada asíncrona a la API:

```kotlin
package com.rojas.consumodatos.ui.notice

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.rojas.consumodatos.domain.repository.NoticeRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class NoticeViewModel @Inject constructor(
    private val repository: NoticeRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(NoticeUiState())
    val uiState: StateFlow<NoticeUiState> = _uiState.asStateFlow()

    init {
        loadNotices()
    }

    fun loadNotices() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null) }
            repository.getNotices()
                .onSuccess { list ->
                    _uiState.update { it.copy(notices = list, isLoading = false) }
                }
                .onFailure { error ->
                    _uiState.update { it.copy(errorMessage = error.message, isLoading = false) }
                }
        }
    }
}
```

---

## 📱 8. Paso 7: Pantalla en Jetpack Compose (`NoticeScreen.kt`)

Renderiza los estados de la interfaz (**Cargando**, **Error**, **Lista Vacía** y **Éxito**):

```kotlin
package com.rojas.consumodatos.ui.notice

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@Composable
fun NoticeScreen(
    viewModel: NoticeViewModel,
    modifier: Modifier = Modifier
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Avisos / Noticias",
                style = MaterialTheme.typography.headlineMedium
            )
            Button(onClick = viewModel::loadNotices) {
                Text("Recargar")
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        when {
            uiState.isLoading -> {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            }
            uiState.errorMessage != null -> {
                Card(
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(
                        text = "Error: ${uiState.errorMessage}",
                        modifier = Modifier.padding(16.dp),
                        color = MaterialTheme.colorScheme.onErrorContainer
                    )
                }
            }
            uiState.notices.isEmpty() -> {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text("No hay avisos disponibles.")
                }
            }
            else -> {
                LazyColumn(
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    items(uiState.notices, key = { it.id }) { notice ->
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text(
                                    text = notice.text,
                                    style = MaterialTheme.typography.titleMedium
                                )
                                Spacer(modifier = Modifier.height(6.dp))
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Text(
                                        text = notice.email,
                                        style = MaterialTheme.typography.bodySmall,
                                        color = MaterialTheme.colorScheme.primary
                                    )
                                    Text(
                                        text = notice.createdAt,
                                        style = MaterialTheme.typography.bodySmall,
                                        color = MaterialTheme.colorScheme.outline
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

---

## 🔒 9. Paso 8: Permisos en AndroidManifest (`AndroidManifest.xml`)

Recuerda solicitar el permiso de red en la manifestación de tu aplicación:

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

---

## 💡 Resumen de Buenas Prácticas para Estudiantes

1. **Centralizar Configuración**: Mantén tus llaves y URLs en archivos o constantes configurables (o mediante `BuildConfig`).
2. **Interceptores de OkHttp**: Utilízalos para inyectar cabeceras comunes (tokens, lenguaje, ApiKey) en lugar de pasarlas manualmente en cada llamada `@GET` o `@POST`.
3. **Manejo de Errores Defensivo**: Utiliza `runCatching` y envoltorios como `Result<T>` para capturar fallos de red (sin conexión, error 500, timeout) sin cerrar la aplicación.
4. **Desacoplamiento de Capas**: Nunca expongas DTOs de red directamente a la vista (Compose UI). Conviértelos siempre a modelos de dominio limpios.
