import os
import re

wrapper_file = "gradle/wrapper/gradle-wrapper.properties"
root_gradle = "build.gradle"
app_gradle = "app/build.gradle"

print("🚀 ফাইনাল আপগ্রেড শুরু হচ্ছে...")

# ১. Gradle Wrapper আপডেট করা
if os.path.exists(wrapper_file):
    with open(wrapper_file, "r") as f: content = f.read()
    content = re.sub(r'gradle-[0-9\.]+(-\w+)?-(bin|all)\.zip', 'gradle-8.7-bin.zip', content)
    with open(wrapper_file, "w") as f: f.write(content)
    print("✅ Gradle Wrapper 8.7-এ আপডেট হয়েছে!")

# ২. Android Gradle Plugin (AGP) আপডেট করা
if os.path.exists(root_gradle):
    with open(root_gradle, "r") as f: content = f.read()
    content = re.sub(r'com\.android\.tools\.build:gradle:[0-9\.]+', 'com.android.tools.build:gradle:8.3.0', content)
    content = re.sub(r'id\s*\(?[\'"]com\.android\.application[\'"]\)?\s*version\s*[\'"][0-9\.]+[\'"]', 'id "com.android.application" version "8.3.0"', content)
    content = re.sub(r'id\s*\(?[\'"]com\.android\.library[\'"]\)?\s*version\s*[\'"][0-9\.]+[\'"]', 'id "com.android.library" version "8.3.0"', content)
    with open(root_gradle, "w") as f: f.write(content)
    print("✅ Android Gradle Plugin 8.3.0-এ আপডেট হয়েছে!")

# ৩. Java 17 Compatibility নিশ্চিত করা
if os.path.exists(app_gradle):
    with open(app_gradle, "r") as f: content = f.read()
    content = re.sub(r'JavaVersion\.VERSION_1_8', 'JavaVersion.VERSION_17', content)
    content = re.sub(r'jvmTarget\s*=\s*[\'"]1\.8[\'"]', 'jvmTarget = "17"', content)
    with open(app_gradle, "w") as f: f.write(content)
    print("✅ Java Compatibility 17-এ সেট করা হয়েছে!")

print("🎉 ফাইনাল আপগ্রেড স্ক্রিপ্ট সম্পন্ন হয়েছে!")
