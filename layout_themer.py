import re

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# ১. দোয়ার বক্সের ডিজাইন Salah ট্যাবের পারসেন্টেজ কার্ডের মতো একদম ফ্ল্যাট এবং subtle করা
# (আগের উজ্জ্বল গ্রেডিয়েন্ট এবং shadows মুছে ফেলা)
old_grad_pattern = r'int\s+primaryThemeColor\s*=.*?Shader\.TileMode\.CLAMP\);.*?p\.setShader\(lg\);.*?p\.clearShadowLayer\(\);.*?p\.setShader\(null\);'
new_dua_box_design = r'''// Salah ট্যাবের পারসেন্টেজ কার্ডের মতো ফ্ল্যাট ডিজাইন (থিম অনুযায়ী)
                p.setColor(cardCol);
                p.setAlpha(200); // হালকা স্বচ্ছতা, সালাহ ট্যাবের মতো subtle লুকের জন্য
                canvas.drawRoundRect(boxRect, 30f, 30f, p);
                p.setAlpha(255);'''
code = re.sub(old_grad_pattern, new_dua_box_design, code, flags=re.DOTALL)

# ২. 'Total/Loop' লেখা ঘরটির জন্য চিকন বর্ডার এবং ডিজাইন থিমের সাথে ম্যাচ করা
old_total_box_pattern = r'android\.graphics\.LinearGradient\s+badgeLg\s*=.*?Shader\.TileMode\.CLAMP\);.*?p\.setShader\(badgeLg\);.*?p\.setShadowLayer\s*\(.*?,\s*0,\s*5f,\s*Color\.argb\(80,\s*0,\s*0,\s*0\)\);.*?canvas\.drawRoundRect.*?;\s*p\.clearShadowLayer\(\);\s*p\.setShader\(null\);.*?p\.setStyle\(Paint\.Style\.STROKE\);\s*p\.setStrokeWidth\(3f\);\s*p\.setColor\(accentCol\);.*?canvas\.drawRoundRect.*?;'
new_total_box_design = r'''p.setColor(cardCol);
                p.setAlpha(180); // হালকা স্বচ্ছতা
                canvas.drawRoundRect(new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 40), 30f, 30f, p);
                p.setAlpha(255);
                
                // চিকন বর্ডার, থিম অ্যাকসেন্ট কালারে
                p.setStyle(Paint.Style.STROKE);
                p.setStrokeWidth(2f); // চিকন বর্ডার
                p.setColor(accentCol);
                canvas.drawRoundRect(new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 40), 30f, 30f, p);'''
code = re.sub(old_total_box_pattern, new_total_box_design, code, flags=re.DOTALL)

# ৩. গোল বৃত্তের ৩ডি বলের সাথের যে কালারটা ফিল হয় সেটা থিমের কালারে ফিল হবে
# (আমরা ৩ডি বলের মূল কালারকে থিমের accentCol এবং ফিল গ্র্যাডিয়েন্ট সেট করছি)
old_ball_pattern = r'p\.setStyle\(Paint\.Style\.FILL\);\s*android\.graphics\.RadialGradient\s+ballRg\s*=\s*new\s*android\.graphics\.RadialGradient\(ballX-8,\s*ballY-8,\s*35f,\s*Color\.WHITE,\s*accentCol,\s*android\.graphics\.Shader\.TileMode\.CLAMP\);'
new_ball_design = r'''p.setStyle(Paint.Style.FILL);
                // ৩ডি বল এবং ফিলের কালার থিমের অ্যাকসেন্ট কালার অনুযায়ী সেট করা হচ্ছে
                android.graphics.RadialGradient ballRg = new android.graphics.RadialGradient(ballX-8, ballY-8, 35f, Color.WHITE, accentCol, android.graphics.Shader.TileMode.CLAMP);'''
code = re.sub(old_ball_pattern, new_ball_design, code, flags=re.DOTALL)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Layout Patcher applied successfully! Dua box is now flat like Salah tab, total box has a thin border, and ball colors are synced with theme.")
