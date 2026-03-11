import os, re
java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# Theme Button text থেকে image এ রূপান্তর
new_theme = 'View themeToggleBtn = ui.getRoundImage(isDarkTheme ? "ic_moon" : "ic_sun", 6, android.graphics.Color.TRANSPARENT, colorAccent);'
mc = re.sub(r'TextView themeToggleBtn = new TextView\(this\);\s*themeToggleBtn\.setText\([^;]+;\s*themeToggleBtn\.setGravity\([^;]+;\s*themeToggleBtn\.setTextSize\([^;]+;', new_theme, mc)

# periodBtn এবং settingsBtn এর সাদা কালার মুছে থিম কালার বসানো
mc = re.sub(r'ui\.getRoundImage\("img_period", 6, android\.graphics\.Color\.TRANSPARENT, [^)]+\)', 'ui.getRoundImage("img_period", 6, android.graphics.Color.TRANSPARENT, colorAccent)', mc)
mc = re.sub(r'ui\.getRoundImage\("img_settings", 6, android\.graphics\.Color\.TRANSPARENT, [^)]+\)', 'ui.getRoundImage("img_settings", 6, android.graphics.Color.TRANSPARENT, colorAccent)', mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)
print("✅ ১. Top Icons Fixed!")
