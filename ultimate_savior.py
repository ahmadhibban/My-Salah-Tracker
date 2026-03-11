import os, re

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
    if end != -1: return code[:start] + code[end:]
    return code

def ultimate_savior():
    main_file = None
    ui_file = None
    for root, _, files in os.walk("."):
        if "MainActivity.java" in files: main_file = os.path.join(root, "MainActivity.java")
        if "UIComponents.java" in files: ui_file = os.path.join(root, "UIComponents.java")

    # --- ১. UIComponents.java (পারফেক্ট Squircle চেকবক্স) ---
    if ui_file:
        with open(ui_file, 'r', encoding='utf-8') as f: ui_code = f.read()
        
        new_checkbox = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) { 
        android.widget.TextView tv = new android.widget.TextView(activity);
        tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14); 
        float d = activity.getResources().getDisplayMetrics().density;
        android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(28*d), (int)(28*d)); 
        tv.setLayoutParams(lp); 
        
        android.content.SharedPreferences sp = activity.getSharedPreferences("salah_pro_final", android.content.Context.MODE_PRIVATE);
        boolean systemDark = (activity.getResources().getConfiguration().uiMode & android.content.res.Configuration.UI_MODE_NIGHT_MASK) == android.content.res.Configuration.UI_MODE_NIGHT_YES;
        boolean isDark = sp.getBoolean("is_dark_mode", systemDark);
        
        boolean isChecked = status.equals("yes") || status.equals("excused");
        float radius = 8f * d; // কি-বোর্ড বাটনের মত Squircle শেপ
        
        int surfaceColor = isChecked ? activeColorHex : (isDark ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE);
        int shadowColor = isDark ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0");
        
        android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable();
        shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
        android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable();
        surface.setColor(surfaceColor); surface.setCornerRadius(radius);
        if (!isChecked) surface.setStroke((int)(1.5f*d), isDark ? android.graphics.Color.parseColor("#333333") : android.graphics.Color.parseColor("#E0E0E0"));
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
        int offset = isChecked ? (int)(1f * d) : (int)(3f * d); // আনচেক থাকলে ভেসে থাকবে, চেক করলে ডেবে যাবে
        ld.setLayerInset(0, 0, offset, 0, 0);
        ld.setLayerInset(1, 0, 0, 0, offset);
        tv.setBackground(ld);
        
        if(isChecked) { tv.setText(status.equals("yes") ? "✓" : "🌸"); tv.setTextColor(android.graphics.Color.WHITE); } 
        else { tv.setText(""); }
        
        // ম্যাজিক প্যাডিং: টিককে ১০০% মাঝখানে রাখার সূত্র
        tv.setPadding(0, 0, 0, offset); 
        return tv;
    }"""
        ui_code = remove_method(ui_code, "public android.view.View getPremiumCheckbox")
        last_brace = ui_code.rfind('}')
        ui_code = ui_code[:last_brace] + new_checkbox + "\n" + ui_code[last_brace:]
        with open(ui_file, 'w', encoding='utf-8') as f: f.write(ui_code)

    # --- ২. MainActivity.java (লেআউট ফিক্স ও সেফ ৩ডি ইঞ্জিন) ---
    if main_file:
        with open(main_file, 'r', encoding='utf-8') as f: code = f.read()

        # পুরনো সমস্ত ইঞ্জিন মুছে ফেলা
        code = remove_method(code, "public android.graphics.drawable.Drawable getSolid3DDrawable")
        code = remove_method(code, "public android.graphics.drawable.Drawable getCarvedDrawable")
        code = remove_method(code, "public android.graphics.drawable.Drawable getCustom3DDrawable")
        code = remove_method(code, "public android.graphics.drawable.Drawable getFlawless3DDrawable")

        # একদম নতুন এবং সুরক্ষিত ইঞ্জিন (যা ডানে-বামে সরাবে না)
        safe_engine = """public android.graphics.drawable.Drawable getFlawless3DDrawable(int surfaceColor, int shadowColor, float radius, float shadowSizeDp) {
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable();
        shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
        android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable();
        surface.setColor(surfaceColor); surface.setCornerRadius(radius);
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
        int offset = (int)(shadowSizeDp * d);
        ld.setLayerInset(0, 0, offset, 0, 0); // ছায়া নিচে
        ld.setLayerInset(1, 0, 0, 0, offset); // সারফেস উপরে
        return ld;
    }"""
        last_brace = code.rfind('}')
        code = code[:last_brace] + safe_engine + "\n" + code[last_brace:]

        # পুরনো সমস্ত ভুল প্যাডিং এবং ব্যাকগ্রাউন্ড মুছে ফেলা
        targets = ["themeToggleBtn", "offBtn", "periodBtn", "settingsBtn", "streakBadge", "iconTxt", "t", "sunnahBtn", "pCard", "card", "markAllBtn", "todayBtn"]
        for t in targets:
            code = re.sub(rf'{t}\.setBackground\(get[A-Za-z0-9]+3DDrawable.*?\);\s*', '', code)
            code = re.sub(rf'{t}\.setBackground\(getCarvedDrawable.*?\);\s*', '', code)
            code = re.sub(rf'{t}\.setPadding\(.*?\);\s*', '', code)
            code = re.sub(rf'{t}\.setGravity\(.*?\);\s*', '', code)
            code = re.sub(rf'{t}\.setIncludeFontPadding\(.*?\);\s*', '', code)

        # নতুন করে সঠিক মাপের প্যাডিং ও ব্যাকগ্রাউন্ড ইনজেক্ট করা
        injections = {
            "rightHeader.addView(themeToggleBtn);": 
                "themeToggleBtn.setBackground(getFlawless3DDrawable(isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor(\"#0A0A0C\") : android.graphics.Color.parseColor(\"#cbd5e0\"), 100f, 2f)); themeToggleBtn.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(10*DENSITY));\n        rightHeader.addView(themeToggleBtn);",
            "rightHeader.addView(offBtn);": 
                "offBtn.setBackground(getFlawless3DDrawable(isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor(\"#0A0A0C\") : android.graphics.Color.parseColor(\"#cbd5e0\"), 100f, 2f)); offBtn.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(10*DENSITY));\n        rightHeader.addView(offBtn);",
            "rightHeader.addView(periodBtn);": 
                "periodBtn.setBackground(getFlawless3DDrawable(isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor(\"#0A0A0C\") : android.graphics.Color.parseColor(\"#cbd5e0\"), 100f, 2f)); periodBtn.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(10*DENSITY));\n        rightHeader.addView(periodBtn);",
            "rightHeader.addView(settingsBtn);": 
                "settingsBtn.setBackground(getFlawless3DDrawable(isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor(\"#0A0A0C\") : android.graphics.Color.parseColor(\"#cbd5e0\"), 100f, 2f)); settingsBtn.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(10*DENSITY));\n        rightHeader.addView(settingsBtn);",
            "leftHeader.addView(streakBadge);": 
                "streakBadge.setBackground(getFlawless3DDrawable(isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor(\"#0A0A0C\") : android.graphics.Color.parseColor(\"#cbd5e0\"), 20f*DENSITY, 3f)); streakBadge.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(9*DENSITY));\n        leftHeader.addView(streakBadge);",
            "iconTxt.setText(prayerIcons[i]);": 
                "iconTxt.setText(prayerIcons[i]);\n        iconTxt.setBackground(getFlawless3DDrawable(isDarkTheme ? android.graphics.Color.parseColor(\"#2C2C2E\") : android.graphics.Color.parseColor(\"#F5F7FA\"), isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#cbd5e0\"), 100f, 2f)); iconTxt.setPadding((int)(10*DENSITY), (int)(6*DENSITY), (int)(10*DENSITY), (int)(8*DENSITY));",
            "t.setText(dayNames[i]);": 
                "t.setText(dayNames[i]);\n        t.setBackground(getFlawless3DDrawable(isSel ? colorAccent : themeColors[1], isSel ? android.graphics.Color.parseColor(\"#0A0A0C\") : themeColors[4], 8f * DENSITY, isSel ? 1f : 3f)); t.setPadding(0, 0, 0, isSel ? (int)(1*DENSITY) : (int)(3*DENSITY));",
            "sunnahBtn.setText(sunnahStr);": 
                "sunnahBtn.setText(sunnahStr);\n        sunnahBtn.setBackground(getFlawless3DDrawable(doneSunnahs > 0 ? colorAccent : themeColors[1], themeColors[4], 10f*DENSITY, 2f)); sunnahBtn.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY));",
            "rootLayout.addView(pCard);": 
                "int pShadow = isDayTime ? android.graphics.Color.parseColor(\"#C77600\") : android.graphics.Color.parseColor(\"#0A0A0C\");\n        pCard.setBackground(getFlawless3DDrawable(pMainColor, pShadow, 16f*DENSITY, 6f)); pCard.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(26*DENSITY));\n        rootLayout.addView(pCard);",
            "markAllBtn.setOnClickListener": 
                "markAllBtn.setBackground(getFlawless3DDrawable(themeColors[1], themeColors[4], 12f*DENSITY, 4f)); markAllBtn.setPadding(0, (int)(12*DENSITY), 0, (int)(16*DENSITY));\n        markAllBtn.setOnClickListener",
            "todayBtn.setOnClickListener": 
                "todayBtn.setBackground(getFlawless3DDrawable(themeColors[1], themeColors[4], 12f*DENSITY, 4f)); todayBtn.setPadding(0, (int)(12*DENSITY), 0, (int)(16*DENSITY));\n        todayBtn.setOnClickListener",
            "card.addView(leftContent);": 
                "int cColor = stat.equals(\"excused\") ? (isDarkTheme ? android.graphics.Color.parseColor(\"#1A1115\") : android.graphics.Color.parseColor(\"#FCE4EC\")) : themeColors[1];\n        int cShadow = isDarkTheme ? android.graphics.Color.parseColor(\"#0A0A0C\") : android.graphics.Color.parseColor(\"#cbd5e0\");\n        card.setBackground(getFlawless3DDrawable(cColor, cShadow, 14f*DENSITY, 6f)); card.setPadding((int)(15*DENSITY), (int)(cardPadV*DENSITY), (int)(20*DENSITY), (int)((cardPadV+6)*DENSITY));\n        card.addView(leftContent);"
        }
        
        for k, v in injections.items(): code = code.replace(k, v)
        with open(main_file, 'w', encoding='utf-8') as f: f.write(code)

if __name__ == '__main__':
    ultimate_savior()
    