import os

app_g = "app/build.gradle"
if os.path.exists(app_g):
    with open(app_g, 'r', encoding='utf-8') as f:
        content = f.read()
    if "com.github.fornewid:neumorphism" not in content:
        with open(app_g, 'a', encoding='utf-8') as f:
            f.write("\ndependencies {\n    implementation 'com.github.fornewid:neumorphism:0.3.0'\n}\n")
        print("✔ Neumorphism added to App Gradle!")
    else:
        print("✔ Neumorphism already exists in App Gradle.")

root_g = "build.gradle"
if os.path.exists(root_g):
    with open(root_g, 'r', encoding='utf-8') as f:
        content = f.read()
    if "jitpack.io" not in content:
        with open(root_g, 'a', encoding='utf-8') as f:
            f.write("\nallprojects { repositories { maven { url 'https://jitpack.io' } } }\n")
        print("✔ Jitpack added to Root Gradle!")
    else:
        print("✔ Jitpack already exists in Root Gradle.")
