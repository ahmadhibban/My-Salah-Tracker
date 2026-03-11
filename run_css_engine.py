import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# পুরোনো সমস্ত জঞ্জাল মুছে ফেলা হচ্ছে
content = re.sub(r'public android\.graphics\.drawable\.LayerDrawable getUltimate3D.*?return ld;\s*\}', '', content, flags=re.DOTALL)
content = re.sub(r'public android\.graphics\.drawable\.LayerDrawable get3DDrawable.*?return ld;\s*\}', '', content, flags=re.DOTALL)

# আপনার HTML-এর হুবহু লজিক দিয়ে "CSS Engine" বসানো হচ্ছে
css_engine = """
    // --- PURE CSS TO JAVA ENGINE ---
    public android.graphics.drawable.LayerDrawable getCssBoxShadow(android.graphics.drawable.Drawable mainFg, int shadowBaseColor, float radius, boolean isOval) {
        // আপনার HTML এর box-shadow ভ্যালুগুলো:
        float[] cssOffsets = { 6f, 5f, 3.5f, 2f, 1f, 0f }; 
        float[] cssDarkness = { 0.70f, 0.75f, 0.80f, 0.85f, 0.90f, 1.0f }; 
        
        android.graphics.drawable.Drawable[] layers = new android.graphics.drawable.Drawable[cssOffsets.length];
        float[] hsv = new float[3]; android.graphics.Color.colorToHSV(shadowBaseColor, hsv);
        
        for(int i=0; i<cssOffsets.length; i++) {
            if(i == cssOffsets.length - 1) { layers[i] = mainFg; } // আপনার অরিজিনাল মেইন কার্ড
            else {
                android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
                float[] tempHsv = {hsv[0], hsv[1], hsv[2] * cssDarkness[i]};
                gd.setColor(android.graphics.Color.HSVToColor(tempHsv));
                if(isOval) gd.setShape(android.graphics.drawable.GradientDrawable.OVAL); else gd.setCornerRadius(radius * DENSITY);
                layers[i] = gd;
            }
        }
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(layers);
        for(int i=0; i<cssOffsets.length; i++) {
            int left = (int)((6f - cssOffsets[i]) * DENSITY); int top = (int)(cssOffsets[i] * DENSITY);
            int right = (int)(cssOffsets[i] * DENSITY); int bottom = (int)((6f - cssOffsets[i]) * DENSITY);
            ld.setLayerInset(i, left, top, right, bottom); // একদম CSS-এর translate(-6px, 6px) ইফেক্ট
        }
        return ld;
    }
    
    public void applyCssToView(android.view.View v, android.graphics.drawable.Drawable mainBg, int shadowColor, float radius, boolean isOval) {
        v.setBackground(getCssBoxShadow(mainBg, shadowColor, radius, isOval));
        // ম্যাজিক প্যাডিং: ভেতরের আইকন বা টেক্সট যেন কোনোভাবেই নষ্ট না হয়!
        v.setPadding(v.getPaddingLeft() + (int)(6*DENSITY), v.getPaddingTop(), v.getPaddingRight(), v.getPaddingBottom() + (int)(6*DENSITY));
    }
    // ---------------------------------"""

if "applyCssToView(" not in content:
    content = content.replace('private void loadTodayPage() {', css_engine + '\n    private void loadTodayPage() {')

# সমস্ত কার্ড এবং বাটনে CSS Engine অ্যাপ্লাই করা হচ্ছে
pattern_ultimate = r'([a-zA-Z0-9_]+)\.setBackground\(\s*getUltimate3DBorder\(\s*(.*?),\s*([0-9.]+[fF]?),\s*(true|false),\s*([a-zA-Z0-9_]+)\s*\)\s*\);'
content = re.sub(pattern_ultimate, r'applyCssToView(\1, \2, \5, \3, \4);', content)

pattern_3d = r'([a-zA-Z0-9_]+)\.setBackground\(\s*get3DDrawable\(\s*(.*?),\s*([0-9.]+[fF]?),\s*(true|false)\s*\)\s*\);'
content = re.sub(pattern_3d, r'applyCssToView(\1, \2, colorAccent, \3, \4);', content)

# ৭ দিনের ঘরগুলো স্কয়ার করার জন্য
content = content.replace('applyCssToView(t, getProgressBorder(dKey, isSel), colorAccent, 0, true);', 'applyCssToView(t, getProgressBorder(dKey, isSel), colorAccent, 10f, false);')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("CSS Engine Injected! HTML code is now ruling your Android App!")
