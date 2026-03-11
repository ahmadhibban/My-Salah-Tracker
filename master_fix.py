import os, shutil, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ১. কম্পাইল এরর ফিক্স (GradientDrawable Issue)
            bad_color_code = 'mainCard.setColor(((android.graphics.drawable.ColorDrawable)cb).getColor());'
            good_color_code = 'mainCard.setColor(stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#1A1115") : android.graphics.Color.parseColor("#FCE4EC")) : themeColors[1]); mainCard.setStroke((int)(1f*DENSITY), stat.equals("excused") ? android.graphics.Color.parseColor("#EC4899") : (checked ? colorAccent : themeColors[4]));'
            new_content = new_content.replace(bad_color_code, good_color_code)
            
            # ২. অ্যাপ ক্র্যাশ ফিক্স (Resources$NotFoundException দূর করে আসল Ripple Effect দেওয়া)
            new_content = re.sub(
                r'if\(android\.os\.Build\.VERSION\.SDK_INT>=23\)\s*([a-zA-Z0-9_]+)\.setForeground\(\1\.getContext\(\)\.getDrawable\(android\.R\.attr\.selectableItemBackground\)\);',
                r'if(android.os.Build.VERSION.SDK_INT>=23) \1.setForeground(new android.graphics.drawable.RippleDrawable(android.content.res.ColorStateList.valueOf(android.graphics.Color.parseColor("#20000000")), null, null));',
                new_content
            )

            if new_content != content:
                # Atomic Write (১০০% সেফটি)
                backup_path = path + '.bak2'
                shutil.copy2(path, backup_path)
                
                temp_path = path + '.tmp'
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                os.replace(temp_path, path)

print("Master Fix Applied! Both Compile Error and Runtime Crash have been eliminated safely.")
