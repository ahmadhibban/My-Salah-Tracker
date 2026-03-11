import os

app_gradle = "app/build.gradle.kts"
if os.path.exists(app_gradle):
    with open(app_gradle, 'r', encoding='utf-8') as f:
        content = f.read()

    # মুছে যাওয়া Chart Library আবার যোগ করা হচ্ছে
    if "MPAndroidChart" not in content:
        addition = '\n    implementation("com.github.PhilJay:MPAndroidChart:v3.1.0")\n'
        content = content.replace("dependencies {", "dependencies {" + addition)
        
        with open(app_gradle, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✔ Chart Library Successfully Restored! 🚀")
    else:
        print("✔ Chart Library already exists. Try cleaning the project.")
else:
    print("❌ app/build.gradle.kts not found!")
