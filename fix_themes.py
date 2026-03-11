import os

app_gradle = "app/build.gradle.kts"
if os.path.exists(app_gradle):
    with open(app_gradle, 'r', encoding='utf-8') as f:
        content = f.read()

    deps_to_add = []
    if "androidx.appcompat:appcompat" not in content:
        deps_to_add.append('    implementation("androidx.appcompat:appcompat:1.6.1")')
    if "com.google.android.material:material" not in content:
        deps_to_add.append('    implementation("com.google.android.material:material:1.10.0")')

    if deps_to_add:
        addition = "\n" + "\n".join(deps_to_add) + "\n"
        content = content.replace("dependencies {", "dependencies {" + addition)
        with open(app_gradle, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✔ Material Design and AppCompat libraries successfully added! 🚀")
    else:
        print("✔ Libraries already exist. If error persists, clean the project.")
else:
    print("❌ app/build.gradle.kts not found!")
