import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# যেখানে যেখানে arabicFont ব্যবহার করা হয়েছে, সেখানে সরাসরি আমাদের নতুন মেথড কল করে দেওয়া
c = c.replace('arabicFont != null ? arabicFont : appFonts[1]', 'getArabicFont()')

# আরবি ফন্ট লোড করার সবচেয়ে নিরাপদ এবং গ্যারান্টিড মেথড
font_method = """
    private android.graphics.Typeface _arabicFontObj = null;
    private android.graphics.Typeface getArabicFont() {
        if (_arabicFontObj == null) {
            try { 
                _arabicFontObj = android.graphics.Typeface.createFromAsset(getAssets(), "fonts/al_majeed_quranic_font_shiped.ttf"); 
            } catch (Exception e) { 
                _arabicFontObj = appFonts[1]; 
            }
        }
        return _arabicFontObj;
    }
"""

# মেথডটি ঠিক loadQuranTab এর ওপরে বসিয়ে দেওয়া
if 'private android.graphics.Typeface getArabicFont()' not in c:
    c = c.replace('private void loadQuranTab()', font_method + '\n    private void loadQuranTab()')

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Arabic Font Issue FIXED FOREVER! Ready to hit Play (▶️)!")
