import os

app_gradle = "app/build.gradle"
if os.path.exists(app_gradle):
    with open(app_gradle, "r") as f:
        content = f.read()

    # কোটলিন প্লাগিন যুক্ত করা
    if "apply plugin: 'kotlin-android'" not in content:
        content = content.replace("apply plugin: 'com.android.application'", "apply plugin: 'com.android.application'\napply plugin: 'kotlin-android'", 1)

    # কোটলিন লাইব্রেরি যুক্ত করা
    if "kotlin-stdlib" not in content:
        content = content.replace("dependencies {", "dependencies {\n    implementation \"org.jetbrains.kotlin:kotlin-stdlib:1.8.22\"", 1)

    with open(app_gradle, "w") as f:
        f.write(content)
    print("✅ App build.gradle updated successfully!")
else:
    print("❌ app/build.gradle not found!")
