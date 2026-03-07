import os

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
if os.path.exists(f):
    c = open(f).read()
    
    # 1. Custom Icon Setup (img_custom_nafl)
    o_ic = 'android.widget.TextView iconView = new android.widget.TextView(this); iconView.setText("⭐"); iconView.setTextSize(40); iconView.setGravity(android.view.Gravity.CENTER); main.addView(iconView);'
    n_ic = 'android.view.View iconView = ui.getRoundImage("img_custom_nafl", 0, android.graphics.Color.TRANSPARENT, 0); android.widget.LinearLayout.LayoutParams icLp = new android.widget.LinearLayout.LayoutParams((int)(60*DENSITY), (int)(60*DENSITY)); icLp.gravity = android.view.Gravity.CENTER; icLp.setMargins(0, 0, 0, (int)(15*DENSITY)); iconView.setLayoutParams(icLp); main.addView(iconView);'
    c = c.replace(o_ic, n_ic)
    
    # 2. Main Page Sunnah Badge Color (Restore Amber)
    o_bg = 'customSunnahBg.setColor(colorAccent);sunnahBtn.setTextColor(android.graphics.Color.WHITE);'
    n_bg = 'customSunnahBg.setColor(android.graphics.Color.parseColor("#F59E0B"));sunnahBtn.setTextColor(android.graphics.Color.WHITE);'
    c = c.replace(o_bg, n_bg)
    
    # 3. Sunnah Dialog Complete Amber Theme
    i1 = c.find('private void showSunnahDialog')
    i2 = c.find('private void showAddCustomPrayerDialog')
    if i1 != -1 and i2 != -1:
        c = c[:i1] + c[i1:i2].replace('colorAccent', 'android.graphics.Color.parseColor("#F59E0B")') + c[i2:]
        
    open(f, 'w').write(c)
    print("✅ Custom Icon & Sunnah Colors Restored! YOU ARE READY TO BUILD.")
else:
    print("Error: MainActivity not found.")
