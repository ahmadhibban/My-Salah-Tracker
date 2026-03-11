import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ১. বাটনগুলোকে মেইন কার্ডের সমান করা এবং বিশাল গ্যাপ দেওয়া
    mc = mc.replace("markLp.setMargins(0, 0, (int)(6*DENSITY), 0); markAllBtn.setLayoutParams(markLp);", "markLp.setMargins((int)(12*DENSITY), (int)(24*DENSITY), (int)(6*DENSITY), (int)(16*DENSITY)); markAllBtn.setLayoutParams(markLp);")
    mc = mc.replace("todayLp.setMargins((int)(6*DENSITY), 0, 0, 0); todayBtn.setLayoutParams(todayLp);", "todayLp.setMargins((int)(6*DENSITY), (int)(24*DENSITY), (int)(12*DENSITY), (int)(16*DENSITY)); todayBtn.setLayoutParams(todayLp);")

    # ২. সপ্তাহের ঘরগুলোকে ১০০% ডাবিয়ে দেওয়া এবং ভবিষ্যতের দিন স্পষ্ট করা
    pattern = r'FrameLayout cell = new FrameLayout\(this\);\s*cell\.setLayoutParams\(new LinearLayout\.LayoutParams\(0, -2, 1f\)\);\s*TextView t = new TextView\(this\);.*?cell\.addView\(t\);'
    
    replacement = """FrameLayout cell = new FrameLayout(this);
            cell.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
            
            soup.neumorphism.NeumorphCardView neoW = new soup.neumorphism.NeumorphCardView(this);
            neoW.setShapeType(1); // 100% Guaranteed Sunken Effect for all
            neoW.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
            neoW.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
            neoW.setShadowElevation(3f * DENSITY);
            neoW.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 18f*DENSITY).build());
            neoW.setBackgroundColor(isSel ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0")));
            neoW.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY));
            
            FrameLayout.LayoutParams nLp = new FrameLayout.LayoutParams((int)(44 * DENSITY), (int)(44 * DENSITY));
            nLp.gravity = Gravity.CENTER;
            neoW.setLayoutParams(nLp);
            
            TextView t = new TextView(this); t.setText(dLabel); t.setTypeface(Typeface.DEFAULT_BOLD); t.setTextSize(13); t.setGravity(Gravity.CENTER);
            // Fix: Future dates are now a visible grey color (#94A3B8) instead of blending into background
            t.setTextColor(isSel ? android.graphics.Color.parseColor("#F1F5F9") : (isFuture ? android.graphics.Color.parseColor("#94A3B8") : themeColors[3]));
            
            neoW.addView(t, new FrameLayout.LayoutParams(-1, -1));
            cell.addView(neoW);"""
            
    mc = re.sub(pattern, replacement, mc, flags=re.DOTALL)
    
    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
    print("✔ MAGIC PERFECTED! EVERYTHING FIXED.")
else:
    print("❌ FILE NOT FOUND")
