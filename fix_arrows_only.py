import re
path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f: mc = f.read()

# তীরচিহ্নের সাইজ ৪৪ ডিপি এবং রেডিয়াস ২২ ডিপি (নিখুঁত গোল) করা হচ্ছে
mc = re.sub(r'prevW\.setLayoutParams\(new LinearLayout\.LayoutParams\([^)]+\)\);', 'prevW.setLayoutParams(new LinearLayout.LayoutParams((int)(44*DENSITY), (int)(44*DENSITY)));', mc)
mc = re.sub(r'nextW\.setLayoutParams\(new LinearLayout\.LayoutParams\([^)]+\)\);', 'nextW.setLayoutParams(new LinearLayout.LayoutParams((int)(44*DENSITY), (int)(44*DENSITY)));', mc)
mc = re.sub(r'prevW\.setShapeAppearanceModel\(new soup\.neumorphism\.NeumorphShapeAppearanceModel\.Builder\(\)\.setAllCorners\(0,\s*[^)]+\)\.build\(\)\);', 'prevW.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 22f*DENSITY).build());', mc)
mc = re.sub(r'nextW\.setShapeAppearanceModel\(new soup\.neumorphism\.NeumorphShapeAppearanceModel\.Builder\(\)\.setAllCorners\(0,\s*[^)]+\)\.build\(\)\);', 'nextW.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 22f*DENSITY).build());', mc)

with open(path, "w", encoding="utf-8") as f: f.write(mc)
print("✅ ২. তীরচিহ্নের সাইজ এবং গোল আকার ঠিক করা হয়েছে!")
