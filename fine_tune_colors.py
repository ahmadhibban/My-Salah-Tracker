import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. ব্যানার এবং থিম বাটনের জন্য ডাইনামিক নীল/হলুদ কালার লজিক
theme_color_logic = "(isDarkTheme ? android.graphics.Color.parseColor(\"#1E88E5\") : android.graphics.Color.parseColor(\"#F59E0B\"))"

# Progress Card এর শ্যাডো কালার আপডেট
content = re.sub(r'applyCssToView\(\s*pCard\s*,\s*pcBg\s*,\s*colorAccent', f'applyCssToView(pCard, pcBg, {theme_color_logic}', content)

# Theme Toggle Button এর শ্যাডো কালার আপডেট
content = re.sub(r'applyCssToView\(\s*themeToggleBtn\s*,\s*([a-zA-Z0-9_.]+)\s*,\s*colorAccent', rf'applyCssToView(themeToggleBtn, \1, {theme_color_logic}', content)

# ২. ওপরের আইকনগুলোর ভেতরের রং পরিবর্তন (থিম বাটন নীল/হলুদ, বাকিগুলো সাদা)
icon_colors = f"""
        try {{
            int dynCol = {theme_color_logic};
            if(themeToggleBtn instanceof TextView) ((TextView)themeToggleBtn).setTextColor(dynCol);
            if(settingsBtn instanceof TextView) ((TextView)settingsBtn).setTextColor(android.graphics.Color.WHITE);
            if(periodBtn instanceof TextView) ((TextView)periodBtn).setTextColor(android.graphics.Color.WHITE);
            if(offBtn instanceof TextView) ((TextView)offBtn).setTextColor(android.graphics.Color.WHITE);
        }} catch(Exception e) {{}}
"""
content = re.sub(r'(applyCssToView\(\s*themeToggleBtn[^;]+;\s*)', r'\1' + icon_colors, content)

# ৩. ৭ দিনের ঘরের লেখা সাদা করা এবং সিলেক্টেড দিনটিকে প্রফেশনালি ১৫% বড় করা
day_mod = """applyCssToView(t, getProgressBorder(dKey, isSel), colorAccent, 10f, false);
            t.setTextColor(android.graphics.Color.WHITE);
            // প্রফেশনাল স্কেলিং ইফেক্ট
            if (isSel) {
                t.setScaleX(1.15f);
                t.setScaleY(1.15f);
            } else {
                t.setScaleX(1.0f);
                t.setScaleY(1.0f);
            }"""
content = content.replace('applyCssToView(t, getProgressBorder(dKey, isSel), colorAccent, 10f, false);', day_mod)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Pro-level Colors & Selected Day Scaling applied successfully!")
