import os

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
if not os.path.exists(mf):
    for r, d, f in os.walk("."):
        if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")

with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

# ডুপ্লিকেট মেথড রিমুভ করার স্মার্ট ব্র্যাকেট ফাংশন
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
        if end != -1:
            code = code[:start] + code[end:]
        else:
            break
    return code

# পুরনো সব ভার্সন মুছে ফেলা হচ্ছে
mc = remove_method(mc, "Drawable getExplicit3D")
mc = remove_method(mc, "Drawable getAccent3D")
mc = remove_method(mc, "Drawable getCarvedInner")

# নতুন পারফেক্ট ৩ডি ইঞ্জিনগুলো শুধু একবার ইনজেক্ট করা হচ্ছে
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
    int off = (int)(1.8f * d); ld.setLayerInset(1, off, off, 0, 0); // খোদাই করা (Inner Shadow) ইফেক্ট
    return ld;
}"""

mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n    " + new_engines)

with open(mf, 'w', encoding='utf-8') as f: f.write(mc)
print("✔ DUPLICATE METHODS REMOVED SUCCESSFULLY!")
