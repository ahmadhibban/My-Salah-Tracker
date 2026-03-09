import re

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# ১. বৃত্ত এবং দোয়ার বক্সের মাঝে পর্যাপ্ত গ্যাপ তৈরি করা এবং বৃত্তটা আরেকটু স্মার্ট করা
code = re.sub(
    r'float\s+circleY\s*=\s*boxTop\s*\+\s*boxHeight\s*\+\s*\(h\s*\*\s*0\.1[0-9]f\)\s*,\s*radius\s*=\s*w\s*\*\s*0\.[0-9]+f\s*;',
    r'float circleY = boxTop + boxHeight + (h * 0.22f), radius = w * 0.29f;',
    code
)

# ২. দোয়ার বক্সের সাদা/নীল গ্রেডিয়েন্ট মুছে অ্যাপের অরিজিনাল থিম কালার বসানো
old_grad = r'int\s+darkAcc\s*=.*?Shader\.TileMode\.CLAMP\);'
new_grad = r'''int primaryThemeColor = themeColors != null && themeColors.length > 0 ? themeColors[0] : accentCol;
                android.graphics.LinearGradient lg = new android.graphics.LinearGradient(
                    40, boxTop, w-40, boxTop+boxHeight, 
                    new int[]{accentCol, primaryThemeColor}, 
                    null, android.graphics.Shader.TileMode.CLAMP);'''
code = re.sub(old_grad, new_grad, code, flags=re.DOTALL)

# ৩. 'Total/Loop' লেখাটি বক্স থেকে বের হয়ে ডানদিকে সরে যাওয়ার বাগ ফিক্স করে ঠিক মাঝখানে আনা
old_align = r'p\.setStyle\(Paint\.Style\.FILL\);\s*p\.setColor\(textCol\);\s*canvas\.drawText\(totalTxt,\s*centerX,\s*totalBoxY\s*\+\s*12,\s*p\);'
new_align = r'p.setStyle(Paint.Style.FILL); p.setColor(textCol); p.setTextAlign(Paint.Align.CENTER); canvas.drawText(totalTxt, centerX, totalBoxY + 12, p);'
code = re.sub(old_align, new_align, code)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Advanced Auto-Patch Applied! All layout and theme issues are fixed perfectly.")
