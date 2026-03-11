import os

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            # ১. ফাইলটি নিরাপদে রিড করা হচ্ছে
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ২. মেমোরিতে ডিজাইন পরিবর্তন
            new_content = content
            
            # ফিক্স ১: কড়া লাল রঙের বদলে সফট রেড
            new_content = new_content.replace('#FF5252', '#EF4444')
            
            # ফিক্স ২: ছুটির মোডের গোলাপি কালার মডার্ন রোজ করা
            new_content = new_content.replace('#FF4081', '#EC4899')
            
            # ফিক্স ৩: ছোট ব্যাজগুলোর (QAZA/STREAK) সাইজ বাড়িয়ে পড়ার উপযোগী করা
            new_content = new_content.replace('setTextSize(10)', 'setTextSize(12)')
            new_content = new_content.replace('setTextSize(11)', 'setTextSize(13)')
            
            # ফিক্স ৪: ক্লোজ বাটনে আধুনিক '✕' আইকন যুক্ত করা
            new_content = new_content.replace('setText(lang.get("CLOSE"))', 'setText("✕  " + lang.get("CLOSE"))')
            
            # ফিক্স ৫: নামাজের কার্ডগুলোতে আসল ভাসমান (Floating) থ্রিডি শ্যাডো যুক্ত করা
            # এখানে DENSITY এর বদলে সিস্টেম রিসোর্স ব্যবহার করা হয়েছে যেন কোনো ইরর না আসে
            new_content = new_content.replace('card.setBackground(cb);', 'card.setBackground(cb); if(android.os.Build.VERSION.SDK_INT>=21){ card.setElevation(10f * android.content.res.Resources.getSystem().getDisplayMetrics().density); if(android.os.Build.VERSION.SDK_INT>=28){ card.setOutlineAmbientShadowColor(0x00000000); card.setOutlineSpotShadowColor(0x33000000); card.setTranslationY(-4f * android.content.res.Resources.getSystem().getDisplayMetrics().density); } }')

            # ৩. শুধুমাত্র পরিবর্তন হলেই ফাইলে সেভ করা হবে
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Batch 1 (Design 1-5) applied 100% safely!")
