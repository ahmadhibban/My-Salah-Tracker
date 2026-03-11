import os, re

# পুরনো ভুল মেথডগুলো মুছে ফেলার ফাংশন
def remove_method(code, method_name):
    start = code.find(method_name)
    if start == -1: return code
    brace_start = code.find('{', start)
    if brace_start == -1: return code
    brace_count = 1
    end = -1
    for i in range(brace_start + 1, len(code)):
        if code[i] == '{': brace_count += 1
        elif code[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break
    if end != -1:
        return code[:start] + code[end:]
    return code

def ultimate_redemption():
    main_file = None
    ui_file = None
    for root, _, files in os.walk("."):
        if "MainActivity.java" in files: main_file = os.path.join(root, "MainActivity.java")
        if "UIComponents.java" in files: ui_file = os.path.join(root, "UIComponents.java")

    # --- ১. UIComponents.java (নতুন ইন্টারেক্টিভ চেকবক্স) ---
    if ui_file:
        with open(ui_file, 'r', encoding='utf-8') as f: ui_code = f.read()
        
        new_checkbox = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) { 
        android.widget.TextView tv = new android.widget.TextView(activity);
        tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14); tv.setIncludeFontPadding(false); 
        float d = activity.getResources().getDisplayMetrics().density;
        android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(32*d), (int)(32*d)); 
        tv.setLayoutParams(lp); 
        
        android.content.SharedPreferences sp = activity.getSharedPreferences("salah_pro_final", android.content.Context.MODE_PRIVATE);
        boolean systemDark = (activity.getResources().getConfiguration().uiMode & android.content.res.Configuration.UI_MODE_NIGHT_MASK) == android.content.res.Configuration.UI_MODE_NIGHT_YES;
        boolean isDark = sp.getBoolean("is_dark_mode", systemDark);
        
        float rad = 10f * d; // গোল এর বদলে স্মার্ট Squircle
        
        // ✨ ইন্টারেক্টিভ থ্রিডি: চেক না করলে ভেসে থাকবে (depth 4), চেক করলে ডেবে যাবে (depth 1) ✨
        int depth = status.equals("yes") || status.equals("excused") ? 1 : 4; 
        
        int mainColor = (status.equals("yes") || status.equals("excused")) ? activeColorHex : (isDark ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE);
        int borderColor = (status.equals("yes") || status.equals("excused")) ? android.graphics.Color.TRANSPARENT : (isDark ? android.graphics.Color.parseColor("#333333") : android.graphics.Color.parseColor("#E0E0E0"));
        
        int r = android.graphics.Color.red(activeColorHex); int g = android.graphics.Color.green(activeColorHex); int b = android.graphics.Color.blue(activeColorHex);
        float darkenFactor = isDark ? 0.45f : 0.75f; 
        int shadowColor = android.graphics.Color.rgb((int)(r * darkenFactor), (int)(g * darkenFactor), (int)(b * darkenFactor));

        android.graphics.drawable.Drawable[] layers = new android.graphics.drawable.Drawable[depth + 1];
        for (int i = 0; i <= depth; i++) {
            android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
            gd.setCornerRadius(rad);
            if (i == depth) { gd.setColor(mainColor); if (borderColor != android.graphics.Color.TRANSPARENT) gd.setStroke((int)(1.0f * d), borderColor); } 
            else { gd.setColor(shadowColor); }
            layers[i] = gd;
        }
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(layers);
        for (int i = 0; i <= depth; i++) { int step = (int) (1.5f * d); ld.setLayerInset(i, i * step, (depth - i) * step, (depth - i) * step, i * step); }
        tv.setBackground(ld);
        
        if(status.equals("yes") || status.equals("excused")) { tv.setText(status.equals("yes") ? "✓" : "🌸"); tv.setTextColor(android.graphics.Color.WHITE); } 
        else { tv.setText(""); }
        
        // ✨ পারফেক্ট ম্যাথমেটিক্যাল প্যাডিং: টিক চিহ্নকে ১০০% মাঝখানে রাখার জাদুকরী সূত্র ✨
        int shift = (int)(depth * 1.5f * d);
        tv.setPadding(shift, 0, 0, shift);
        
        return tv;
    }"""
        ui_code = remove_method(ui_code, "public android.view.View getPremiumCheckbox")
        last_brace = ui_code.rfind('}')
        ui_code = ui_code[:last_brace] + new_checkbox + "\n" + ui_code[last_brace:]
        with open(ui_file, 'w', encoding='utf-8') as f: f.write(ui_code)

    # --- ২. MainActivity.java (এলাইনমেন্ট ফিক্স ও নতুন ডিজাইন) ---
    if main_file:
        with open(main_file, 'r', encoding='utf-8') as f: code = f.read()

        # পুরনো ইঞ্জিনগুলো পরিষ্কার করা
        code = remove_method(code, "public android.graphics.drawable.Drawable getSolid3DDrawable")
        code = remove_method(code, "public android.graphics.drawable.Drawable getCarvedDrawable")
        code = remove_method(code, "public android.graphics.drawable.Drawable getCustom3DDrawable")

        # নতুন মাস্টার ইঞ্জিন 
        engine = """public android.graphics.drawable.Drawable getCustom3DDrawable(int mainColor, int borderColor, float radius, boolean isDark, int depth) {
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.Drawable[] layers = new android.graphics.drawable.Drawable[depth + 1];
        
        int depthBaseColor = mainColor;
        if (mainColor == android.graphics.Color.WHITE || mainColor == android.graphics.Color.parseColor("#1A1115") || mainColor == android.graphics.Color.parseColor("#121212") || mainColor == android.graphics.Color.parseColor("#F5F7FA") || mainColor == android.graphics.Color.parseColor("#1C1C1E")) { depthBaseColor = colorAccent; }
        
        int r = android.graphics.Color.red(depthBaseColor); int g = android.graphics.Color.green(depthBaseColor); int b = android.graphics.Color.blue(depthBaseColor);
        float darkenFactor = isDark ? 0.45f : 0.75f; 
        int shadowColor = android.graphics.Color.rgb((int)(r * darkenFactor), (int)(g * darkenFactor), (int)(b * darkenFactor));

        for (int i = 0; i <= depth; i++) {
            android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
            gd.setCornerRadius(radius);
            if (i == depth) { gd.setColor(mainColor); if (borderColor != android.graphics.Color.TRANSPARENT) gd.setStroke((int)(1.0f * d), borderColor); } 
            else { gd.setColor(shadowColor); }
            layers[i] = gd;
        }
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(layers);
        for (int i = 0; i <= depth; i++) { int step = (int) (1.5f * d); ld.setLayerInset(i, i * step, (depth - i) * step, (depth - i) * step, i * step); }
        return ld;
    }"""
        last_brace = code.rfind('}')
        code = code[:last_brace] + engine + "\n" + code[last_brace:]

        # পুরনো সব সেটআপ মুছে ফেলা
        targets = ["themeToggleBtn", "offBtn", "periodBtn", "settingsBtn", "streakBadge", "iconTxt", "t", "sunnahBtn", "pCard", "markAllBtn", "todayBtn", "card"]
        for t in targets:
            code = re.sub(rf'{t}\.setBackground\(.*?\);', '', code)
            code = re.sub(rf'{t}\.setPadding\(.*?\);', '', code)
            code = re.sub(rf'{t}\.setGravity\(.*?\);', '', code)
            code = re.sub(rf'{t}\.setIncludeFontPadding\(.*?\);', '', code)

        # ✨ পারফেক্ট অফসেট প্যাডিং দিয়ে নতুন করে ডিজাইন বসানো হচ্ছে ✨
        injections = {
            "rightHeader.addView(themeToggleBtn);": 
                """themeToggleBtn.setBackground(getCustom3DDrawable(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, themeColors[4], 100f, isDarkTheme, 2)); themeToggleBtn.setPadding((int)(11*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(11*DENSITY));\n        rightHeader.addView(themeToggleBtn);""",
                
            "rightHeader.addView(offBtn);": 
                """offBtn.setBackground(getCustom3DDrawable(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, themeColors[4], 100f, isDarkTheme, 2)); offBtn.setPadding((int)(11*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(11*DENSITY));\n        rightHeader.addView(offBtn);""",
                
            "rightHeader.addView(periodBtn);": 
                """periodBtn.setBackground(getCustom3DDrawable(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, themeColors[4], 100f, isDarkTheme, 2)); periodBtn.setPadding((int)(11*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(11*DENSITY));\n        rightHeader.addView(periodBtn);""",
                
            "rightHeader.addView(settingsBtn);": 
                """settingsBtn.setBackground(getCustom3DDrawable(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, themeColors[4], 100f, isDarkTheme, 2)); settingsBtn.setPadding((int)(11*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(11*DENSITY));\n        rightHeader.addView(settingsBtn);""",
                
            "leftHeader.addView(streakBadge);": 
                """streakBadge.setBackground(getCustom3DDrawable(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, themeColors[4], 20f*DENSITY, isDarkTheme, 2)); streakBadge.setTextColor(colorAccent); streakBadge.setPadding((int)(15*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(9*DENSITY)); streakBadge.setGravity(android.view.Gravity.CENTER); streakBadge.setIncludeFontPadding(false);\n        leftHeader.addView(streakBadge);""",
                
            "iconTxt.setText(prayerIcons[i]);": 
                """iconTxt.setText(prayerIcons[i]);\n        iconTxt.setBackground(getCustom3DDrawable(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, themeColors[4], 100f, isDarkTheme, 2)); iconTxt.setPadding((int)(15*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY), (int)(11*DENSITY)); iconTxt.setGravity(android.view.Gravity.CENTER); iconTxt.setIncludeFontPadding(false);""",
                
            "t.setText(dayNames[i]);": 
                """t.setText(dayNames[i]);\n        t.setBackground(getCustom3DDrawable(isSel ? colorAccent : themeColors[1], isSel ? android.graphics.Color.TRANSPARENT : themeColors[4], 8f * DENSITY, isDarkTheme, 2)); t.setPadding((int)(3*DENSITY), 0, 0, (int)(3*DENSITY)); t.setGravity(android.view.Gravity.CENTER); t.setIncludeFontPadding(false);""",
                
            "sunnahBtn.setText(sunnahStr);": 
                """sunnahBtn.setText(sunnahStr);\n        sunnahBtn.setBackground(getCustom3DDrawable(doneSunnahs > 0 ? colorAccent : themeColors[1], themeColors[4], 12f*DENSITY, isDarkTheme, 2)); sunnahBtn.setPadding((int)(15*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(9*DENSITY)); sunnahBtn.setGravity(android.view.Gravity.CENTER); sunnahBtn.setIncludeFontPadding(false);""",
                
            "rootLayout.addView(pCard);": 
                """pCard.setBackground(getCustom3DDrawable(pMainColor, android.graphics.Color.TRANSPARENT, 16f*DENSITY, !isDayTime, 8)); pCard.setPadding((int)(32*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(32*DENSITY));\n        rootLayout.addView(pCard);""",
                
            "markAllBtn.setOnClickListener": 
                """markAllBtn.setBackground(getCustom3DDrawable(themeColors[1], themeColors[4], 12f*DENSITY, isDarkTheme, 5)); markAllBtn.setPadding((int)(22*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(22*DENSITY)); markAllBtn.setGravity(android.view.Gravity.CENTER); markAllBtn.setIncludeFontPadding(false);\n        markAllBtn.setOnClickListener""",
                
            "todayBtn.setOnClickListener": 
                """todayBtn.setBackground(getCustom3DDrawable(themeColors[1], themeColors[4], 12f*DENSITY, isDarkTheme, 5)); todayBtn.setPadding((int)(22*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(22*DENSITY)); todayBtn.setGravity(android.view.Gravity.CENTER); todayBtn.setIncludeFontPadding(false);\n        todayBtn.setOnClickListener""",
                
            "card.addView(leftContent);": 
                """int cColor = stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#1A1115") : android.graphics.Color.parseColor("#FCE4EC")) : themeColors[1];\n        int bColor = stat.equals("excused") ? android.graphics.Color.parseColor("#FF4081") : (checked ? colorAccent : themeColors[4]);\n        card.setBackground(getCustom3DDrawable(cColor, bColor, 14f*DENSITY, isDarkTheme, 8)); card.setPadding((int)(32*DENSITY), (int)((cardPadV)*DENSITY), (int)(20*DENSITY), (int)((cardPadV+12)*DENSITY));\n        card.addView(leftContent);"""
        }
        
        for k, v in injections.items(): code = code.replace(k, v)
        with open(main_file, 'w', encoding='utf-8') as f: f.write(code)

if __name__ == '__main__':
    ultimate_redemption()
    