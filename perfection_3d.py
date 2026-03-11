import os, re

def apply_perfection():
    mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
    uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"
    for r, d, f in os.walk("."):
        if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")
        if "UIComponents.java" in f: uf = os.path.join(r, "UIComponents.java")

    with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

    # ১. পুরনো ইঞ্জিন মুছে ফেলা
    mc = re.sub(r'public android\.graphics\.drawable\.Drawable getAccent3D.*?return base;\n    \}', '', mc, flags=re.DOTALL)
    
    # ২. ৩টি নতুন সুপার-পারফেক্ট ইঞ্জিন (Explicit3D, Accent3D, CarvedInner)
    new_engines = """public android.graphics.drawable.Drawable getExplicit3D(int surfaceColor, int shadowColor, float radius, float depthDp) {
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
        android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable(); surface.setColor(surfaceColor); surface.setCornerRadius(radius);
        surface.setStroke((int)(2.0f * d), shadowColor); // চতুর্দিকে মোটা বর্ডার
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
        int offY = (int)(depthDp * d); ld.setLayerInset(0, 0, offY, 0, 0); ld.setLayerInset(1, 0, 0, 0, offY); return ld;
    }
    public android.graphics.drawable.Drawable getAccent3D(int surfaceColor, float radius, float depthDp, boolean isDark, int accentColor) {
        float d = getResources().getDisplayMetrics().density;
        int r = android.graphics.Color.red(accentColor); int g = android.graphics.Color.green(accentColor); int b = android.graphics.Color.blue(accentColor);
        // হোয়াইট এবং ডার্ক উভয় মোডেই থিম কালারের বর্ডার
        int shadowColor = isDark ? android.graphics.Color.rgb((int)(r*0.35f), (int)(g*0.35f), (int)(b*0.35f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
        android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
        android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable(); surface.setColor(surfaceColor); surface.setCornerRadius(radius);
        surface.setStroke((int)(2.0f * d), shadowColor); // চতুর্দিকে মোটা বর্ডার
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
        int offY = (int)(depthDp * d); ld.setLayerInset(0, 0, offY, 0, 0); ld.setLayerInset(1, 0, 0, 0, offY); return ld;
    }
    public android.graphics.drawable.Drawable getCarvedInner(int bgColor, float radius, boolean isDark, int accentColor) {
        float d = getResources().getDisplayMetrics().density;
        int r = android.graphics.Color.red(accentColor); int g = android.graphics.Color.green(accentColor); int b = android.graphics.Color.blue(accentColor);
        int shadowColor = isDark ? android.graphics.Color.rgb((int)(r*0.35f), (int)(g*0.35f), (int)(b*0.35f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
        android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
        android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable(); surface.setColor(bgColor); surface.setCornerRadius(radius);
        surface.setStroke((int)(1.0f * d), shadowColor);
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
        int off = (int)(1.8f * d); ld.setLayerInset(1, off, off, 0, 0); // পারফেক্ট খোদাই করা (Inner Shadow) ইফেক্ট
        return ld;
    }"""
    if "getExplicit3D" not in mc: mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n    " + new_engines)

    # ৩. চাঁদ/সূর্য আইকন এবং পার্সেন্টেজ কার্ড ফিক্স (Explicit3D দিয়ে সব সময় নীল/হলুদ)
    mc = re.sub(r'themeToggleBtn\.setBackground\(getAccent3D.*?\);', 'int tSur = isDayTime ? android.graphics.Color.parseColor("#FF9500") : android.graphics.Color.parseColor("#1A2980"); int tShd = isDayTime ? android.graphics.Color.parseColor("#C77600") : android.graphics.Color.parseColor("#0F184A"); themeToggleBtn.setBackground(getExplicit3D(tSur, tShd, 100f, 3f));', mc)
    
    mc = re.sub(r'pCard\.setBackground\(getAccent3D.*?\);', 'int ptSur = isDayTime ? android.graphics.Color.parseColor("#FF9500") : android.graphics.Color.parseColor("#1A2980"); int ptShd = isDayTime ? android.graphics.Color.parseColor("#C77600") : android.graphics.Color.parseColor("#0F184A"); pCard.setBackground(getExplicit3D(ptSur, ptShd, 20f*DENSITY, 6f));', mc)

    with open(mf, 'w', encoding='utf-8') as f: f.write(mc)

    # ৪. চেকবক্স (UIComponents.java) এর খোদাই ও ৩ডি ফিক্স
    with open(uf, 'r', encoding='utf-8') as f: uc = f.read()
    chk_engine = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) {
        android.widget.TextView tv = new android.widget.TextView(activity); tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14);
        float d = activity.getResources().getDisplayMetrics().density;
        android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(28*d), (int)(28*d)); tv.setLayoutParams(lp);
        boolean dk = activity.getSharedPreferences("salah_pro_final", 0).getBoolean("is_dark_mode", false);
        boolean isChk = status.equals("yes") || status.equals("excused");
        
        int r = android.graphics.Color.red(activeColorHex); int g = android.graphics.Color.green(activeColorHex); int b = android.graphics.Color.blue(activeColorHex);
        int shadowColor = dk ? android.graphics.Color.rgb((int)(r*0.35f), (int)(g*0.35f), (int)(b*0.35f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
        
        android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(8f*d);
        android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable();
        
        android.graphics.drawable.LayerDrawable ld;
        if(isChk) {
            surface.setColor(activeColorHex); surface.setCornerRadius(8f*d);
            surface.setStroke((int)(2.0f*d), shadowColor); // চতুর্দিকে মোটা বর্ডার
            ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
            ld.setLayerInset(0, 0, (int)(2f*d), 0, 0); ld.setLayerInset(1, 0, 0, 0, (int)(2f*d));
            tv.setPadding(0, 0, 0, (int)(2f*d));
            tv.setText(status.equals("yes")?"✓":"🌸"); tv.setTextColor(android.graphics.Color.WHITE);
        } else {
            surface.setColor(dk ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#F5F7FA")); surface.setCornerRadius(8f*d);
            surface.setStroke((int)(1.0f*d), shadowColor);
            ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
            ld.setLayerInset(1, (int)(1.8f*d), (int)(1.8f*d), 0, 0); // খোদাই করা ইফেক্ট
            tv.setPadding(0, 0, 0, 0); tv.setText("");
        }
        tv.setBackground(ld); return tv;
    }"""
    uc = re.sub(r'public android\.view\.View getPremiumCheckbox.*?return tv;\n    \}', chk_engine, uc, flags=re.DOTALL)
    with open(uf, 'w', encoding='utf-8') as f: f.write(uc)
    print("✔ PERFECTION ACHIEVED! Thick borders, vivid colors, and clear carved effects applied.")

apply_perfection()
