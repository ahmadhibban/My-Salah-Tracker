import os
import re

# ১. Project build.gradle.kts ঠিক করা
p_file = 'build.gradle.kts'
if os.path.exists(p_file):
    with open(p_file, 'r') as f:
        txt = f.read()
    
    # আগের স্ক্রিপ্টের ভুলে সরে যাওয়া ভার্সন নাম্বার ঠিক করা
    broken_pattern = r'id\("com\.android\.application"\)\s*id\("kotlin-android"\)\s*version\s*"([^"]+)"\s*apply\s*false'
    fixed_pattern = r'id("com.android.application") version "\1" apply false\n    id("org.jetbrains.kotlin.android") version "1.8.22" apply false'
    txt = re.sub(broken_pattern, fixed_pattern, txt)
    
    # যদি অন্য কোনোভাবে ভার্সন মুছে গিয়ে থাকে, তবে ডিফল্ট 7.2.1 বসানো
    if 'id("com.android.application")' in txt and 'version' not in txt.split('id("com.android.application")')[1].split('\n')[0]:
        txt = txt.replace('id("com.android.application")', 'id("com.android.application") version "7.2.1" apply false')
        
    # কোটলিন প্লাগিন নিশ্চিত করা
    if 'org.jetbrains.kotlin.android' not in txt:
        txt = re.sub(r'plugins\s*\{', 'plugins {\n    id("org.jetbrains.kotlin.android") version "1.8.22" apply false', txt)
    
    with open(p_file, 'w') as f:
        f.write(txt)
    print("✅ Fixed Project build.gradle.kts")

# ২. App build.gradle.kts ঠিক করা
a_file = 'app/build.gradle.kts'
if os.path.exists(a_file):
    with open(a_file, 'r') as f:
        txt = f.read()
    
    txt = txt.replace('id("kotlin-android")', 'id("org.jetbrains.kotlin.android")')
    
    if 'org.jetbrains.kotlin.android' not in txt:
        txt = re.sub(r'plugins\s*\{', 'plugins {\n    id("org.jetbrains.kotlin.android")', txt)

    with open(a_file, 'w') as f:
        f.write(txt)
    print("✅ Fixed App build.gradle.kts")

print("🚀 Auto-Repair Complete! Please Build again.")
