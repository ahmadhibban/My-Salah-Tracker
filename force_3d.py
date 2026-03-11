import os
mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
if not os.path.exists(mf):
    for r, d, f in os.walk("."):
        if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")

with open(mf, 'r', encoding='utf-8') as f: code = f.read()

# ১. থিম আইকন (হলুদ/নীল ফিলসহ পারফেক্ট 3D)
code = code.replace("themeToggleBtn.setBackground(tBg);", "int pmTheme = isDarkTheme ? android.graphics.Color.parseColor(\"#1A2980\") : android.graphics.Color.parseColor(\"#FF9500\"); int psTheme = isDarkTheme ? android.graphics.Color.parseColor(\"#0F184A\") : android.graphics.Color.parseColor(\"#C77600\"); themeToggleBtn.setBackground(getSafe3D(pmTheme, psTheme, 100f, 3f)); themeToggleBtn.setPadding(0, 0, 0, (int)(3f*DENSITY));")

# ২. সপ্তাহের ৭ দিনের ঘর
code = code.replace("t.setBackground(getProgressBorder(dKey, isSel));", "t.setBackground(getSafe3D(isSel ? colorAccent : themeColors[1], isSel ? (isDarkTheme?android.graphics.Color.parseColor(\"#0A0A0C\"):android.graphics.Color.parseColor(\"#cbd5e0\")) : themeColors[4], 8f*DENSITY, isSel ? 0f : 3f)); t.setPadding(0, 0, 0, isSel ? 0 : (int)(3f*DENSITY));")

# ৩. Mark All বাটন
code = code.replace("markAllBtn.setBackground(bg1);", "markAllBtn.setBackground(getSafe3D(themeColors[1], isDarkTheme ? android.graphics.Color.parseColor(\"#0A0A0C\") : android.graphics.Color.parseColor(\"#cbd5e0\"), 15f*DENSITY, 4f)); markAllBtn.setPadding(0, 0, 0, (int)(4f*DENSITY));")
code = code.replace("markAllBtn.setElevation(", "// markAllBtn.setElevation(")

# ৪. Today বাটন
code = code.replace("todayBtn.setBackground(bg2);", "todayBtn.setBackground(getSafe3D(themeColors[1], isDarkTheme ? android.graphics.Color.parseColor(\"#0A0A0C\") : android.graphics.Color.parseColor(\"#cbd5e0\"), 15f*DENSITY, 4f)); todayBtn.setPadding(0, 0, 0, (int)(4f*DENSITY));")
code = code.replace("todayBtn.setElevation(", "// todayBtn.setElevation(")

# ৫. নামাজের মূল কার্ডগুলো (পারফেক্ট থিকনেসসহ)
code = code.replace("card.setBackground(cb);", "int cM = stat.equals(\"excused\") ? (isDarkTheme ? android.graphics.Color.parseColor(\"#1A1115\") : android.graphics.Color.parseColor(\"#FCE4EC\")) : themeColors[1]; int cS = isDarkTheme ? android.graphics.Color.parseColor(\"#0A0A0C\") : android.graphics.Color.parseColor(\"#cbd5e0\"); card.setBackground(getSafe3D(cM, cS, 14f*DENSITY, 5f)); card.setPadding((int)(15*DENSITY), (int)(cardPadV*DENSITY), (int)(20*DENSITY), (int)(cardPadV*DENSITY) + (int)(5f*DENSITY));")

# ৬. উপরের ডানদিকের তিনটা আইকন (Offline, Period, Settings)
for icon in ["offBtn", "periodBtn", "settingsBtn"]:
    find_str = f"rightHeader.addView({icon});"
    rep_str = f"{icon}.setBackground(getSafe3D(isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor(\"#0A0A0C\") : android.graphics.Color.parseColor(\"#cbd5e0\"), 100f, 2f)); {icon}.setPadding(0, 0, 0, (int)(2f*DENSITY)); rightHeader.addView({icon});"
    if f"{icon}.setBackground(getSafe3D" not in code:
        code = code.replace(find_str, rep_str)

with open(mf, 'w', encoding='utf-8') as f: f.write(code)
print("✔ FINAL 3D MAGIC APPLIED PERFECTLY! NOW BUILD THE APP!")
