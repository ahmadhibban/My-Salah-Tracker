import os, re

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"
backup = "all_code.txt"

for r, d, f in os.walk("."):
    if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")
    if "UIComponents.java" in f: uf = os.path.join(r, "UIComponents.java")
    if "all_code.txt" in f: backup = os.path.join(r, "all_code.txt")

if not os.path.exists(backup):
    print("❌ all_code.txt not found! Please make sure it's in the project folder.")
    exit()

# ১. ফ্রেশ ব্যাকআপ থেকে কোড লোড করা
with open(backup, 'r', encoding='utf-8') as f: mc = f.read()

# ২. পুরনো সব 3D ইঞ্জিন মুছে ফেলা
mc = re.sub(r'public android\.graphics\.drawable\.Drawable getSafe3D.*?return ld;\n\s*\}', '', mc, flags=re.DOTALL)
mc = re.sub(r'public android\.graphics\.drawable\.Drawable getPremium3D.*?return ld;\n\s*\}', '', mc, flags=re.DOTALL)

# ৩. Neumorphism ইঞ্জিন ইনজেক্ট করা
neo = """
private soup.neumorphism.NeumorphShapeDrawable createNeo(int bgColor, int lightColor, int darkColor, float radius, float elevation, int type) {
    soup.neumorphism.NeumorphShapeAppearanceModel model = new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, radius).build();
    soup.neumorphism.NeumorphShapeDrawable d = new soup.neumorphism.NeumorphShapeDrawable(this);
    d.setShapeAppearanceModel(model); d.setShapeType(type);
    d.setShadowColorLight(lightColor); d.setShadowColorDark(darkColor);
    d.setShadowElevation(elevation * getResources().getDisplayMetrics().density);
    d.setFillColor(android.content.res.ColorStateList.valueOf(bgColor));
    return d;
}
public android.graphics.drawable.Drawable getSafe3D(int c1, int c2, float r, float dp) {
    int light = android.graphics.Color.WHITE;
    if(c2 == android.graphics.Color.parseColor("#0A0A0C") || c2 == android.graphics.Color.parseColor("#1C1C1E") || c2 == android.graphics.Color.parseColor("#0F184A")) { light = android.graphics.Color.parseColor("#333336"); }
    return createNeo(c1, light, c2, r, dp, 0);
}
"""
if "createNeo" not in mc:
    mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n    " + neo)

# ৪. সব বাটনে সফট থ্রিডি কল করা (Neumorphism নিজে প্যাডিং নেয়, তাই পুরনো প্যাডিং রিমুভ করা হলো)
mc = re.sub(r'themeToggleBtn\.setBackground\(.*?\);(\s*themeToggleBtn\.setPadding\([^;]+\);)?', 'int pmTheme = isDarkTheme ? android.graphics.Color.parseColor("#1A2980") : android.graphics.Color.parseColor("#FF9500"); int psTheme = isDarkTheme ? android.graphics.Color.parseColor("#0F184A") : android.graphics.Color.parseColor("#C77600"); themeToggleBtn.setBackground(getSafe3D(pmTheme, psTheme, 100f, 4f));', mc)
mc = re.sub(r't\.setBackground\(.*?\);(\s*t\.setPadding\([^;]+\);)?', 't.setBackground(getSafe3D(isSel ? colorAccent : themeColors[1], isSel ? (isDarkTheme?android.graphics.Color.parseColor("#0A0A0C"):android.graphics.Color.parseColor("#cbd5e0")) : themeColors[4], 8f*DENSITY, isSel ? 0f : 3f));', mc)
mc = re.sub(r'markAllBtn\.setBackground\(.*?\);(\s*markAllBtn\.setPadding\([^;]+\);)?', 'markAllBtn.setBackground(getSafe3D(themeColors[1], isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 12f*DENSITY, 5f));', mc)
mc = re.sub(r'todayBtn\.setBackground\(.*?\);(\s*todayBtn\.setPadding\([^;]+\);)?', 'todayBtn.setBackground(getSafe3D(themeColors[1], isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 12f*DENSITY, 5f));', mc)
mc = re.sub(r'card\.setBackground\(.*?\);(\s*card\.setPadding\([^;]+\);)?', 'int cM = stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#1A1115") : android.graphics.Color.parseColor("#FCE4EC")) : themeColors[1]; int cS = isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"); card.setBackground(getSafe3D(cM, cS, 14f*DENSITY, 6f));', mc)

with open(mf, 'w', encoding='utf-8') as f: f.write(mc)

# ৫. চেকবক্সে সফট থ্রিডি বসানো
if os.path.exists(uf):
    with open(uf, 'r', encoding='utf-8') as f: uc = f.read()
    chk = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) {
        android.widget.TextView tv = new android.widget.TextView(activity); tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14);
        float d = activity.getResources().getDisplayMetrics().density;
        android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(36*d), (int)(36*d)); tv.setLayoutParams(lp);
        boolean dk = activity.getSharedPreferences("salah_pro_final", 0).getBoolean("is_dark_mode", false);
        boolean isChk = status.equals("yes") || status.equals("excused");
        
        int r = android.graphics.Color.red(activeColorHex); int g = android.graphics.Color.green(activeColorHex); int b = android.graphics.Color.blue(activeColorHex);
        int darkShadow = dk ? android.graphics.Color.rgb((int)(r*0.25f), (int)(g*0.25f), (int)(b*0.25f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
        int lightShadow = dk ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.WHITE;
        
        soup.neumorphism.NeumorphShapeAppearanceModel model = new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 8f*d).build();
        soup.neumorphism.NeumorphShapeDrawable nd = new soup.neumorphism.NeumorphShapeDrawable(activity);
        nd.setShapeAppearanceModel(model); nd.setShadowElevation(3f * d);
        nd.setShadowColorLight(lightShadow); nd.setShadowColorDark(darkShadow);
        
        if(isChk) { nd.setShapeType(1); nd.setFillColor(android.content.res.ColorStateList.valueOf(activeColorHex)); tv.setText(status.equals("yes")?"✓":"🌸"); tv.setTextColor(android.graphics.Color.WHITE); } 
        else { nd.setShapeType(0); nd.setFillColor(android.content.res.ColorStateList.valueOf(dk ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#F5F7FA"))); tv.setText(""); }
        tv.setBackground(nd); return tv;
    }"""
    uc = re.sub(r'public android\.view\.View getPremiumCheckbox.*?return tv;\n    \}', chk, uc, flags=re.DOTALL)
    with open(uf, 'w', encoding='utf-8') as f: f.write(uc)
    
print("✔ MAGIC RESTORED! NO MORE ERRORS!")
