import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. হুবহু নিচের কার্ডের লজিক (৩.৫ ডেপথ এবং একই থিম কালার)
new_method = """public android.graphics.drawable.LayerDrawable get3DDrawable(android.graphics.drawable.Drawable fg, float radius, boolean isOval) {
        int depth = (int)(3.5f * DENSITY); // একদম নিচের কার্ডের সমান ডেপথ!
        
        android.graphics.drawable.GradientDrawable depthLayer = new android.graphics.drawable.GradientDrawable();
        float[] hsv = new float[3];
        android.graphics.Color.colorToHSV(colorAccent, hsv);
        hsv[1] *= 0.5f; hsv[2] *= isDarkTheme ? 0.3f : 0.75f; // একদম নিচের কার্ডের সমান কালার!
        depthLayer.setColor(android.graphics.Color.HSVToColor(hsv));
        
        if (isOval) depthLayer.setShape(android.graphics.drawable.GradientDrawable.OVAL);
        else depthLayer.setCornerRadius(radius * DENSITY);
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{depthLayer, fg});
        
        // হুবহু কার্ডের সমান ইনসেট (যাতে থ্রিডি অ্যাঙ্গেল ১০০% সেম থাকে)
        ld.setLayerInset(0, 0, depth, depth, 0); 
        ld.setLayerInset(1, depth, 0, 0, depth); 
        return ld;
    }"""

content = re.sub(r'public android\.graphics\.drawable\.LayerDrawable get3DDrawable.*?return ld;\s*\}', new_method, content, flags=re.DOTALL)

# ২. পুরোনো সব ভুল প্যাডিং মুছে ফেলা
content = re.sub(r't\.setPadding\([^;]+\);', '', content)
content = re.sub(r'prevW\.setPadding\([^;]+\);', '', content)
content = re.sub(r'nextW\.setPadding\([^;]+\);', '', content)
content = re.sub(r'markAllBtn\.setPadding\([^;]+\);(?: /\* 3D padding applied \*/)?', '', content)
content = re.sub(r'todayBtn\.setPadding\([^;]+\);', '', content)

# ৩. লেখা ও আইকন একদম সেন্টারে রাখার জন্য নিখুঁত ম্যাথমেটিক্যাল প্যাডিং
content = re.sub(r'(t\.setBackground\(get3DDrawable[^;]+;\s*(?:if[^;]+;)?)', r'\1 t.setPadding((int)(3.5f*DENSITY), 0, 0, (int)(3.5f*DENSITY));', content)
content = re.sub(r'(prevW\.setBackground\(get3DDrawable[^;]+;\s*(?:if[^;]+;)?)', r'\1 prevW.setPadding((int)(3.5f*DENSITY), 0, 0, (int)(3.5f*DENSITY));', content)
content = re.sub(r'(nextW\.setBackground\(get3DDrawable[^;]+;\s*(?:if[^;]+;)?)', r'\1 nextW.setPadding((int)(3.5f*DENSITY), 0, 0, (int)(3.5f*DENSITY));', content)

# Mark All এবং Today বাটনের জন্য সুন্দর প্যাডিং
content = re.sub(r'(markAllBtn\.setBackground\(get3DDrawable[^;]+;\s*(?:if[^;]+;)?)', r'\1 markAllBtn.setPadding((int)(15f*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(9.5f*DENSITY));', content)
content = re.sub(r'(todayBtn\.setBackground\(get3DDrawable[^;]+;\s*(?:if[^;]+;)?)', r'\1 todayBtn.setPadding((int)(15f*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(9.5f*DENSITY));', content)

# ৪. বৃত্তগুলোর সাইজ আরেকটু বড় করা (যাতে ৩.৫ ডেপথ নেওয়ার পরও সুন্দর দেখায়)
content = content.replace('int circleSize = (int)(36 * DENSITY);', 'int circleSize = (int)(44 * DENSITY);')
content = content.replace('int circleSize = (int)(40 * DENSITY);', 'int circleSize = (int)(44 * DENSITY);')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("100% Match Applied! Top boxes now perfectly mirror the bottom cards.")
