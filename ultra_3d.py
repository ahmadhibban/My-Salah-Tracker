import os, re

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"
for r, d, f in os.walk("."):
    if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")
    if "UIComponents.java" in f: uf = os.path.join(r, "UIComponents.java")

with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

# ১. নতুন Ultra 3D ইঞ্জিন
ultra = """public android.graphics.drawable.Drawable getUltra3D(int surfaceColor, int shadowColor, float radius, float depthDp) {
    float d = getResources().getDisplayMetrics().density;
    android.graphics.drawable.GradientDrawable shadow = new android.graphics.drawable.GradientDrawable(); shadow.setColor(shadowColor); shadow.setCornerRadius(radius);
    android.graphics.drawable.GradientDrawable surface = new android.graphics.drawable.GradientDrawable(); surface.setColor(surfaceColor); surface.setCornerRadius(radius);
    surface.setStroke((int)(1.0f * d), shadowColor); // চারদিকে সূক্ষ্ম আউটলাইন
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
    int offX = (int)((depthDp/2.0f) * d); int offY = (int)(depthDp * d); // সামান্য কোণাকুণি (Isometric) ছায়া
    ld.setLayerInset(0, offX, offY, 0, 0); ld.setLayerInset(1, 0, 0, offX, offY); return ld;
}"""
if "getUltra3D" not in mc: mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n    " + ultra)

# ডাইনামিক শ্যাডো ক্যালকুলেটর
if "int accShd =" not in mc: 
    mc = mc.replace("boolean isDayTime = hour >= 6 && hour < 18;", "boolean isDayTime = hour >= 6 && hour < 18;\n        int _r = android.graphics.Color.red(colorAccent); int _g = android.graphics.Color.green(colorAccent); int _b = android.graphics.Color.blue(colorAccent); int accShd = isDarkTheme ? android.graphics.Color.rgb((int)(_r*0.4f), (int)(_g*0.4f), (int)(_b*0.4f)) : android.graphics.Color.argb(100, _r, _g, _b);")

# ২. পার্সেন্টেজ বক্স ও থিম আইকন (সবসময় হলুদ বা নীল)
mc = re.sub(r'(int pmTheme =.*?)?themeToggleBtn\.setBackground\(getPremium3D.*?\);\s*themeToggleBtn\.setPadding.*?;', 'int tSur = isDayTime ? android.graphics.Color.parseColor("#FF9500") : android.graphics.Color.parseColor("#1A2980"); int tShd = isDayTime ? android.graphics.Color.parseColor("#C77600") : android.graphics.Color.parseColor("#0F184A"); themeToggleBtn.setBackground(getUltra3D(tSur, tShd, 100f, 4f)); themeToggleBtn.setPadding(0, 0, 0, (int)(4f*DENSITY));', mc, flags=re.DOTALL)

mc = re.sub(r'(int pm =.*?)?pCard\.setBackground\(getPremium3D.*?\);\s*pCard\.setPadding.*?;', 'int tSur = isDayTime ? android.graphics.Color.parseColor("#FF9500") : android.graphics.Color.parseColor("#1A2980"); int tShd = isDayTime ? android.graphics.Color.parseColor("#C77600") : android.graphics.Color.parseColor("#0F184A"); pCard.setBackground(getUltra3D(tSur, tShd, 20f*DENSITY, 8f)); pCard.setPadding((int)(20*DENSITY), (int)(pCardPadV*DENSITY), (int)(20*DENSITY), (int)(pCardPadV*DENSITY) + (int)(8f*DENSITY));', mc, flags=re.DOTALL)

# ৩. উপরের ডানদিকের আইকন (সাদা রং ফিক্স এবং ৩ডি)
mc = re.sub(r'View periodBtn = ui\.getRoundImage.*?;', 'View periodBtn = ui.getRoundImage("img_period", 6, android.graphics.Color.TRANSPARENT, isDarkTheme ? android.graphics.Color.WHITE : colorAccent);', mc)
mc = re.sub(r'View settingsBtn = ui\.getRoundImage.*?;', 'View settingsBtn = ui.getRoundImage("img_settings", 6, android.graphics.Color.TRANSPARENT, isDarkTheme ? android.graphics.Color.WHITE : colorAccent);', mc)

for btn in ['offBtn', 'periodBtn', 'settingsBtn']:
    mc = re.sub(rf'{btn}\.setBackground\(getPremium3D.*?\);\s*{btn}\.setPadding.*?;', f'{btn}.setBackground(getUltra3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 100f, 3f)); {btn}.setPadding(0, 0, 0, (int)(3f*DENSITY));', mc)

# ৪. নামাজের আইকন (iconTxt)
mc = re.sub(r'iconTxt\.setBackground\(getPremium3D.*?\);\s*iconTxt\.setPadding.*?;', 'iconTxt.setBackground(getUltra3D(isDarkTheme ? android.graphics.Color.parseColor("#2C2C2E") : android.graphics.Color.parseColor("#F5F7FA"), isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#cbd5e0"), 100f, 3f)); iconTxt.setPadding((int)(10*DENSITY), (int)(6*DENSITY), (int)(10*DENSITY), (int)(6*DENSITY) + (int)(3f*DENSITY)); iconTxt.setTextColor(isDarkTheme ? android.graphics.Color.WHITE : themeColors[2]);', mc)

# ৫. সুন্নাহর ঘর (ছিমছাম এবং সুন্দর)
mc = re.sub(r'sunnahBtn\.setBackground\(getPremium3D.*?\);\s*sunnahBtn\.setTextColor.*?\s*sunnahBtn\.setPadding.*?;', 'int sSur = doneSunnahs > 0 ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#2C2C2E") : themeColors[1]); int sShd = doneSunnahs > 0 ? accShd : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : themeColors[4]); sunnahBtn.setBackground(getUltra3D(sSur, sShd, 12f*DENSITY, 2f)); sunnahBtn.setTextColor(doneSunnahs > 0 ? android.graphics.Color.WHITE : themeColors[2]); sunnahBtn.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY) + (int)(2f*DENSITY));', mc)

# অন্যান্য উপাদান Ultra 3D তে কনভার্ট
mc = re.sub(r'getPremium3D\((.*?),.*?, (.*?), isDarkTheme, colorAccent\)', r'getUltra3D(\1, isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), \2)', mc)
mc = re.sub(r'getPremium3D\((.*?), (.*?), (.*?), isDarkTheme, colorAccent\)', r'getUltra3D(\1, isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), \2, \3)', mc)

with open(mf, 'w', encoding='utf-8') as f: f.write(mc)

# ৬. টিক বক্স (পারফেক্ট ৩ডি ইফেক্ট)
with open(uf, 'r', encoding='utf-8') as f: uc = f.read()
new_chk = """public android.view.View getPremiumCheckbox(String status, int activeColorHex) {
    android.widget.TextView tv = new android.widget.TextView(activity); tv.setGravity(android.view.Gravity.CENTER); tv.setTextSize(14);
    float d = activity.getResources().getDisplayMetrics().density;
    android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams((int)(28*d), (int)(28*d)); tv.setLayoutParams(lp);
    boolean dk = activity.getSharedPreferences("salah_pro_final", 0).getBoolean("is_dark_mode", false);
    boolean chk = status.equals("yes") || status.equals("excused"); float dp = chk ? 1f : 4f;
    int r = android.graphics.Color.red(activeColorHex); int g = android.graphics.Color.green(activeColorHex); int b = android.graphics.Color.blue(activeColorHex);
    int accShadow = dk ? android.graphics.Color.rgb((int)(r*0.4f), (int)(g*0.4f), (int)(b*0.4f)) : android.graphics.Color.argb(100, r, g, b);
    int cSur = chk ? activeColorHex : (dk ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE);
    int cShd = chk ? accShadow : (dk ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
    android.graphics.drawable.GradientDrawable sh = new android.graphics.drawable.GradientDrawable(); sh.setColor(cShd); sh.setCornerRadius(8f*d);
    android.graphics.drawable.GradientDrawable su = new android.graphics.drawable.GradientDrawable(); su.setColor(cSur); su.setCornerRadius(8f*d);
    su.setStroke((int)(1.0f*d), cShd);
    android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{sh, su});
    int offX = (int)((dp/2f) * d); int offY = (int)(dp * d); ld.setLayerInset(0, offX, offY, 0, 0); ld.setLayerInset(1, 0, 0, offX, offY);
    tv.setBackground(ld);
    if(chk) { tv.setText(status.equals("yes")?"✓":"🌸"); tv.setTextColor(android.graphics.Color.WHITE); }
    tv.setPadding(0, 0, 0, offY); return tv;
}"""
uc = re.sub(r'public android\.view\.View getPremiumCheckbox.*?return tv;\n    \}', new_chk, uc, flags=re.DOTALL)
with open(uf, 'w', encoding='utf-8') as f: f.write(uc)
print("✔ ULTRA 3D MASTERPIECE APPLIED!")
