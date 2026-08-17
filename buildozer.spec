[app]
title = BIST Tarayici
package.name = bistapp
package.domain = org.bist

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy,requests,urllib3,certifi,idna,chardet

orientation = portrait
osx.kivy_version = 2.2.1

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
p4a.branch = master
