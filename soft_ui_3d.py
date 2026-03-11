import os, re

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"
for r, d, f in os.walk("."):
    if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")
    if "UIComponents.java" in f: uf = os.path.join(r, "UIComponents.java")

with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

# পুরনো ইঞ্জিনগুলো মুছে ফেলা হচ্ছে
def remove_method(code, m_name):
    while True:
        idx = code.find(m_name)
        if idx == -1: break
        start = code.rfind("public android.graphics.drawable.Drawable", 0, idx)
        if start == -1: start = code.rfind("public", 0, idx)
        if start == -1: break
        brace_start = code.find("{", idx)
        if brace_start == -1: break
        count = 1
        end = -1
        for i in range(brace_start + 1, len(code)):
            if code[i] == "{": count += 1
            elif code[i] == "}":
                count -= 1
                if count == 0:
                    end = i + 1
                    break
        if end != -1: code = code[:start] + code[end:]
        else: break
    return code

mc = remove_method(mc, "Drawable getExplicit3D")
mc = remove_method(mc, "Drawable getAccent3D")
mc = remove_method(mc, "Drawable getCarvedInner")

# আপনার দেওয়া কোড অনুসারে নতুন Neumorphism (Soft UI) ইঞ্জিন ইনজেক্ট করা হচ্ছে
new_engines = """public android.graphics.drawable.Drawable getExplicit3D(int surfaceColor, int shadowColor, float radius, float depthDp) {
    float d = getResources().getDisplayMetrics().density;
    int highlightColor = android.graphics.Color.WHITE;
    if(surfaceColor == android.graphics.Color.parseColor("#1A2980")) highlightColor = android.graphics.Color.parseColor("#324BB0"); // ডার্ক মোডে চাঁদের জন্য হালকা আলো
    
    android.graphics.drawable.GradientDrawable highlight = new android.graphics.drawable.GradientDrawable(); highlight.setColor(highlightColor); highlight.setCornerRadius(radius);
    android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
    android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable(); surface.setColor(surfaceColor); surface.setCornerRadius(radius);
    surface.setStroke((int)(1.5f * d), shadowColor);
    
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{highlight, shadow, surface});
    int off = (int)(depthDp * d); int hOff = off/2;
    ld.setLayerInset(0, 0, 0, off, off); // ওপরের বাঁয়ে সাদা আলো (Highlight)
    ld.setLayerInset(1, off, off, 0, 0); // নিচের ডানে গাঢ় ছায়া (Shadow)
    ld.setLayerInset(2, hOff, hOff, hOff, hOff); // মাঝখানে মূল সারফেস
    return ld;
}
public android.graphics.drawable.Drawable getAccent3D(int surfaceColor, float radius, float depthDp, boolean isDark, int accentColor) {
    float d = getResources().getDisplayMetrics().density;
    int r = android.graphics.Color.red(accentColor); int g = android.graphics.Color.green(accentColor); int b = android.graphics.Color.blue(accentColor);
    int shadowColor = isDark ? android.graphics.Color.rgb((int)(r*0.35f), (int)(g*0.35f), (int)(b*0.35f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
    int highlightColor = isDark ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.WHITE;
    
    android.graphics.drawable.GradientDrawable highlight = new android.graphics.drawable.GradientDrawable(); highlight.setColor(highlightColor); highlight.setCornerRadius(radius);
    android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
    android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable(); surface.setColor(surfaceColor); surface.setCornerRadius(radius);
    surface.setStroke((int)(1.5f * d), shadowColor);
    
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{highlight, shadow, surface});
    int off = (int)(depthDp * d); int hOff = off/2;
    ld.setLayerInset(0, 0, 0, off, off);
    ld.setLayerInset(1, off, off, 0, 0);
    ld.setLayerInset(2, hOff, hOff, hOff, hOff);
    return ld;
}
public android.graphics.drawable.Drawable getCarvedInner(int bgColor, float radius, boolean isDark, int accentColor) {
    float d = getResources().getDisplayMetrics().density;
    int r = android.graphics.Color.red(accentColor); int g = android.graphics.Color.green(accentColor); int b = android.graphics.Color.blue(accentColor);
    int shadowColor = isDark ? android.graphics.Color.rgb((int)(r*0.35f), (int)(g*0.35f), (int)(b*0.35f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
    int highlightColor = isDark ? android.graphics.Color.parseColor("#3A3A3C") : android.graphics.Color.WHITE;
    
    android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
    android.graphics.drawable.GradientDrawable highlight = new android.graphics.drawable.GradientDrawable(); highlight.setColor(highlightColor); highlight.setCornerRadius(radius);
    android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable(); surface.setColor(bgColor); surface.setCornerRadius(radius);
    surface.setStroke((int)(1.0f * d), shadowColor);
    
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, highlight, surface});
    int off = (int)(2.0f * d); int hOff = off/2;
    ld.setLayerInset(0, 0, 0, off, off); // খোদাইয়ের জন্য আলো-ছায়া উল্টে দেওয়া হলো (ওপরে ছায়া)
    ld.setLayerInset(1, off, off, 0, 0); // নিচে আলো
    ld.setLayerInset(2, hOff, hOff, hOff, hOff);
    return ld;
}"""

mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n    " + new_engines)
with open(mf, 'w', encoding='utf-8') as f: f.write(mc)

# চেকবক্সে সফট ইউআই (Neumorphism) অ্যাপ্লাই করা হচ্ছে
with open(uf, 'r', encoding='utf-8') as f: uc = f.read()
chk_engine = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) {
    android.widget.TextView tv = new android.widget.TextView(activity); tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14);
    float d = activity.getResources().getDisplayMetrics().density;
    android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(28*d), (int)(28*d)); tv.setLayoutParams(lp);
    boolean dk = activity.getSharedPreferences("salah_pro_final", 0).getBoolean("is_dark_mode", false);
    boolean isChk = status.equals("yes") || status.equals("excused");
    
    int r = android.graphics.Color.red(activeColorHex); int g = android.graphics.Color.green(activeColorHex); int b = android.graphics.Color.blue(activeColorHex);
    int shadowColor = dk ? android.graphics.Color.rgb((int)(r*0.35f), (int)(g*0.35f), (int)(b*0.35f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
    int highlightColor = dk ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.WHITE;
    
    android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(8f*d);
    android.graphics.drawable.GradientDrawable highlight = new android.graphics.drawable.GradientDrawable(); highlight.setColor(highlightColor); highlight.setCornerRadius(8f*d);
    android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable();
    
    android.graphics.drawable.LayerDrawable ld;
    int off = (int)(2.0f * d); int hOff = off/2;

    if(isChk) {
        surface.setColor(activeColorHex); surface.setCornerRadius(8f*d);
        surface.setStroke((int)(1.5f*d), shadowColor);
        ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, highlight, surface});
        ld.setLayerInset(0, 0, 0, off, off); // খোদাই করা (Carved)
        ld.setLayerInset(1, off, off, 0, 0); 
        ld.setLayerInset(2, hOff, hOff, hOff, hOff);
        tv.setText(status.equals("yes")?"✓":"🌸"); tv.setTextColor(android.graphics.Color.WHITE);
    } else {
        surface.setColor(dk ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#F5F7FA")); surface.setCornerRadius(8f*d);
        surface.setStroke((int)(1.0f*d), shadowColor);
        ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{highlight, shadow, surface});
        ld.setLayerInset(0, 0, 0, off, off); // ফুলে থাকা (Raised)
        ld.setLayerInset(1, off, off, 0, 0);
        ld.setLayerInset(2, hOff, hOff, hOff, hOff);
        tv.setText("");
    }
    tv.setBackground(ld); tv.setPadding(0, 0, 0, 0); return tv;
}"""
uc = re.sub(r'public android\.view\.View getPremiumCheckbox.*?return tv;\n    \}', chk_engine, uc, flags=re.DOTALL)
with open(uf, 'w', encoding='utf-8') as f: f.write(uc)
print("✔ NEUMORPHISM (SOFT UI) APPLIED SUCCESSFULLY!")
