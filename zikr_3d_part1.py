import re
fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# ৩ডি শাইন এবং রিফ্লেকশন কোড আপডেট
new_bead_draw = """
                    // Main body with 3D Depth
                    p.setStyle(Paint.Style.FILL);
                    RadialGradient rg = new RadialGradient(bx - 15f, beadY - 15f, beadRadius * 1.5f, 
                        new int[]{beadThemes[currentBeadTheme][1], beadThemes[currentBeadTheme][0], Color.BLACK}, 
                        new float[]{0f, 0.8f, 1f}, Shader.TileMode.CLAMP);
                    p.setShader(rg);
                    p.setShadowLayer(25f, 5f, 15f, Color.argb(150, 0, 0, 0));
                    canvas.drawCircle(bx, beadY, beadRadius, p);
                    p.clearShadowLayer(); p.setShader(null);
                    
                    // Glossy Reflection (উপরের চকচকে অংশ)
                    p.setColor(Color.argb(200, 255, 255, 255));
                    canvas.drawOval(new RectF(bx - 25f, beadY - 35f, bx + 5f, beadY - 12f), p);
                    
                    // Bottom Light (নিচের দিক থেকে হালকা আলো)
                    p.setColor(Color.argb(80, 255, 255, 255));
                    canvas.drawOval(new RectF(bx - 10f, beadY + 18f, bx + 22f, beadY + 32f), p);
"""

# দানা ড্রয়িং এরিয়া পরিবর্তন
code = re.sub(r'// Main body.*?p\.setShader\(null\);.*?p\.setColor\(Color\.argb\(60, 255, 255, 255\)\);.*?canvas\.drawOval\(new RectF\(bx - 10f, beadY \+ 15f, bx \+ 20f, beadY \+ 30f\), p\);', 
              new_bead_draw, code, flags=re.DOTALL)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Part 1: High-End 3D Beads & Shine applied!")
