import os, re

def bypass_package():
    # 1. build.gradle এর প্যাকেজ নেম আপডেট করা
    path_g = "app/build.gradle"
    if os.path.exists(path_g):
        with open(path_g, 'r', encoding='utf-8') as f:
            content = f.read()
        # প্যাকেজ নেমের শেষে '.pro' যুক্ত করে দেওয়া হচ্ছে
        new_content = re.sub(r'(applicationId\s+["\'])([^"\']+)(["\'])', r'\1\2.pro\3', content)
        with open(path_g, 'w', encoding='utf-8') as f:
            f.write(new_content)

    # 2. AndroidManifest.xml এর প্রোভাইডার আপডেট করা (যদি থাকে)
    path_m = "app/src/main/AndroidManifest.xml"
    if os.path.exists(path_m):
        with open(path_m, 'r', encoding='utf-8') as f:
            content = f.read()
        # FileProvider কনফ্লিক্ট দূর করতে '.pro' যুক্ত করা হচ্ছে
        new_content = re.sub(r'android:authorities=["\']([^"\'$]+)\.provider["\']', r'android:authorities="\1.pro.provider"', content)
        with open(path_m, 'w', encoding='utf-8') as f:
            f.write(new_content)

bypass_package()
print("Install Bypass Ready! Application ID changed to .pro successfully.")
