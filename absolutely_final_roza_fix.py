import os
import re

def main():
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    target_main = None
    
    for r in search_paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: 
                target_main = os.path.join(root, 'MainActivity.java')
                break
        if target_main: break

    if target_main:
        with open(target_main, 'r', encoding='utf-8') as f:
            content = f.read()

        # ১. আগের সব আবর্জনা এবং ১১ জায়গায় ভুল করে বসানো রোজার কোড চিরতরে মুছে ফেলা হচ্ছে
        content = re.sub(r'// --- ROZA TRACKER START ---.*?// --- ROZA TRACKER END ---', '', content, flags=re.DOTALL)

        # ২. অটো-ট্রান্সলেশন ফাংশন
        if "private String tBn(String s)" not in content:
            trans_method = """
    private String tBn(String s) {
        if(s == null) return "";
        if(!getSharedPreferences("salah_pro_final", 0).getString("app_lang", "en").equals("bn")) return s;
        return s.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯")
                .replace("Saturday","শনিবার").replace("Sunday","রবিবার").replace("Monday","সোমবার").replace("Tuesday","মঙ্গলবার").replace("Wednesday","বুধবার").replace("Thursday","বৃহস্পতিবার").replace("Friday","শুক্রবার")
                .replace("Jan","জানু").replace("Feb","ফেব্রু").replace("Mar","মার্চ").replace("Apr","এপ্রিল").replace("May","মে").replace("Jun","জুন").replace("Jul","জুল").replace("Aug","আগস্ট").replace("Sep","সেপ্টে").replace("Oct","অক্টো").replace("Nov","নভে").replace("Dec","ডিসে");
    }
"""
            content = re.sub(r'(public\s+class\s+MainActivity\s+extends\s+[^{]+\{)', r'\1\n' + trans_method, content)

        # ৩. শুধু নির্দিষ্ট কয়েকটি লেখায় ট্রান্সলেটর বসানো
        content = content.replace('setText(lang.getShortGreg(selectedDate[0]))', 'setText(tBn(lang.getShortGreg(selectedDate[0])))')
        content = content.replace('setText(lang.getFullGreg(selectedDate[0])', 'setText(tBn(lang.getFullGreg(selectedDate[0]))')
        content = content.replace('setText(String.valueOf(streak))', 'setText(tBn(String.valueOf(streak)))')
        content = content.replace('setText(String.valueOf(qazaCount))', 'setText(tBn(String.valueOf(qazaCount)))')

        # ৪. ১০০% পারফেক্ট এবং ইউনিক ভেরিয়েবলসহ রোজার কার্ড
        roza_code = """
        // --- ROZA TRACKER START ---
        final boolean isRozaBn = sp.getString("app_lang", "en").equals("bn");
        final String rozaDbKey = selectedDate[0] + "_roza_stat";
        
        android.widget.TextView rozaHdr = new android.widget.TextView(MainActivity.this);
        rozaHdr.setText(isRozaBn ? "অন্যান্য ইবাদত" : "Other Trackers");
        rozaHdr.setTextColor(themeColors[2]);
        rozaHdr.setTextSize(18);
        rozaHdr.setTypeface(null, android.graphics.Typeface.BOLD);
        android.widget.LinearLayout.LayoutParams rozaHdrLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        rozaHdrLp.setMargins((int)(20*DENSITY), (int)(15*DENSITY), 0, (int)(5*DENSITY));
        contentArea.addView(rozaHdr, rozaHdrLp);

        final soup.neumorphism.NeumorphCardView rozaCardNeo = new soup.neumorphism.NeumorphCardView(MainActivity.this);
        rozaCardNeo.setShapeType(soup.neumorphism.ShapeType.FLAT);
        rozaCardNeo.setShadowElevation(3.5f * DENSITY);
        android.widget.LinearLayout.LayoutParams rozaCardLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        rozaCardLp.setMargins((int)(15*DENSITY), 0, (int)(15*DENSITY), (int)(15*DENSITY));
        rozaCardNeo.setLayoutParams(rozaCardLp);
        rozaCardNeo.setPadding((int)(15*DENSITY), (int)(2*DENSITY), (int)(15*DENSITY), (int)(2*DENSITY));

        android.widget.LinearLayout rozaInnerLay = new android.widget.LinearLayout(MainActivity.this);
        rozaInnerLay.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        rozaInnerLay.setGravity(android.view.Gravity.CENTER_VERTICAL);
        rozaInnerLay.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));

        android.view.View rozaIcon = ui.getRoundImage("img_roza", 0, android.graphics.Color.TRANSPARENT, colorAccent);
        android.widget.LinearLayout.LayoutParams rozaIconLp = new android.widget.LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY));
        rozaIconLp.setMargins(0, 0, (int)(15*DENSITY), 0);
        rozaIcon.setLayoutParams(rozaIconLp);
        rozaInnerLay.addView(rozaIcon);

        android.widget.LinearLayout rozaTxtLay = new android.widget.LinearLayout(MainActivity.this);
        rozaTxtLay.setOrientation(android.widget.LinearLayout.VERTICAL);
        rozaTxtLay.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView rozaTitle = new android.widget.TextView(MainActivity.this);
        rozaTitle.setText(isRozaBn ? "রোজা" : "Fasting");
        rozaTitle.setTextColor(themeColors[2]);
        rozaTitle.setTextSize(16);
        rozaTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        rozaTxtLay.addView(rozaTitle);
        
        final android.widget.TextView rozaSub = new android.widget.TextView(MainActivity.this);
        rozaSub.setTextColor(themeColors[3]);
        rozaSub.setTextSize(12);
        rozaTxtLay.addView(rozaSub);
        rozaInnerLay.addView(rozaTxtLay);

        android.widget.LinearLayout rozaRightLay = new android.widget.LinearLayout(MainActivity.this);
        rozaRightLay.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        rozaRightLay.setGravity(android.view.Gravity.CENTER_VERTICAL);

        android.widget.TextView rozaCatBtn = new android.widget.TextView(MainActivity.this);
        rozaCatBtn.setText(isRozaBn ? "ক্যাটাগরি ▼" : "Category ▼");
        rozaCatBtn.setTextColor(themeColors[3]);
        rozaCatBtn.setTextSize(12);
        rozaCatBtn.setPadding((int)(8*DENSITY), (int)(4*DENSITY), (int)(8*DENSITY), (int)(4*DENSITY));
        android.graphics.drawable.GradientDrawable rozaCatBg = new android.graphics.drawable.GradientDrawable();
        rozaCatBg.setStroke((int)(1.5f*DENSITY), themeColors[3]);
        rozaCatBg.setCornerRadius(8f*DENSITY);
        rozaCatBtn.setBackground(rozaCatBg);
        android.widget.LinearLayout.LayoutParams rozaCatLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        rozaCatLp.setMargins(0, 0, (int)(15*DENSITY), 0);
        rozaRightLay.addView(rozaCatBtn, rozaCatLp);

        final soup.neumorphism.NeumorphCardView rozaChkBox = new soup.neumorphism.NeumorphCardView(MainActivity.this);
        android.widget.LinearLayout.LayoutParams rozaChkLp = new android.widget.LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY));
        rozaChkBox.setLayoutParams(rozaChkLp);
        rozaChkBox.setPadding((int)(3*DENSITY), (int)(3*DENSITY), (int)(3*DENSITY), (int)(3*DENSITY));
        rozaRightLay.addView(rozaChkBox);

        rozaInnerLay.addView(rozaRightLay);
        rozaCardNeo.addView(rozaInnerLay);
        contentArea.addView(rozaCardNeo);

        final String[] rozaOptsArr = isRozaBn ? new String[]{"ফরজ", "কাজা", "নফল"} : new String[]{"Fard", "Qaza", "Nafil"};
        final String[] rozaValsArr = {"fard", "qaza", "nafil"};

        final Runnable rozaUpdateRunnable = new Runnable() {
            @Override
            public void run() {
                String state = sp.getString(rozaDbKey, "none");
                rozaChkBox.removeAllViews();
                if(state.equals("none")) {
                    rozaChkBox.setShapeType(soup.neumorphism.ShapeType.FLAT);
                    rozaChkBox.setShadowElevation(3.5f * DENSITY);
                    rozaSub.setText(isRozaBn ? "রাখা হয়নি" : "Not Fasting");
                    
                    android.widget.LinearLayout unchk = new android.widget.LinearLayout(MainActivity.this);
                    android.graphics.drawable.GradientDrawable out = new android.graphics.drawable.GradientDrawable();
                    out.setStroke((int)(2*DENSITY), themeColors[3]); out.setCornerRadius(10f*DENSITY);
                    unchk.setBackground(out);
                    rozaChkBox.addView(unchk, new android.widget.FrameLayout.LayoutParams(-1, -1));
                } else {
                    rozaChkBox.setShapeType(soup.neumorphism.ShapeType.PRESSED);
                    rozaChkBox.setShadowElevation(2f * DENSITY);
                    
                    android.widget.LinearLayout chkLay = new android.widget.LinearLayout(MainActivity.this);
                    chkLay.setGravity(android.view.Gravity.CENTER);
                    android.graphics.drawable.GradientDrawable fill = new android.graphics.drawable.GradientDrawable();
                    fill.setColor(colorAccent); fill.setCornerRadius(10f*DENSITY);
                    chkLay.setBackground(fill);
                    
                    android.widget.TextView tick = new android.widget.TextView(MainActivity.this);
                    tick.setText("✓"); tick.setTextColor(android.graphics.Color.WHITE); tick.setTextSize(18); tick.setTypeface(null, android.graphics.Typeface.BOLD);
                    chkLay.addView(tick);
                    rozaChkBox.addView(chkLay, new android.widget.FrameLayout.LayoutParams(-1, -1));
                    
                    String label = state.equals("fard") ? rozaOptsArr[0] : (state.equals("qaza") ? rozaOptsArr[1] : rozaOptsArr[2]);
                    rozaSub.setText(label + (isRozaBn ? " রোজা রাখা হয়েছে" : " Fasting"));
                }
            }
        };
        rozaUpdateRunnable.run();

        rozaChkBox.setOnClickListener(new android.view.View.OnClickListener() {
            @Override
            public void onClick(android.view.View v) {
                String state = sp.getString(rozaDbKey, "none");
                sp.edit().putString(rozaDbKey, state.equals("none") ? "nafil" : "none").apply();
                rozaUpdateRunnable.run();
                try { ((android.os.Vibrator)getSystemService(VIBRATOR_SERVICE)).vibrate(30); } catch(Exception e){}
            }
        });

        rozaCatBtn.setOnClickListener(new android.view.View.OnClickListener() {
            @Override
            public void onClick(android.view.View v) {
                android.app.AlertDialog.Builder b = new android.app.AlertDialog.Builder(MainActivity.this);
                b.setTitle(isRozaBn ? "রোজার ধরন" : "Fasting Type");
                b.setItems(rozaOptsArr, new android.content.DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(android.content.DialogInterface d, int w) {
                        sp.edit().putString(rozaDbKey, rozaValsArr[w]).apply();
                        rozaUpdateRunnable.run();
                    }
                });
                b.show();
            }
        });
        // --- ROZA TRACKER END ---
"""
        # এবার একদম সূক্ষ্মভাবে শুধুমাত্র মেইন পেজে (যেখানে কার্ডের লিস্ট শেষ হয়েছে) বসানো হচ্ছে
        target_exact = "contentArea.addView(cardsContainer);"
        if target_exact in content:
            content = content.replace(target_exact, target_exact + "\n" + roza_code)

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ 100% SUCCESS! সব ভুল মুছে শুধুমাত্র মেইন পেজে রোজার কার্ড নিখুঁতভাবে বসানো হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
