import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('MainActivity.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ১. chipBg এর কোড মুছে ফেলা
            content = re.sub(r'android\.graphics\.drawable\.GradientDrawable chipBg\s*=\s*new\s+android\.graphics\.drawable\.GradientDrawable\(\);.*?chipBg\.setStroke\([^;]+\);', '', content, flags=re.DOTALL)
            
            # ২. timeLayout, pName এবং checkLayout থেকে বাজে ব্যাকগ্রাউন্ড ও প্যাডিং মুছে ফেলা
            content = content.replace('timeLayout.setBackground(chipBg); timeLayout.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY));', '')
            content = content.replace('pName.setBackground(chipBg); pName.setPadding((int)(12*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY));', '')
            content = content.replace('checkLayout.setBackground(chipBg); checkLayout.setPadding((int)(12*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY));', '')

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

print("Ugly melted boxes removed! Design is back to normal.")
