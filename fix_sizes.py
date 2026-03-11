import os, re
java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. তীরচিহ্নগুলোকে সপ্তাহের ঘরের সমান (44dp) করা
mc = re.sub(r'prevW\.setLayoutParams\([^;]+;', 'prevW.setLayoutParams(new LinearLayout.LayoutParams((int)(44*DENSITY), (int)(44*DENSITY)));', mc)
mc = re.sub(r'nextW\.setLayoutParams\([^;]+;', 'nextW.setLayoutParams(new LinearLayout.LayoutParams((int)(44*DENSITY), (int)(44*DENSITY)));', mc)

# ২. নিচের বাটন দুটোকে মেইন কার্ডের মাপে (পাশে 16dp) মেলানো
mc = re.sub(r'markLp\.setMargins\([^;]+;', 'markLp.setMargins((int)(16*DENSITY), (int)(24*DENSITY), (int)(6*DENSITY), 0);', mc)
mc = re.sub(r'todayLp\.setMargins\([^;]+;', 'todayLp.setMargins((int)(6*DENSITY), (int)(24*DENSITY), (int)(16*DENSITY), 0);', mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)
print("✅ ১. Arrows & Buttons Size Perfectly Matched!")
