import os, re

def rpl(pat, rep, txt): return re.sub(pat, rep, txt, flags=re.DOTALL)

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"
if not os.path.exists(mf):
    for r, d, f in os.walk("."):
        if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")
        if "UIComponents.java" in f: uf = os.path.join(r, "UIComponents.java")

with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

# ১. মাস্টার 3D ইঞ্জিন (কালার মিক্সিং ও সব দিকে বর্ডারসহ)
eng = """public android.graphics.drawable.Drawable getPremium3D(int c1, float r, float dp, boolean isDark, int accent) {
    float d = getResources().getDisplayMetrics().density;
    int shadow;
    int red = android.graphics.Color.red(accent); int grn = android.graphics.Color.green(accent); int blu = android.graphics.Color.blue(accent);
    if (isDark) { shadow = android.graphics.Color.rgb((int)(red*0.4f), (int)(grn*0.4f), (int)(blu*0.4f)); } 
    else { shadow = android.graphics.Color.argb(80, red, grn, blu); }
    
    android.graphics.drawable.GradientDrawable sh = new android.graphics.drawable.GradientDrawable(); sh.setColor(shadow); sh.setCornerRadius(r);
    android.graphics.drawable.GradientDrawable su = new android.graphics.drawable.GradientDrawable(); su.setColor(c1); su.setCornerRadius(r);
    su.setStroke((int)(1.5f * d), shadow); // সব দিকে মোটা বর্ডার
    
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{sh, su});
    int ox = (int)((dp/1.5f) * d); int oy = (int)(dp * d);
    ld.setLayerInset(0, ox, oy, 0, 0); ld.setLayerInset(1, 0, 0, ox, oy); return ld;
}"""
if "getPremium3D" not in mc: mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n    " + eng)
# ২. UI উপাদানগুলোতে নতুন ইঞ্জিন প্রয়োগ
mc = rpl(r'pCard\.setBackground\(.*?\);\s*pCard\.setPadding.*?;', 'int pm = isDayTime ? android.graphics.Color.parseColor("#FF9500") : android.graphics.Color.parseColor("#1A2980");\n        pCard.setBackground(getPremium3D(pm, 20f*DENSITY, 8f, isDarkTheme, colorAccent));\n        pCard.setPadding((int)(20*DENSITY), (int)(pCardPadV*DENSITY), (int)(20*DENSITY), (int)(pCardPadV*DENSITY) + (int)(8f*DENSITY));', mc)
mc = rpl(r'pCard\.setBackground\(pcBg\);', 'int pm = isDayTime ? android.graphics.Color.parseColor("#FF9500") : android.graphics.Color.parseColor("#1A2980");\n        pCard.setBackground(getPremium3D(pm, 20f*DENSITY, 8f, isDarkTheme, colorAccent));', mc)

mc = rpl(r'themeToggleBtn\.setBackground\(.*?\);\s*themeToggleBtn\.setPadding.*?;', 'int pmTheme = isDarkTheme ? android.graphics.Color.parseColor("#1A2980") : android.graphics.Color.parseColor("#FF9500");\n        themeToggleBtn.setBackground(getPremium3D(pmTheme, 100f, 3f, isDarkTheme, colorAccent));\n        themeToggleBtn.setPadding(0,0,0,(int)(3f*DENSITY));', mc)
mc = rpl(r'themeToggleBtn\.setBackground\(tBg\);', 'int pmTheme = isDarkTheme ? android.graphics.Color.parseColor("#1A2980") : android.graphics.Color.parseColor("#FF9500");\n        themeToggleBtn.setBackground(getPremium3D(pmTheme, 100f, 3f, isDarkTheme, colorAccent));\n        themeToggleBtn.setPadding(0,0,0,(int)(3f*DENSITY));', mc)

for btn in ['offBtn', 'periodBtn', 'settingsBtn']:
    mc = rpl(rf'{btn}\.setBackground\(.*?\);\s*{btn}\.setPadding.*?;', f'{btn}.setBackground(getPremium3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, 100f, 3f, isDarkTheme, colorAccent)); {btn}.setPadding(0, 0, 0, (int)(3f*DENSITY));', mc)
    mc = rpl(rf'View {btn} = ui\.getRoundImage.*?;\n?\s*LinearLayout\.LayoutParams', f'View {btn} = ui.getRoundImage("img_dummy", 6, android.graphics.Color.TRANSPARENT, colorAccent); {btn}.setBackground(getPremium3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, 100f, 3f, isDarkTheme, colorAccent)); {btn}.setPadding(0, 0, 0, (int)(3f*DENSITY)); LinearLayout.LayoutParams', mc)

mc = rpl(r'streakBadge\.setBackground\(.*?\);\s*streakBadge\.setPadding.*?;', 'streakBadge.setBackground(getPremium3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, 20f*DENSITY, 3f, isDarkTheme, colorAccent)); streakBadge.setPadding((int)(10*DENSITY), (int)(4*DENSITY), (int)(10*DENSITY), (int)(4*DENSITY) + (int)(3f*DENSITY));', mc)
mc = rpl(r'streakBadge\.setBackground\(badgeBg\);', 'streakBadge.setBackground(getPremium3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, 20f*DENSITY, 3f, isDarkTheme, colorAccent)); streakBadge.setPadding((int)(10*DENSITY), (int)(4*DENSITY), (int)(10*DENSITY), (int)(4*DENSITY) + (int)(3f*DENSITY));', mc)

mc = rpl(r't\.setBackground\(.*?\);\s*t\.setPadding.*?;', 't.setBackground(getPremium3D(isSel ? colorAccent : themeColors[1], 8f*DENSITY, isSel ? 0f : 3f, isDarkTheme, colorAccent)); t.setPadding(0, 0, 0, isSel ? 0 : (int)(3f*DENSITY));', mc)
mc = rpl(r't\.setBackground\(getProgressBorder\(dKey, isSel\)\);', 't.setBackground(getPremium3D(isSel ? colorAccent : themeColors[1], 8f*DENSITY, isSel ? 0f : 3f, isDarkTheme, colorAccent)); t.setPadding(0, 0, 0, isSel ? 0 : (int)(3f*DENSITY));', mc)

for mBtn in ['markAllBtn', 'todayBtn']:
    mc = rpl(rf'{mBtn}\.setBackground\(.*?\);\s*{mBtn}\.setPadding.*?;', f'{mBtn}.setBackground(getPremium3D(themeColors[1], 15f*DENSITY, 5f, isDarkTheme, colorAccent)); {mBtn}.setPadding(0, 0, 0, (int)(5f*DENSITY));', mc)
    mc = rpl(rf'{mBtn}\.setBackground\(bg[12]\);', f'{mBtn}.setBackground(getPremium3D(themeColors[1], 15f*DENSITY, 5f, isDarkTheme, colorAccent)); {mBtn}.setPadding(0, 0, 0, (int)(5f*DENSITY));', mc)
mc = rpl(r'card\.setBackground\(.*?\);\s*card\.setPadding.*?;', 'int cM = stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#1A1115") : android.graphics.Color.parseColor("#FCE4EC")) : themeColors[1]; card.setBackground(getPremium3D(cM, 14f*DENSITY, 6f, isDarkTheme, colorAccent)); card.setPadding((int)(15*DENSITY), (int)(cardPadV*DENSITY), (int)(20*DENSITY), (int)(cardPadV*DENSITY) + (int)(6f*DENSITY));', mc)
mc = rpl(r'card\.setBackground\(cb\);', 'int cM = stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#1A1115") : android.graphics.Color.parseColor("#FCE4EC")) : themeColors[1]; card.setBackground(getPremium3D(cM, 14f*DENSITY, 6f, isDarkTheme, colorAccent)); card.setPadding((int)(15*DENSITY), (int)(cardPadV*DENSITY), (int)(20*DENSITY), (int)(cardPadV*DENSITY) + (int)(6f*DENSITY));', mc)

mc = rpl(r'sunnahBtn\.setBackground\(.*?\);\s*sunnahBtn\.setTextColor.*?\s*sunnahBtn\.setPadding.*?;', 'sunnahBtn.setBackground(getPremium3D(doneSunnahs > 0 ? colorAccent : themeColors[1], 12f*DENSITY, 3f, isDarkTheme, colorAccent)); sunnahBtn.setTextColor(doneSunnahs > 0 ? android.graphics.Color.WHITE : themeColors[2]); sunnahBtn.setPadding((int)(10*DENSITY), (int)(5*DENSITY), (int)(10*DENSITY), (int)(5*DENSITY) + (int)(3f*DENSITY));', mc)
mc = rpl(r'sunnahBtn\.setBackground\(customSunnahBg\);', 'sunnahBtn.setBackground(getPremium3D(doneSunnahs > 0 ? colorAccent : themeColors[1], 12f*DENSITY, 3f, isDarkTheme, colorAccent)); sunnahBtn.setTextColor(doneSunnahs > 0 ? android.graphics.Color.WHITE : themeColors[2]); sunnahBtn.setPadding((int)(10*DENSITY), (int)(5*DENSITY), (int)(10*DENSITY), (int)(5*DENSITY) + (int)(3f*DENSITY));', mc)

mc = rpl(r'TextView iconTxt = new TextView\(this\); iconTxt\.setText\(prayerIcons\[i\]\); iconTxt\.setTextSize\(22f\); iconTxt\.setGravity\(Gravity\.CENTER\);', 'TextView iconTxt = new TextView(this); iconTxt.setText(prayerIcons[i]); iconTxt.setTextSize(22f); iconTxt.setGravity(Gravity.CENTER); iconTxt.setBackground(getPremium3D(isDarkTheme ? android.graphics.Color.parseColor("#2C2C2E") : android.graphics.Color.parseColor("#F5F7FA"), 100f, 3f, isDarkTheme, colorAccent)); iconTxt.setPadding((int)(10*DENSITY), (int)(6*DENSITY), (int)(10*DENSITY), (int)(6*DENSITY) + (int)(3f*DENSITY));', mc)

with open(mf, 'w', encoding='utf-8') as f: f.write(mc)

# ৩. UIComponents (চেকবক্স) আপডেট
with open(uf, 'r', encoding='utf-8') as f: uc = f.read()
n_ui = """public View getPremiumCheckbox(String status, int activeColorHex) { 
    TextView tv = new TextView(activity); tv.setGravity(Gravity.CENTER); tv.setTextSize(14);
    boolean chk = status.equals("yes") || status.equals("excused"); float dp = chk ? 1f : 4f; float d = activity.getResources().getDisplayMetrics().density;
    LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams((int)(28*d), (int)(28*d)); tv.setLayoutParams(lp); 
    boolean dk = activity.getSharedPreferences("salah_pro_final", 0).getBoolean("is_dark_mode", false);
    int sCol = chk ? activeColorHex : (dk ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE);
    int shCol; int r = android.graphics.Color.red(activeColorHex); int g = android.graphics.Color.green(activeColorHex); int b = android.graphics.Color.blue(activeColorHex);
    if (dk) { shCol = android.graphics.Color.rgb((int)(r*0.4f), (int)(g*0.4f), (int)(b*0.4f)); } else { shCol = android.graphics.Color.argb(80, r, g, b); }
    android.graphics.drawable.GradientDrawable sh = new android.graphics.drawable.GradientDrawable(); sh.setColor(shCol); sh.setCornerRadius(8f*d);
    android.graphics.drawable.GradientDrawable su = new android.graphics.drawable.GradientDrawable(); su.setColor(sCol); su.setCornerRadius(8f*d);
    su.setStroke((int)(1.5f*d), shCol);
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{sh, su});
    int offX = (int)((dp/1.5f) * d); int offY = (int)(dp * d); ld.setLayerInset(0, offX, offY, 0, 0); ld.setLayerInset(1, 0, 0, offX, offY);
    tv.setBackground(ld); if (chk) { tv.setText(status.equals("yes")?"✓":"🌸"); tv.setTextColor(android.graphics.Color.WHITE); } else tv.setText("");
    tv.setPadding(0, 0, 0, offY); return tv;
}"""
uc = rpl(r'public View getPremiumCheckbox.*?return tv;\n    \}', n_ui, uc)
with open(uf, 'w', encoding='utf-8') as f: f.write(uc)
print("✔ ULTIMATE COLOR-MATCHED 3D APPLIED!")
