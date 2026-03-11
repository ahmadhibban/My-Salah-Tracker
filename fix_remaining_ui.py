import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(java_file):
    print("❌ MainActivity.java not found!")
    exit()

with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. যেকোনো ভিউকে সফট থ্রিডিতে মুড়িয়ে দেওয়ার মেগা মেথড ইনজেক্ট করা
neo_wrapper = """
    private soup.neumorphism.NeumorphCardView createNeoWrapper(android.view.View child, int type, float radiusDp, float elevDp, int bgColor, int leftMarginDp, int rightMarginDp, int width, int height, float weight) {
        soup.neumorphism.NeumorphCardView neo = new soup.neumorphism.NeumorphCardView(this);
        neo.setShapeType(type); // 0 = Flat (ওপরের দিকে ফোলা), 1 = Pressed (ভেতরের দিকে ডেবে থাকা)
        neo.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.WHITE);
        neo.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
        neo.setShadowElevation(elevDp * DENSITY);
        neo.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, radiusDp * DENSITY).build());
        neo.setBackgroundColor(bgColor);
        
        android.widget.LinearLayout.LayoutParams lp;
        if (weight > 0) { lp = new android.widget.LinearLayout.LayoutParams(width, height, weight); } 
        else { lp = new android.widget.LinearLayout.LayoutParams(width, height); }
        lp.setMargins((int)(leftMarginDp * DENSITY), (int)(6*DENSITY), (int)(rightMarginDp * DENSITY), (int)(6*DENSITY));
        neo.setLayoutParams(lp);
        
        if (child.getParent() != null) { ((android.view.ViewGroup)child.getParent()).removeView(child); }
        child.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        
        android.widget.FrameLayout.LayoutParams clp = new android.widget.FrameLayout.LayoutParams(-1, -1);
        clp.gravity = android.view.Gravity.CENTER;
        child.setLayoutParams(clp);
        
        neo.addView(child);
        return neo;
    }
"""
if "createNeoWrapper" not in mc:
    mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n" + neo_wrapper)

# ২. পুরনো শক্ত বর্ডার (Background) মুছে ফেলা
for var in ["streakBadge", "themeToggleBtn", "offBtn", "periodBtn", "settingsBtn", "markAllBtn", "todayBtn", "t", "sunnahBtn", "pCard"]:
    mc = re.sub(rf'{var}\.setBackground\(get[A-Za-z0-9_]+\([^)]+\)\);', f'{var}.setBackgroundColor(android.graphics.Color.TRANSPARENT);', mc)

# ৩. সবগুলো বাটন ও কার্ডকে সফট থ্রিডি দিয়ে র‍্যাপ (Wrap) করা
replacements = {
    "leftHeader.addView(streakBadge);": "streakBadge.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY)); leftHeader.addView(createNeoWrapper(streakBadge, 0, 15f, 3f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), 0, 0, -2, -2, 0));",
    
    "rightHeader.addView(themeToggleBtn);": "rightHeader.addView(createNeoWrapper(themeToggleBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), 0, 8, (int)(40*DENSITY), (int)(40*DENSITY), 0));",
    
    "rightHeader.addView(offBtn);": "rightHeader.addView(createNeoWrapper(offBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), 0, 8, (int)(40*DENSITY), (int)(40*DENSITY), 0));",
    
    "rightHeader.addView(periodBtn);": "rightHeader.addView(createNeoWrapper(periodBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), 0, 8, (int)(40*DENSITY), (int)(40*DENSITY), 0));",
    
    "rightHeader.addView(settingsBtn);": "rightHeader.addView(createNeoWrapper(settingsBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), 0, 8, (int)(40*DENSITY), (int)(40*DENSITY), 0));",
    
    "row.addView(t);": "t.setPadding(0, (int)(10*DENSITY), 0, (int)(10*DENSITY)); row.addView(createNeoWrapper(t, isSel ? 1 : 0, 10f, isSel ? 1.5f : 3f, isSel ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\")), 2, 2, 0, -2, 1f));",
    
    "topBtns.addView(markAllBtn);": "markAllBtn.setPadding((int)(16*DENSITY), (int)(10*DENSITY), (int)(16*DENSITY), (int)(10*DENSITY)); topBtns.addView(createNeoWrapper(markAllBtn, 0, 12f, 4f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), 4, 4, -2, -2, 0));",
    
    "topBtns.addView(todayBtn);": "todayBtn.setPadding((int)(16*DENSITY), (int)(10*DENSITY), (int)(16*DENSITY), (int)(10*DENSITY)); topBtns.addView(createNeoWrapper(todayBtn, 0, 12f, 4f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), 4, 4, -2, -2, 0));",
    
    "innerCard.addView(sunnahBtn);": "sunnahBtn.setPadding((int)(14*DENSITY), (int)(8*DENSITY), (int)(14*DENSITY), (int)(8*DENSITY)); innerCard.addView(createNeoWrapper(sunnahBtn, 1, 12f, 2f, doneSunnahs > 0 ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\")), 0, 12, -2, -2, 0));",
    
    "card.addView(sunnahBtn);": "sunnahBtn.setPadding((int)(14*DENSITY), (int)(8*DENSITY), (int)(14*DENSITY), (int)(8*DENSITY)); card.addView(createNeoWrapper(sunnahBtn, 1, 12f, 2f, doneSunnahs > 0 ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\")), 0, 12, -2, -2, 0));",
    
    "contentArea.addView(pCard);": "pCard.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY)); contentArea.addView(createNeoWrapper(pCard, 0, 20f, 6f, tSur, 10, 10, -1, -2, 0));"
}

for old, new in replacements.items():
    mc = mc.replace(old, new)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✔ ALL REMAINING UI ELEMENTS UPDATED PERFECTLY! 🚀")
