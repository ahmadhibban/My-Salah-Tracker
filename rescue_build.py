import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ওই শয়তান আইকন কালার কোডটা খুঁজে বের করে সমূলে বিনাশ করা হচ্ছে 😈
    bad_code = r'try\s*\{\s*if\s*\(\s*themeToggleBtn\s*instanceof\s*android\.widget\.TextView\s*\)[\s\S]*?catch\s*\(\s*Exception\s*e\s*\)\s*\{\s*\}'
    
    mc_new = re.sub(bad_code, '', mc)
    
    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc_new)
        
    print("✔ BAD CODE REMOVED! THE DEVIL IS GONE. READY TO BUILD.")
else:
    print("❌ FILE NOT FOUND")
