package com.omor.browser.web

import android.annotation.SuppressLint
import android.content.Context
import android.os.Build
import android.webkit.CookieManager
import android.webkit.WebSettings
import android.webkit.WebView
import com.omor.browser.settings.BrowserSettings

@SuppressLint("SetJavaScriptEnabled")
fun createSecureWebView(context: Context, s: BrowserSettings): WebView {
    return WebView(context).apply {
        settings.apply {
            javaScriptEnabled = s.javaScriptEnabled
            domStorageEnabled = true
            databaseEnabled = false
            allowFileAccess = false
            allowContentAccess = false
            setGeolocationEnabled(false)
            mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
            cacheMode = WebSettings.LOAD_DEFAULT
            if (s.desktopMode) {
                userAgentString = userAgentString
                    .replace("Android", "X11; Linux x86_64")
                    .replace("Mobile", "")
            }
            if (Build.VERSION.SDK_INT >= 26) safeBrowsingEnabled = s.safeBrowsing
        }
        CookieManager.getInstance().setAcceptCookie(true)
        CookieManager.getInstance().setAcceptThirdPartyCookies(this, !s.blockThirdPartyCookies)
    }
}
