import os
import re

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# ১. ড্রয়িং লজিক (onDraw) আপডেট
draw_replacement = """
                // আইকন দুটি স্ক্রিনের দুই কোণায় (১৫% দূরত্বে) রাখা হলো
                float sideMargin = w * 0.15f; 
                float[] iconXs = {sideMargin, w - sideMargin};
                String[] icons = {"↻", (isSoundOn[0] ? "🔊" : "🔇")};
                int[] ringColors = { Color.parseColor("#2E7D32"), Color.parseColor("#E65100") };

                for(int i=0; i<2; i++) {
                    float shift = (pressedButton == i) ? 8f : 0f; 
                    float currentX = iconXs[i];
                    
                    p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(10f); p.setColor(ringColors[i]);
                    canvas.drawCircle(currentX, btnY + shift, 80f, p);
                    
                    p.setStyle(Paint.Style.FILL); p.setColor(themeColors != null ? themeColors[1] : Color.WHITE);
                    if (pressedButton != i) p.setShadowLayer(15, 0, 10, Color.LTGRAY);
                    canvas.drawCircle(currentX, btnY + shift, 75f, p); p.clearShadowLayer();
                    
                    p.setTextAlign(Paint.Align.CENTER); p.setColor(ringColors[i]); p.setTypeface(Typeface.DEFAULT);
                    p.setTextSize((i==0)?100f:70f); 
                    canvas.drawText(icons[i], currentX, btnY + shift + ((i==0)?35f:25f), p);
                }
                
                float sweep"""

code = re.sub(r'float btnSp = w / 3;.*?float sweep', draw_replacement, code, flags=re.DOTALL)

# ২. টাচ লজিক (onTouch) আপডেট
touch_replacement = """
                    float sideMargin = w * 0.15f;
                    float[] iconXs = {sideMargin, w - sideMargin};
                    
                    if (Math.abs(y - btnY) < 110) {
                        if (Math.abs(x - iconXs[0]) < 90) { 
                            new android.app.AlertDialog.Builder(v.getContext()).setTitle("Reset").setMessage("Do you want to reset counts for this Dua?")
                                .setPositiveButton("Yes", (dialog, which) -> { individualCounts[idx] = 0; individualTotals[idx] = 0; individualRounds[idx] = 0; v.invalidate(); v.getContext().getSharedPreferences("TasbihPrefs", 0).edit().putInt("ind_"+idx, 0).putInt("total_"+idx, 0).putInt("round_"+idx, 0).apply(); }).setNegativeButton("No", null).show(); return true;
                        } else if (Math.abs(x - iconXs[1]) < 90) { 
                            isSoundOn[0] = !isSoundOn[0]; v.invalidate(); return true; 
                        }
                    }"""

code = re.sub(r'if\s*\(\s*Math\.abs\(y\s*-\s*[a-zA-Z0-9_]+\)\s*<\s*1[01]0\s*\)\s*\{.*?return\s*true;\s*\}\s*\}', touch_replacement, code, flags=re.DOTALL)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: Icons successfully pushed to the edges!")
