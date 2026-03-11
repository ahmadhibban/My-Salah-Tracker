import os

print("🔍 Searching for build.gradle files...")

for root_dir, dirs, files in os.walk('.'):
    if 'build.gradle' in files:
        file_path = os.path.join(root_dir, 'build.gradle')
        with open(file_path, 'r') as f:
            content = f.read()

        modified = False

        # ১. App লেভেলের build.gradle ফিক্স
        if "com.android.application" in content:
            print(f"⚙️ Found App build.gradle at: {file_path}")
            if "kotlin-android" not in content:
                content = content.replace("apply plugin: 'com.android.application'", "apply plugin: 'com.android.application'\napply plugin: 'kotlin-android'", 1)
                modified = True
            if "kotlin-stdlib" not in content:
                content = content.replace("dependencies {", "dependencies {\n    implementation 'org.jetbrains.kotlin:kotlin-stdlib:1.8.22'", 1)
                modified = True

        # ২. Project লেভেলের build.gradle ফিক্স
        elif "buildscript" in content:
            print(f"⚙️ Found Project build.gradle at: {file_path}")
            if "ext.kotlin_version" not in content:
                content = content.replace("buildscript {", "buildscript {\n    ext.kotlin_version = '1.8.22'", 1)
                modified = True
            if "kotlin-gradle-plugin" not in content:
                content = content.replace("dependencies {", "dependencies {\n        classpath \"org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version\"", 1)
                modified = True

        if modified:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Updated {file_path}")
        else:
            print(f"⚡ {file_path} is already up-to date.")

print("\n🔍 Fixing SalahWidget.java...")
for root_dir, dirs, files in os.walk('.'):
    if 'SalahWidget.java' in files:
        old_path = os.path.join(root_dir, 'SalahWidget.java')
        new_path = os.path.join(root_dir, 'SalahWidget.kt')
        os.rename(old_path, new_path)
        print(f"✅ Renamed successfully: {old_path} -> {new_path}")

print("\n🚀 All tasks complete! Now sync and build the project.")
