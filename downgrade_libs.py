import os, re

app_gradle = "app/build.gradle.kts"
if os.path.exists(app_gradle):
    with open(app_gradle, 'r', encoding='utf-8') as f:
        content = f.read()

    # লেটেস্ট ভার্সন কমিয়ে SDK 33 এর উপযোগী করা হচ্ছে
    content = re.sub(r'implementation\("androidx\.appcompat:appcompat:.*?"\)', 'implementation("androidx.appcompat:appcompat:1.5.1")', content)
    content = re.sub(r'implementation\("com\.google\.android\.material:material:.*?"\)', 'implementation("com.google.android.material:material:1.8.0")', content)

    with open(app_gradle, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✔ Library versions successfully matched with your SDK 33! 🚀")
else:
    print("❌ app/build.gradle.kts not found!")
