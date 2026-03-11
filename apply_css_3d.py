import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# যেখানে card.setBackground(cb) আছে, সেখানে CSS 3D লজিক বসানো হচ্ছে
target = r'(cb\.setStroke\(\(int\)\(1f\*DENSITY\),[^;]+\);)\s*card\.setBackground\(cb\);'

replacement = r"""\1
            
            // আপনার দেওয়া HTML/CSS এর হুবহু ৩ডি বর্ডার শুধুমাত্র প্রথম কার্ডের (i == 0) জন্য
            if (i == 0) {
                int depth = (int)(3.5f * DENSITY); // CSS এর 4.5px পুরুত্ব
                
                // নিচের সলিড গাঢ় লেয়ার (CSS এর #91a0b5)
                android.graphics.drawable.GradientDrawable depthLayer = new android.graphics.drawable.GradientDrawable();
                depthLayer.setColor(isDarkTheme ? android.graphics.Color.parseColor("#334155") : android.graphics.Color.parseColor("#91a0b5"));
                depthLayer.setCornerRadius(16f * DENSITY);
                
                // লেয়ার মিলিয়ে থ্রিডি ব্লক তৈরি
                android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{depthLayer, cb});
                
                // CSS এর transform: translate(4px, -4px) এর ইফেক্ট আনা হচ্ছে
                ld.setLayerInset(0, 0, depth, depth, 0); // শ্যাডোকে নিচে ও বামে ঠেলে দেওয়া
                ld.setLayerInset(1, depth, 0, 0, depth); // মেইন কার্ডকে ওপরে ও ডানে ঠেলে দেওয়া
                
                card.setBackground(ld);
                if(android.os.Build.VERSION.SDK_INT >= 21) card.setElevation(8f * DENSITY); // CSS এর গ্রাউন্ড শ্যাডো
            } else {
                card.setBackground(cb);
            }"""

new_content = re.sub(target, replacement, content)

if new_content != content:
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("CSS 3D Magic applied perfectly to the first card!")
else:
    print("Error: Could not find the target code. Make sure the file is saved.")
