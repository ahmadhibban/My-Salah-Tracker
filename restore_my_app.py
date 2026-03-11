import os

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()
    
    # টেস্টের জন্য দেওয়া লাইনগুলো মুছে ফেলা হচ্ছে
    mc = mc.replace("setContentView(R.layout.activity_main);", "")
    mc = mc.replace("if (true) return; // UI টেস্ট করার জন্য পুরনো জাভা কোডগুলো আপাতত অফ রাখা হলো", "")
    mc = mc.replace("if (true) return; // UI টেস্ট করার জন্য", "")
    
    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
        
print("✔ Test Screen Removed! Your Original App is Back.")
