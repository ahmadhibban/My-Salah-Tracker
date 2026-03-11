import os
import re

def update_3d_design():
    main_file = None
    ui_file = None
    for root, _, files in os.walk("."):
        if "MainActivity.java" in files: main_file = os.path.join(root, "MainActivity.java")
        if "UIComponents.java" in files: ui_file = os.path.join(root, "UIComponents.java")

    # ১. UIComponents.java ফিক্স (চেক বক্স আগের মত ফ্ল্যাট করা)
    if ui_file:
        with open(ui_file, 'r', encoding='utf-8') as f:
            ui_code = f.read()
        
        flat_checkbox = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) { 
        android.widget.TextView tv = new android.widget.TextView(activity);
        tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14); 
        android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); tv.setLayoutParams(lp); 
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setShape(android.graphics.drawable.GradientDrawable.OVAL); 
        if(status.equals("yes")) { gd.setColor(activeColorHex); tv.setText("✓"); tv.setTextColor(android.graphics.Color.WHITE); } 
        else if (status.equals("excused")) { gd.setColor(activeColorHex); tv.setText("🌸"); tv.setTextColor(android.graphics.Color.WHITE); } 
        else { gd.setColor(android.graphics.Color.TRANSPARENT); gd.setStroke((int)(2*DENSITY), themeColors[4]); tv.setText(""); } 
        tv.setBackground(gd); return tv;
    }"""
        ui_code = re.sub(r'public android\.view\.View getPremiumCheckbox.*?return (?:chk|tv);\n    }', flat_checkbox, ui_code, flags=re.DOTALL)
        with open(ui_file, 'w', encoding='utf-8') as f:
            f.write(ui_code)
        print("✔ Checkbox reverted to original flat design.")

    # ২. MainActivity.java ফিক্স
    if main_file:
        with open(main_file, 'r', encoding='utf-8') as f:
            main_code = f.read()

        # A. বর্ডার আরও মোটা করার জন্য 3D ইঞ্জিন আপডেট (Depth 7 এবং Offset 2.0f)
        new_3d_engine = """public android.graphics.drawable.Drawable getSolid3DDrawable(int mainColor, int borderColor, float radius, boolean isDark, boolean isRound) {
        int depth = isRound ? 4 : 7; // বর্ডার আরও মোটা করা হলো
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.Drawable[] layers = new android.graphics.drawable.Drawable[depth + 1];
        
        int[] lightShadows = {android.graphics.Color.parseColor("#d8dee9"), android.graphics.Color.parseColor("#cbd5e0"), android.graphics.Color.parseColor("#adb9ca"), android.graphics.Color.parseColor("#91a0b5"), android.graphics.Color.parseColor("#8595a8"), android.graphics.Color.parseColor("#7a8a9e"), android.graphics.Color.parseColor("#6f7f94")};
        int[] darkShadows = {android.graphics.Color.parseColor("#0A0A0C"), android.graphics.Color.parseColor("#101012"), android.graphics.Color.parseColor("#121214"), android.graphics.Color.parseColor("#151517"), android.graphics.Color.parseColor("#18181A"), android.graphics.Color.parseColor("#1A1A1C"), android.graphics.Color.parseColor("#1c1c1f")};
        int[] shadows = isDark ? darkShadows : lightShadows;
        
        for (int i = 0; i <= depth; i++) {
            android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
            gd.setCornerRadius(radius);
            if (isRound) gd.setShape(android.graphics.drawable.GradientDrawable.OVAL);
            
            if (i == depth) {
                gd.setColor(mainColor);
                if (borderColor != android.graphics.Color.TRANSPARENT) gd.setStroke((int)(1.5f * d), borderColor);
            } else { gd.setColor(shadows[i % shadows.length]); }
            layers[i] = gd;
        }
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(layers);
        for (int i = 0; i <= depth; i++) {
            int currL = (int)((i * 2.0f * d)); // Offset বাড়ানো হয়েছে যাতে মোটা দেখায়
            int currT = (int)(((depth - i) * 2.0f * d)); 
            int currR = (int)(((depth - i) * 2.0f * d)); 
            int currB = (int)((i * 2.0f * d)); 
            ld.setLayerInset(i, currL, currT, currR, currB);
        }
        return ld;
    }"""
        main_code = re.sub(r'public android\.graphics\.drawable\.Drawable getSolid3DDrawable.*?return ld;\n    }', new_3d_engine, main_code, flags=re.DOTALL)

        # B. সুন্নাহ বাটন আগের মত করা
        flat_sunnah = """GradientDrawable customSunnahBg = new GradientDrawable(); customSunnahBg.setCornerRadius(12f*DENSITY); if(doneSunnahs > 0){customSunnahBg.setColor(colorAccent);sunnahBtn.setTextColor(android.graphics.Color.WHITE);}else{customSunnahBg.setColor(themeColors[5]);sunnahBtn.setTextColor(themeColors[2]);} 
                sunnahBtn.setPadding((int)(10*DENSITY), (int)(5*DENSITY), (int)(10*DENSITY), (int)(5*DENSITY));
                sunnahBtn.setBackground(customSunnahBg);"""
        main_code = re.sub(r'int sBgColor = doneSunnahs > 0 \? colorAccent : themeColors\[4\];.*?sunnahBtn\.setPadding.*?DENSITY\)\);', flat_sunnah, main_code, flags=re.DOTALL)

        # C. স্ট্রিক পিল 3D করা
        if "streakBadge.setBackground(getSolid3DDrawable" not in main_code:
            main_code = re.sub(r'streakBadge\.setBackground\(badgeBg\);', 'streakBadge.setBackground(getSolid3DDrawable(colorAccent, android.graphics.Color.TRANSPARENT, 15f * DENSITY, isDarkTheme, false));', main_code)

        # D. আইকনগুলো 3D করা
        if "themeToggleBtn.setBackground(getSolid3DDrawable" not in main_code:
            main_code = re.sub(r'themeToggleBtn\.setBackground\(tBg\);', 'themeToggleBtn.setBackground(getSolid3DDrawable(isDarkTheme ? android.graphics.Color.parseColor("#1A2980") : android.graphics.Color.parseColor("#FF9500"), themeColors[4], 100f, isDarkTheme, true));', main_code)
            main_code = re.sub(r'rightHeader\.addView\(offBtn\);', 'offBtn.setBackground(getSolid3DDrawable(themeColors[1], android.graphics.Color.parseColor("#FF5252"), 100f, isDarkTheme, true)); rightHeader.addView(offBtn);', main_code)
            main_code = re.sub(r'rightHeader\.addView\(periodBtn\);', 'periodBtn.setBackground(getSolid3DDrawable(themeColors[1], colorAccent, 100f, isDarkTheme, true)); rightHeader.addView(periodBtn);', main_code)
            main_code = re.sub(r'rightHeader\.addView\(settingsBtn\);', 'settingsBtn.setBackground(getSolid3DDrawable(themeColors[1], colorAccent, 100f, isDarkTheme, true)); rightHeader.addView(settingsBtn);', main_code)

        # E. ৭ দিনের ক্যালেন্ডার 3D করা (বর্গাকার বা স্কয়ার শেপে)
        if "t.setBackground(getSolid3DDrawable" not in main_code:
            main_code = re.sub(r't\.setBackground\(getProgressBorder\(dKey, isSel\)\);', 
                't.setBackground(getSolid3DDrawable(isSel ? colorAccent : themeColors[1], isSel ? android.graphics.Color.TRANSPARENT : themeColors[4], 10f * DENSITY, isDarkTheme, false));', main_code)

        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(main_code)
        print("✔ MainActivity updated: Thicker borders, 3D Week & Icons, Flat Sunnah.")

update_3d_design()
