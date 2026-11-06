package com.rojas.consumodatos.ui.notice

import com.rojas.consumodatos.domain.model.Notice

data class NoticeUiState(
    val notices: List<Notice> = emptyList(),
    val isLoading: Boolean = false,
    val errorMessage: String? = null
)
