import re

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# ১. বৃত্তের সিলভার বর্ডার খুঁজে বের করে থিমের মেইন কালার (themeColors[0]) বসানো
code = re.sub(
    r'android\.graphics\.SweepGradient\s+\w+\s*=\s*new\s*android\.graphics\.SweepGradient\([^)]+Color\.GRAY[^)]+\);',
    r'int themeMain = themeColors != null && themeColors.length > 0 ? themeColors[0] : accentCol;\n                android.graphics.SweepGradient themeRing = new android.graphics.SweepGradient(centerX, circleY, new int[]{cardCol, themeMain, cardCol, themeMain, cardCol}, null);',
    code
)
code = re.sub(r'p\.setShader\(metallic\);', r'p.setShader(themeRing);', code)

# ২. প্রোগ্রেস আর্ক (লাইন) এবং ৩ডি বলের কালার থিমের সাথে সিঙ্ক করা
code = re.sub(
    r'p\.setColor\(accentCol\);\s*canvas\.drawArc',
    r'p.setColor(themeMain);\n                canvas.drawArc',
    code
)
code = re.sub(
    r'Color\.WHITE,\s*accentCol,\s*android\.graphics\.Shader\.TileMode\.CLAMP\)',
    r'Color.WHITE, themeMain, android.graphics.Shader.TileMode.CLAMP)',
    code
)

# ৩. টোটাল লেখার বক্সের ফিল এবং বর্ডার থিমের কালার দিয়ে সেট করা
pattern = r'RectF\s+totalRect\s*=\s*new\s*RectF[^;]+;.*?p\.setTextAlign\(Paint\.Align\.CENTER\);'
replacement = r'''RectF totalRect = new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 40);
                int themeMain = themeColors != null && themeColors.length > 0 ? themeColors[0] : accentCol;
                
                // থিম কালারে হালকা ফিল (Background)
                p.setStyle(Paint.Style.FILL); p.setColor(themeMain); p.setAlpha(30);
                canvas.drawRoundRect(totalRect, 40f, 40f, p); p.setAlpha(255);
                
                // থিম কালারে স্পষ্ট বর্ডার
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(4f); p.setColor(themeMain);
                canvas.drawRoundRect(totalRect, 40f, 40f, p);
                
                // লেখা মাঝখানে রাখা
                p.setStyle(Paint.Style.FILL); p.setColor(textCol); p.setTextAlign(Paint.Align.CENTER);'''

code = re.sub(pattern, replacement, code, flags=re.DOTALL)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Bruteforce Sync Applied! The ring, ball, and total box are now FORCE-SYNCED with your Salah themes.")
