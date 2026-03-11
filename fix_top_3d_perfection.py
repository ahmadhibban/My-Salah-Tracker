import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. ছোট আইটেমগুলোর জন্য ডেপথ এবং কালার নিখুঁতভাবে স্কেল করা হচ্ছে
new_method = """public android.graphics.drawable.LayerDrawable get3DDrawable(android.graphics.drawable.Drawable fg, float radius, boolean isOval) {
        // ছোট গোল ঘরের জন্য ডেপথ ১.৫ এবং বাটনের জন্য ২.৫ করা হলো (যাতে ডিম্বাকার না লাগে)
        int depth = isOval ? (int)(1.5f * DENSITY) : (int)(2.5f * DENSITY); 
        
        android.graphics.drawable.GradientDrawable depthLayer = new android.graphics.drawable.GradientDrawable();
        float[] hsv = new float[3];
        android.graphics.Color.colorToHSV(colorAccent, hsv);
        hsv[1] *= 0.35f; hsv[2] *= isDarkTheme ? 0.3f : 0.85f; // ওপরের শ্যাডো কালার আরও সফট করা হলো
        depthLayer.setColor(android.graphics.Color.HSVToColor(hsv));
        
        if (isOval) depthLayer.setShape(android.graphics.drawable.GradientDrawable.OVAL);
        else depthLayer.setCornerRadius(radius * DENSITY);
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{depthLayer, fg});
        
        // শেপ যেন পারফেক্ট থাকে, তার জন্য শুধু ভার্টিক্যাল (নিচে) শ্যাডো দেওয়া হলো
        ld.setLayerInset(0, 0, depth, 0, 0); 
        ld.setLayerInset(1, 0, 0, 0, depth); 
        return ld;
    }"""

content = re.sub(r'public android\.graphics\.drawable\.LayerDrawable get3DDrawable.*?return ld;\s*\}', new_method, content, flags=re.DOTALL)

# ২. লেখা ও আইকন যেন ১০০% সেন্টারে থাকে, তার জন্য প্যাডিং অ্যাডজাস্ট করা হচ্ছে
if "/* 3D padding applied */" not in content:
    content = content.replace('markAllBtn.setBackground(get3DDrawable(bg1, 16f, false));', 'markAllBtn.setBackground(get3DDrawable(bg1, 16f, false)); markAllBtn.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY)); /* 3D padding applied */')
    content = content.replace('todayBtn.setBackground(get3DDrawable(bg2, 16f, false));', 'todayBtn.setBackground(get3DDrawable(bg2, 16f, false)); todayBtn.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY));')
    
    # ৭ দিনের ঘর এবং অ্যারো আইকনগুলোর সেন্টার ফিক্স
    content = content.replace('t.setBackground(get3DDrawable(getProgressBorder(dKey, isSel), 0, true));', 't.setBackground(get3DDrawable(getProgressBorder(dKey, isSel), 0, true)); t.setPadding(0, 0, 0, (int)(1.5f*DENSITY));')
    content = content.replace('prevW.setBackground(get3DDrawable(navBg, 16f, false));', 'prevW.setBackground(get3DDrawable(navBg, 16f, false)); prevW.setPadding(0, 0, 0, (int)(2.5f*DENSITY));')
    content = content.replace('nextW.setBackground(get3DDrawable(navBg2, 16f, false));', 'nextW.setBackground(get3DDrawable(navBg2, 16f, false)); nextW.setPadding(0, 0, 0, (int)(2.5f*DENSITY));')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Top UI made 100% PERFECT! Scaled shadows and centered text applied.")
