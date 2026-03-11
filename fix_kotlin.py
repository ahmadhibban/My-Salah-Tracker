import os

# ১. Project build.gradle ফিক্স করা
proj_gradle = "build.gradle"
if os.path.exists(proj_gradle):
    with open(proj_gradle, "r") as f:
        p_data = f.read()
    
    # কোটলিন প্লাগিন যুক্ত করা
    if "kotlin-gradle-plugin" not in p_data:
        p_data = p_data.replace("dependencies {", "dependencies {\n        classpath 'org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.22'", 1)
        with open(proj_gradle, "w") as f:
            f.write(p_data)
        print("✅ Project build.gradle updated!")
else:
    print("❌ build.gradle not found in root!")

# ২. App build.gradle ফিক্স করা
app_gradle = "app/build.gradle"
if os.path.exists(app_gradle):
    with open(app_gradle, "r") as f:
        a_data = f.read()
    
    if "kotlin-android" not in a_data and "org.jetbrains.kotlin.android" not in a_data:
        if "apply plugin: 'com.android.application'" in a_data:
            a_data = a_data.replace("apply plugin: 'com.android.application'", "apply plugin: 'com.android.application'\napply plugin: 'kotlin-android'")
        
        a_data = a_data.replace("dependencies {", "dependencies {\n    implementation 'org.jetbrains.kotlin:kotlin-stdlib:1.8.22'", 1)
        with open(app_gradle, "w") as f:
            f.write(a_data)
        print("✅ App build.gradle updated!")

# ৩. ডুপ্লিকেট Java ফাইল রিমুভ করা
java_dir = "app/src/main/java/com/my/salah/tracker/app/"
if os.path.exists(java_dir):
    for file_name in os.listdir(java_dir):
        if file_name.endswith(".java"):
            base_name = file_name[:-5]
            kt_path = os.path.join(java_dir, base_name + ".kt")
            java_path = os.path.join(java_dir, file_name)
            
            # যদি একই নামের .kt ফাইল থাকে, তবে পুরোনো .java ডিলিট করবে
            if os.path.exists(kt_path):
                os.remove(java_path)
                print(f"🗑️ Removed duplicate java file: {file_name}")

print("🚀 All fixes applied successfully! Now sync and build the project.")
