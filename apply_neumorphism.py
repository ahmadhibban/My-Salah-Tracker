import os, re

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"
for r, d, f in os.walk("."):
    if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")
    if "UIComponents.java" in f: uf = os.path.join(r, "UIComponents.java")

with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

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

mc = remove_method(mc, "Drawable getExplicit3D")
mc = remove_method(mc, "Drawable getAccent3D")
mc = remove_method(mc, "Drawable getCarvedInner")
mc = remove_method(mc, "NeumorphShapeDrawable createNeo")

new_engines = """private soup.neumorphism.NeumorphShapeDrawable createNeo(int bgColor, int lightColor, int darkColor, float radius, float elevation, int type) {
    soup.neumorphism.NeumorphShapeAppearanceModel model = new soup.neumorphism.NeumorphShapeAppearanceModel.Builder()
        .setAllCorners(0, radius) // 0 = ROUNDED
        .build();
    soup.neumorphism.NeumorphShapeDrawable d = new soup.neumorphism.NeumorphShapeDrawable(this);
    d.setShapeAppearanceModel(model);
    d.setShapeType(type); // 0 = FLAT (Raised), 1 = PRESSED (Carved)
    d.setShadowColorLight(lightColor);
    d.setShadowColorDark(darkColor);
    d.setShadowElevation(elevation * getResources().getDisplayMetrics().density);
    d.setFillColor(android.content.res.ColorStateList.valueOf(bgColor));
    return d;
}
public android.graphics.drawable.Drawable getExplicit3D(int surfaceColor, int shadowColor, float radius, float depthDp) {
    int lightShadow = (surfaceColor == android.graphics.Color.parseColor("#1A2980")) ? android.graphics.Color.parseColor("#293D99") : android.graphics.Color.parseColor("#FFC85C");
    return createNeo(surfaceColor, lightShadow, shadowColor, radius, depthDp, 0);
}
public android.graphics.drawable.Drawable getAccent3D(int surfaceColor, float radius, float depthDp, boolean isDark, int accentColor) {
    int r = android.graphics.Color.red(accentColor); int g = android.graphics.Color.green(accentColor); int b = android.graphics.Color.blue(accentColor);
    int darkShadow = isDark ? android.graphics.Color.rgb((int)(r*0.25f), (int)(g*0.25f), (int)(b*0.25f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
    int lightShadow = isDark ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.WHITE;
    return createNeo(surfaceColor, lightShadow, darkShadow, radius, depthDp, 0);
}
public android.graphics.drawable.Drawable getCarvedInner(int bgColor, float radius, boolean isDark, int accentColor) {
    int r = android.graphics.Color.red(accentColor); int g = android.graphics.Color.green(accentColor); int b = android.graphics.Color.blue(accentColor);
    int darkShadow = isDark ? android.graphics.Color.rgb((int)(r*0.25f), (int)(g*0.25f), (int)(b*0.25f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
    int lightShadow = isDark ? android.graphics.Color.parseColor("#3A3A3C") : android.graphics.Color.WHITE;
    return createNeo(bgColor, lightShadow, darkShadow, radius, 4f, 1); // 1 = PRESSED
}"""

mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n    " + new_engines)

# Neumorphism নিজে থেকেই Padding তৈরি করে, তাই ম্যানুয়াল Padding গুলো মুছে ফেলা হচ্ছে
mc = re.sub(r'(\.setBackground\(getExplicit3D.*?\);\s*)[a-zA-Z0-9_]+\.setPadding\([^;]+\);', r'\1', mc)
mc = re.sub(r'(\.setBackground\(getAccent3D.*?\);\s*)[a-zA-Z0-9_]+\.setPadding\([^;]+\);', r'\1', mc)
mc = re.sub(r'(\.setBackground\(getCarvedInner.*?\);\s*)[a-zA-Z0-9_]+\.setPadding\([^;]+\);', r'\1', mc)

# আইকনের ছায়া যেন কেটে না যায় তাই LayoutParams সামান্য বড় করা হলো
mc = re.sub(r'LinearLayout\.LayoutParams\(\(int\)\(34\s*\*\s*DENSITY\),\s*\(int\)\(34\s*\*\s*DENSITY\)\)', 'LinearLayout.LayoutParams((int)(44 * DENSITY), (int)(44 * DENSITY))', mc)

with open(mf, 'w', encoding='utf-8') as f: f.write(mc)

# UIComponents (চেকবক্স) আপডেট করা হচ্ছে
with open(uf, 'r', encoding='utf-8') as f: uc = f.read()
chk_engine = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) {
    android.widget.TextView tv = new android.widget.TextView(activity); tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14);
    float d = activity.getResources().getDisplayMetrics().density;
    android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(40*d), (int)(40*d)); tv.setLayoutParams(lp);
    boolean dk = activity.getSharedPreferences("salah_pro_final", 0).getBoolean("is_dark_mode", false);
    boolean isChk = status.equals("yes") || status.equals("excused");
    
    int r = android.graphics.Color.red(activeColorHex); int g = android.graphics.Color.green(activeColorHex); int b = android.graphics.Color.blue(activeColorHex);
    int darkShadow = dk ? android.graphics.Color.rgb((int)(r*0.25f), (int)(g*0.25f), (int)(b*0.25f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
    int lightShadow = dk ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.WHITE;
    
    soup.neumorphism.NeumorphShapeAppearanceModel model = new soup.neumorphism.NeumorphShapeAppearanceModel.Builder()
        .setAllCorners(0, 8f*d)
        .build();
    soup.neumorphism.NeumorphShapeDrawable nd = new soup.neumorphism.NeumorphShapeDrawable(activity);
    nd.setShapeAppearanceModel(model);
    nd.setShadowElevation(3f * d);
    nd.setShadowColorLight(lightShadow);
    nd.setShadowColorDark(darkShadow);
    
    if(isChk) {
        nd.setShapeType(1); // PRESSED (ডেবে থাকবে)
        nd.setFillColor(android.content.res.ColorStateList.valueOf(activeColorHex));
        tv.setText(status.equals("yes")?"✓":"🌸"); tv.setTextColor(android.graphics.Color.WHITE);
    } else {
        nd.setShapeType(0); // FLAT (উঁচুতে থাকবে)
        nd.setFillColor(android.content.res.ColorStateList.valueOf(dk ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#F5F7FA")));
        tv.setText("");
    }
    tv.setBackground(nd); return tv;
}"""
uc = re.sub(r'public android\.view\.View getPremiumCheckbox.*?return tv;\n    \}', chk_engine, uc, flags=re.DOTALL)
with open(uf, 'w', encoding='utf-8') as f: f.write(uc)
print("✔ NEUMORPHISM MAGIC APPLIED VIA JAVA! 🚀")
