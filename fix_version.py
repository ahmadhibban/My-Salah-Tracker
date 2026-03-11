import os

p_file = 'build.gradle.kts'
if os.path.exists(p_file):
    with open(p_file, 'r') as f:
        lines = f.readlines()
    
    with open(p_file, 'w') as f:
        for line in lines:
            # মেইন ফাইলে kapt থাকার দরকার নেই, তাই মুছে দিচ্ছি
            if 'id("kotlin-kapt")' in line:
                continue
            
            # কোটলিন প্লাগিনে হারানো ভার্সন নাম্বার ফিরিয়ে দিচ্ছি
            if 'id("org.jetbrains.kotlin.android")' in line and 'version' not in line:
                line = line.replace('id("org.jetbrains.kotlin.android")', 'id("org.jetbrains.kotlin.android") version "1.8.22" apply false')
            
            f.write(line)
            
    print("✅ Version issue fixed successfully!")
else:
    print("❌ build.gradle.kts not found!")
