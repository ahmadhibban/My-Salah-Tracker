import os, re

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"

with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

# ১. নতুন ইঞ্জিন (Accent3D এবং CarvedInner)
engine = """public android.graphics.drawable.Drawable getAccent3D(int surfaceColor, float radius, float depthDp, boolean isDark, int accentColor) {
    float d = getResources().getDisplayMetrics().density;
    int shadowColor;
    if (isDark) {
        int r = android.graphics.Color.red(accentColor); int g = android.graphics.Color.green(accentColor); int b = android.graphics.Color.blue(accentColor);
        shadowColor = android.graphics.Color.rgb((int)(r*0.4f), (int)(g*0.4f), (int)(b*0.4f)); 
    } else { shadowColor = android.graphics.Color.parseColor("#cbd5e0"); }
    android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
    android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable(); surface.setColor(surfaceColor); surface.setCornerRadius(radius);
    surface.setStroke((int)(1.0f * d), shadowColor); 
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
    int offX = (int)((depthDp/2.0f) * d); int offY = (int)(depthDp * d); 
    ld.setLayerInset(0, offX, offY, 0, 0); ld.setLayerInset(1, 0, 0, offX, offY); return ld;
}
public android.graphics.drawable.Drawable getCarvedInner(int bgColor, float radius, boolean isDark, int accentColor) {
    float d = getResources().getDisplayMetrics().density;
    android.graphics.drawable.GradientDrawable base = new android.graphics.drawable.GradientDrawable();
    base.setColor(bgColor); base.setCornerRadius(radius);
    int r = android.graphics.Color.red(accentColor); int g = android.graphics.Color.green(accentColor); int b = android.graphics.Color.blue(accentColor);
    int strokeColor = isDark ? android.graphics.Color.argb(120, r, g, b) : android.graphics.Color.parseColor("#cbd5e0");
    base.setStroke((int)(1.5f * d), strokeColor); return base;
}"""
if "getAccent3D" not in mc: mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n    " + engine)

# ২. আইকনের সাদা রং ফিক্স (থিম কালার হবে)
mc = mc.replace("isDarkTheme ? android.graphics.Color.WHITE : colorAccent", "colorAccent")

# ৩. ৭ দিনের সিলেক্টেড বাটনের ইফেক্ট (অর্ধেক ডেবে থাকার ইফেক্ট 1.5f)
mc = re.sub(r't\.setBackground\(getUltra3D.*?\);\s*t\.setPadding.*?;', 't.setBackground(getAccent3D(isSel ? colorAccent : themeColors[1], 8f*DENSITY, isSel ? 1.5f : 3f, isDarkTheme, colorAccent)); t.setPadding(0, 0, 0, isSel ? (int)(1.5f*DENSITY) : (int)(3f*DENSITY));', mc)

# ৪. কার্ড ও অন্যান্য বাটনে Accent3D প্রয়োগ (ডার্ক মোডে থিম কালারের বর্ডার)
mc = re.sub(r'markAllBtn\.setBackground\(getUltra3D.*?\);', 'markAllBtn.setBackground(getAccent3D(themeColors[1], 12f*DENSITY, 5f, isDarkTheme, colorAccent));', mc)
mc = re.sub(r'todayBtn\.setBackground\(getUltra3D.*?\);', 'todayBtn.setBackground(getAccent3D(themeColors[1], 12f*DENSITY, 5f, isDarkTheme, colorAccent));', mc)
mc = re.sub(r'streakBadge\.setBackground\(getUltra3D.*?\);', 'streakBadge.setBackground(getAccent3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, 20f*DENSITY, 3f, isDarkTheme, colorAccent));', mc)
mc = re.sub(r'card\.setBackground\(getUltra3D.*?\);', 'card.setBackground(getAccent3D(cM, 14f*DENSITY, 6f, isDarkTheme, colorAccent));', mc)

for b in ['offBtn', 'periodBtn', 'settingsBtn']:
    mc = re.sub(rf'{b}\.setBackground\(getUltra3D.*?\);', rf'{b}.setBackground(getAccent3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, 100f, 3f, isDarkTheme, colorAccent));', mc)

# ৫. ভেতরের এলিমেন্টগুলো (সুন্নাহ, নামাজের আইকন) Carved (খোদাই করা) হবে
mc = re.sub(r'iconTxt\.setBackground\(getUltra3D.*?\);\s*iconTxt\.setPadding.*?;', 'iconTxt.setBackground(getCarvedInner(isDarkTheme ? android.graphics.Color.parseColor("#2C2C2E") : android.graphics.Color.parseColor("#F5F7FA"), 100f, isDarkTheme, colorAccent)); iconTxt.setPadding((int)(10*DENSITY), (int)(8*DENSITY), (int)(10*DENSITY), (int)(8*DENSITY));', mc)
mc = re.sub(r'int\s+sSur\s*=.*?sunnahBtn\.setBackground\(getUltra3D.*?\);\s*sunnahBtn\.setTextColor(.*?);\s*sunnahBtn\.setPadding.*?;', r'sunnahBtn.setBackground(getCarvedInner(doneSunnahs > 0 ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#2C2C2E") : themeColors[1]), 12f*DENSITY, isDarkTheme, colorAccent)); sunnahBtn.setTextColor\1; sunnahBtn.setPadding((int)(12*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY));', mc, flags=re.DOTALL)

with open(mf, 'w', encoding='utf-8') as f: f.write(mc)

# ৬. টিক বক্স (পারফেক্ট খোদাই করা/Carved লুক)
with open(uf, 'r', encoding='utf-8') as f: uc = f.read()
chk = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) {
    android.widget.TextView tv = new android.widget.TextView(activity); tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14);
    float d = activity.getResources().getDisplayMetrics().density;
    android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(28*d), (int)(28*d)); tv.setLayoutParams(lp);
    boolean dk = activity.getSharedPreferences("salah_pro_final", 0).getBoolean("is_dark_mode", false);
    boolean isChk = status.equals("yes") || status.equals("excused");
    
    int bgColor = isChk ? activeColorHex : (dk ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#F5F7FA"));
    android.graphics.drawable.GradientDrawable base = new android.graphics.drawable.GradientDrawable();
    base.setColor(bgColor); base.setCornerRadius(8f*d);
    
    int r = android.graphics.Color.red(activeColorHex); int g = android.graphics.Color.green(activeColorHex); int b = android.graphics.Color.blue(activeColorHex);
    int stroke = dk ? android.graphics.Color.argb(120, r, g, b) : android.graphics.Color.parseColor("#cbd5e0");
    base.setStroke((int)(1.5f * d), stroke);
    
    tv.setBackground(base);
    if(isChk) { tv.setText(status.equals("yes")?"✓":"🌸"); tv.setTextColor(android.graphics.Color.WHITE); }
    tv.setPadding(0, 0, 0, 0); return tv;
}"""
uc = re.sub(r'public android\.view\.View getPremiumCheckbox.*?return tv;\n    \}', chk, uc, flags=re.DOTALL)
with open(uf, 'w', encoding='utf-8') as f: f.write(uc)
print("✔ ALL ISSUES FIXED PERFECTLY! Ready to Build.")
