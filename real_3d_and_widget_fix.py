import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ১. আগের বাজে XML থ্রিডি মুছে ফেলা (যদি থাকে)
            bad_3d_pattern = r'try\s*\{[^}]*R\.drawable\.premium_3d_shadow[^}]*\}\s*catch[^}]*\}'
            new_content = re.sub(bad_3d_pattern, 'card.setBackground(cb);', new_content)
            
            # ২. একদম আসল, মডার্ন সলিড থ্রিডি (Duolingo Style) তৈরি করা
            real_3d_code = """
            int cardCol = ((android.graphics.drawable.ColorDrawable)cb).getColor();
            android.graphics.drawable.GradientDrawable top = new android.graphics.drawable.GradientDrawable();
            top.setColor(cardCol); top.setCornerRadius(16f * DENSITY);
            
            android.graphics.drawable.GradientDrawable bottom = new android.graphics.drawable.GradientDrawable();
            float[] hsv = new float[3]; android.graphics.Color.colorToHSV(cardCol, hsv);
            hsv[2] *= 0.75f; // কার্ডের কালার থেকে ২৫% গাঢ় করা হলো আসল থ্রিডি ডেপথের জন্য
            bottom.setColor(android.graphics.Color.HSVToColor(hsv)); bottom.setCornerRadius(16f * DENSITY);
            
            android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{bottom, top});
            ld.setLayerInset(0, 0, (int)(6*DENSITY), 0, 0); // নিচের গাঢ় ব্লকটি ৬ পিক্সেল নিচে নামানো হলো
            ld.setLayerInset(1, 0, 0, 0, (int)(6*DENSITY)); // ওপরের মূল কার্ডটি ৬ পিক্সেল ওপরে ওঠানো হলো
            card.setBackground(ld);
            """
            
            new_content = new_content.replace('card.setBackground(cb);', real_3d_code)
            
            # ৩. উইজেটের হারানো লেখা ফেরানো (উইজেট বা স্ট্যাটস ফাইলে গ্রে কালার হোয়াইট করা)
            if 'Widget' in file or 'Helper' in file or 'Provider' in file:
                new_content = new_content.replace('Color.parseColor("#9A9A9F")', 'android.graphics.Color.WHITE')
                new_content = new_content.replace('Color.parseColor("#B0B0B5")', 'android.graphics.Color.WHITE')
                new_content = new_content.replace('Color.parseColor("#A0A0A5")', 'android.graphics.Color.WHITE')

            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Pro-Level 3D Applied and Widget Text Restored!")
