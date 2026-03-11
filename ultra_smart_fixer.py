import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ১. সপ্তাহের ঘরগুলো জোর করে ডাবিয়ে দেওয়া (applyNeo এর দ্বিতীয় ভ্যালু 1 করে দেওয়া)
    # এটি যেভাবেই লেখা থাকুক না কেন, ঠিকই খুঁজে 1 বসিয়ে দেবে
    mc = re.sub(r'(applyNeo\s*\(\s*t\s*,\s*)[^,]+(\s*,)', r'\g<1>1\g<2>', mc)

    # ২. ভবিষ্যতের দিনগুলোকে ১০০% স্পষ্ট করা (সব হাইড/স্বচ্ছতা রিমুভ)
    mc = re.sub(r't\.setAlpha\s*\(\s*(0(\.0)?f|0\.35f|0\.6f|0\.5f)\s*\)\s*;', 't.setAlpha(1.0f);', mc)
    mc = re.sub(r't\.setVisibility\s*\(\s*[^)]*INVISIBLE[^)]*\)\s*;', 't.setVisibility(android.view.View.VISIBLE);', mc)
    mc = re.sub(r't\.setTextColor\s*\(\s*[^)]*TRANSPARENT[^)]*\)\s*;', 't.setTextColor(android.graphics.Color.parseColor("#94A3B8"));', mc)

    # ৩. মার্ক অল এবং টুডে বাটনের পারফেক্ট সাইজ ও গ্যাপ
    btn_fix = """
        // আল্ট্রা ফিক্স: বাটন সাইজ ও গ্যাপ
        LinearLayout.LayoutParams fLp1 = new LinearLayout.LayoutParams(0, -2, 1f);
        fLp1.setMargins((int)(16*DENSITY), (int)(24*DENSITY), (int)(8*DENSITY), (int)(16*DENSITY));
        markAllBtn.setLayoutParams(fLp1);

        LinearLayout.LayoutParams fLp2 = new LinearLayout.LayoutParams(0, -2, 1f);
        fLp2.setMargins((int)(8*DENSITY), (int)(24*DENSITY), (int)(16*DENSITY), (int)(16*DENSITY));
        todayBtn.setLayoutParams(fLp2);
        
        topBtns.setPadding(0, 0, 0, 0);
    """
    
    # পুরনো লেআউট প্যারামিটার থাকলে মুছে ফেলা (যাতে ডাবল না হয়)
    mc = re.sub(r'LinearLayout\.LayoutParams\s+btnLp1.*?markAllBtn\.setLayoutParams\s*\([^)]+\)\s*;', '', mc, flags=re.DOTALL)
    mc = re.sub(r'LinearLayout\.LayoutParams\s+btnLp2.*?todayBtn\.setLayoutParams\s*\([^)]+\)\s*;', '', mc, flags=re.DOTALL)
    
    # নতুন পারফেক্ট সাইজগুলো বসানো
    if "topBtns.addView(todayBtn);" in mc:
        mc = mc.replace("topBtns.addView(todayBtn);", "topBtns.addView(todayBtn);\n" + btn_fix)
    elif "topBtns.addView(markAllBtn);" in mc:
        mc = mc.replace("topBtns.addView(markAllBtn);", "topBtns.addView(markAllBtn);\n" + btn_fix)

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
    print("✔ ULTRA SMART FIX APPLIED! EVERYTHING IS SET PERFECTLY.")
else:
    print("❌ FILE NOT FOUND!")
