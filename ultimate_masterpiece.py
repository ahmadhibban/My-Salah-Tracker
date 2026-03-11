import os
import re

def create_ultimate_masterpiece():
    main_file = None
    ui_file = None
    for root, _, files in os.walk("."):
        if "MainActivity.java" in files: main_file = os.path.join(root, "MainActivity.java")
        if "UIComponents.java" in files: ui_file = os.path.join(root, "UIComponents.java")

    # --- ১. MainActivity.java ফিক্স ---
    if main_file:
        with open(main_file, 'r', encoding='utf-8') as f: code = f.read()

        # নতুন Carved Engine: এটি আর বর্ডারকে বাঁকা করবে না। চারপাশে সমান সুন্দর খোদাই ইফেক্ট দেবে।
        new_carved_engine = """// === INSET/CARVED 3D ENGINE ===
    public android.graphics.drawable.Drawable getCarvedDrawable(int bgColor, float radius, boolean isDark) {
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
        gd.setColor(bgColor);
        gd.setCornerRadius(radius);
        // চারদিকে সমান বর্ডার, ফলে গোল শেপ আর বাঁকা হবে না
        int strokeCol = isDark ? android.graphics.Color.parseColor("#4D000000") : android.graphics.Color.parseColor("#1A000000");
        gd.setStroke((int)(1.5f * d), strokeCol);
        return gd;
    }"""
        code = re.sub(r'// === INSET/CARVED 3D ENGINE ===.*?return ld;\n    \}', new_carved_engine, code, flags=re.DOTALL)

        # উপরের ৩টি আইকনের ফিক্স: বাঁকা বর্ডার বাতিল, প্যাডিং দিয়ে আইকন ছোট করা
        code = re.sub(r'themeToggleBtn\.setBackground\(.*?\);.*?themeToggleBtn\.setGravity\(android\.view\.Gravity\.CENTER\);', 
                      'themeToggleBtn.setBackground(getCarvedDrawable(isDarkTheme ? android.graphics.Color.parseColor("#121212") : android.graphics.Color.WHITE, 100f, isDarkTheme)); themeToggleBtn.setPadding((int)(8*DENSITY),(int)(8*DENSITY),(int)(8*DENSITY),(int)(8*DENSITY));', code, flags=re.DOTALL)
                      
        code = re.sub(r'offBtn\.setBackground\(.*?\);.*?offBtn\.setGravity\(android\.view\.Gravity\.CENTER\);', 
                      'offBtn.setBackground(getCarvedDrawable(isDarkTheme ? android.graphics.Color.parseColor("#121212") : android.graphics.Color.WHITE, 100f, isDarkTheme)); offBtn.setPadding((int)(8*DENSITY),(int)(8*DENSITY),(int)(8*DENSITY),(int)(8*DENSITY));', code, flags=re.DOTALL)

        code = re.sub(r'periodBtn\.setBackground\(.*?\);.*?periodBtn\.setGravity\(android\.view\.Gravity\.CENTER\);', 
                      'periodBtn.setBackground(getCarvedDrawable(isDarkTheme ? android.graphics.Color.parseColor("#121212") : android.graphics.Color.WHITE, 100f, isDarkTheme)); periodBtn.setPadding((int)(8*DENSITY),(int)(8*DENSITY),(int)(8*DENSITY),(int)(8*DENSITY));', code, flags=re.DOTALL)
        
        code = re.sub(r'settingsBtn\.setBackground\(.*?\);.*?settingsBtn\.setGravity\(android\.view\.Gravity\.CENTER\);', 
                      'settingsBtn.setBackground(getCarvedDrawable(isDarkTheme ? android.graphics.Color.parseColor("#121212") : android.graphics.Color.WHITE, 100f, isDarkTheme)); settingsBtn.setPadding((int)(8*DENSITY),(int)(8*DENSITY),(int)(8*DENSITY),(int)(8*DENSITY));', code, flags=re.DOTALL)

        # স্ট্রিক পিল ফিক্স: ডার্ক মোডে সুন্দর দেখানোর জন্য খোদাই করা স্টাইল ও অ্যাকসেন্ট কালার টেক্সট
        code = re.sub(r'streakBadge\.setBackground\(getSolid3DDrawable.*?\);', 
                      'streakBadge.setBackground(getCarvedDrawable(isDarkTheme ? android.graphics.Color.parseColor("#121212") : android.graphics.Color.parseColor("#F5F7FA"), 20f*DENSITY, isDarkTheme)); streakBadge.setTextColor(colorAccent);', code)

        # নামাজের আইকন ফিক্স: আইকনের পেছনে একটি সুন্দর খোদাই করা গোল বৃত্ত যুক্ত করা হলো
        if "iconTxt.setBackground(getCarvedDrawable" not in code:
            code = re.sub(r'(iconTxt\.setTextSize\(22f\);)', 
                          r'\1 iconTxt.setBackground(getCarvedDrawable(isDarkTheme ? android.graphics.Color.parseColor("#151515") : android.graphics.Color.parseColor("#F5F7FA"), 100f, isDarkTheme)); iconTxt.setPadding((int)(12*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY));', code)

        with open(main_file, 'w', encoding='utf-8') as f: f.write(code)
        print("✔ MainActivity Perfected: Symmetrical icons, beautiful streak, and carved prayer icons!")

    # --- ২. UIComponents.java ফিক্স (টিক বক্স) ---
    if ui_file:
        with open(ui_file, 'r', encoding='utf-8') as f: ui_code = f.read()
        
        # নতুন প্রিমিয়াম টিক বক্স: গোল থেকে "রাউন্ডেড স্কয়ার" করা হলো এবং টেক্সট শিফটিং ফিক্স করা হলো
        new_checkbox = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) { 
        android.widget.TextView tv = new android.widget.TextView(activity);
        tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14); tv.setIncludeFontPadding(false); 
        float d = activity.getResources().getDisplayMetrics().density;
        android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(28*d), (int)(28*d)); 
        tv.setLayoutParams(lp); 
        
        android.content.SharedPreferences sp = activity.getSharedPreferences("salah_pro_final", android.content.Context.MODE_PRIVATE);
        boolean systemDark = (activity.getResources().getConfiguration().uiMode & android.content.res.Configuration.UI_MODE_NIGHT_MASK) == android.content.res.Configuration.UI_MODE_NIGHT_YES;
        boolean isDark = sp.getBoolean("is_dark_mode", systemDark);
        
        float rad = 8f * d; // গোল এর বদলে রাউন্ডেড স্কয়ার (Squircle) - অনেক বেশি প্রিমিয়াম

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
            // টিক চিহ্ন একপাশে সরে যাওয়ার ফিক্স: ক্যানভাস যতটুকু সরেছে, প্যাডিং দিয়ে ততটুকু ব্যালেন্স করা হলো
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
        ui_code = re.sub(r'public android\.view\.View getPremiumCheckbox.*?return (?:chk|tv);\n    \}', new_checkbox, ui_code, flags=re.DOTALL)
        
        with open(ui_file, 'w', encoding='utf-8') as f: f.write(ui_code)
        print("✔ UIComponents Perfected: Squircle checkboxes and perfectly centered ticks!")

create_ultimate_masterpiece()
