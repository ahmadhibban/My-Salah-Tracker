import os

app_g = None
root_g = "build.gradle"
set_g = "settings.gradle"

# অ্যাপ গ্রেডল ফাইল খোঁজা
for r, d, f in os.walk("."):
    if "build.gradle" in f and "app" in r:
        app_g = os.path.join(r, "build.gradle")
        break

# ১. অ্যাপের build.gradle এর একদম শেষে ডিপেন্ডেন্সি ফোর্স করে বসানো
if app_g and os.path.exists(app_g):
    with open(app_g, "r", encoding='utf-8') as f: content = f.read()
    if "com.github.fornewid:neumorphism" not in content:
        with open(app_g, "a", encoding='utf-8') as f:
            f.write("\n\ndependencies {\n    implementation 'com.github.fornewid:neumorphism:0.3.2'\n}\n")
        print("✔ Neumorphism Library forced into App Gradle!")
    else:
        print("✔ Neumorphism is already in App Gradle.")

# ২. settings.gradle এ Jitpack যোগ করা
if os.path.exists(set_g):
    with open(set_g, "r", encoding='utf-8') as f: content = f.read()
    if "jitpack.io" not in content:
        content = content.replace("repositories {", "repositories {\n        maven { url 'https://jitpack.io' }")
        with open(set_g, "w", encoding='utf-8') as f: f.write(content)
        print("✔ Jitpack repository forced into settings.gradle!")

# ৩. root build.gradle এ Jitpack যোগ করা
if os.path.exists(root_g):
    with open(root_g, "r", encoding='utf-8') as f: content = f.read()
    if "jitpack.io" not in content:
        content = content.replace("repositories {", "repositories {\n        maven { url 'https://jitpack.io' }")
        with open(root_g, "w", encoding='utf-8') as f: f.write(content)
        print("✔ Jitpack repository forced into Root Gradle!")

print("✔ All Gradle Files are Perfectly Synced via Script!")
