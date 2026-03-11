import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ১. আগের ভুল কোডগুলো (setColorFilter) মুছে ফেলা হচ্ছে
    mc = re.sub(r'themeToggleBtn\.setColorFilter[^;]+;', '', mc)
    mc = re.sub(r'if\s*\([^)]+\)\s*offBtn\.setColorFilter[^;]+;', '', mc)
    mc = re.sub(r'if\s*\([^)]+\)\s*periodBtn\.setColorFilter[^;]+;', '', mc)
    mc = re.sub(r'settingsBtn\.setColorFilter[^;]+;', '', mc)

    # ২. স্মার্ট এবং সেফ কোড বসানো হচ্ছে (যেটা View এর টাইপ বুঝে কালার চেঞ্জ করবে)
    safe_tint_code = """
        try {
            if (themeToggleBtn instanceof android.widget.TextView) ((android.widget.TextView)themeToggleBtn).setTextColor(colorAccent);
            else if (themeToggleBtn.getBackground() != null) themeToggleBtn.getBackground().setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
            
            if (offBtn != null) {
                if (offBtn instanceof android.widget.TextView) ((android.widget.TextView)offBtn).setTextColor(colorAccent);
                else if (offBtn.getBackground() != null) offBtn.getBackground().setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
            }
            if (periodBtn != null) {
                if (periodBtn instanceof android.widget.TextView) ((android.widget.TextView)periodBtn).setTextColor(colorAccent);
                else if (periodBtn.getBackground() != null) periodBtn.getBackground().setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
            }
            if (settingsBtn != null) {
                if (settingsBtn instanceof android.widget.TextView) ((android.widget.TextView)settingsBtn).setTextColor(colorAccent);
                else if (settingsBtn.getBackground() != null) settingsBtn.getBackground().setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
            }
        } catch(Exception e){}
    """
    
    if "themeToggleBtn instanceof android.widget.TextView" not in mc:
        mc = mc.replace("rightHeader.addView(settingsBtn);", "rightHeader.addView(settingsBtn);\n" + safe_tint_code)

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
    print("✔ ICON COLOR ERROR FIXED PERFECTLY!")
else:
    print("❌ FILE NOT FOUND")
