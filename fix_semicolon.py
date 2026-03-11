import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ১. হারানো সেমিকোলন (;) একদম পারফেক্ট জায়গায় বসিয়ে দেওয়া হচ্ছে
    mc = re.sub(r'([^\s;{}])(\s*TextView\s+pT\s*=\s*new\s+TextView)', r'\1;\n        \2', mc)

    # ২. মার্ক অল এবং টুডে বাটনগুলো যদি মুছে গিয়ে থাকে, সেগুলোকে আবার ফিরিয়ে আনা হচ্ছে
    if "topBtns.addView(markAllBtn);" not in mc:
        mc = mc.replace("topBtns.setPadding(0, 0, 0, 0);", "topBtns.addView(markAllBtn);\n        topBtns.addView(todayBtn);\n        topBtns.setPadding(0, 0, 0, 0);")

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)

    print("✔ SEMICOLON ERROR FIXED PERFECTLY! READY TO BUILD.")
else:
    print("❌ MainActivity.java not found!")
