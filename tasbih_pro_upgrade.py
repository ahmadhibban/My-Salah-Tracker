import re
import os

file_path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# নিখুঁত ৩ডি তাসবিহ ডিজাইন (স্যাম্পল ছবি অনুযায়ী)
new_design = """
        // --- Premium 3D Tasbih (As per Sample) ---
        LinearLayout tasbihBox = new LinearLayout(this);
        tasbihBox.setOrientation(LinearLayout.VERTICAL);
        tasbihBox.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 0.8f));
        tasbihBox.setGravity(Gravity.RIGHT | Gravity.CENTER_VERTICAL);
        
        // Digital Screen (Inset/Pressed Look)
        soup.neumorphism.NeumorphCardView tDispNeo = new soup.neumorphism.NeumorphCardView(this);
        tDispNeo.setShapeType(soup.neumorphism.ShapeType.PRESSED);
        tDispNeo.setShadowColorLight(isDarkTheme ? Color.parseColor("#333336") : Color.parseColor("#FFFFFF"));
        tDispNeo.setShadowColorDark(isDarkTheme ? Color.parseColor("#0A0A0C") : Color.parseColor("#cbd5e0"));
        tDispNeo.setBackgroundColor(isDarkTheme ? Color.parseColor("#151515") : Color.parseColor("#D1D9E6"));
        tDispNeo.setShadowElevation(5f * DENSITY);
        tDispNeo.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 12f*DENSITY).build());
        
        final TextView tCountTxt = new TextView(this);
        final android.content.SharedPreferences tSp = getSharedPreferences("MiniTasbih", MODE_PRIVATE);
        tCountTxt.setText(String.format("%03d", tSp.getInt("count", 0)));
        tCountTxt.setTextColor(colorAccent);
        tCountTxt.setTypeface(Typeface.MONOSPACE, Typeface.BOLD);
        tCountTxt.setTextSize(26f);
        tCountTxt.setGravity(Gravity.CENTER);
        tCountTxt.setPadding((int)(18*DENSITY), (int)(10*DENSITY), (int)(18*DENSITY), (int)(10*DENSITY));
        tDispNeo.addView(tCountTxt);
        
        // Rounded Tap Button
        final soup.neumorphism.NeumorphCardView tBtnNeo = new soup.neumorphism.NeumorphCardView(this);
        tBtnNeo.setShapeType(soup.neumorphism.ShapeType.FLAT);
        tBtnNeo.setBackgroundColor(colorAccent);
        tBtnNeo.setShadowElevation(6f * DENSITY);
        tBtnNeo.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 35f*DENSITY).build());
        
        LinearLayout.LayoutParams btnLp = new LinearLayout.LayoutParams((int)(70*DENSITY), (int)(70*DENSITY));
        btnLp.gravity = Gravity.RIGHT;
        btnLp.setMargins(0, (int)(12*DENSITY), (int)(5*DENSITY), 0);
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
            return true;
        });

        LinearLayout tGroup = new LinearLayout(this);
        tGroup.setOrientation(LinearLayout.VERTICAL);
        tGroup.setGravity(Gravity.RIGHT);
        tGroup.addView(tDispNeo);
        tGroup.addView(tBtnNeo);
        tasbihBox.addView(tGroup);
        
        pCard.addView(left); 
        pCard.addView(tasbihBox);
        contentArea.addView(pNeo);
"""

# আপনার কোডের পুরনো অংশটি রিপ্লেস করা হচ্ছে
start_marker = "// --- Mini 3D Tasbih"
end_marker = "// --- End Mini 3D Tasbih ---"

if start_marker in content and end_marker in content:
    pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
    content = pattern.sub(new_design, content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Tasbih Pro UI Upgraded Successfully!")
else:
    print("❌ Error: Markers not found. Please ensure the code tags are present.")
