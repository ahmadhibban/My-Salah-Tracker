import os
import re

def fix_3d_direction():
    target = None
    for root, _, files in os.walk("."):
        if "MainActivity.java" in files:
            target = os.path.join(root, "MainActivity.java")
            break
    
    if not target:
        print("MainActivity.java খুঁজে পাওয়া যায়নি!")
        return

    with open(target, 'r', encoding='utf-8') as f:
        code = f.read()

    correct_3d_engine = """public android.graphics.drawable.Drawable getSolid3DDrawable(int mainColor, int borderColor, float radius, boolean isDark, boolean isRound) {
        int depth = isRound ? 4 : 8; 
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.Drawable[] layers = new android.graphics.drawable.Drawable[depth + 1];
        
        int r = android.graphics.Color.red(mainColor);
        int g = android.graphics.Color.green(mainColor);
        int b = android.graphics.Color.blue(mainColor);
        float darkenFactor = isDark ? 0.5f : 0.75f; 
        int shadowColor = android.graphics.Color.rgb((int)(r * darkenFactor), (int)(g * darkenFactor), (int)(b * darkenFactor));

        for (int i = 0; i <= depth; i++) {
            android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
            gd.setCornerRadius(radius);
            if (isRound) gd.setShape(android.graphics.drawable.GradientDrawable.OVAL);
            
            if (i == depth) {
                gd.setColor(mainColor); 
                if (borderColor != android.graphics.Color.TRANSPARENT) {
                    gd.setStroke((int)(1.5f * d), borderColor);
                }
            } else {
                gd.setColor(shadowColor); 
            }
            layers[i] = gd;
        }
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(layers);
        for (int i = 0; i <= depth; i++) {
            int step = (int) (1.5f * d); 
            // ✨ ম্যাথমেটিক্যাল ফিক্স: এবার পুরুত্ব পারফেক্টলি বামে এবং নিচে দেখাবে ✨
            int left = i * step; 
            int bottom = i * step;
            int top = (depth - i) * step;
            int right = (depth - i) * step;
            ld.setLayerInset(i, left, top, right, bottom);
        }
        return ld;
    }"""

    # আগের ইঞ্জিনটি সরিয়ে সঠিক দিকের ইঞ্জিনটি বসানো হচ্ছে
    code = re.sub(r'public android\.graphics\.drawable\.Drawable getSolid3DDrawable.*?return ld;\n    \}', correct_3d_engine, code, flags=re.DOTALL)

    with open(target, 'w', encoding='utf-8') as f:
        f.write(code)
    print("✔ Direction Fixed! 3D effect will now show properly on the Left and Bottom.")

fix_3d_direction()
