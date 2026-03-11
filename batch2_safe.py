import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            # ১. নিরাপদে রিড
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ফিক্স: থ্রিডি শ্যাডো সম্পূর্ণ মুছে ফেলা এবং হারানো দাগ ফিরিয়ে আনা
            bad_3d = 'card.setBackground(cb); if(android.os.Build.VERSION.SDK_INT>=21){ card.setElevation(10f * android.content.res.Resources.getSystem().getDisplayMetrics().density); if(android.os.Build.VERSION.SDK_INT>=28){ card.setOutlineAmbientShadowColor(0x00000000); card.setOutlineSpotShadowColor(0x33000000); card.setTranslationY(-4f * android.content.res.Resources.getSystem().getDisplayMetrics().density); } }'
            new_content = new_content.replace(bad_3d, 'card.setBackground(cb);')
            
            # ফিক্স ৬: হেডারের আইকনগুলোর 'টাচ টার্গেট' বড় করা (ক্লিক করতে আরাম হবে)
            new_content = new_content.replace('(int)(34 * DENSITY)', '(int)(42 * DENSITY)')
            new_content = new_content.replace('(int)(34*DENSITY)', '(int)(42*DENSITY)')
            
            # ফিক্স ৭: কার্ডের বর্ডারগুলো (Stroke) চিকন ও প্রিমিয়াম করা (1.5 থেকে 1.0)
            new_content = new_content.replace('1.5f*DENSITY', '1f*DENSITY')
            new_content = new_content.replace('1.5f * DENSITY', '1f * DENSITY')
            
            # ফিক্স ৮: ডায়ালগ ওপেন হলে পেছনের স্ক্রিন সুন্দরভাবে ব্লার বা Dim করা
            new_content = re.sub(r'([a-zA-Z0-9_\[\]]+)\.getWindow\(\)\.setBackgroundDrawableResource\(android\.R\.color\.transparent\);', r'\1.getWindow().setBackgroundDrawableResource(android.R.color.transparent); if(android.os.Build.VERSION.SDK_INT >= 14) { \1.getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_DIM_BEHIND); \1.getWindow().setDimAmount(0.50f); }', new_content)
            
            # ফিক্স ৯: মাল্টি-লাইন টেক্সটের লাইন স্পেসিং বাড়ানো (পড়তে আরাম হবে)
            new_content = new_content.replace('setLineSpacing(0, 1.2f)', 'setLineSpacing(0, 1.4f)')
            
            # ফিক্স ১০: অ্যাকশন বাটনগুলোর (Mark All / Today) ক্লিক এরিয়া বড় করা
            new_content = new_content.replace('setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY))', 'setPadding(0, (int)(16*DENSITY), 0, (int)(16*DENSITY))')
            new_content = new_content.replace('setPadding((int)(10*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY), (int)(12*DENSITY))', 'setPadding((int)(10*DENSITY), (int)(16*DENSITY), (int)(10*DENSITY), (int)(16*DENSITY))')

            # ২. শুধু পরিবর্তন হলেই রাইট করবে
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Batch 2 (Design 6-10 & 3D Fix) applied safely!")
