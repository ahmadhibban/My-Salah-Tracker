import os

gradle_file = "build.gradle"
if os.path.exists(gradle_file):
    with open(gradle_file, "r") as f:
        content = f.read()

    # কোটলিন ভার্সন যুক্ত করা
    if "ext.kotlin_version" not in content:
        content = content.replace("buildscript {", "buildscript {\n    ext.kotlin_version = '1.8.22'", 1)
    
    # ক্লাসপাথ যুক্ত করা
    if "kotlin-gradle-plugin" not in content:
        content = content.replace("dependencies {", "dependencies {\n        classpath \"org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version\"", 1)

    with open(gradle_file, "w") as f:
        f.write(content)
    print("✅ Project build.gradle updated successfully!")
else:
    print("❌ build.gradle not found!")
