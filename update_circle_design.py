import os
import re

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

def replace_block(start_marker, end_marker, new_content, text):
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker, start_idx)
    if start_idx != -1 and end_idx != -1:
        return text[:start_idx] + new_content + text[end_idx:]
    else:
        print(f"Error: Could not find {start_marker}")
        return text

# ২. গোল বৃত্তের নতুন ডিজাইন (ছবির মতো)
new_circle_code = """// --- 2. Dynamic Progress Ring & Ball (New Design from Image) ---
                float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
                float rOuter = radius + 25f;
                
                // বৃত্তের ভেতরের অংশ ডার্ক করার জন্য
                p.setStyle(Paint.Style.FILL); p.setColor(Color.parseColor("#111111"));
                canvas.drawCircle(centerX, circleY, rOuter + 10f, p);

                // গোল বর্ডার/ট্র্যাক (ডার্ক গ্রে)
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(25f); p.setColor(Color.parseColor("#333333"));
                canvas.drawCircle(centerX, circleY, radius, p);
                
                // উজ্জ্বল সবুজ প্রোগ্রেস লাইন
                p.setStrokeWidth(25f); p.setStrokeCap(Paint.Cap.ROUND); p.setColor(Color.parseColor("#00E676")); // Bright Green
                canvas.drawArc(new RectF(centerX-radius, circleY-radius, centerX+radius, circleY+radius), -90, sweep, false, p);
                
                // সবুজ রঙের ৩ডি বল (প্রোগ্রেস লাইনের মাথায়)
                double angle = Math.toRadians(sweep - 90);
                float ballX = (float) (centerX + radius * Math.cos(angle)), ballY = (float) (circleY + radius * Math.sin(angle));
                p.setStyle(Paint.Style.FILL); 
                RadialGradient ballRg = new RadialGradient(ballX-5, ballY-5, 30f, Color.WHITE, Color.parseColor("#00E676"), Shader.TileMode.CLAMP);
                p.setShader(ballRg); p.setShadowLayer(15, 0, 8, Color.argb(150,0,0,0));
                canvas.drawCircle(ballX, ballY, 28f, p); p.clearShadowLayer(); p.setShader(null);

                // ভেতরে সাদা সংখ্যা ও লক্ষ্য
                p.setStyle(Paint.Style.FILL); if(bnFont != null) p.setTypeface(bnFont); p.setColor(Color.WHITE); 
                String mainCountStr = formatNum(curVal); String targetPart = " / " + formatNum(d.target); 
                p.setTextSize(260f); float mainTextWidth = p.measureText(mainCountStr);
                Paint targetPaint = new Paint(p); targetPaint.setTextSize(55f); targetPaint.setColor(Color.WHITE); 
                float targetWidth = targetPaint.measureText(targetPart); float startX = centerX - ((mainTextWidth + targetWidth) / 2f);
                p.setTextAlign(Paint.Align.LEFT); canvas.drawText(mainCountStr, startX, circleY + 85f, p);
                targetPaint.setTextAlign(Paint.Align.LEFT); canvas.drawText(targetPart, startX + mainTextWidth, circleY + 85f, targetPaint);

                """
code = replace_block("// --- 2.", "// --- 3.", new_circle_code, code)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success! Circular Zikr counter updated to the new design.")
