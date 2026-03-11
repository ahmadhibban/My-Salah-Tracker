import os
import re

print("🔍 Fixing Room Database for Kotlin...")

found = False
for root_dir, dirs, files in os.walk('.'):
    for f in files:
        if f in ['build.gradle', 'build.gradle.kts']:
            path = os.path.join(root_dir, f)
            with open(path, 'r') as file:
                data = file.read()
            
            changed = False
            is_kts = f.endswith('.kts')
            
            # শুধুমাত্র App লেভেলের ফাইলে কাজ করবে
            if 'com.android.application' in data:
                found = True
                # ১. KAPT প্লাগিন যুক্ত করা
                if 'kotlin-kapt' not in data:
                    if is_kts:
                        data = data.replace('id("org.jetbrains.kotlin.android")', 'id("org.jetbrains.kotlin.android")\n    id("kotlin-kapt")')
                    else:
                        data = data.replace("apply plugin: 'kotlin-android'", "apply plugin: 'kotlin-android'\napply plugin: 'kotlin-kapt'")
                    changed = True
                
                # ২. annotationProcessor কে kapt দিয়ে রিপ্লেস করা
                if 'annotationProcessor' in data:
                    data = re.sub(r'annotationProcessor', 'kapt', data)
                    changed = True
                
            if changed:
                with open(path, 'w') as file:
                    file.write(data)
                print(f"✅ Fixed Database KAPT issue in {f}!")
            elif found and not changed:
                print(f"⚡ {f} already has KAPT configured.")

if not found:
    print("❌ build.gradle files not found!")
else:
    print("\n🚀 Database Fix Complete! Please Sync and Build again.")
