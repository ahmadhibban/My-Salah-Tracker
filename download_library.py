import os, re, urllib.request

# ১. প্রজেক্টে libs ফোল্ডার তৈরি করা
libs_dir = "app/libs"
os.makedirs(libs_dir, exist_ok=True)
aar_path = os.path.join(libs_dir, "neumorphism.aar")

# ২. সরাসরি লাইব্রেরি ফাইল (.aar) ডাউনলোড করা
url = "https://jitpack.io/com/github/fornewid/neumorphism/0.3.0/neumorphism-0.3.0.aar"
print("⏳ Downloading Neumorphism library directly... Please wait.")
try:
    urllib.request.urlretrieve(url, aar_path)
    print("✔ Library successfully downloaded and saved to app/libs/!")
except Exception as e:
    print(f"❌ Download failed: {e}")
    exit()

# ৩. অ্যাপের build.gradle ফাইল আপডেট করা (যাতে সে লোকাল ফাইলটা ব্যবহার করে)
app_gradle = "app/build.gradle"
if os.path.exists(app_gradle):
    with open(app_gradle, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ইন্টারনেটের ডিপেন্ডেন্সি মুছে ফেলা
    content = re.sub(r"implementation\s+['\"]com.github.fornewid:neumorphism.*?['\"]", "", content)
    
    # লোকাল ফাইল ডিপেন্ডেন্সি যুক্ত করা
    if "implementation files('libs/neumorphism.aar')" not in content:
        content = content.replace("dependencies {", "dependencies {\n    implementation files('libs/neumorphism.aar')")
    
    with open(app_gradle, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✔ App Gradle updated to use the downloaded library!")

print("🚀 DONE! Now build the app.")
