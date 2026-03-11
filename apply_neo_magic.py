import os, re

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"

for r, d, f in os.walk("."):
    if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")
    if "UIComponents.java" in f: uf = os.path.join(r, "UIComponents.java")

with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

# পুরনো যেকোনো 3D ইঞ্জিন নিরাপদভাবে মুছে ফেলার লজিক
def remove_method(code, m_name):
    while True:
        idx = code.find(m_name)
        if idx == -1: break
        start = code.rfind("public android.graphics.drawable.Drawable", 0, idx)
        if start == -1: start = code.rfind("public", 0, idx)
        if start == -1: start = code.rfind("private", 0, idx)
        if start == -1: break
        brace_start = code.find("{", idx)
        if brace_start == -1: break
        count = 1; end = -1
        for i in range(brace_start + 1, len(code)):
            if code[i] == "{": count += 1
            elif code[i] == "}":
                count -= 1
                if count == 0: end = i + 1; break
        if end != -1: code = code[:start] + code[end:]
        else: break
    return code

mc = remove_method(mc, "Drawable getPremium3D")
mc = remove_method(mc, "Drawable getSafe3D")
mc = remove_method(mc, "Drawable getExplicit3D")
mc = remove_method(mc, "Drawable getAccent3D")
mc = remove_method(mc, "Drawable getCarvedInner")
mc = remove_method(mc, "NeumorphShapeDrawable createNeo")

# আসল Neumorphism ম্যাজিক ইঞ্জিন
neo_engine = """
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
public android.graphics.drawable.Drawable getPremium3D(int surfaceColor, float radius, float depthDp, boolean isDark, int accentColor) {
    int rX = android.graphics.Color.red(accentColor); int gX = android.graphics.Color.green(accentColor); int bX = android.graphics.Color.blue(accentColor);
    int darkShadow = isDark ? android.graphics.Color.rgb((int)(rX*0.25f), (int)(gX*0.25f), (int)(bX*0.25f)) : android.graphics.Color.rgb((int)(rX*0.65f), (int)(gX*0.65f), (int)(bX*0.65f));
    int lightShadow = isDark ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.WHITE;
    return createNeo(surfaceColor, lightShadow, darkShadow, radius, depthDp, 0);
}
"""

mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n    " + neo_engine)

# Neumorphism লাইব্রেরি নিজে থেকেই শ্যাডোর জন্য জায়গা (Padding) নিয়ে নেয়, তাই ডাবল প্যাডিং রিমুভ করা হলো
mc = re.sub(r'(\.setBackground\([^)]+3D[^)]+\)\s*;)\s*[a-zA-Z0-9_]+\.setPadding\([^;]+\);', r'\1', mc)

with open(mf, 'w', encoding='utf-8') as f: f.write(mc)

# চেকবক্সকে (UIComponents) সফট থ্রিডিতে কনভার্ট করা (চেক করলে ডেবে যাবে!)
if os.path.exists(uf):
    with open(uf, 'r', encoding='utf-8') as f: uc = f.read()
    chk = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) {
        android.widget.TextView tv = new android.widget.TextView(activity); tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14);
        float d = activity.getResources().getDisplayMetrics().density;
        android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(40*d), (int)(40*d)); tv.setLayoutParams(lp);
        boolean dk = activity.getSharedPreferences("salah_pro_final", 0).getBoolean("is_dark_mode", false);
        boolean isChk = status.equals("yes") || status.equals("excused");
        
        int rX = android.graphics.Color.red(activeColorHex); int gX = android.graphics.Color.green(activeColorHex); int bX = android.graphics.Color.blue(activeColorHex);
        int darkShadow = dk ? android.graphics.Color.rgb((int)(rX*0.25f), (int)(gX*0.25f), (int)(bX*0.25f)) : android.graphics.Color.rgb((int)(rX*0.65f), (int)(gX*0.65f), (int)(bX*0.65f));
        int lightShadow = dk ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.WHITE;
        
        soup.neumorphism.NeumorphShapeAppearanceModel model = new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 8f*d).build();
        soup.neumorphism.NeumorphShapeDrawable nd = new soup.neumorphism.NeumorphShapeDrawable(activity);
        nd.setShapeAppearanceModel(model); nd.setShadowElevation(4f * d);
        nd.setShadowColorLight(lightShadow); nd.setShadowColorDark(darkShadow);
        
        if(isChk) { nd.setShapeType(1); nd.setFillColor(android.content.res.ColorStateList.valueOf(activeColorHex)); tv.setText(status.equals("yes")?"✓":"🌸"); tv.setTextColor(android.graphics.Color.WHITE); } 
        else { nd.setShapeType(0); nd.setFillColor(android.content.res.ColorStateList.valueOf(dk ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#F5F7FA"))); tv.setText(""); }
        tv.setBackground(nd); return tv;
    }"""
    uc = re.sub(r'public android\.view\.View getPremiumCheckbox.*?return tv;\n    \}', chk, uc, flags=re.DOTALL)
    with open(uf, 'w', encoding='utf-8') as f: f.write(uc)

print("✔ FINAL NEUMORPHISM MAGIC APPLIED PERFECTLY! 🚀")
