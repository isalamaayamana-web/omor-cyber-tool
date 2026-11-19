package com.omor.browser.adblock

import android.content.Context
import android.webkit.WebResourceResponse
import java.io.ByteArrayInputStream
import java.util.concurrent.ConcurrentHashMap

class AdBlocker(private val context: Context) {
    @Volatile var enabled: Boolean = true
    private val blockedHosts: Set<String> by lazy { loadHosts() }
    private val cache = ConcurrentHashMap<String, Boolean>()

    private fun loadHosts(): Set<String> = try {
        context.assets.open("adblock_hosts.txt").bufferedReader().useLines { lines ->
            lines.map { it.trim().lowercase() }
                .filter { it.isNotEmpty() && !it.startsWith("#") }
                .toSet()
        }
    } catch (_: Exception) { emptySet() }

    fun isBlocked(host: String?): Boolean {
        if (!enabled || host.isNullOrBlank()) return false
        val key = host.lowercase().trimEnd('.')
        cache[key]?.let { return it }
        val result = matches(key)
        cache[key] = result
        return result
    }

    private fun matches(host: String): Boolean {
        var current = host
        while (true) {
            if (current in blockedHosts) return true
            val dot = current.indexOf('.')
            if (dot < 0) return false
            current = current.substring(dot + 1)
        }
    }

    fun clearCache() = cache.clear()

    fun emptyResponse() = WebResourceResponse(
        "text/plain", "utf-8", ByteArrayInputStream(ByteArray(0))
    )
}
