import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. আগের জগাখিচুড়ি ইঞ্জিন মুছে "Premium Pro UI Engine" বসানো হচ্ছে
premium_engine = """
    // --- PREMIUM PRO UI ENGINE ---
    public android.graphics.drawable.LayerDrawable getSolid3D(int bgColor, int shadowColor, float radius, boolean isOval, int strokeColor, int strokeWidth) {
        int depth = (int)(3.5f * DENSITY);
        
        android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable();
        shadow.setColor(shadowColor);
        if(isOval) shadow.setShape(android.graphics.drawable.GradientDrawable.OVAL);
        else shadow.setCornerRadius(radius * DENSITY);
        
        android.graphics.drawable.GradientDrawable main = new android.graphics.drawable.GradientDrawable();
        main.setColor(bgColor);
        if(isOval) main.setShape(android.graphics.drawable.GradientDrawable.OVAL);
        else main.setCornerRadius(radius * DENSITY);
        
        // সিলেক্টেড দিনের সাদা গোল দাগ
        if(strokeWidth > 0) main.setStroke((int)(strokeWidth * DENSITY), strokeColor);
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, main});
        
        // ছায়াকে নিচে ডানে পাঠিয়ে, মেইন কার্ডকে জায়গা দেওয়া হলো
        ld.setLayerInset(0, depth, depth, 0, 0); 
        ld.setLayerInset(1, 0, 0, depth, depth); 
        
        return ld;
    }
    
    public void setProStyle(android.view.View v, int bgColor, int shadowColor, float radius, boolean isOval, int strokeColor, int strokeWidth, int padDp) {
        v.setBackground(getSolid3D(bgColor, shadowColor, radius, isOval, strokeColor, strokeWidth));
        int p = (int)(padDp * DENSITY);
        // ম্যাজিক প্যাডিং: ছায়ার কারণে ভেতরের লেখা আর কখনো চ্যাপ্টা হবে না!
        v.setPadding(p, p, p + (int)(3.5f * DENSITY), p + (int)(3.5f * DENSITY));
    }
"""
content = re.sub(r'// --- PURE CSS TO JAVA ENGINE ---.*?// ---------------------------------', premium_engine, content, flags=re.DOTALL)

# ২. প্রফেশনাল কালার ভ্যারিয়েবল (সাদা আইকনের জন্য গ্রে শ্যাডো)
color_vars = """
        int uiBg = isDarkTheme ? android.graphics.Color.parseColor("#2C2C2E") : android.graphics.Color.parseColor("#FFFFFF");
        int uiShadow = isDarkTheme ? android.graphics.Color.parseColor("#151515") : android.graphics.Color.parseColor("#C2C9D6"); 
        float[] hsv = new float[3]; android.graphics.Color.colorToHSV(colorAccent, hsv); hsv[2] *= 0.70f; 
        int accShadow = android.graphics.Color.HSVToColor(hsv);
"""
if "int uiBg =" not in content:
    content = content.replace("private void loadTodayPage() {", "private void loadTodayPage() {\n" + color_vars)

# ৩. মেইন কার্ড এবং বাটনগুলোকে নতুন প্রফেশনাল ইঞ্জিনে শিফট করা হচ্ছে
content = re.sub(r'applyCssToView\(\s*card[^;]+;', r'setProStyle(card, stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#331520") : android.graphics.Color.parseColor("#FCE4EC")) : uiBg, uiShadow, 16f, false, checked ? colorAccent : android.graphics.Color.TRANSPARENT, checked ? 1 : 0, 14);', content)

content = re.sub(r'applyCssToView\(\s*settingsBtn[^;]+;', r'setProStyle(settingsBtn, uiBg, uiShadow, 0, true, 0, 0, 8); if(settingsBtn instanceof TextView) ((TextView)settingsBtn).setTextColor(colorAccent);', content)
content = re.sub(r'applyCssToView\(\s*periodBtn[^;]+;', r'setProStyle(periodBtn, uiBg, uiShadow, 0, true, 0, 0, 8); if(periodBtn instanceof TextView) ((TextView)periodBtn).setTextColor(colorAccent);', content)
content = re.sub(r'applyCssToView\(\s*offBtn[^;]+;', r'setProStyle(offBtn, uiBg, uiShadow, 0, true, 0, 0, 8); if(offBtn instanceof TextView) ((TextView)offBtn).setTextColor(colorAccent);', content)
content = re.sub(r'applyCssToView\(\s*themeToggleBtn[^;]+;', r'setProStyle(themeToggleBtn, colorAccent, accShadow, 0, true, 0, 0, 8); if(themeToggleBtn instanceof TextView) ((TextView)themeToggleBtn).setTextColor(android.graphics.Color.WHITE);', content)

content = re.sub(r'applyCssToView\(\s*prevW[^;]+;', r'setProStyle(prevW, uiBg, uiShadow, 10f, false, 0, 0, 8);', content)
content = re.sub(r'applyCssToView\(\s*nextW[^;]+;', r'setProStyle(nextW, uiBg, uiShadow, 10f, false, 0, 0, 8);', content)

day_logic = """
        if (isSel) {
            setProStyle(t, colorAccent, accShadow, 10f, false, android.graphics.Color.WHITE, 2, 8);
            t.setTextColor(android.graphics.Color.WHITE);
            t.setScaleX(1.1f); t.setScaleY(1.1f);
        } else {
            setProStyle(t, uiBg, uiShadow, 10f, false, 0, 0, 8);
            t.setTextColor(themeColors[2]);
            t.setScaleX(1.0f); t.setScaleY(1.0f);
        }
"""
content = re.sub(r'applyCssToView\(\s*t\s*,\s*getProgressBorder.*?t\.setScaleY\([^;]+;\s*\}', day_logic, content, flags=re.DOTALL)

content = re.sub(r'applyCssToView\(\s*markAllBtn[^;]+;', r'setProStyle(markAllBtn, uiBg, uiShadow, 14f, false, 0, 0, 12);', content)
content = re.sub(r'applyCssToView\(\s*todayBtn[^;]+;', r'setProStyle(todayBtn, uiBg, uiShadow, 14f, false, 0, 0, 12);', content)
content = re.sub(r'applyCssToView\(\s*dateBtn[^;]+;', r'setProStyle(dateBtn, uiBg, uiShadow, 14f, false, 0, 0, 12);', content)
content = re.sub(r'applyCssToView\(\s*viewToggle[^;]+;', r'setProStyle(viewToggle, uiBg, uiShadow, 14f, false, 0, 0, 12);', content)
content = re.sub(r'applyCssToView\(\s*pCard[^;]+;', r'setProStyle(pCard, colorAccent, accShadow, 16f, false, 0, 0, 16);', content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Absolute Perfection! Pro UI Engine Applied.")
