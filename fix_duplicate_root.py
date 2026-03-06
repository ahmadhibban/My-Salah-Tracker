import os
import re

path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # আগের ভুল ডিক্লেয়ারেশনগুলো মুছে ফেলা হচ্ছে
    content = content.replace('android.widget.FrameLayout root = activity.findViewById(android.R.id.content);', '')
    content = content.replace('FrameLayout root = activity.findViewById(android.R.id.content);', '')
    
    # root এর জায়গায় সরাসরি ফ্রেমলেআউট কল করা হচ্ছে
    content = re.sub(r'ui\.showSmartBanner\s*\(\s*root\s*,', 'ui.showSmartBanner((android.widget.FrameLayout) activity.findViewById(android.R.id.content),', content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Duplicate 'root' variable completely fixed!")
else:
    print("❌ File not found.")
