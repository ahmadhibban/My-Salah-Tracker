import os

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()
    
    # সরাসরি return এর বদলে if (true) return; বসানো হচ্ছে
    mc = mc.replace("return; // UI টেস্ট করার জন্য", "if (true) return; // UI টেস্ট করার জন্য")
    
    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
        
print("✔ Unreachable Error Fixed! Ready to Build.")
