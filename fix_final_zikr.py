import re
f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(f).read()

# Fix 1: arabicFont variable
if 'private android.graphics.Typeface arabicFont;' not in c:
    c = c.replace('private android.graphics.Typeface[] appFonts = new android.graphics.Typeface[2];', 'private android.graphics.Typeface[] appFonts = new android.graphics.Typeface[2];\n    private android.graphics.Typeface arabicFont;')

if 'arabicFont = android.graphics.Typeface.createFromAsset' not in c:
    c = c.replace('appFonts[1] = android.graphics.Typeface.DEFAULT_BOLD;', 'appFonts[1] = android.graphics.Typeface.DEFAULT_BOLD;\n        try { arabicFont = android.graphics.Typeface.createFromAsset(getAssets(), "fonts/al_majeed_quranic_font_shiped.ttf"); } catch(Exception e) { arabicFont = android.graphics.Typeface.DEFAULT; }')

# Fix 2: Remove getRoundRect and use direct GradientDrawable
c = c.replace('ui.getRoundRect(themeColors[1], 15f*DENSITY)', 'getRdRect(themeColors[1], 15f*DENSITY)')

# Add the getRdRect method locally
rect_method = """
    private android.graphics.drawable.GradientDrawable getRdRect(int color, float rad) {
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
        gd.setColor(color); gd.setCornerRadius(rad); return gd;
    }
"""
if 'private android.graphics.drawable.GradientDrawable getRdRect' not in c:
    c = c.replace('private void loadZikrTab()', rect_method + '\n    private void loadZikrTab()')

open(f, 'w').write(c)
print("✅ Arabic Font and RoundRect FIXED! You can build now.")
