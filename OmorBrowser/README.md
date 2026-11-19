# Omor Browser

Android WebView browser starter project:
- URL/search input
- Back, forward, reload
- Navigation progress
- Basic host-based blocking
- Download confirmation and executable-extension blocking
- HTTPS-only network policy

## Build
Open this folder in Android Studio and build an APK, or run:
`gradle assembleDebug`.

Output: `app/build/outputs/apk/debug/app-debug.apk`.

GitHub Actions builds the debug APK when this branch is pushed. Download the artifact named `OmorBrowser-debug-apk`.

## Limitations
This is not a full browser yet. It does not include tabs, history/bookmarks database, incognito, settings UI, analytics, backend, or Telegram bot. The block list is a small sample.
