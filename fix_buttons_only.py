import re
path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f: mc = f.read()

# বাটন দুটোর মার্জিন একদম পারফেক্ট করা হচ্ছে
mc = re.sub(r'markLp\.setMargins\([^;]+;', 'markLp.setMargins((int)(16*DENSITY), (int)(16*DENSITY), (int)(8*DENSITY), (int)(16*DENSITY));', mc)
mc = re.sub(r'todayLp\.setMargins\([^;]+;', 'todayLp.setMargins((int)(8*DENSITY), (int)(16*DENSITY), (int)(16*DENSITY), (int)(16*DENSITY));', mc)

with open(path, "w", encoding="utf-8") as f: f.write(mc)
print("✅ ১. বাটনের গ্যাপ এবং সাইজ ঠিক করা হয়েছে!")
