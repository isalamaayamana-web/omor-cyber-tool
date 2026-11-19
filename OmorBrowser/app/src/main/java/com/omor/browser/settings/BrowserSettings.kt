package com.omor.browser.settings

data class BrowserSettings(
    val javaScriptEnabled: Boolean = true,
    val blockThirdPartyCookies: Boolean = true,
    val safeBrowsing: Boolean = true,
    val blockExecutableDownloads: Boolean = true,
    val adBlockEnabled: Boolean = true,
    val desktopMode: Boolean = false
)
