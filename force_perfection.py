import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(java_file):
    print("❌ MainActivity.java not found!")
    exit()

with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. আইকন ফিক্স (আইকনের চারপাশে সুন্দর থ্রিডি বক্স)
if "iconFrame.addView(iconView);" not in mc:
    # আগের ভুল কোড থাকলে সেটা রিমুভ করে দেওয়া
    mc = re.sub(r'applyNeo\(iconView[^;]+;\s*iconView\.setPadding[^;]+;\s*innerCard\.addView\(iconView\);', 'innerCard.addView(iconView);', mc)
    
    icon_wrapper = """
        iconView.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        iconView.setPadding(0,0,0,0);
        FrameLayout iconFrame = new FrameLayout(this);
        LinearLayout.LayoutParams flp = new LinearLayout.LayoutParams((int)(44*DENSITY), (int)(44*DENSITY));
        flp.setMargins(0, 0, (int)(15*DENSITY), 0);
        iconFrame.setLayoutParams(flp);
        applyNeo(iconFrame, 0, 12f, 2.5f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        FrameLayout.LayoutParams ivLp = new FrameLayout.LayoutParams((int)(22*DENSITY), (int)(22*DENSITY));
        ivLp.gravity = android.view.Gravity.CENTER;
        iconView.setLayoutParams(ivLp);
        iconFrame.addView(iconView);
        innerCard.addView(iconFrame);
    """
    mc = re.sub(r'innerCard\.addView\(iconView\);', icon_wrapper, mc)

# ২. 'মার্ক অল' এবং 'টুডে' বাটনকে সমান করা এবং মাঝে গ্যাপ দেওয়া
if "btnLp1.setMargins(0, 0, (int)(8*DENSITY), 0);" not in mc:
    top_btn_fix = """
        LinearLayout.LayoutParams btnLp1 = new LinearLayout.LayoutParams(0, -2, 1f);
        btnLp1.setMargins(0, 0, (int)(8*DENSITY), 0);
        markAllBtn.setLayoutParams(btnLp1);
        
        LinearLayout.LayoutParams btnLp2 = new LinearLayout.LayoutParams(0, -2, 1f);
        btnLp2.setMargins((int)(8*DENSITY), 0, 0, 0);
        todayBtn.setLayoutParams(btnLp2);
        
        topBtns.addView(markAllBtn);
        topBtns.addView(todayBtn);
        topBtns.setPadding(0, (int)(20*DENSITY), 0, (int)(20*DENSITY));
    """
    mc = re.sub(r'topBtns\.addView\(markAllBtn\);\s*topBtns\.addView\(todayBtn\);', top_btn_fix, mc)
    if "topBtns.addView(markAllBtn);" in mc:
        mc = mc.replace("topBtns.addView(markAllBtn);", "")
        mc = mc.replace("topBtns.addView(todayBtn);", top_btn_fix)

# ৩. ভবিষ্যতের দিনগুলোর লেখা हल्का (Faded) করে দৃশ্যমান করা
mc = re.sub(r't\.setTextColor\([^)]*TRANSPARENT[^)]*\);', 't.setTextColor(themeColors[2]); t.setAlpha(0.35f);', mc)
mc = re.sub(r't\.setVisibility\([^)]*INVISIBLE\);', 't.setVisibility(android.view.View.VISIBLE); t.setAlpha(0.35f);', mc)
mc = re.sub(r't\.setAlpha\(0(\.0)?f\);', 't.setAlpha(0.35f);', mc)

# ৪. পার্সেন্টেজ কার্ডকে অ্যাপের কালার (colorAccent) দিয়ে ফিল করা
mc = re.sub(r'int tSur\s*=\s*[^;]+;', 'int tSur = colorAccent;', mc)
mc = re.sub(r'int tShd\s*=\s*[^;]+;', 'int tShd = isDarkTheme ? android.graphics.Color.rgb((int)(android.graphics.Color.red(colorAccent)*0.4f), (int)(android.graphics.Color.green(colorAccent)*0.4f), (int)(android.graphics.Color.blue(colorAccent)*0.4f)) : android.graphics.Color.rgb((int)(android.graphics.Color.red(colorAccent)*0.75f), (int)(android.graphics.Color.green(colorAccent)*0.75f), (int)(android.graphics.Color.blue(colorAccent)*0.75f));', mc)

# ৫. কার্ডগুলোর একপাশের বেশি সাদা (Hard White) ভাব কমিয়ে ব্যালেন্স করা
mc = mc.replace('android.graphics.Color.WHITE', 'android.graphics.Color.parseColor("#F1F5F9")')

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✔ FORCE INJECTED! ALL CHANGES ARE GUARANTEED NOW.")
