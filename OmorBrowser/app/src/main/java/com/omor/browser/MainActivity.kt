package com.omor.browser

import android.annotation.SuppressLint
import android.graphics.Color
import android.os.Bundle
import android.view.View
import android.view.inputmethod.EditorInfo
import android.webkit.WebView
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.Toast
import androidx.activity.ComponentActivity
import com.omor.browser.adblock.AdBlocker
import com.omor.browser.download.handleDownload
import com.omor.browser.settings.BrowserSettings
import com.omor.browser.web.BrowserWebViewClient
import com.omor.browser.web.createSecureWebView

class MainActivity : ComponentActivity() {
    private lateinit var webView: WebView
    private lateinit var address: EditText
    private lateinit var progress: ProgressBar
    private lateinit var adBlocker: AdBlocker
    private val settings = BrowserSettings()

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        adBlocker = AdBlocker(this).also { it.enabled = settings.adBlockEnabled }

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.WHITE)
        }
        val toolbar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(8, 8, 8, 8)
        }
        address = EditText(this).apply {
            hint = "Search or enter website"
            singleLine = true
            imeOptions = EditorInfo.IME_ACTION_GO
            layoutParams = LinearLayout.LayoutParams(0, dp(48), 1f)
        }
        val go = Button(this).apply {
            text = "Go"
            setOnClickListener { loadInput() }
        }
        val back = Button(this).apply {
            text = "‹"
            contentDescription = "Back"
            setOnClickListener { if (webView.canGoBack()) webView.goBack() }
        }
        val forward = Button(this).apply {
            text = "›"
            contentDescription = "Forward"
            setOnClickListener { if (webView.canGoForward()) webView.goForward() }
        }
        val reload = Button(this).apply {
            text = "↻"
            contentDescription = "Reload"
            setOnClickListener { webView.reload() }
        }
        toolbar.addView(back)
        toolbar.addView(forward)
        toolbar.addView(address)
        toolbar.addView(go)
        toolbar.addView(reload)

        progress = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
            max = 100
            visibility = View.GONE
        }
        webView = createSecureWebView(this, settings)
        webView.webViewClient = BrowserWebViewClient(
            adBlocker,
            onPageStarted = { url ->
                if (!url.isNullOrBlank()) address.setText(url)
                progress.visibility = View.VISIBLE
            },
            onPageFinished = { url ->
                if (!url.isNullOrBlank()) address.setText(url)
                progress.visibility = View.GONE
            }
        )
        webView.webChromeClient = object : android.webkit.WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                progress.progress = newProgress
                progress.visibility = if (newProgress >= 100) View.GONE else View.VISIBLE
            }
        }
        webView.setDownloadListener { url, userAgent, contentDisposition, mimeType, _ ->
            handleDownload(this, url, userAgent, contentDisposition, mimeType, settings)
        }

        root.addView(toolbar)
        root.addView(progress, LinearLayout.LayoutParams(-1, dp(3)))
        root.addView(webView, LinearLayout.LayoutParams(-1, 0, 1f))
        setContentView(root)

        address.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_GO || actionId == EditorInfo.IME_ACTION_DONE) {
                loadInput()
                true
            } else false
        }

        if (savedInstanceState == null) webView.loadUrl("https://www.google.com")
        else webView.restoreState(savedInstanceState)
    }

    private fun loadInput() {
        val input = address.text.toString().trim()
        if (input.isEmpty()) return
        val url = when {
            input.startsWith("https://", true) || input.startsWith("http://", true) -> input
            input.contains('.') && !input.contains(' ') -> "https://$input"
            else -> "https://www.google.com/search?q=${UriEncode.encode(input)}"
        }
        webView.loadUrl(url)
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density).toInt()

    override fun onSaveInstanceState(outState: Bundle) {
        webView.saveState(outState)
        super.onSaveInstanceState(outState)
    }

    @Deprecated("Deprecated by Android")
    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) webView.goBack()
        else super.onBackPressed()
    }

    override fun onDestroy() {
        if (::webView.isInitialized) {
            webView.stopLoading()
            webView.loadUrl("about:blank")
            webView.clearHistory()
            webView.removeAllViews()
            webView.destroy()
        }
        super.onDestroy()
    }
}

private object UriEncode {
    fun encode(value: String): String = java.net.URLEncoder.encode(value, "UTF-8")
}
