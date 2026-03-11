import os
import re

def apply_perfect_3d():
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

    # একদম নতুন ডায়নামিক 3D ইঞ্জিন যা যেকোনো থিম কালারের সাথে কাজ করবে
    perfect_3d_engine = """public android.graphics.drawable.Drawable getSolid3DDrawable(int mainColor, int borderColor, float radius, boolean isDark, boolean isRound) {
        int depth = isRound ? 4 : 8; // ৮টি লেয়ার ব্যবহার করে বর্ডার অনেক মোটা করা হলো
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.Drawable[] layers = new android.graphics.drawable.Drawable[depth + 1];
        
        // ডায়নামিক শ্যাডো কালার (আপনার থিমের কালারকে স্বয়ংক্রিয়ভাবে গাঢ় করবে)
        int r = android.graphics.Color.red(mainColor);
        int g = android.graphics.Color.green(mainColor);
        int b = android.graphics.Color.blue(mainColor);
        float darkenFactor = isDark ? 0.5f : 0.75f; // ডার্ক মোডে ৫০% এবং লাইট মোডে ২৫% গাঢ় করবে
        int shadowColor = android.graphics.Color.rgb((int)(r * darkenFactor), (int)(g * darkenFactor), (int)(b * darkenFactor));

        for (int i = 0; i <= depth; i++) {
            android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
            gd.setCornerRadius(radius);
            if (isRound) gd.setShape(android.graphics.drawable.GradientDrawable.OVAL);
            
            if (i == depth) {
                gd.setColor(mainColor); // একদম ওপরের সারফেস
                if (borderColor != android.graphics.Color.TRANSPARENT) {
                    gd.setStroke((int)(1.5f * d), borderColor);
                }
            } else {
                gd.setColor(shadowColor); // সলিড ৩ডি পুরুত্ব
            }
            layers[i] = gd;
        }
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(layers);
        for (int i = 0; i <= depth; i++) {
            int step = (int) (1.5f * d); // পুরুত্বের সাইজ (Thickness step)
            // একদম পারফেক্ট Isometric 3D (বাম ও নিচে পুরুত্ব তৈরি করবে)
            int left = (depth - i) * step; 
            int bottom = (depth - i) * step;
            int top = i * step;
            int right = i * step;
            ld.setLayerInset(i, left, top, right, bottom);
        }
        return ld;
    }"""

    # আগের ভুল 3D ইঞ্জিনটি মুছে নতুন পারফেক্ট ইঞ্জিনটি বসানো হচ্ছে
    code = re.sub(r'public android\.graphics\.drawable\.Drawable getSolid3DDrawable.*?return ld;\n    \}', perfect_3d_engine, code, flags=re.DOTALL)

    with open(target, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Magic Done! Perfect Dynamic 3D Applied. No more thin borders!")

apply_perfect_3d()
