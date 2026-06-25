[app]
# (str) Title of your application
title = Todo

# (str) Package name
package.name = todo_app

# (str) Package domain (needed for android/ios packaging)
package.domain = com.kncept.todo

# (str) Application versioning (method 1)
version = 0.1.0

# (list) Application requirements
requirements = python3,python-dateutil,kivy>=2.2.1,kivy-garden>=0.1.5

# (list) Source file patterns to include
source.include_exts = py,kv,png,jpg,atlas
source.include_patterns = main.py,todo_mobile/**,README.md,LICENSE,pyproject.toml,setup.py,requirements-mobile.txt
source.exclude_patterns = .git/*,tests/*,.venv/*,.github/*

# (str) Supported orientation
orientation = portrait

# (str) Presplash image
presplash.filename =

# (str) Icon file
icon.filename =

# Android specific
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = armeabi-v7a
android.release_artifact = apk

# SDK/NDK paths set via CI environment
android.sdk_path = /home/runner/Android/Sdk
android.ndk_path = /home/runner/Android/Sdk/ndk/25.2.9519653

# Logging
android.logcat_filters = *:S python:D

# Use the SDL2 bootstrap
android.bootstrap = sdl2
