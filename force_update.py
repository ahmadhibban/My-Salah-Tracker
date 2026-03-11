import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            changed = False
            for i in range(len(lines)):
                # ১. আপনার কাঙ্ক্ষিত সলিড থ্রিডি শ্যাডো জোরপূর্বক অ্যাপ্লাই করা
                if 'card.setBackground(cb);' in lines[i] and 'shadowDrawable' not in lines[i]:
                    lines[i] = lines[i].replace('card.setBackground(cb);', '''
                    try {
                        android.graphics.drawable.LayerDrawable shadowDrawable = (android.graphics.drawable.LayerDrawable) androidx.core.content.ContextCompat.getDrawable(card.getContext(), R.drawable.premium_3d_shadow);
                        android.graphics.drawable.GradientDrawable mainCard = (android.graphics.drawable.GradientDrawable) shadowDrawable.getDrawable(1);
                        mainCard.setColor(((android.graphics.drawable.ColorDrawable)cb).getColor());
                        card.setBackground(shadowDrawable);
                    } catch(Exception e) { card.setBackground(cb); }
                    ''')
                    changed = True
                
                # ২. উইজেটের হারানো লেখাগুলো ফিরিয়ে আনতে টেক্সট কালার পিওর সাদা (White) করে দেওয়া
                if 'Color.parseColor("#9A9A9F")' in lines[i] or 'Color.parseColor("#B0B0B5")' in lines[i] or 'Color.parseColor("#A0A0A5")' in lines[i]:
                    lines[i] = re.sub(r'Color\.parseColor\("#[9AB]0[9AB]0[9AB][5F]"\)', 'android.graphics.Color.WHITE', lines[i])
                    changed = True

                # ৩. থিম পরিবর্তনের বাজে রিস্টার্ট অ্যানিমেশনটি জিরো (০) করে দেওয়া
                if 'overridePendingTransition' in lines[i] and 'overridePendingTransition(0, 0)' not in lines[i]:
                    lines[i] = re.sub(r'overridePendingTransition\([^)]+\);', 'overridePendingTransition(0, 0);', lines[i])
                    changed = True
                    
            if changed:
                with open(path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

print("Force Update Complete! Solid 3D Shadow added, Widget Text restored, and Transitions muted.")
