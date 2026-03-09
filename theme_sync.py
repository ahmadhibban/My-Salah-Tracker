import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# ১. গোল বৃত্তের সিলভার বর্ডার মুছে থিমের কালার (accentCol) দিয়ে মেটালিক গ্রেডিয়েন্ট তৈরি করা
old_ring = """android.graphics.SweepGradient metallic = new android.graphics.SweepGradient(centerX, circleY, new int[]{cardCol, Color.GRAY, cardCol, Color.LTGRAY, cardCol}, null);
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(30f); p.setShader(metallic);"""
                
new_ring = """android.graphics.SweepGradient themeRing = new android.graphics.SweepGradient(centerX, circleY, new int[]{cardCol, accentCol, cardCol, accentCol, cardCol}, null);
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(30f); p.setShader(themeRing);"""

code = code.replace(old_ring, new_ring)

# ২. টোটাল লেখার বক্সে থিমের কালার দিয়ে হালকা ফিল (Background) এবং স্পষ্ট বর্ডার তৈরি করা
old_total = """// ব্যাকগ্রাউন্ড
                p.setStyle(Paint.Style.FILL); p.setColor(cardCol);
                p.setShadowLayer(8f, 0, 4f, Color.argb(40, 0, 0, 0));
                canvas.drawRoundRect(totalRect, 40f, 40f, p); p.clearShadowLayer();
                
                // চিকন বর্ডার (থিমের অ্যাকসেন্ট কালারে)
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(3f); p.setColor(accentCol);
                canvas.drawRoundRect(totalRect, 40f, 40f, p);"""

new_total = """// থিম কালারে হালকা ফিল
                p.setStyle(Paint.Style.FILL); p.setColor(accentCol); p.setAlpha(30);
                canvas.drawRoundRect(totalRect, 40f, 40f, p); p.setAlpha(255);
                
                // থিম কালারে স্পষ্ট বর্ডার
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(4f); p.setColor(accentCol);
                canvas.drawRoundRect(totalRect, 40f, 40f, p);"""

code = code.replace(old_total, new_total)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Perfect! Circle border and Total Box are now beautifully synced with your 6 Salah themes.")
