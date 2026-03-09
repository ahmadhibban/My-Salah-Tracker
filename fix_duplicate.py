fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# টোটাল বক্সের অংশে দ্বিতীয়বার 'int themeMain' ডিক্লেয়ার করা লাইনটি মুছে দিচ্ছি
old_line = """RectF totalRect = new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 40);
                int themeMain = (themeColors != null && themeColors.length > 0) ? themeColors[0] : accentCol;"""

new_line = """RectF totalRect = new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 40);
                // themeMain আগেই তৈরি করা আছে, তাই এখানে নতুন করে লেখার দরকার নেই"""

code = code.replace(old_line, new_line)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success! Duplicate variable error is fixed.")
