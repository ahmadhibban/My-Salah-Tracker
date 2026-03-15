import os
import re

build_gradle = "app/build.gradle"
manifest = "app/src/main/AndroidManifest.xml"
package_name = "com.my.salah.tracker.app"

print("🔄 আপগ্রেড শুরু হচ্ছে...")

# ১. build.gradle আপডেট করা (Android 34-এ আপগ্রেড)
if os.path.exists(build_gradle):
    with open(build_gradle, "r") as f:
        content = f.read()
    
    # SDK 33 থেকে 34 করা
    content = re.sub(r'compileSdk(Version)?\s+\d+', 'compileSdk 34', content)
    content = re.sub(r'targetSdk(Version)?\s+\d+', 'targetSdk 34', content)
    
    # Namespace যুক্ত করা (যদি না থাকে)
    if "namespace" not in content:
        content = re.sub(r'(android\s*\{)', r'\1\n    namespace "' + package_name + '"', content, count=1)
        
    with open(build_gradle, "w") as f:
        f.write(content)
    print("✅ build.gradle সফলভাবে Android 34-এ আপগ্রেড হয়েছে!")

# ২. AndroidManifest.xml ফিক্স করা (Warning সমাধান)
if os.path.exists(manifest):
    with open(manifest, "r") as f:
        content = f.read()
        
    # পুরানো package অ্যাট্রিবিউট মুছে ফেলা
    content = re.sub(r'\s*package="[^"]+"', '', content)
    
    with open(manifest, "w") as f:
        f.write(content)
    print("✅ AndroidManifest.xml-এর Warning সমাধান করা হয়েছে!")

print("🎉 আপগ্রেড সফলভাবে সম্পন্ন হয়েছে!")
