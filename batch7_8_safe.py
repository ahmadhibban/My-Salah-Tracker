import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            # ১. ফাইল রিড
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ফিক্স ৩১: নামাজের কার্ডগুলোতে আধুনিক 'Ripple Effect' (জলের ঢেউয়ের মতো টাচ অ্যানিমেশন) যুক্ত করা
            new_content = new_content.replace('card.setBackground(cb);', 'card.setBackground(cb); if(android.os.Build.VERSION.SDK_INT>=23) card.setForeground(card.getContext().getDrawable(android.R.attr.selectableItemBackground));')
            
            # ফিক্স ৩২: অ্যাপের সমস্ত কাস্টম বাটনগুলোতে (Mark All / Save) Ripple Effect দেওয়া
            new_content = re.sub(r'(Button\s+(\w+)\s*=\s*new\s+Button\([^)]+\);)', r'\1 if(android.os.Build.VERSION.SDK_INT>=23) \2.setForeground(\2.getContext().getDrawable(android.R.attr.selectableItemBackground));', new_content)
            
            # ফিক্স ৩৩: ভিজ্যুয়াল হায়ারার্কি ঠিক করতে হেডারের টাইটেলগুলোকে (Size 20) বোল্ড (Bold) করা
            new_content = re.sub(r'(\w+)\.setTextSize\(20\);', r'\1.setTextSize(20); \1.setTypeface(null, android.graphics.Typeface.BOLD);', new_content)
            
            # ফিক্স ৩৪: ডায়ালগের প্রধান টাইটেলগুলোকেও (Size 22) স্পষ্টভাবে বোঝাতে বোল্ড করা
            new_content = re.sub(r'(\w+)\.setTextSize\(22\);', r'\1.setTextSize(22); \1.setTypeface(null, android.graphics.Typeface.BOLD);', new_content)
            
            # ফিক্স ৩৫-৩৬: কাস্টম ডায়ালগের বাইরে (Backdrop) ক্লিক করলে যেন ডায়ালগ সহজে বন্ধ হয়ে যায় (CanceledOnTouchOutside)
            new_content = re.sub(r'([a-zA-Z0-9_]+)\.setContentView\(([^)]+)\);\s*\1\.show\(\);', r'\1.setContentView(\2); \1.setCanceledOnTouchOutside(true); \1.show();', new_content)
            
            # ফিক্স ৩৭: সাব-টাইটেল বা ছোট ডেসক্রিপশনের কালার আরও একটু মিউট করা যেন মেইন টেক্সট ফোকাস পায়
            new_content = new_content.replace('Color.parseColor("#B0B0B5")', 'Color.parseColor("#9A9A9F")')
            
            # ফিক্স ৩৮: উইজেট বা ছোট কার্ডের স্পেসিংয়ে ভারসাম্য আনা
            new_content = new_content.replace('setPadding((int)(10*DENSITY)', 'setPadding((int)(12*DENSITY)')
            
            # ফিক্স ৩৯: 'QAZA' বা 'STREAK' ব্যাজগুলোর প্যাডিং বাড়িয়ে আরেকটু রাউন্ডেড ফিল দেওয়া
            new_content = new_content.replace('setPadding((int)(6 * DENSITY), (int)(2 * DENSITY)', 'setPadding((int)(8 * DENSITY), (int)(4 * DENSITY)')
            
            # ফিক্স ৪০: টেক্সট সাইজ ১৩-কে একটু মডিফাই করে স্ট্যান্ডার্ড ১৪-তে নিয়ে আসা
            new_content = new_content.replace('setTextSize(13)', 'setTextSize(14)')

            # ২. পরিবর্তন হলে ফাইলে সেভ করা হবে
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Batch 7 & 8 (Design 31-40) applied safely!")
