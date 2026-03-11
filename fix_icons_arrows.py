import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ১. তীর চিহ্নগুলোকে সফট থ্রিডি করা (বেশি সাদা ভাব কমানো হলো)
    mc = mc.replace("prevW.setBackground(navBg);", 'applyNeo(prevW, 0, 15f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);')
    mc = mc.replace("nextW.setBackground(navBg);", 'applyNeo(nextW, 0, 15f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);')

    # ২. মার্ক অল বাটনের আইকনকে উঁচা (3D Box) করা
    m_icon_fix = """
        mIcon.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        FrameLayout mIconFrame = new FrameLayout(this);
        LinearLayout.LayoutParams mFlp = new LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY));
        mFlp.setMargins(0, 0, (int)(10*DENSITY), 0);
        mIconFrame.setLayoutParams(mFlp);
        applyNeo(mIconFrame, 0, 12f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        FrameLayout.LayoutParams miLp = new FrameLayout.LayoutParams((int)(22*DENSITY), (int)(22*DENSITY));
        miLp.gravity = Gravity.CENTER;
        mIcon.setLayoutParams(miLp);
        mIconFrame.addView(mIcon);
        markAllBtn.addView(mIconFrame); markAllBtn.addView(markAllTxt);
    """
    mc = re.sub(r'markAllBtn\.addView\(mIcon\);\s*markAllBtn\.addView\(markAllTxt\);', m_icon_fix.strip(), mc)

    # ৩. টুডে বাটনের আইকনকে উঁচা (3D Box) করা
    t_icon_fix = """
        tIcon.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        FrameLayout tIconFrame = new FrameLayout(this);
        LinearLayout.LayoutParams tFlp = new LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY));
        tFlp.setMargins(0, 0, (int)(10*DENSITY), 0);
        tIconFrame.setLayoutParams(tFlp);
        applyNeo(tIconFrame, 0, 12f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        FrameLayout.LayoutParams tiLp = new FrameLayout.LayoutParams((int)(22*DENSITY), (int)(22*DENSITY));
        tiLp.gravity = Gravity.CENTER;
        tIcon.setLayoutParams(tiLp);
        tIconFrame.addView(tIcon);
        todayBtn.addView(tIconFrame); todayBtn.addView(todayTxt); actionRow.addView(todayBtn);
    """
    mc = re.sub(r'todayBtn\.addView\(tIcon\);\s*todayBtn\.addView\(todayTxt\);\s*actionRow\.addView\(todayBtn\);', t_icon_fix.strip(), mc)

    # ৪. সপ্তাহের ঘরগুলোর ডেবে থাকার (Sunken) ইফেক্ট স্পষ্ট করার জন্য ব্যাকগ্রাউন্ড একটু ডার্ক করা হলো
    mc = mc.replace('neoW.setShadowElevation(3f * DENSITY);', 'neoW.setShadowElevation(6f * DENSITY);')
    mc = re.sub(r'neoW\.setBackgroundColor\(isSel \? colorAccent : [^)]+\)\);', 'neoW.setBackgroundColor(isSel ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#141414") : android.graphics.Color.parseColor("#D9E2EC")));', mc)

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
    print("✔ ALL MINOR FIXES APPLIED SUCCESSFULLY!")
else:
    print("❌ FILE NOT FOUND")
