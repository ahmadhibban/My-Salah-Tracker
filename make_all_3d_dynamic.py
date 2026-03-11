import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# আগের ফিক্সড CSS কোডটুকু খুঁজে বের করা
pattern = r'// আপনার দেওয়া HTML/CSS এর হুবহু.*?card\.setBackground\(cb\);\s*\}'

new_code = """// সব কার্ডের জন্য ডাইনামিক CSS 3D বর্ডার (থিম কালারের সাথে ম্যাচ করে)
            int depth = (int)(3.5f * DENSITY); 
            
            android.graphics.drawable.GradientDrawable depthLayer = new android.graphics.drawable.GradientDrawable();
            
            // ম্যাজিক: ইউজার যে কালার সিলেক্ট করবে, তার ওপর ভিত্তি করে সলিড ৩ডি ডেপথ তৈরি হবে
            float[] hsv = new float[3];
            android.graphics.Color.colorToHSV(colorAccent, hsv);
            hsv[1] *= 0.5f; // স্যাচুরেশন কমিয়ে সফট করা হলো
            hsv[2] *= isDarkTheme ? 0.3f : 0.75f; // থিম অনুযায়ী পারফেক্ট গাঢ় করা হলো
            int dynamicShadow = android.graphics.Color.HSVToColor(hsv);
            
            depthLayer.setColor(dynamicShadow);
            depthLayer.setCornerRadius(16f * DENSITY);
            
            android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{depthLayer, cb});
            ld.setLayerInset(0, 0, depth, depth, 0); 
            ld.setLayerInset(1, depth, 0, 0, depth); 
            
            card.setBackground(ld);
            if(android.os.Build.VERSION.SDK_INT >= 21) card.setElevation(8f * DENSITY);"""

new_content = re.sub(pattern, new_code, content, flags=re.DOTALL)

if new_content != content:
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Dynamic CSS 3D applied to ALL 6 CARDS successfully!")
else:
    print("Error: Target code not found.")
