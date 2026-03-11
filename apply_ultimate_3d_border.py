import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. মাস্টার ৩ডি মেথড ইনজেক্ট করা হচ্ছে (এটি HTML-এর মাল্টিপল লেয়ারড শ্যাডোর লজিক)
ultimate_method = """public android.graphics.drawable.LayerDrawable getUltimate3DBorder(android.graphics.drawable.Drawable fg, float radius, boolean isOval, int baseColor) {
        int d1 = (int)(1f * DENSITY); // -1px 1px 0px
        int d2 = (int)(2f * DENSITY); // -2px 2px 0px
        int d3 = (int)(3.5f * DENSITY); // -3.5px 3.5px 0px (Final thickness)

        float[] hsv = new float[3];
        android.graphics.Color.colorToHSV(baseColor, hsv);
        
        // Layer 1 (Lightest shadow)
        hsv[2] *= 0.9f; int c1 = android.graphics.Color.HSVToColor(hsv);
        android.graphics.drawable.GradientDrawable l1 = new android.graphics.drawable.GradientDrawable(); l1.setColor(c1);
        if(isOval) l1.setShape(android.graphics.drawable.GradientDrawable.OVAL); else l1.setCornerRadius(radius * DENSITY);
        
        // Layer 2 (Medium shadow)
        hsv[2] *= 0.85f; int c2 = android.graphics.Color.HSVToColor(hsv);
        android.graphics.drawable.GradientDrawable l2 = new android.graphics.drawable.GradientDrawable(); l2.setColor(c2);
        if(isOval) l2.setShape(android.graphics.drawable.GradientDrawable.OVAL); else l2.setCornerRadius(radius * DENSITY);
        
        // Layer 3 (Darkest thick shadow - Bottom layer)
        hsv[2] *= 0.75f; int c3 = android.graphics.Color.HSVToColor(hsv);
        android.graphics.drawable.GradientDrawable l3 = new android.graphics.drawable.GradientDrawable(); l3.setColor(c3);
        if(isOval) l3.setShape(android.graphics.drawable.GradientDrawable.OVAL); else l3.setCornerRadius(radius * DENSITY);

        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{l3, l2, l1, fg});
        
        // Stacking layers like HTML box-shadow
        ld.setLayerInset(0, 0, d3, d3, 0); 
        ld.setLayerInset(1, d1, d3-d1, d3-d1, d1); 
        ld.setLayerInset(2, d2, d3-d2, d3-d2, d2); 
        ld.setLayerInset(3, d3, 0, 0, d3); 
        
        return ld;
    }"""

if "getUltimate3DBorder(" not in content:
    content = content.replace('private void loadTodayPage() {', ultimate_method + '\n    private void loadTodayPage() {')

# ২. ভেতরের কোনো ফাংশন টাচ না করে শুধু সেটব্যাকগ্রাউন্ড রিপ্লেস করা হচ্ছে

# নামাজের ৬টি কার্ড
content = re.sub(r'card\.setBackground\(cb\);', r'card.setBackground(getUltimate3DBorder(cb, 16f, false, colorAccent)); if(android.os.Build.VERSION.SDK_INT>=21) card.setElevation(10f*DENSITY);', content)

# Progress Card
content = re.sub(r'pCard\.setBackground\([^;]+\);', r'pCard.setBackground(getUltimate3DBorder(pcBg, 16f, false, colorAccent));', content)

# ৭ দিনের ঘর
content = re.sub(r't\.setBackground\([^;]+\);', r't.setBackground(getUltimate3DBorder(getProgressBorder(dKey, isSel), 0, true, colorAccent));', content)

# Mark All এবং Today
content = re.sub(r'markAllBtn\.setBackground\([^;]+\);', r'markAllBtn.setBackground(getUltimate3DBorder(bg1, 16f, false, colorAccent));', content)
content = re.sub(r'todayBtn\.setBackground\([^;]+\);', r'todayBtn.setBackground(getUltimate3DBorder(bg2, 16f, false, colorAccent));', content)

# Date এবং View Toggle
content = re.sub(r'dateBtn\.setBackground\([^;]+\);', r'dateBtn.setBackground(getUltimate3DBorder(bg1, 16f, false, colorAccent));', content)
content = re.sub(r'viewToggle\.setBackground\([^;]+\);', r'viewToggle.setBackground(getUltimate3DBorder(bg2, 16f, false, colorAccent));', content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("HTML Style Ultimate Layered 3D Borders applied purely to outer frames!")
