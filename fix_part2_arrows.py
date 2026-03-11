import re
with open("app/src/main/java/com/my/salah/tracker/app/MainActivity.java", "r", encoding="utf-8") as f: mc = f.read()

p_rep = 'prevW.setLayoutParams(new LinearLayout.LayoutParams((int)(44*DENSITY), (int)(44*DENSITY))); prevW.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 22f*DENSITY).build());'
n_rep = 'nextW.setLayoutParams(new LinearLayout.LayoutParams((int)(44*DENSITY), (int)(44*DENSITY))); nextW.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 22f*DENSITY).build());'

mc = re.sub(r'prevW\.setLayoutParams\([^)]+\);', p_rep, mc)
mc = re.sub(r'nextW\.setLayoutParams\([^)]+\);', n_rep, mc)

with open("app/src/main/java/com/my/salah/tracker/app/MainActivity.java", "w", encoding="utf-8") as f: f.write(mc)
print("✅ ২. তীরচিহ্ন গোল এবং ছোট করা হয়েছে!")
