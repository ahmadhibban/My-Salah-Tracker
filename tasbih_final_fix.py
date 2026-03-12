import re
import os

file_path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# হুবহু ছবির মতো ডিজাইন - পিক্সেল পারফেক্ট
final_design = """
        // --- Premium 3D Tasbih (Final Fix) ---
        LinearLayout tasbihBox = new LinearLayout(this);
        tasbihBox.setOrientation(LinearLayout.VERTICAL);
        tasbihBox.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 0.9f));
        tasbihBox.setGravity(Gravity.RIGHT | Gravity.CENTER_VERTICAL);
        tasbihBox.setPadding(0, 0, (int)(10*DENSITY), 0);
        
        // 1. Digital Display Box (Inset Look)
        soup.neumorphism.NeumorphCardView tDispNeo = new soup.neumorphism.NeumorphCardView(this);
        tDispNeo.setShapeType(soup.neumorphism.ShapeType.PRESSED);
        tDispNeo.setShadowColorLight(isDarkTheme ? Color.parseColor("#333336") : Color.parseColor("#FFFFFF"));
        tDispNeo.setShadowColorDark(isDarkTheme ? Color.parseColor("#0A0A0C") : Color.parseColor("#cbd5e0"));
        tDispNeo.setBackgroundColor(isDarkTheme ? Color.parseColor("#151515") : Color.parseColor("#D1D9E6"));
        tDispNeo.setShadowElevation(6f * DENSITY);
        tDispNeo.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 15f*DENSITY).build());
        
        final TextView tCountTxt = new TextView(this);
        final android.content.SharedPreferences tSp = getSharedPreferences("MiniTasbih", MODE_PRIVATE);
        tCountTxt.setText(String.format("%03d", tSp.getInt("count", 0)));
        tCountTxt.setTextColor(colorAccent);
        tCountTxt.setTypeface(Typeface.MONOSPACE, Typeface.BOLD);
        tCountTxt.setTextSize(28f);
        tCountTxt.setGravity(Gravity.CENTER);
        tCountTxt.setPadding((int)(20*DENSITY), (int)(12*DENSITY), (int)(20*DENSITY), (int)(12*DENSITY));
        tDispNeo.addView(tCountTxt);
        
        // 2. Large Rounded Tap Button (3D Pop Look)
        final soup.neumorphism.NeumorphCardView tBtnNeo = new soup.neumorphism.NeumorphCardView(this);
        tBtnNeo.setShapeType(soup.neumorphism.ShapeType.FLAT);
        tBtnNeo.setBackgroundColor(colorAccent);
        tBtnNeo.setShadowElevation(10f * DENSITY); // High elevation for 3D effect
        tBtnNeo.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 40f*DENSITY).build());
        
        LinearLayout.LayoutParams btnLp = new LinearLayout.LayoutParams((int)(80*DENSITY), (int)(80*DENSITY));
        btnLp.gravity = Gravity.RIGHT;
        btnLp.setMargins(0, (int)(15*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));
        tBtnNeo.setLayoutParams(btnLp);
        
        tBtnNeo.setOnClickListener(v -> {
            tBtnNeo.setShapeType(soup.neumorphism.ShapeType.PRESSED);
            int cur = tSp.getInt("count", 0) + 1;
            tSp.edit().putInt("count", cur).apply();
            tCountTxt.setText(String.format("%03d", cur));
            try { ((android.os.Vibrator) getSystemService(VIBRATOR_SERVICE)).vibrate(35); } catch (Exception e) {}
            tBtnNeo.postDelayed(() -> tBtnNeo.setShapeType(soup.neumorphism.ShapeType.FLAT), 50);
        });
        
        tBtnNeo.setOnLongClickListener(v -> {
            tSp.edit().putInt("count", 0).apply();
            tCountTxt.setText("000");
            try { ((android.os.Vibrator) getSystemService(VIBRATOR_SERVICE)).vibrate(100); } catch (Exception e) {}
            return true;
        });

        tasbihBox.addView(tDispNeo);
        tasbihBox.addView(tBtnNeo);
        
        pCard.addView(left); 
        pCard.addView(tasbihBox);
        contentArea.addView(pNeo);
"""

pattern = re.compile(r"// --- Premium 3D Tasbih.*?// --- End Mini 3D Tasbih ---", re.DOTALL)
if pattern.search(content):
    content = pattern.sub(final_design, content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ ডিজাইন একদম নিখুঁতভাবে আপডেট করা হয়েছে!")
else:
    print("❌ এরর: কোড মার্কার খুঁজে পাওয়া যায়নি।")
