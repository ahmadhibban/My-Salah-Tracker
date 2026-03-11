import os
import re

file_path = 'app/build.gradle.kts' if os.path.exists('app/build.gradle.kts') else 'app/build.gradle'

if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    
    # পুরোনো কোনো অপশন থাকলে সেটা মুছে দেওয়া যেন ডুপ্লিকেট না হয়
    data = re.sub(r'compileOptions\s*\{[^}]*\}', '', data)
    data = re.sub(r'kotlinOptions\s*\{[^}]*\}', '', data)
    
    is_kts = file_path.endswith('.kts')
    
    injection = """
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
""" if is_kts else """
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
"""
    
    # android { } ব্লকের ভেতর নতুন সেটিং বসানো
    data = re.sub(r'android\s*\{', 'android {' + injection, data, count=1)
    
    with open(file_path, 'w') as f:
        f.write(data)
        
    print(f"✅ Fixed JVM Target mismatch in {file_path}!")
else:
    print("❌ build.gradle not found!")
