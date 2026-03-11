import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(java_file):
    print("❌ MainActivity.java not found!")
    exit()

with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. আইকনগুলোকে স্পষ্ট এবং বড় করা (22 থেকে 34 করা হলো)
mc = re.sub(r'FrameLayout\.LayoutParams\(\(int\)\(22\*DENSITY\),\s*\(int\)\(22\*DENSITY\)\);', r'FrameLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY));', mc)

# ২. পার্সেন্টেজ কার্ডকে অ্যাপের কালার (colorAccent) দিয়ে ফিল করা (যাতে পানির মতো সুন্দর ফিল আসে)
mc = re.sub(r'int\s+tSur\s*=\s*[^;]+;', 'int tSur = colorAccent;', mc)
mc = re.sub(r'int\s+tShd\s*=\s*[^;]+;', 'int tShd = isDarkTheme ? android.graphics.Color.rgb((int)(android.graphics.Color.red(colorAccent)*0.4f), (int)(android.graphics.Color.green(colorAccent)*0.4f), (int)(android.graphics.Color.blue(colorAccent)*0.4f)) : android.graphics.Color.rgb((int)(android.graphics.Color.red(colorAccent)*0.75f), (int)(android.graphics.Color.green(colorAccent)*0.75f), (int)(android.graphics.Color.blue(colorAccent)*0.75f));', mc)

# ৩. কার্ডগুলোর একপাশের বেশি সাদা (Hard White) ভাব কমিয়ে ব্যালেন্স করা
mc = mc.replace('android.graphics.Color.WHITE', 'android.graphics.Color.parseColor("#F1F5F9")')

# ৪. ভবিষ্যতের দিনগুলোর লেখা हल्का (Faded) করে দৃশ্যমান করা (Transparent বা Invisible সরাতে হবে)
mc = re.sub(r't\.setTextColor\([^)]*(?:TRANSPARENT|Color\.TRANSPARENT)[^)]*\);', 't.setTextColor(themeColors[2]); t.setAlpha(0.35f);', mc)
mc = re.sub(r't\.setVisibility\([^)]*INVISIBLE\);', 't.setVisibility(android.view.View.VISIBLE); t.setAlpha(0.35f);', mc)
mc = re.sub(r't\.setAlpha\(\s*0(?:\.0)?f\s*\);', 't.setAlpha(0.35f);', mc)

# ৫. 'মার্ক অল' এবং 'টুডে' বাটনকে সমান করা এবং মাঝে গ্যাপ দেওয়া
if "btnLp1.setMargins" not in mc:
    top_btn_fix = """
        LinearLayout.LayoutParams btnLp1 = new LinearLayout.LayoutParams(0, -2, 1f);
        btnLp1.setMargins(0, 0, (int)(8*DENSITY), 0);
        markAllBtn.setLayoutParams(btnLp1);
        
        LinearLayout.LayoutParams btnLp2 = new LinearLayout.LayoutParams(0, -2, 1f);
        btnLp2.setMargins((int)(8*DENSITY), 0, 0, 0);
        todayBtn.setLayoutParams(btnLp2);
        
        topBtns.addView(markAllBtn);
        topBtns.addView(todayBtn);
    """
    mc = re.sub(r'topBtns\.addView\(markAllBtn\);\s*topBtns\.addView\(todayBtn\);', top_btn_fix, mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✔ ABSOLUTE PERFECTION APPLIED! READY TO BUILD.")
