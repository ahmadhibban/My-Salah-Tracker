import os
import re

def upgrade_to_premium_marble():
    main_file = None
    ui_file = None
    for root, _, files in os.walk("."):
        if "MainActivity.java" in files: main_file = os.path.join(root, "MainActivity.java")
        if "UIComponents.java" in files: ui_file = os.path.join(root, "UIComponents.java")

    # --- ১. MainActivity.java আপডেট (শেপ, প্যাডিং এবং খোদাই করা বাটন) ---
    if main_file:
        with open(main_file, 'r', encoding='utf-8') as f:
            code = f.read()

        # নতুন ইঞ্জিন: খোদাই করা (Carved/Inset) শ্যাডো তৈরি করবে
        carved_engine = """// === INSET/CARVED 3D ENGINE ===
    public android.graphics.drawable.Drawable getCarvedDrawable(int bgColor, float radius, boolean isDark) {
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.GradientDrawable base = new android.graphics.drawable.GradientDrawable();
        base.setColor(bgColor);
        base.setCornerRadius(radius);
        
        android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable();
        shadow.setColor(android.graphics.Color.TRANSPARENT);
        // ডার্ক এবং লাইট মোডের জন্য পারফেক্ট খোদাই করা বর্ডার
        shadow.setStroke((int)(1.5f * d), isDark ? android.graphics.Color.parseColor("#4D000000") : android.graphics.Color.parseColor("#1A000000"));
        shadow.setCornerRadius(radius);
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{base, shadow});
        // শ্যাডোকে ওপরে এবং বামে সরানো হলো, যাতে মনে হয় বাটনটি ভেতরের দিকে ডেবে আছে
        ld.setLayerInset(1, 0, 0, (int)(2f * d), (int)(2f * d)); 
        return ld;
    }"""
        if "getCarvedDrawable" not in code:
            code = re.sub(r'(public android\.graphics\.drawable\.Drawable getSolid3DDrawable)', carved_engine + r'\n\n    \1', code)

        # ১. কর্নার রেডিয়াস কমানো (ক্যাপসুল থেকে মার্বেল ব্লক শেপ)
        code = code.replace("16f * DENSITY", "12f * DENSITY")
        code = code.replace("20f * DENSITY", "14f * DENSITY")
        
        # ২. কার্ডের ভেতরে শ্বাস নেওয়ার জায়গা (Vertical Padding) বাড়ানো
        code = re.sub(r'card\.setPadding\(\(int\)\(15\*DENSITY\), \(int\)\(cardPadV\*DENSITY\), \(int\)\(20\*DENSITY\), \(int\)\(\(cardPadV\+4\)\*DENSITY\)\);',
                      r'card.setPadding((int)(20*DENSITY), (int)((cardPadV+8)*DENSITY), (int)(20*DENSITY), (int)((cardPadV+12)*DENSITY));', code)

        # ৩. সুন্নাহ বাটনকে ফ্ল্যাট থেকে "খোদাই করা" (Carved) বানানো
        old_sunnah = r'GradientDrawable customSunnahBg = new GradientDrawable\(\);.*?sunnahBtn\.setBackground\(customSunnahBg\);'
        premium_sunnah = """int sBgColor = doneSunnahs > 0 ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#121212") : android.graphics.Color.parseColor("#F5F7FA"));
                sunnahBtn.setTextColor(doneSunnahs > 0 ? android.graphics.Color.WHITE : themeColors[2]);
                // এখানে নতুন Carved ইঞ্জিন ব্যবহার করা হলো
                sunnahBtn.setBackground(getCarvedDrawable(sBgColor, 8f*DENSITY, isDarkTheme));
                // বাটনের ভেতরের স্পেসিং বাড়ানো হলো
                sunnahBtn.setPadding((int)(16*DENSITY), (int)(8*DENSITY), (int)(16*DENSITY), (int)(8*DENSITY));"""
        code = re.sub(old_sunnah, premium_sunnah, code, flags=re.DOTALL)

        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(code)
        print("✔ MainActivity Upgraded: Marble blocks, generous padding, and carved buttons applied!")

    # --- ২. UIComponents.java আপডেট (টিক বক্স প্রিমিয়াম করা) ---
    if ui_file:
        with open(ui_file, 'r', encoding='utf-8') as f:
            ui_code = f.read()
        
        # ৪. চেক বক্স: আনচেকড থাকলে গর্তের মতো (Carved) দেখাবে, চেক করলে থ্রিডি পপ-আউট হবে
        premium_checkbox = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) { 
        android.widget.TextView tv = new android.widget.TextView(activity);
        tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14); tv.setIncludeFontPadding(false); tv.setPadding(0,0,0,0);
        float d = activity.getResources().getDisplayMetrics().density;
        // সাইজ সামান্য বড় করা হলো
        android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(28*d), (int)(28*d)); 
        tv.setLayoutParams(lp); 
        
        android.content.SharedPreferences sp = activity.getSharedPreferences("salah_pro_final", android.content.Context.MODE_PRIVATE);
        boolean systemDark = (activity.getResources().getConfiguration().uiMode & android.content.res.Configuration.UI_MODE_NIGHT_MASK) == android.content.res.Configuration.UI_MODE_NIGHT_YES;
        boolean isDark = sp.getBoolean("is_dark_mode", systemDark);

        if(status.equals("yes") || status.equals("excused")) { 
            // চেক করা থাকলে সলিড ৩ডি
            android.graphics.drawable.GradientDrawable base = new android.graphics.drawable.GradientDrawable();
            base.setColor(activeColorHex); base.setShape(android.graphics.drawable.GradientDrawable.OVAL);
            android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable();
            shadow.setColor(isDark ? android.graphics.Color.parseColor("#4D000000") : android.graphics.Color.parseColor("#1A000000")); shadow.setShape(android.graphics.drawable.GradientDrawable.OVAL);
            android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, base});
            ld.setLayerInset(1, 0, 0, (int)(1.5f*d), (int)(1.5f*d)); 
            tv.setBackground(ld);
            tv.setText(status.equals("yes") ? "✓" : "🌸"); 
            tv.setTextColor(android.graphics.Color.WHITE); 
        } else { 
            // আনচেকড থাকলে খোদাই করা (Carved)
            int bgColor = isDark ? android.graphics.Color.parseColor("#121212") : android.graphics.Color.parseColor("#F5F7FA");
            android.graphics.drawable.GradientDrawable base = new android.graphics.drawable.GradientDrawable();
            base.setColor(bgColor); base.setShape(android.graphics.drawable.GradientDrawable.OVAL);
            android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable();
            shadow.setColor(android.graphics.Color.TRANSPARENT); shadow.setStroke((int)(1.5f*d), isDark ? android.graphics.Color.parseColor("#4D000000") : android.graphics.Color.parseColor("#1A000000")); shadow.setShape(android.graphics.drawable.GradientDrawable.OVAL);
            android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{base, shadow});
            ld.setLayerInset(1, 0, 0, (int)(1.5f*d), (int)(1.5f*d)); 
            tv.setBackground(ld);
            tv.setText(""); 
        } 
        return tv;
    }"""
        ui_code = re.sub(r'public android\.view\.View getPremiumCheckbox.*?return (?:chk|tv);\n    \}', premium_checkbox, ui_code, flags=re.DOTALL)
        
        with open(ui_file, 'w', encoding='utf-8') as f:
            f.write(ui_code)
        print("✔ UIComponents Upgraded: Beautiful carved checkboxes applied!")

upgrade_to_premium_marble()
