import os, re

def fix():
    mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
    if not os.path.exists(mf):
        for r, d, f in os.walk("."):
            if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")

    with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

    # ১. থিম আইকনের হলুদ/নীল ফিল ফিক্স
    mc = re.sub(r'themeToggleBtn\.setBackground\(getSafe3D[^;]+;\s*themeToggleBtn\.setPadding[^;]+;',
                'int pmTheme = isDarkTheme ? android.graphics.Color.parseColor("#1A2980") : android.graphics.Color.parseColor("#FF9500"); int psTheme = isDarkTheme ? android.graphics.Color.parseColor("#0F184A") : android.graphics.Color.parseColor("#C77600"); themeToggleBtn.setBackground(getSafe3D(pmTheme, psTheme, 100f, 2f)); themeToggleBtn.setPadding(0, 0, 0, (int)(2f*DENSITY));', mc)
    mc = re.sub(r'GradientDrawable tBg = new GradientDrawable[^;]+;\s*tBg\.setCornerRadius[^;]+;\s*themeToggleBtn\.setBackground\(tBg\);',
                'int pmTheme = isDarkTheme ? android.graphics.Color.parseColor("#1A2980") : android.graphics.Color.parseColor("#FF9500"); int psTheme = isDarkTheme ? android.graphics.Color.parseColor("#0F184A") : android.graphics.Color.parseColor("#C77600"); themeToggleBtn.setBackground(getSafe3D(pmTheme, psTheme, 100f, 2f)); themeToggleBtn.setPadding(0, 0, 0, (int)(2f*DENSITY));', mc)

    # ২. সপ্তাহের ৭ দিনের ঘর ফিক্স
    mc = re.sub(r't\.setBackground\(getProgressBorder\(dKey,\s*isSel\)\);',
                't.setBackground(getSafe3D(isSel ? colorAccent : themeColors[1], isSel ? (isDarkTheme?android.graphics.Color.parseColor("#0A0A0C"):android.graphics.Color.parseColor("#cbd5e0")) : themeColors[4], 8f*DENSITY, isSel ? 0f : 3f)); t.setPadding(0, 0, 0, isSel ? 0 : (int)(3f*DENSITY));', mc)

    # ৩. Mark All বাটন ফিক্স
    mc = re.sub(r'markAllBtn\.setBackground\(bg1\);\s*markAllBtn\.setPadding\([^;]+\);',
                'markAllBtn.setBackground(getSafe3D(themeColors[1], isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 12f*DENSITY, 4f)); markAllBtn.setPadding((int)(22*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(22*DENSITY) + (int)(4f*DENSITY));', mc)
    mc = re.sub(r'if\s*\(Build\.VERSION\.SDK_INT >= 21\)\s*markAllBtn\.setElevation[^;]+;\n?', '', mc)

    # ৪. Today বাটন ফিক্স
    mc = re.sub(r'todayBtn\.setBackground\(bg2\);\s*todayBtn\.setPadding\([^;]+\);',
                'todayBtn.setBackground(getSafe3D(themeColors[1], isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 12f*DENSITY, 4f)); todayBtn.setPadding((int)(22*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(22*DENSITY) + (int)(4f*DENSITY));', mc)
    mc = re.sub(r'if\s*\(Build\.VERSION\.SDK_INT >= 21\)\s*todayBtn\.setElevation[^;]+;\n?', '', mc)

    # ৫. নামাজের কার্ডগুলোর ফিক্স
    mc = re.sub(r'card\.setBackground\(cb\);\s*card\.setPadding\([^;]+\);',
                'int cM = stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#1A1115") : android.graphics.Color.parseColor("#FCE4EC")) : themeColors[1]; int cS = isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"); card.setBackground(getSafe3D(cM, cS, 14f*DENSITY, 6f)); card.setPadding((int)(15*DENSITY), (int)(cardPadV*DENSITY), (int)(20*DENSITY), (int)((cardPadV+4)*DENSITY) + (int)(6f*DENSITY));', mc)

    with open(mf, 'w', encoding='utf-8') as f: f.write(mc)
    print("✔ All remaining UI elements successfully upgraded to Safe 3D!")

fix()
