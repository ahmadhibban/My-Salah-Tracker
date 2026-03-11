import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('MainActivity.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ১. কার্ডে ক্লিকের ফ্ল্যাশ (LayoutTransition) রিমুভ করা
            content = content.replace('contentArea.setLayoutTransition(new android.animation.LayoutTransition());', 'contentArea.setLayoutTransition(null);')
            
            # ২. ডার্ক/লাইট থিম পরিবর্তনের রিস্টার্ট (finish) বন্ধ করে ডাইনামিক আপডেট
            theme_old = r'sp\.edit\(\)\.putBoolean\("is_dark_mode", !isDarkTheme\)\.apply\(\);\s*finish\(\);\s*(?:android\.content\.)?Intent tIntent = getIntent\(\);\s*tIntent\.addFlags\((?:android\.content\.)?Intent\.FLAG_ACTIVITY_NO_ANIMATION\);\s*startActivity\(tIntent\);\s*overridePendingTransition\([^;]+\);'
            theme_new = '''isDarkTheme = !isDarkTheme; sp.edit().putBoolean("is_dark_mode", isDarkTheme).apply();
                if (isDarkTheme) { themeColors[0] = android.graphics.Color.parseColor("#121212"); themeColors[1] = android.graphics.Color.parseColor("#1C1C1E"); themeColors[2] = android.graphics.Color.parseColor("#FFFFFF"); themeColors[3] = android.graphics.Color.parseColor("#9A9A9F"); themeColors[4] = android.graphics.Color.parseColor("#2C2C2E"); }
                else { themeColors[0] = android.graphics.Color.parseColor("#F8FAFC"); themeColors[1] = android.graphics.Color.parseColor("#FFFFFF"); themeColors[2] = android.graphics.Color.parseColor("#141416"); themeColors[3] = android.graphics.Color.parseColor("#64748B"); themeColors[4] = android.graphics.Color.parseColor("#E2E8F0"); }
                if (android.os.Build.VERSION.SDK_INT >= 21) { getWindow().setStatusBarColor((!isDarkTheme && android.os.Build.VERSION.SDK_INT < 23) ? android.graphics.Color.parseColor("#40000000") : android.graphics.Color.TRANSPARENT); getWindow().setNavigationBarColor(themeColors[0]); getWindow().getDecorView().setSystemUiVisibility(android.view.View.SYSTEM_UI_FLAG_LAYOUT_STABLE | android.view.View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | (!isDarkTheme && android.os.Build.VERSION.SDK_INT >= 23 ? android.view.View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR : 0)); }
                loadTodayPage(); refreshWidget();'''
            content = re.sub(theme_old, theme_new, content)
            
            # ৩. কালার পরিবর্তনের রিস্টার্ট (finish) বন্ধ করে ডাইনামিক আপডেট
            color_old = r'sp\.edit\(\)\.putInt\("app_theme", \(activeTheme \+ 1\) % 6\)\.apply\(\);\s*finish\(\);.*?(?:overridePendingTransition\([^;]+\);)'
            color_new = '''activeTheme = (activeTheme + 1) % 6; sp.edit().putInt("app_theme", activeTheme).apply();
                String[] themeAccents = {"#00BFA5", "#3B82F6", "#FF9559", "#D81B60", "#A67BFF", "#3BCC75"};
                colorAccent = android.graphics.Color.parseColor(themeAccents[activeTheme]);
                themeColors[5] = android.graphics.Color.argb(40, android.graphics.Color.red(colorAccent), android.graphics.Color.green(colorAccent), android.graphics.Color.blue(colorAccent));
                loadTodayPage(); refreshWidget();'''
            content = re.sub(color_old, color_new, content, flags=re.DOTALL)
            
            # ৪. ভাষা পরিবর্তনের রিস্টার্ট (finish) বন্ধ করে ডাইনামিক আপডেট
            lang_old = r'String nextL = sp\.getString\("app_lang", "en"\)\.equals\("en"\) \? "bn" : "en";\s*sp\.edit\(\)\.putString\("app_lang", nextL\)\.apply\(\);\s*finish\(\);.*?(?:overridePendingTransition\([^;]+\);)'
            lang_new = '''String nextL = sp.getString("app_lang", "en").equals("en") ? "bn" : "en"; sp.edit().putString("app_lang", nextL).apply();
                lang = new LanguageEngine(nextL); ui = new UIComponents(MainActivity.this, DENSITY, themeColors, lang);
                try { if(nextL.equals("bn")) { appFonts[0] = android.graphics.Typeface.createFromAsset(getAssets(), "fonts/hind_reg.ttf"); appFonts[1] = android.graphics.Typeface.createFromAsset(getAssets(), "fonts/hind_bold.ttf"); } else { appFonts[0] = android.graphics.Typeface.createFromAsset(getAssets(), "fonts/poppins_reg.ttf"); appFonts[1] = android.graphics.Typeface.createFromAsset(getAssets(), "fonts/poppins_bold.ttf"); } } catch(Exception e){}
                loadTodayPage(); refreshWidget();'''
            content = re.sub(lang_old, lang_new, content, flags=re.DOTALL)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

print("All restarts removed! App will now update instantly in-place.")
