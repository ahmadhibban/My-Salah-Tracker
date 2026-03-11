import os

print("🔍 Hunting for build.gradle files...")

found_any = False

for root_dir, dirs, files in os.walk('.'):
    if 'build.gradle' in files:
        found_any = True
        file_path = os.path.join(root_dir, 'build.gradle')
        with open(file_path, 'r') as f:
            data = f.read()
        
        changed = False

        # ১. App Level Gradle (যেখানে application লেখা থাকে)
        if 'com.android.application' in data:
            if 'kotlin-android' not in data:
                data = data.replace("apply plugin: 'com.android.application'", "apply plugin: 'com.android.application'\napply plugin: 'kotlin-android'")
                if "plugins {" in data and "apply plugin" not in data:
                    data = data.replace("plugins {", "plugins {\n    id 'kotlin-android'")
                changed = True
            
            if 'kotlin-stdlib' not in data:
                data = data.replace("dependencies {", "dependencies {\n    implementation \"org.jetbrains.kotlin:kotlin-stdlib:1.8.22\"")
                changed = True
                
            if changed:
                print(f"✅ App Gradle patched -> {file_path}")

        # ২. Project Level Gradle (যেখানে buildscript লেখা থাকে)
        elif 'buildscript' in data:
            if 'ext.kotlin_version' not in data:
                data = data.replace("buildscript {", "buildscript {\n    ext.kotlin_version = '1.8.22'")
                changed = True
                
            if 'kotlin-gradle-plugin' not in data:
                data = data.replace("dependencies {", "dependencies {\n        classpath \"org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version\"")
                changed = True
                
            if changed:
                print(f"✅ Project Gradle patched -> {file_path}")

        if changed:
            with open(file_path, 'w') as f:
                f.write(data)

if not found_any:
    print("❌ No build.gradle files found anywhere! Check if you are in the right folder.")
else:
    print("🎉 Done! Kotlin is now armed and ready.")
