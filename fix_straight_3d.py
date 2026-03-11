import os, re

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"
for r, d, f in os.walk("."):
    if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")
    if "UIComponents.java" in f: uf = os.path.join(r, "UIComponents.java")

with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

# ১. চতুর্দিকে বর্ডার আরও মোটা করা (2.0f থেকে 2.5f)
mc = mc.replace('surface.setStroke((int)(2.0f * d), shadowColor);', 'surface.setStroke((int)(2.5f * d), shadowColor);')

# ২. খোদাই করা (Carved Inner) ইফেক্টকে বাঁকা থেকে একদম সোজা করা
carved_old = r'public android\.graphics\.drawable\.Drawable getCarvedInner.*?return ld;\n\s*\}'
carved_new = """public android.graphics.drawable.Drawable getCarvedInner(int bgColor, float radius, boolean isDark, int accentColor) {
    float d = getResources().getDisplayMetrics().density;
    int r = android.graphics.Color.red(accentColor); int g = android.graphics.Color.green(accentColor); int b = android.graphics.Color.blue(accentColor);
    int shadowColor = isDark ? android.graphics.Color.rgb((int)(r*0.35f), (int)(g*0.35f), (int)(b*0.35f)) : android.graphics.Color.rgb((int)(r*0.65f), (int)(g*0.65f), (int)(b*0.65f));
    android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
    android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable(); surface.setColor(bgColor); surface.setCornerRadius(radius);
    surface.setStroke((int)(2.5f * d), shadowColor); // চতুর্দিকে স্পষ্ট মোটা বর্ডার
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
    int off = (int)(2.0f * d); ld.setLayerInset(0, 0, 0, 0, off); ld.setLayerInset(1, 0, off, 0, 0); // কোনো ডানে-বামে শিফট নেই, একদম সোজা খোদাই!
    return ld;
}"""
mc = re.sub(carved_old, carved_new, mc, flags=re.DOTALL)
with open(mf, 'w', encoding='utf-8') as f: f.write(mc)

# ৩. চেকবক্সের খোদাই ইফেক্ট সোজা করা এবং বর্ডার মোটা করা
with open(uf, 'r', encoding='utf-8') as f: uc = f.read()
uc = re.sub(r'ld\.setLayerInset\(1, \(int\)\(1\.8f\*d\), \(int\)\(1\.8f\*d\), 0, 0\); // খোদাই করা.*?', 'ld.setLayerInset(0, 0, 0, 0, (int)(2.0f*d)); ld.setLayerInset(1, 0, (int)(2.0f*d), 0, 0); // একদম সোজা খোদাই', uc)
uc = re.sub(r'surface\.setStroke\(\(int\)\(1\.0f\*d\), shadowColor\);', 'surface.setStroke((int)(2.5f*d), shadowColor);', uc)
with open(uf, 'w', encoding='utf-8') as f: f.write(uc)

print("✔ DESIGN STRAIGHTENED & THICK BORDERS APPLIED!")
