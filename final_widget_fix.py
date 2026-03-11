import os

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('SalahWidget.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ১. আসল কালপ্রিট: Center অ্যালাইনমেন্ট মুছে Left করে দেওয়া, যেন লেখা ফ্রেমের বাইরে না যায়
            new_content = new_content.replace('paint.setTextAlign(Paint.Align.CENTER);', 'paint.setTextAlign(Paint.Align.LEFT);')
            
            # ২. ছবির (Bitmap) ডানে-বামে একটু প্যাডিং বাড়ানো, যেন কোণা কেটে না যায়
            new_content = new_content.replace('Bitmap.createBitmap((int) w + 4, (int) h + 4', 'Bitmap.createBitmap((int) w + 16, (int) h + 8')
            new_content = new_content.replace('canvas.drawText(text, 2, -fm.ascent + 2', 'canvas.drawText(text, 8, -fm.ascent + 4')
            
            # ৩. উইজেটের ফন্ট সাইজ সামান্য কমানো যেন বক্সের ভেতর পারফেক্টলি ফিট হয়
            new_content = new_content.replace('18f, appFontBold', '16f, appFontBold')
            new_content = new_content.replace('14f, appFontBold', '12f, appFontBold')
            new_content = new_content.replace('13f, appFontBold', '11f, appFontBold')

            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Widget text rendering fixed! Sizes optimized and alignment corrected.")
