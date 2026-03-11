import os, re

app_g = None
settings_g = None
root_g = None

for r, d, f in os.walk("."):
    if "build.gradle" in f:
        if "app" in r.split(os.sep): app_g = os.path.join(r, "build.gradle")
        else: root_g = os.path.join(r, "build.gradle")
    if "settings.gradle" in f:
        settings_g = os.path.join(r, "settings.gradle")

# অ্যাপ গ্রেডল ফিক্স
if app_g:
    with open(app_g, 'r', encoding='utf-8') as f: c = f.read()
    # আগের ভুল ডিপেন্ডেন্সি মুছে ফেলা
    c = re.sub(r'\n+dependencies\s*\{\s*implementation\s*\'com\.github\.fornewid:neumorphism[^\}]+\}\s*', '\n', c)
    # মূল ব্লকে সঠিক ভার্সন বসানো
    if "com.github.fornewid:neumorphism" not in c:
        c = re.sub(r'dependencies\s*\{', "dependencies {\n    implementation 'com.github.fornewid:neumorphism:0.3.0'", c, count=1)
    with open(app_g, 'w', encoding='utf-8') as f: f.write(c)

# সেটিংস গ্রেডল ফিক্স
if settings_g:
    with open(settings_g, 'r', encoding='utf-8') as f: c = f.read()
    if "jitpack.io" not in c:
        c = re.sub(r'repositories\s*\{', "repositories {\n        maven { url 'https://jitpack.io' }", c)
    with open(settings_g, 'w', encoding='utf-8') as f: f.write(c)

# রুট গ্রেডল ফিক্স
if root_g:
    with open(root_g, 'r', encoding='utf-8') as f: c = f.read()
    if "jitpack.io" not in c:
        c = re.sub(r'repositories\s*\{', "repositories {\n        maven { url 'https://jitpack.io' }", c)
    with open(root_g, 'w', encoding='utf-8') as f: f.write(c)

print("✔ GRADLE FIXED PERFECTLY! Ready for Clean and Build.")
