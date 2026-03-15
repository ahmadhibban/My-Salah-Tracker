import os
import re

manifest = "app/src/main/AndroidManifest.xml"
main_activity = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

print("🚀 প্রজেক্ট ফিক্স এবং আপগ্রেড শুরু হচ্ছে...")

# ১. AndroidManifest.xml থেকে অপ্রয়োজনীয় স্টোরেজ পারমিশন রিমুভ (API 33+ Issue Fix)
if os.path.exists(manifest):
    with open(manifest, "r") as f: content = f.read()
    content = re.sub(r'<uses-permission android:name="android\.permission\.(READ|WRITE)_EXTERNAL_STORAGE" />\n?', '', content)
    with open(manifest, "w") as f: f.write(content)
    print("✅ Storage Permissions কনফ্লিক্ট ফিক্স করা হয়েছে!")

# ২. MainActivity.java এর বাগ ফিক্স করা
if os.path.exists(main_activity):
    with open(main_activity, "r") as f: content = f.read()
    
    # Handler Looper Bug Fix
    content = re.sub(r'new Handler\(\)\.postDelayed', 'new Handler(android.os.Looper.getMainLooper()).postDelayed', content)
    
    # Transition Conflict Fix (API 34 Support)
    transition_code = """
        if (android.os.Build.VERSION.SDK_INT >= 34) {
            overrideActivityTransition(OVERRIDE_TRANSITION_OPEN, 0, 0);
        } else {
            overridePendingTransition(0, 0);
        }
    """
    content = re.sub(r'overridePendingTransition\(0,\s*0\);', transition_code.strip(), content)
    
    # Kaza Namaz Visibility Fix (Make sure it's set to true or visible)
    content = re.sub(r'prefs\.getBoolean\("show_kaza",\s*false\)', 'prefs.getBoolean("show_kaza", true)', content)
    
    with open(main_activity, "w") as f: f.write(content)
    print("✅ Handler, Transition এবং Kaza Namaz এর সমস্যাগুলো ফিক্স করা হয়েছে!")

print("🎉 প্রথম ধাপের আপগ্রেড সফলভাবে সম্পন্ন হয়েছে!")
