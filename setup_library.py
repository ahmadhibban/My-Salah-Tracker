import os, re

app_gradle = None
settings_gradle = None
root_gradle = None

# প্রোজেক্টের গ্রেডল ফাইলগুলো খুঁজে বের করা
for root, dirs, files in os.walk("."):
    if "build.gradle" in files:
        if "app" in root.split(os.sep):
            app_gradle = os.path.join(root, "build.gradle")
        elif root == ".":
            root_gradle = os.path.join(root, "build.gradle")
    if "settings.gradle" in files and root == ".":
        settings_gradle = os.path.join(root, "settings.gradle")

# ১. App build.gradle এ লাইব্রেরি যুক্ত করা
if app_gradle:
    with open(app_gradle, 'r', encoding='utf-8') as f:
        app_content = f.read()
    if "com.github.fornewid:neumorphism" not in app_content:
        # dependencies ব্লকের ভেতর লাইব্রেরি ইনজেক্ট করা
        app_content = re.sub(r'dependencies\s*\{', "dependencies {\n    implementation 'com.github.fornewid:neumorphism:0.3.2'", app_content, count=1)
        with open(app_gradle, 'w', encoding='utf-8') as f:
            f.write(app_content)
        print(f"✔ Neumorphism Library added to {app_gradle}")
    else:
        print("✔ Neumorphism Library is already present.")

# ২. Jitpack রিপোজিটরি যুক্ত করা
def add_jitpack(path):
    if path and os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "jitpack.io" not in content and "repositories {" in content:
            content = re.sub(r'repositories\s*\{', "repositories {\n        maven { url 'https://jitpack.io' }", content)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    return False

if not add_jitpack(settings_gradle):
    add_jitpack(root_gradle)
print("✔ Jitpack Repository setup complete!")
