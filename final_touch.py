import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(java_file):
    print("❌ MainActivity.java not found!")
    exit()

with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. আইকন ফিক্স (আইকনকে সরাসরি শ্যাডো না দিয়ে, সুন্দর একটি থ্রিডি বক্সের ভেতর রাখা হলো)
bad_icon_code = 'applyNeo(iconView, 0, 12f, 2.5f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); iconView.setPadding((int)(10*DENSITY),(int)(10*DENSITY),(int)(10*DENSITY),(int)(10*DENSITY)); innerCard.addView(iconView);'

good_icon_code = """
        iconView.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        iconView.setPadding(0,0,0,0);
        FrameLayout iconFrame = new FrameLayout(this);
        LinearLayout.LayoutParams flp = new LinearLayout.LayoutParams((int)(44*DENSITY), (int)(44*DENSITY));
        flp.setMargins(0, 0, (int)(15*DENSITY), 0);
        iconFrame.setLayoutParams(flp);
        applyNeo(iconFrame, 0, 12f, 2.5f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        
        FrameLayout.LayoutParams ivLp = new FrameLayout.LayoutParams((int)(22*DENSITY), (int)(22*DENSITY));
        ivLp.gravity = Gravity.CENTER;
        iconView.setLayoutParams(ivLp);
        iconFrame.addView(iconView);
        innerCard.addView(iconFrame);
"""
mc = mc.replace(bad_icon_code, good_icon_code)

# ২. ভবিষ্যতের দিনগুলোর লেখা দৃশ্যমান করা (হালকা রঙে)
mc = mc.replace("t.setTextColor(android.graphics.Color.TRANSPARENT);", "")
mc = mc.replace("t.setTextColor(Color.TRANSPARENT);", "")
mc = re.sub(r't\.setAlpha\(0\.35f\);', r't.setTextColor(themeColors[2]); t.setAlpha(0.35f);', mc)

# ৩. মার্ক অল এবং টুডে বাটনকে একদম মাপে মাপে কার্ডের সমান করা এবং স্পেসিং দেওয়া
btn_fix = """
        topBtns.addView(todayBtn);
        
        LinearLayout.LayoutParams btnLp1 = new LinearLayout.LayoutParams(0, -2, 1f);
        btnLp1.setMargins(0, 0, (int)(8*DENSITY), 0);
        markAllBtn.setLayoutParams(btnLp1);
        
        LinearLayout.LayoutParams btnLp2 = new LinearLayout.LayoutParams(0, -2, 1f);
        btnLp2.setMargins((int)(8*DENSITY), 0, 0, 0);
        todayBtn.setLayoutParams(btnLp2);
        
        topBtns.setPadding(0, (int)(20*DENSITY), 0, (int)(20*DENSITY));
"""
if "topBtns.setPadding(0, (int)(20*DENSITY), 0, (int)(20*DENSITY));" not in mc:
    mc = mc.replace("topBtns.addView(todayBtn);", btn_fix)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✔ FINAL TOUCHES APPLIED PERFECTLY!")
