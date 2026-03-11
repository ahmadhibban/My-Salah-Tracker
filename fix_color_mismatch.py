import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('MainActivity.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ১. ডার্ক থিমের পারফেক্ট রিস্টার্ট (জিরো অ্যানিমেশন)
            content = re.sub(r'isDarkTheme = !isDarkTheme; sp\.edit\(\)\.putBoolean\("is_dark_mode", isDarkTheme\)\.apply\(\);.*?loadTodayPage\(\);\s*refreshWidget\(\);', r'sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); finish(); startActivity(getIntent().addFlags(android.content.Intent.FLAG_ACTIVITY_NO_ANIMATION)); overridePendingTransition(0, 0);', content, flags=re.DOTALL)
            
            # ২. কালার পরিবর্তনের পারফেক্ট রিস্টার্ট (জিরো অ্যানিমেশন)
            content = re.sub(r'activeTheme = \(activeTheme \+ 1\) % 6; sp\.edit\(\)\.putInt\("app_theme", activeTheme\)\.apply\(\);.*?loadTodayPage\(\);\s*refreshWidget\(\);', r'sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply(); finish(); startActivity(getIntent().addFlags(android.content.Intent.FLAG_ACTIVITY_NO_ANIMATION)); overridePendingTransition(0, 0);', content, flags=re.DOTALL)
            
            # ৩. ভাষা পরিবর্তনের পারফেক্ট রিস্টার্ট (জিরো অ্যানিমেশন)
            content = re.sub(r'String nextL = sp\.getString\("app_lang", "en"\)\.equals\("en"\) \? "bn" : "en"; sp\.edit\(\)\.putString\("app_lang", nextL\)\.apply\(\);.*?loadTodayPage\(\);\s*refreshWidget\(\);', r'String nextL = sp.getString("app_lang", "en").equals("en") ? "bn" : "en"; sp.edit().putString("app_lang", nextL).apply(); finish(); startActivity(getIntent().addFlags(android.content.Intent.FLAG_ACTIVITY_NO_ANIMATION)); overridePendingTransition(0, 0);', content, flags=re.DOTALL)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

print("Color mismatch fixed! Settings will now update perfectly with zero lag.")
