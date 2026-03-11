import os, shutil

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ১. কোডের সর্বোচ্চ ক্ষমতা ব্যবহার করে Gradient + Bevel 3D তৈরি করা
            ultimate_3d = """
            try {
                int cCol = ((android.graphics.drawable.ColorDrawable)cb).getColor();
                float[] hsv = new float[3]; 
                
                // ডার্ক শ্যাডো কালার (নিচের অংশের জন্য)
                android.graphics.Color.colorToHSV(cCol, hsv);
                hsv[2] *= 0.70f; int shadowCol = android.graphics.Color.HSVToColor(hsv);
                
                // হাইলাইট কালার (ওপরের আলোর জন্য)
                android.graphics.Color.colorToHSV(cCol, hsv);
                hsv[1] *= 0.50f; hsv[2] = Math.min(1.0f, hsv[2] * 1.4f); int highCol = android.graphics.Color.HSVToColor(hsv);
                
                // লেয়ার ১: সলিড ডার্ক বেস (ভাসমান লুকের জন্য)
                android.graphics.drawable.GradientDrawable base = new android.graphics.drawable.GradientDrawable();
                base.setColor(shadowCol); base.setCornerRadius(16f * DENSITY);
                
                // লেয়ার ২: গ্রেডিয়েন্ট ফেস (আলো থেকে ছায়ার দিকে, কার্ভড লুকের জন্য)
                android.graphics.drawable.GradientDrawable face = new android.graphics.drawable.GradientDrawable(android.graphics.drawable.GradientDrawable.Orientation.TL_BR, new int[]{highCol, cCol, shadowCol});
                face.setCornerRadius(16f * DENSITY);
                
                // লেয়ার ৩: ইনার স্ট্রোক (কাঁচের মতো চকচকে বর্ডারের জন্য)
                android.graphics.drawable.GradientDrawable edge = new android.graphics.drawable.GradientDrawable();
                edge.setColor(0); edge.setStroke((int)(1.5f * DENSITY), highCol); edge.setCornerRadius(16f * DENSITY);
                
                // সব লেয়ার একসাথে করা
                android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{base, face, edge});
                ld.setLayerInset(0, 0, (int)(6*DENSITY), 0, 0); // বেস নিচে নামানো
                ld.setLayerInset(1, 0, 0, 0, (int)(6*DENSITY)); // মূল কার্ড ওপরে তোলা
                ld.setLayerInset(2, 0, 0, 0, (int)(6*DENSITY)); // বর্ডার ওপরে তোলা
                
                card.setBackground(ld);
            } catch(Exception e) { card.setBackground(cb); }
            """
            
            # আগের থ্রিডি কোড বা নরমাল ব্যাকগ্রাউন্ড রিপ্লেস করা
            if 'int cardCol = ((android.graphics.drawable.ColorDrawable)cb).getColor();' in new_content:
                # যদি আগের স্ক্রিপ্টের কোড থাকে, সেটা মুছে ফেলা
                import re
                new_content = re.sub(r'int cardCol.*?card\.setBackground\(ld\);', ultimate_3d, new_content, flags=re.DOTALL)
            elif 'card.setBackground(cb);' in new_content:
                new_content = new_content.replace('card.setBackground(cb);', ultimate_3d)

            # ২. উইজেট (Widget) বা স্ট্যাটস ফাইলের হারানো টেক্সট সাদা করা
            if 'Widget' in file or 'Helper' in file or 'Provider' in file:
                new_content = new_content.replace('Color.parseColor("#9A9A9F")', 'android.graphics.Color.WHITE')
                new_content = new_content.replace('Color.parseColor("#B0B0B5")', 'android.graphics.Color.WHITE')
                new_content = new_content.replace('Color.parseColor("#A0A0A5")', 'android.graphics.Color.WHITE')

            if new_content != content:
                # ১০০% নিরাপদ অ্যাটমিক রাইট
                backup_path = path + '.bak_max3d'
                shutil.copy2(path, backup_path)
                temp_path = path + '.tmp'
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                os.replace(temp_path, path)

print("Ultimate Code-based 3D Applied and Widget Text Fixed!")
