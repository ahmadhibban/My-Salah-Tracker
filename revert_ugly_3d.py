import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # আগের বাজে থ্রিডি ব্লকটি খুঁজে বের করে অরিজিনাল কোডে (card.setBackground(cb)) ফেরত নেওয়া
            ugly_3d_pattern = r'try\s*\{\s*int cCol\s*=\s*\(\(android\.graphics\.drawable\.ColorDrawable\)cb\)\.getColor\(\);.*?catch\(Exception e\)\s*\{\s*card\.setBackground\(cb\);\s*\}'
            new_content = re.sub(ugly_3d_pattern, 'card.setBackground(cb);', content, flags=re.DOTALL)
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Ugly 3D removed! Cards are back to their original clean state.")
