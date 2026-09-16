[app]
title = Quotex Smart Bot
package.name = quotexbot
package.domain = org.quotex

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = kivy

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
