import os

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ফালতু 'gTex;' অংশটুকু মুছে ফেলা হচ্ছে
    mc = mc.replace("gText.setTypeface(Typeface.DEFAULT_BOLD); gTex;", "gText.setTypeface(Typeface.DEFAULT_BOLD);")

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)

    print("✔ TINY TYPO FIXED PERFECTLY! READY TO BUILD.")
else:
    print("❌ MainActivity.java not found!")
