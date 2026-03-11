import re
with open("app/src/main/java/com/my/salah/tracker/app/MainActivity.java", "r", encoding="utf-8") as f: mc = f.read()

mc = re.sub(r'markLp\.setMargins\([^)]+\);', 'markLp.setMargins((int)(16*DENSITY), (int)(16*DENSITY), (int)(8*DENSITY), (int)(16*DENSITY));', mc)
mc = re.sub(r'todayLp\.setMargins\([^)]+\);', 'todayLp.setMargins((int)(8*DENSITY), (int)(16*DENSITY), (int)(16*DENSITY), (int)(16*DENSITY));', mc)

with open("app/src/main/java/com/my/salah/tracker/app/MainActivity.java", "w", encoding="utf-8") as f: f.write(mc)
print("✅ ১. বাটন গ্যাপ ফিক্সড!")
