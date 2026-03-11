import os
import re

def fix_small_elements_alignment():
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

    # স্মার্ট থ্রিডি ইঞ্জিন: যা সাইজ বুঝে পুরুত্ব কম-বেশি করবে
    smart_3d_engine = """public android.graphics.drawable.Drawable getSolid3DDrawable(int mainColor, int borderColor, float radius, boolean isDark, boolean isRound) {
        float d = getResources().getDisplayMetrics().density;
        
        int depth;
        float stepMultiplier;
        
        // ডায়নামিক ডেপথ কন্ট্রোল
        if (isRound || radius >= 50f) {
            depth = 2; stepMultiplier = 1.0f; // উপরের ছোট আইকনের জন্য পাতলা থ্রিডি
        } else if (radius <= 15f * d) {
            depth = 3; stepMultiplier = 1.0f; // ৭ দিনের ক্যালেন্ডার ও স্ট্রিক পিলের জন্য মাঝারি থ্রিডি
        } else {
            depth = 8; stepMultiplier = 1.5f; // নামাজের কার্ডের জন্য মোটা থ্রিডি
        }

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
                    gd.setStroke((int)(1.0f * d), borderColor); // বর্ডার স্ট্রোক একটু কমানো হলো
                }
            } else {
                gd.setColor(shadowColor); 
            }
            layers[i] = gd;
        }
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(layers);
        for (int i = 0; i <= depth; i++) {
            int step = (int) (stepMultiplier * d); 
            int left = i * step; 
            int bottom = i * step;
            int top = (depth - i) * step;
            int right = (depth - i) * step;
            ld.setLayerInset(i, left, top, right, bottom);
        }
        return ld;
    }"""

    # আগের ইঞ্জিনটি রিপ্লেস করা
    code = re.sub(r'public android\.graphics\.drawable\.Drawable getSolid3DDrawable.*?return ld;\n    \}', smart_3d_engine, code, flags=re.DOTALL)

    # ৭ দিনের ক্যালেন্ডারের লেখা একদম মাঝে আনার ফিক্স
    if "t.setGravity(android.view.Gravity.CENTER);" not in code:
        code = re.sub(r't\.setTextSize\(12\);', 't.setTextSize(13); t.setGravity(android.view.Gravity.CENTER); t.setPadding(0, 0, 0, 0);', code)

    # স্ট্রিক পিলের লেখা মাঝে আনার ফিক্স
    code = re.sub(r'streakBadge\.setPadding\(.*?\);', 'streakBadge.setPadding((int)(10*DENSITY), (int)(4*DENSITY), (int)(10*DENSITY), (int)(4*DENSITY));\n        streakBadge.setGravity(android.view.Gravity.CENTER);', code)

    with open(target, 'w', encoding='utf-8') as f:
        f.write(code)
    print("✔ Everything Aligned Perfectly! Small elements now have proper 3D thickness and centered text.")

fix_small_elements_alignment()
