import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('MainActivity.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ১. ইনার চিপ বা ছোট বক্সের জন্য মডার্ন ব্যাকগ্রাউন্ড ডিজাইন তৈরি (হালকা ব্যাকগ্রাউন্ড + বর্ডার)
            chip_bg_code = '''
            android.graphics.drawable.GradientDrawable chipBg = new android.graphics.drawable.GradientDrawable();
            chipBg.setColor(isDarkTheme ? android.graphics.Color.parseColor("#1A1A1C") : android.graphics.Color.parseColor("#F1F5F9"));
            chipBg.setCornerRadius(12f * DENSITY);
            chipBg.setStroke((int)(1f * DENSITY), isDarkTheme ? android.graphics.Color.parseColor("#2C2C2E") : android.graphics.Color.parseColor("#E2E8F0"));
            '''
            
            # আইকন এবং সময়ের অংশটিকে আলাদা বক্স বানানো
            if 'timeLayout.setBackground(chipBg);' not in new_content:
                new_content = re.sub(r'(LinearLayout\s+timeLayout\s*=\s*new\s+LinearLayout\(this\);)',
                                     chip_bg_code + r'\1 timeLayout.setBackground(chipBg); timeLayout.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY));', new_content)
            
            # নামাজের নামের অংশটিকে আলাদা বক্স বানানো
            if 'pName.setBackground(chipBg);' not in new_content:
                new_content = re.sub(r'(TextView\s+pName\s*=\s*new\s+TextView\(this\);)',
                                     r'\1 pName.setBackground(chipBg); pName.setPadding((int)(12*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY));', new_content)
            
            # সুন্নত ও চেকবক্সের অংশটিকে আলাদা বক্স বানানো
            if 'checkLayout.setBackground(chipBg);' not in new_content:
                new_content = re.sub(r'(LinearLayout\s+checkLayout\s*=\s*new\s+LinearLayout\(this\);)',
                                     r'\1 checkLayout.setBackground(chipBg); checkLayout.setPadding((int)(12*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY));', new_content)
            
            # ২. কার্ডে ক্লিকের ফ্ল্যাশ বা লাফানো বন্ধ করা (RemoveAllViews Fix)
            # চেকবক্সে ক্লিক করলে যেন loadTodayPage() কল হয়ে পুরো পেজ রিলোড না হয়, শুধু উইজেট আপডেট হয়।
            new_content = new_content.replace('loadTodayPage(); refreshWidget();', '/* Removed loadTodayPage to fix flash */ refreshWidget(); if(circleView != null) circleView.invalidate();')

            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Master Plan Executed! Inner boxes created and Checkbox flash eliminated.")
