import os, re

for root, _, files in os.walk('.'):
    for file in files:
        path = os.path.join(root, file)
        
        # ১. উইজেটের আসল ফিক্স (XML ফাইলগুলো স্ক্যান করে লেখা সাদা করা)
        if file.endswith('.xml') and ('res/layout' in path.replace('\\', '/')):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            # ডার্ক ব্যাকগ্রাউন্ডে হারিয়ে যাওয়া গ্রে কালারগুলোকে সাদা করে দেওয়া
            new_content = new_content.replace('#A0A0A5', '#FFFFFF').replace('#9A9A9F', '#FFFFFF').replace('#B0B0B5', '#FFFFFF')
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
        # ২. জঘন্য গ্রেডিয়েন্ট থ্রিডি মুছে একদম সলিড ও ক্লিন থ্রিডি বসানো
        elif file.endswith('.java'):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            new_content = content
            
            clean_solid_3d = """
            try {
                int cCol = ((android.graphics.drawable.ColorDrawable)cb).getColor();
                
                // সলিড 3D বেসের জন্য কার্ডের চেয়ে ৪০% গাঢ় রং
                float[] hsv = new float[3];
                android.graphics.Color.colorToHSV(cCol, hsv);
                hsv[2] *= 0.60f; 
                int shadowCol = android.graphics.Color.HSVToColor(hsv);

                // নিচের সলিড শ্যাডো লেয়ার (কোনো ব্লার বা গ্রেডিয়েন্ট ছাড়া)
                android.graphics.drawable.GradientDrawable bottom = new android.graphics.drawable.GradientDrawable();
                bottom.setColor(shadowCol); 
                bottom.setCornerRadius(16f * DENSITY);

                // ওপরের মূল কার্ড লেয়ার
                android.graphics.drawable.GradientDrawable top = new android.graphics.drawable.GradientDrawable();
                top.setColor(cCol); 
                top.setCornerRadius(16f * DENSITY);

                // দুটি লেয়ার একসাথে করে পারফেক্ট 3D বাটন তৈরি
                android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{bottom, top});
                ld.setLayerInset(0, 0, 0, 0, 0); // নিচের শ্যাডো পুরো জায়গা নেবে
                ld.setLayerInset(1, 0, 0, 0, (int)(5*DENSITY)); // ওপরের কার্ড ৫ পিক্সেল ওপরে থাকবে
                
                card.setBackground(ld);
            } catch(Exception e) { card.setBackground(cb); }
            """
            
            # আগের বাজে থ্রিডি কোড খুঁজে বের করে রিপ্লেস করা
            if 'Orientation.TL_BR' in content and 'hsv[2] * 1.4f' in content:
                new_content = re.sub(r'try\s*\{\s*int cCol.*?catch\(Exception e\)\s*\{\s*card\.setBackground\(cb\);\s*\}', clean_solid_3d, new_content, flags=re.DOTALL)
                
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Widgets Fixed (XML scanned) & Clean Solid 3D Applied!")
