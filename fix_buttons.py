import os, re
java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ActionRow এর ভেতরে মার্জিন ফিক্স করা হচ্ছে যাতে কার্ডের সমান হয়
mc = re.sub(r'markLp\.setMargins\([^;]+;', 'markLp.setMargins(0, (int)(24*DENSITY), (int)(8*DENSITY), (int)(16*DENSITY));', mc)
mc = re.sub(r'todayLp\.setMargins\([^;]+;', 'todayLp.setMargins((int)(8*DENSITY), (int)(24*DENSITY), 0, (int)(16*DENSITY));', mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)
print("✅ ৩. Action Buttons Gap Fixed!")
