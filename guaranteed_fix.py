import os
import re

# এই ফাংশনটি ব্র্যাকেট গুণে নিখুঁতভাবে পুরনো কোড রিপ্লেস করবে
def replace_method(code, method_name, new_method_code):
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
        return code[:start] + new_method_code + code[end:]
    return code

def fix_everything_guaranteed():
    main_file = None
    ui_file = None
    for root, _, files in os.walk("."):
        if "MainActivity.java" in files: main_file = os.path.join(root, "MainActivity.java")
        if "UIComponents.java" in files: ui_file = os.path.join(root, "UIComponents.java")

    # --- ১. UIComponents.java ফিক্স (Squircle চেক বক্স ও টিক এলাইনমেন্ট) ---
    if ui_file:
        with open(ui_file, 'r', encoding='utf-8') as f: ui_code = f.read()
        
        new_checkbox = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) { 
        android.widget.TextView tv = new android.widget.TextView(activity);
        tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14); tv.setIncludeFontPadding(false); 
        float d = activity.getResources().getDisplayMetrics().density;
        android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(28*d), (int)(28*d)); 
        tv.setLayoutParams(lp); 
        
        android.content.SharedPreferences sp = activity.getSharedPreferences("salah_pro_final", android.content.Context.MODE_PRIVATE);
        boolean systemDark = (activity.getResources().getConfiguration().uiMode & android.content.res.Configuration.UI_MODE_NIGHT_MASK) == android.content.res.Configuration.UI_MODE_NIGHT_YES;
        boolean isDark = sp.getBoolean("is_dark_mode", systemDark);
        
        float rad = 8f * d; // গোল এর বদলে রাউন্ডেড স্কয়ার (Squircle)

        if(status.equals("yes") || status.equals("excused")) { 
            android.graphics.drawable.GradientDrawable base = new android.graphics.drawable.GradientDrawable();
            base.setColor(activeColorHex); base.setCornerRadius(rad);
            android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable();
            shadow.setColor(isDark ? android.graphics.Color.parseColor("#4D000000") : android.graphics.Color.parseColor("#22000000")); shadow.setCornerRadius(rad);
            android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, base});
            ld.setLayerInset(1, 0, 0, (int)(2f*d), (int)(2f*d)); 
            tv.setBackground(ld);
            tv.setText(status.equals("yes") ? "✓" : "🌸"); 
            tv.setTextColor(android.graphics.Color.WHITE); 
            // টিক পারফেক্ট মাঝে আনার জন্য ম্যাথমেটিক্যাল প্যাডিং
            tv.setPadding((int)(2f*d), (int)(2f*d), 0, 0); 
        } else { 
            int bgColor = isDark ? android.graphics.Color.parseColor("#121212") : android.graphics.Color.parseColor("#F5F7FA");
            android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
            gd.setColor(bgColor); gd.setCornerRadius(rad);
            gd.setStroke((int)(1.5f*d), isDark ? android.graphics.Color.parseColor("#4D000000") : android.graphics.Color.parseColor("#1A000000"));
            tv.setBackground(gd);
            tv.setText(""); 
            tv.setPadding(0, 0, 0, 0);
        } 
        return tv;
    }"""
        ui_code = replace_method(ui_code, "public android.view.View getPremiumCheckbox", new_checkbox)
        with open(ui_file, 'w', encoding='utf-8') as f: f.write(ui_code)
        print("✔ Checkboxes upgraded to Squircles!")

    # --- ২. MainActivity.java ফিক্স ---
    if main_file:
        with open(main_file, 'r', encoding='utf-8') as f: code = f.read()

        # নতুন Carved Engine ইনজেক্ট করা হচ্ছে
        carved_engine = """public android.graphics.drawable.Drawable getCarvedDrawable(int bgColor, float radius, boolean isDark) {
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
        gd.setColor(bgColor);
        gd.setCornerRadius(radius);
        int strokeCol = isDark ? android.graphics.Color.parseColor("#4D000000") : android.graphics.Color.parseColor("#1A000000");
        gd.setStroke((int)(1.5f * d), strokeCol);
        return gd;
    }"""
        if "getCarvedDrawable" not in code:
            solid_idx = code.find("public android.graphics.drawable.Drawable getSolid3DDrawable")
            if solid_idx != -1: code = code[:solid_idx] + carved_engine + "\n\n    " + code[solid_idx:]

        # উপরের আইকনগুলোর ফিক্স (বর্ডার সোজা এবং আইকন ছোট করা)
        btns = ["themeToggleBtn", "offBtn", "periodBtn", "settingsBtn"]
        for btn in btns:
            code = re.sub(rf'{btn}\.setPadding\(.*?\);', '', code)
            code = re.sub(rf'{btn}\.setBackground\(getSolid3DDrawable.*?\);', f'{btn}.setBackground(getCarvedDrawable(isDarkTheme ? android.graphics.Color.parseColor("#121212") : android.graphics.Color.WHITE, 100f, isDarkTheme)); {btn}.setPadding((int)(8*DENSITY),(int)(8*DENSITY),(int)(8*DENSITY),(int)(8*DENSITY));', code)

        # স্ট্রিক পিল ফিক্স
        code = re.sub(r'streakBadge\.setPadding\(.*?\);', '', code)
        code = re.sub(r'streakBadge\.setBackground\(getSolid3DDrawable.*?\);', 'streakBadge.setBackground(getCarvedDrawable(isDarkTheme ? android.graphics.Color.parseColor("#121212") : android.graphics.Color.parseColor("#F5F7FA"), 20f*DENSITY, isDarkTheme)); streakBadge.setTextColor(colorAccent); streakBadge.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY));', code)

        # নামাজের আইকনে খোদাই করা ব্যাকগ্রাউন্ড
        if "iconTxt.setBackground(getCarvedDrawable" not in code:
            code = code.replace("iconTxt.setTextSize(22f);", 'iconTxt.setTextSize(22f); iconTxt.setBackground(getCarvedDrawable(isDarkTheme ? android.graphics.Color.parseColor("#151515") : android.graphics.Color.parseColor("#F5F7FA"), 100f, isDarkTheme)); iconTxt.setPadding((int)(12*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY));')

        with open(main_file, 'w', encoding='utf-8') as f: f.write(code)
        print("✔ Top Icons, Streak, and Prayer Icons fixed completely!")

fix_everything_guaranteed()
