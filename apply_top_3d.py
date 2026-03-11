import os

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ডাইনামিক ৩ডি শ্যাডো তৈরি করার জাদুকরী মেথড
helper_code = """
    public android.graphics.drawable.LayerDrawable get3DDrawable(android.graphics.drawable.Drawable fg, float radius, boolean isOval) {
        int depth = (int)(3.5f * DENSITY);
        android.graphics.drawable.GradientDrawable depthLayer = new android.graphics.drawable.GradientDrawable();
        float[] hsv = new float[3];
        android.graphics.Color.colorToHSV(colorAccent, hsv);
        hsv[1] *= 0.5f; hsv[2] *= isDarkTheme ? 0.3f : 0.75f;
        depthLayer.setColor(android.graphics.Color.HSVToColor(hsv));
        if (isOval) depthLayer.setShape(android.graphics.drawable.GradientDrawable.OVAL);
        else depthLayer.setCornerRadius(radius * DENSITY);
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{depthLayer, fg});
        ld.setLayerInset(0, 0, depth, depth, 0); 
        ld.setLayerInset(1, depth, 0, 0, depth); 
        return ld;
    }
"""

if "get3DDrawable(" not in content:
    # মেথডটি ইনজেক্ট করা হচ্ছে
    content = content.replace('private void loadTodayPage() {', helper_code + '\n    private void loadTodayPage() {')

    # ১. বাঁ-দিকের অ্যারো (❮)
    content = content.replace('prevW.setBackground(navBg);', 'prevW.setBackground(get3DDrawable(navBg, 16f, false)); if(android.os.Build.VERSION.SDK_INT >= 21) prevW.setElevation(4f * DENSITY);')
    
    # ২. ডান-দিকের অ্যারো (❯)
    content = content.replace('nextW.setBackground(navBg);', 'android.graphics.drawable.GradientDrawable navBg2 = new android.graphics.drawable.GradientDrawable(); navBg2.setColor(themeColors[1]); navBg2.setCornerRadius(16f * DENSITY); navBg2.setStroke((int)(1f*DENSITY), themeColors[4]); nextW.setBackground(get3DDrawable(navBg2, 16f, false)); if(android.os.Build.VERSION.SDK_INT >= 21) nextW.setElevation(4f * DENSITY);')
    
    # ৩. ৭ দিনের গোলাকার ঘরগুলো
    content = content.replace('t.setBackground(getProgressBorder(dKey, isSel));', 't.setBackground(get3DDrawable(getProgressBorder(dKey, isSel), 0, true)); if(android.os.Build.VERSION.SDK_INT >= 21) t.setElevation(4f * DENSITY);')
    
    # ৪. Mark All (সব সম্পন্ন) বাটন
    content = content.replace('markAllBtn.setBackground(bg1);', 'markAllBtn.setBackground(get3DDrawable(bg1, 16f, false)); if(android.os.Build.VERSION.SDK_INT >= 21) markAllBtn.setElevation(4f * DENSITY);')
    
    # ৫. Today (আজকে/এই সপ্তাহ) বাটন
    content = content.replace('todayBtn.setBackground(bg2);', 'todayBtn.setBackground(get3DDrawable(bg2, 16f, false)); if(android.os.Build.VERSION.SDK_INT >= 21) todayBtn.setElevation(4f * DENSITY);')

    # যেহেতু ৩ডি ডেপথ এর জন্য কিছুটা জায়গা লাগে, তাই ৭ দিনের বৃত্তের সাইজ হালকা বড় করা হলো
    content = content.replace('int circleSize = (int)(36 * DENSITY);', 'int circleSize = (int)(40 * DENSITY);')

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Top UI Dynamic 3D applied successfully!")
else:
    print("Code already applied.")
