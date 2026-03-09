import re

files = [
    "app/src/main/java/com/my/salah/tracker/app/fragments/QuranFragment.java",
    "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
]

for fpath in files:
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            code = f.read()
        
        # যেকোনো বড়/ছোট হাতের ফন্টের নামকে হুবহু ছোট হাতের নামে রূপান্তর করা হচ্ছে
        code = re.sub(r'"fonts/[Aa]l_?[Mm]ajeed.*?\.ttf"', '"fonts/al_majeed_quranic_font_shiped.ttf"', code)
        
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"✅ Success: Font name updated to lowercase in {fpath.split('/')[-1]}")
    except Exception as e:
        print(f"❌ Error with {fpath}: {e}")
