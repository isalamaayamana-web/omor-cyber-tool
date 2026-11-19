package com.omor.browser.download

import android.app.AlertDialog
import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Environment
import android.webkit.CookieManager
import android.webkit.URLUtil
import android.widget.Toast
import com.omor.browser.settings.BrowserSettings

private val RISKY_EXTENSIONS = setOf(
    "apk", "exe", "msi", "bat", "cmd", "scr", "ps1", "vbs", "jar", "sh", "dmg", "app"
)

fun handleDownload(
    context: Context,
    url: String,
    userAgent: String,
    contentDisposition: String?,
    mimeType: String?,
    settings: BrowserSettings
) {
    val fileName = URLUtil.guessFileName(url, contentDisposition, mimeType)
    val ext = fileName.substringAfterLast('.', "").lowercase()

    if (settings.blockExecutableDownloads && ext in RISKY_EXTENSIONS) {
        Toast.makeText(context, "ঝুঁকিপূর্ণ ফাইল ব্লক করা হয়েছে: $fileName", Toast.LENGTH_LONG).show()
        return
    }

    AlertDialog.Builder(context)
        .setTitle("ডাউনলোড করবেন?")
        .setMessage(fileName)
        .setPositiveButton("ডাউনলোড") { _, _ ->
            try {
                val request = DownloadManager.Request(Uri.parse(url)).apply {
                    mimeType?.let { setMimeType(it) }
                    addRequestHeader("User-Agent", userAgent)
                    CookieManager.getInstance().getCookie(url)?.let { addRequestHeader("Cookie", it) }
                    setTitle(fileName)
                    setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
                    setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, fileName)
                }
                (context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager).enqueue(request)
                Toast.makeText(context, "ডাউনলোড শুরু হয়েছে", Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                Toast.makeText(context, "ডাউনলোড শুরু করা যায়নি", Toast.LENGTH_LONG).show()
            }
        }
        .setNegativeButton("বাতিল", null)
        .show()
}
