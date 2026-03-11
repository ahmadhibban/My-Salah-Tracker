import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. ফালতু ওভারলোডেড মেথড ডিলিট করে, একদম ক্লিন HTML টু জাভা মেথড বসানো হলো
clean_method = """public android.graphics.drawable.LayerDrawable getUltimate3DBorder(android.graphics.drawable.Drawable fg, float radius, boolean isOval, int baseColor) {
        int depth = (int)(4f * DENSITY); // HTML এর transform: translate(4px, -4px) এর সমান
        
        // আপনার HTML কোডের হুবহু সেই প্রিমিয়াম ছাই-নীল শ্যাডো কালার
        int shadowColor = isDarkTheme ? android.graphics.Color.parseColor("#1e293b") : android.graphics.Color.parseColor("#91a0b5");
        
        android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable();
        shadow.setColor(shadowColor);
        
        if (isOval) {
            shadow.setShape(android.graphics.drawable.GradientDrawable.OVAL);
        } else {
            shadow.setCornerRadius(radius * DENSITY);
        }
        
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, fg});
        
        // একদম পারফেক্ট শ্যাডো প্লেসমেন্ট (কোনো জগাখিচুড়ি লেয়ার নেই)
        ld.setLayerInset(0, 0, depth, depth, 0); 
        ld.setLayerInset(1, depth, 0, 0, depth); 
        
        return ld;
    }"""

content = re.sub(r'public android\.graphics\.drawable\.LayerDrawable getUltimate3DBorder.*?return ld;\s*\}', clean_method, content, flags=re.DOTALL)

# ২. আপনার HTML অনুযায়ী ৭ দিনের ঘরগুলোকে বৃত্ত থেকে স্কয়ার (১০ পিক্সেল রাউন্ড) করা হলো
content = content.replace('getUltimate3DBorder(getProgressBorder(dKey, isSel), 0, true', 'getUltimate3DBorder(getProgressBorder(dKey, isSel), 10f, false')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Ugly mess FIXED! Clean HTML design applied successfully.")
