import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# মেথড ক্লিন করার জন্য একটি স্মার্ট ফাংশন (যাতে কোনো ডুপ্লিকেট না থাকে)
def remove_method(text, method_signature):
    while True:
        idx = text.find(method_signature)
        if idx == -1: break
        start = text.find('{', idx)
        if start == -1: break
        count = 1
        i = start + 1
        while i < len(text) and count > 0:
            if text[i] == '{': count += 1
            elif text[i] == '}': count -= 1
            i += 1
        if count == 0:
            text = text[:idx] + text[i:]
        else:
            break
    return text

# যদি আগে কোনো ভাঙা মেথড থাকে, সেগুলো মুছে ফেলা
c = remove_method(c, "private void showAddCustomPrayerDialog()")
c = remove_method(c, "private void showDeleteCustomPrayerDialog(")

# ফাইলের একদম শেষের ব্র্যাকেটটি (Class closing brace) রিমুভ করা
c = c.rstrip()
if c.endswith('}'):
    c = c[:-1].rstrip()

# মেথডগুলোর সঠিক কোড
dialogs = """
    private void showAddCustomPrayerDialog() {
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
        android.widget.LinearLayout main = new android.widget.LinearLayout(this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(30f * DENSITY); main.setBackground(gd);
        android.widget.TextView iconView = new android.widget.TextView(this); iconView.setText("⭐"); iconView.setTextSize(40); iconView.setGravity(android.view.Gravity.CENTER); main.addView(iconView);
        android.widget.TextView title = new android.widget.TextView(this); title.setText(lang.get("Add Extra Prayer")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setGravity(android.view.Gravity.CENTER); title.setPadding(0, (int)(10*DENSITY), 0, (int)(25*DENSITY)); main.addView(title);
        final android.widget.EditText nameIn = new android.widget.EditText(this); nameIn.setHint(lang.get("Prayer Name (e.g. Ishraq)")); nameIn.setTextColor(themeColors[2]); nameIn.setHintTextColor(themeColors[3]); android.graphics.drawable.GradientDrawable iBg = new android.graphics.drawable.GradientDrawable(); iBg.setColor(themeColors[4]); iBg.setCornerRadius(15f*DENSITY); nameIn.setBackground(iBg); nameIn.setPadding((int)(20*DENSITY),(int)(15*DENSITY),(int)(20*DENSITY),(int)(15*DENSITY)); main.addView(nameIn, new android.widget.LinearLayout.LayoutParams(-1, -2));
        final android.widget.EditText rakIn = new android.widget.EditText(this); rakIn.setHint(lang.get("Rakats (e.g. 2)")); rakIn.setInputType(android.text.InputType.TYPE_CLASS_NUMBER); rakIn.setTextColor(themeColors[2]); rakIn.setHintTextColor(themeColors[3]); rakIn.setBackground(iBg); rakIn.setPadding((int)(20*DENSITY),(int)(15*DENSITY),(int)(20*DENSITY),(int)(15*DENSITY)); android.widget.LinearLayout.LayoutParams rLp = new android.widget.LinearLayout.LayoutParams(-1, -2); rLp.setMargins(0,(int)(10*DENSITY),0,(int)(25*DENSITY)); main.addView(rakIn, rLp);
        android.widget.Button btn = new android.widget.Button(this); btn.setText(lang.get("Add Prayer")); btn.setTextColor(android.graphics.Color.WHITE); btn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btn.setAllCaps(false); android.graphics.drawable.GradientDrawable bBg = new android.graphics.drawable.GradientDrawable(); bBg.setColor(android.graphics.Color.parseColor("#F59E0B")); bBg.setCornerRadius(20f*DENSITY); btn.setBackground(bBg); main.addView(btn, new android.widget.LinearLayout.LayoutParams(-1, (int)(55*DENSITY)));
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]);
        btn.setOnClickListener(new android.view.View.OnClickListener(){@Override public void onClick(android.view.View v){
            String n = nameIn.getText().toString().trim().replace(":", "").replace(",", ""); String r = rakIn.getText().toString().trim();
            if(!n.isEmpty()) { String cList = sp.getString("custom_nafl_list", ""); sp.edit().putString("custom_nafl_list", cList + (cList.isEmpty()?"":",") + n + ":" + (r.isEmpty()?"2":r)).apply(); ad.dismiss(); loadTodayPage(); refreshWidget(); }
        }}); ad.show();
    }
    
    private void showDeleteCustomPrayerDialog(final String cName) {
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1)); android.widget.LinearLayout main = new android.widget.LinearLayout(this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        android.widget.TextView title = new android.widget.TextView(this); title.setText(lang.get("Delete Extra Prayer?")); title.setTextColor(android.graphics.Color.parseColor("#FF5252")); title.setTextSize(20); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setGravity(android.view.Gravity.CENTER); main.addView(title);
        android.widget.TextView sub = new android.widget.TextView(this); sub.setText(lang.get("This will remove it from your list.")); sub.setTextColor(themeColors[3]); sub.setGravity(android.view.Gravity.CENTER); sub.setPadding(0,(int)(10*DENSITY),0,(int)(25*DENSITY)); main.addView(sub);
        android.widget.LinearLayout row = new android.widget.LinearLayout(this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        android.widget.Button btnC = new android.widget.Button(this); btnC.setText(lang.get("CANCEL")); btnC.setTextColor(themeColors[2]); btnC.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btnC.setAllCaps(false); android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); cBg.setColor(themeColors[4]); cBg.setCornerRadius(15f*DENSITY); btnC.setBackground(cBg); android.widget.LinearLayout.LayoutParams lpC = new android.widget.LinearLayout.LayoutParams(0, (int)(50*DENSITY), 1f); lpC.setMargins(0,0,(int)(10*DENSITY),0); row.addView(btnC, lpC);
        android.widget.Button btnD = new android.widget.Button(this); btnD.setText(lang.get("Delete")); btnD.setTextColor(android.graphics.Color.WHITE); btnD.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btnD.setAllCaps(false); android.graphics.drawable.GradientDrawable dBg = new android.graphics.drawable.GradientDrawable(); dBg.setColor(android.graphics.Color.parseColor("#FF5252")); dBg.setCornerRadius(15f*DENSITY); btnD.setBackground(dBg); row.addView(btnD, new android.widget.LinearLayout.LayoutParams(0, (int)(50*DENSITY), 1f)); main.addView(row);
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]);
        btnC.setOnClickListener(new android.view.View.OnClickListener(){@Override public void onClick(android.view.View v){ad.dismiss();}});
        btnD.setOnClickListener(new android.view.View.OnClickListener(){@Override public void onClick(android.view.View v){ String cList = sp.getString("custom_nafl_list", ""); String[] pts = cList.split(","); StringBuilder sb = new StringBuilder(); for(String p : pts) { if(!p.startsWith(cName+":") && !p.equals(cName)) { sb.append(p).append(","); } } String res = sb.toString(); if(res.endsWith(",")) res = res.substring(0, res.length()-1); sp.edit().putString("custom_nafl_list", res).apply(); ad.dismiss(); loadTodayPage(); refreshWidget(); }}); ad.show();
    }
"""

# এবার ক্লাসটির ভেতরে ডায়ালগগুলো ইনজেক্ট করে শেষে ব্র্যাকেট বন্ধ করে দেওয়া
c = c + '\n' + dialogs + '\n}\n'

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Dialog Methods PERFECTLY Injected! You can Build NOW.")
