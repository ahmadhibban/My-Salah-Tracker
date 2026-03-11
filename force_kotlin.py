import os
import re

print("🚀 Forcing Kotlin Configuration...")

# 1. Project build.gradle
if os.path.exists('build.gradle'):
    with open('build.gradle', 'r') as f: data = f.read()
    if 'kotlin-gradle-plugin' not in data:
        data = re.sub(r'buildscript\s*\{', "buildscript {\n    ext.kotlin_version = '1.8.22'", data, count=1)
        data = re.sub(r'dependencies\s*\{', "dependencies {\n        classpath \"org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version\"", data, count=1)
        with open('build.gradle', 'w') as f: f.write(data)
        print("✅ Project build.gradle patched!")
    else:
        print("⚡ Project build.gradle already OK.")
else:
    print("❌ build.gradle not found!")

# 2. App build.gradle
if os.path.exists('app/build.gradle'):
    with open('app/build.gradle', 'r') as f: data = f.read()
    if 'kotlin-android' not in data:
        if "apply plugin: 'com.android.application'" in data:
            data = data.replace("apply plugin: 'com.android.application'", "apply plugin: 'com.android.application'\napply plugin: 'kotlin-android'")
        elif "plugins {" in data:
            data = re.sub(r'plugins\s*\{', "plugins {\n    id 'kotlin-android'", data, count=1)
        
        data = re.sub(r'dependencies\s*\{', "dependencies {\n    implementation \"org.jetbrains.kotlin:kotlin-stdlib:1.8.22\"", data, count=1)
        with open('app/build.gradle', 'w') as f: f.write(data)
        print("✅ App build.gradle patched!")
    else:
        print("⚡ App build.gradle already OK.")
else:
    print("❌ app/build.gradle not found!")

print("🎉 Done! Please Build the project again.")
