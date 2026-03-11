import os
import re

print("🔍 Scanning AndroidIDE Project for Gradle files...")

found = False
for root_dir, dirs, files in os.walk('.'):
    for f in files:
        if 'gradle' in f.lower() and os.path.isfile(os.path.join(root_dir, f)):
            path = os.path.join(root_dir, f)
            try:
                with open(path, 'r') as file:
                    data = file.read()
            except:
                continue
            
            changed = False
            is_kts = f.endswith('.kts')
            
            # ১. App লেভেলের Gradle ফিক্স
            if 'com.android.application' in data:
                found = True
                print(f"⚙️ Found App Gradle: {path}")
                if 'kotlin-android' not in data and 'kotlin.android' not in data:
                    if is_kts:
                        data = re.sub(r'id\s*\(\s*"com\.android\.application"\s*\)', 'id("com.android.application")\n    id("kotlin-android")', data)
                    else:
                        if 'apply plugin' in data:
                            data = re.sub(r"apply plugin:\s*'com\.android\.application'", "apply plugin: 'com.android.application'\napply plugin: 'kotlin-android'", data)
                        elif 'plugins {' in data:
                            data = re.sub(r"id\s*'com\.android\.application'", "id 'com.android.application'\n    id 'kotlin-android'", data)
                    changed = True
                    
                if 'kotlin-stdlib' not in data:
                    if is_kts:
                        data = re.sub(r'dependencies\s*\{', 'dependencies {\n    implementation("org.jetbrains.kotlin:kotlin-stdlib:1.8.22")', data)
                    else:
                        data = re.sub(r'dependencies\s*\{', "dependencies {\n    implementation 'org.jetbrains.kotlin:kotlin-stdlib:1.8.22'", data)
                    changed = True

            # ২. Project লেভেলের Gradle ফিক্স
            elif ('buildscript' in data or 'apply false' in data) and 'dependencies' in data:
                found = True
                print(f"⚙️ Found Project Gradle: {path}")
                if 'kotlin-gradle-plugin' not in data and 'org.jetbrains.kotlin.android' not in data:
                    if is_kts:
                        if 'plugins {' in data:
                            data = re.sub(r'plugins\s*\{', 'plugins {\n    id("org.jetbrains.kotlin.android") version "1.8.22" apply false', data)
                            changed = True
                    else:
                        if 'buildscript {' in data:
                            data = re.sub(r'buildscript\s*\{', "buildscript {\n    ext.kotlin_version = '1.8.22'", data)
                            data = re.sub(r'dependencies\s*\{', "dependencies {\n        classpath \"org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version\"", data, count=1)
                            changed = True
                        elif 'plugins {' in data:
                            data = re.sub(r'plugins\s*\{', "plugins {\n    id 'org.jetbrains.kotlin.android' version '1.8.22' apply false", data)
                            changed = True

            if changed:
                with open(path, 'w') as file:
                    file.write(data)
                print(f"✅ Successfully patched {f}!")
            elif 'com.android.application' in data or 'buildscript' in data or 'apply false' in data:
                print(f"⚡ {f} is already configured for Kotlin.")

if not found:
    print("❌ Still couldn't find any gradle files. Please manually check your folder structure.")
else:
    print("\n🎉 All done! Now sync and build the project.")
