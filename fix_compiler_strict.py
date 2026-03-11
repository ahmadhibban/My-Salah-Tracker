import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ফিক্স ১: ফন্ট সাইজের পূর্ণসংখ্যার পাশে 'f' বসানো (যেমন 11 কে 11f করা)
            new_content = re.sub(r'\.setTextSize\((\d+)\)', r'.setTextSize(\1f)', new_content)
            
            # ফিক্স ২: RemoteViews এর ফন্ট সাইজে 'f' বসানো
            new_content = re.sub(r'\.setTextViewTextSize\(([^,]+),\s*([^,]+),\s*(\d+)\)', r'.setTextViewTextSize(\1, \2, \3f)', new_content)
            
            # ফিক্স ৩: RemoteViews এর প্যাডিং মেথডের নাম ঠিক করা (setPadding -> setViewPadding)
            new_content = re.sub(r'\.setPadding\(R\.id\.', r'.setViewPadding(R.id.', new_content)

            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Compiler strict-type errors fixed successfully!")
