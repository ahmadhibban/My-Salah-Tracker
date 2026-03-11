import os
import re

def inject_3d_effects():
    target = None
    # MainActivity.java ফাইলটি খুঁজে বের করা
    for root, _, files in os.walk("."):
        if "MainActivity.java" in files:
            target = os.path.join(root, "MainActivity.java")
            break
    
    if not target:
        print("MainActivity.java খুঁজে পাওয়া যায়নি!")
        return

    with open(target, 'r', encoding='utf-8') as f:
        code = f.read()

    # ১. ৩ডি ইঞ্জিন মেথডটি ইনজেক্ট করা
    helper = """
    // === 3D SOLID UI GENERATOR ===
    public android.graphics.drawable.Drawable getSolid3DDrawable(int mainColor, int borderColor, float radius, boolean isDark, boolean isRound) {
        int depth = isRound ? 3 : 5; 
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.Drawable[] layers = new android.graphics.drawable.Drawable[depth + 1];
        
        int[] lightShadows = {android.graphics.Color.parseColor("#d8dee9"), android.graphics.Color.parseColor("#cbd5e0"), android.graphics.Color.parseColor("#adb9ca"), android.graphics.Color.parseColor("#91a0b5"), android.graphics.Color.parseColor("#8595a8")};
        int[] darkShadows = {android.graphics.Color.parseColor("#0A0A0C"), android.graphics.Color.parseColor("#121214"), android.graphics.Color.parseColor("#151517"), android.graphics.Color.parseColor("#18181A"), android.graphics.Color.parseColor("#1A1A1C")};
        int[] shadows = isDark ? darkShadows : lightShadows;
        
        for (int i = 0; i <= depth; i++) {
            android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
            gd.setCornerRadius(radius);
            if (isRound) gd.setShape(android.graphics.drawable.GradientDrawable.OVAL);
            
            if (i == depth) {
                gd.setColor(mainColor);
                if (borderColor != android.graphics.Color.TRANSPARENT) gd.setStroke((int)(1f * d), borderColor);
            } else { gd.setColor(shadows[i % shadows.length]); }
            layers[i] = gd;
        }
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(layers);
        for (int i = 0; i <= depth; i++) {
            int currL = (int)((i * 1.5f * d)); 
            int currT = (int)(((depth - i) * 1.5f * d)); 
            int currR = (int)(((depth - i) * 1.5f * d)); 
            int currB = (int)((i * 1.5f * d)); 
            ld.setLayerInset(i, currL, currT, currR, currB);
        }
        return ld;
    }
"""
    if "getSolid3DDrawable" not in code:
        code = code[:code.rfind("}")] + helper + "\n}"

    # ২. উপরের ১০০% কার্ডকে থ্রিডি করা
    code = re.sub(r'int\[\] pColors =.*?pCard\.setBackground\(pcBg\);', 
                  '''int pMainColor = isDayTime ? android.graphics.Color.parseColor("#FF9500") : android.graphics.Color.parseColor("#1A2980");
        pCard.setBackground(getSolid3DDrawable(pMainColor, android.graphics.Color.TRANSPARENT, 20f * DENSITY, !isDayTime, false));''', 
                  code, flags=re.DOTALL)

    # ৩. Mark All বাটনকে থ্রিডি করা
    code = re.sub(r'GradientDrawable bg1 = new GradientDrawable\(\);.*?markAllBtn\.setBackground\(bg1\);', 
                  '''markAllBtn.setBackground(getSolid3DDrawable(themeColors[1], themeColors[4], 16f * DENSITY, isDarkTheme, false));''', 
                  code, flags=re.DOTALL)

    # ৪. Today বাটনকে থ্রিডি করা
    code = re.sub(r'GradientDrawable bg2 = new GradientDrawable\(\);.*?todayBtn\.setBackground\(bg2\);', 
                  '''todayBtn.setBackground(getSolid3DDrawable(themeColors[1], themeColors[4], 16f * DENSITY, isDarkTheme, false));''', 
                  code, flags=re.DOTALL)

    # ৫. সবগুলো নামাজের ঘরকে (Fajr, Dhuhr...) একসাথে থ্রিডি ফ্রেমে রূপান্তর করা
    code = re.sub(r'GradientDrawable cb = new GradientDrawable\(\);.*?card\.setBackground\(cb\);', 
                  '''int cColor = stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#1A1115") : android.graphics.Color.parseColor("#FCE4EC")) : themeColors[1];
            int bColor = stat.equals("excused") ? android.graphics.Color.parseColor("#FF4081") : (checked ? colorAccent : themeColors[4]);
            card.setBackground(getSolid3DDrawable(cColor, bColor, 16f * DENSITY, isDarkTheme, false));
            card.setPadding((int)(15*DENSITY), (int)(cardPadV*DENSITY), (int)(20*DENSITY), (int)((cardPadV+4)*DENSITY));''', 
                  code, flags=re.DOTALL)

    # ৬. Sunnah/Extras বাটনকে ডেবে থাকা ৩ডি লুক দেওয়া
    code = re.sub(r'GradientDrawable customSunnahBg = new GradientDrawable\(\);.*?sunnahBtn\.setBackground\(customSunnahBg\);', 
                  '''int sBgColor = doneSunnahs > 0 ? colorAccent : themeColors[4];
                sunnahBtn.setTextColor(doneSunnahs > 0 ? android.graphics.Color.WHITE : themeColors[2]);
                sunnahBtn.setBackground(getSolid3DDrawable(sBgColor, android.graphics.Color.TRANSPARENT, 10f*DENSITY, isDarkTheme, false));
                sunnahBtn.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY));''', 
                  code, flags=re.DOTALL)

    with open(target, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Magic Done! MainActivity 3D Effect Applied Successfully.")

inject_3d_effects()
