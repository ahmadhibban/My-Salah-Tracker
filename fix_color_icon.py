import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
try:
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    
    # 1. সব অ্যাম্বার/গোল্ডেন কালার মুছে ডাইনামিক থিম কালার (colorAccent) সেট করা
    c = c.replace('android.graphics.Color.parseColor("#F59E0B")', 'colorAccent')
    c = c.replace('Color.parseColor("#F59E0B")', 'colorAccent')

    # 2. অ্যাডভান্সড লজিক দিয়ে ⭐ আইকন মুছে কাস্টম ইমেজ বসানো
    pattern = r'(?:android\.widget\.)?TextView\s+iconView\s*=\s*new\s+(?:android\.widget\.)?TextView\([^)]+\);\s*iconView\.setText\([^)]+\);\s*iconView\.setTextSize\([^)]+\);\s*iconView\.setGravity\([^)]+\);\s*main\.addView\(iconView\);'
    
    replacement = r'''android.view.View iconView = ui.getRoundImage("img_custom_nafl", 0, android.graphics.Color.TRANSPARENT, colorAccent); android.widget.LinearLayout.LayoutParams icLp = new android.widget.LinearLayout.LayoutParams((int)(60*DENSITY), (int)(60*DENSITY)); icLp.gravity = android.view.Gravity.CENTER; icLp.setMargins(0, 0, 0, (int)(15*DENSITY)); iconView.setLayoutParams(icLp); main.addView(iconView);'''
    
    c = re.sub(pattern, replacement, c)

    # 3. লিস্টের নামের আগে থেকে এক্সট্রা ⭐ মুছে ফেলা
    c = c.replace('"⭐ " + cName', 'cName')
    c = c.replace('tv.setText("⭐ " + cName);', 'tv.setText(cName);')

    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)
    print("✅ Custom Icon & Theme Colors PERFECTLY Restored! YOU CAN BUILD NOW.")
except Exception as e:
    print("Error:", e)
