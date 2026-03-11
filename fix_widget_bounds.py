import os

for root, _, files in os.walk('.'):
    for file in files:
        # শুধু উইজেট বা স্ট্যাটস সম্পর্কিত ফাইলগুলোতে কাজ করবে
        if 'Widget' in file or 'Helper' in file or 'Provider' in file:
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ফন্ট সাইজ ছোট করে আগের অবস্থায় (বা তার চেয়েও ছোট) আনা হচ্ছে
            new_content = new_content.replace('setTextSize(14)', 'setTextSize(11)')
            new_content = new_content.replace('setTextSize(13)', 'setTextSize(10)')
            new_content = new_content.replace('setTextSize(12)', 'setTextSize(10)')
            new_content = new_content.replace('setTextSize(20)', 'setTextSize(16)')
            new_content = new_content.replace('setTextSize(22)', 'setTextSize(18)')
            
            # অতিরিক্ত প্যাডিং কমিয়ে দেওয়া হচ্ছে যাতে লেখা জায়গা পায়
            new_content = new_content.replace('setPadding((int)(16*DENSITY)', 'setPadding((int)(8*DENSITY)')
            new_content = new_content.replace('setPadding((int)(12*DENSITY)', 'setPadding((int)(6*DENSITY)')
            new_content = new_content.replace('setPadding((int)(8*DENSITY)', 'setPadding((int)(4*DENSITY)')

            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Widget font sizes and padding reduced to fit the bounds perfectly!")
