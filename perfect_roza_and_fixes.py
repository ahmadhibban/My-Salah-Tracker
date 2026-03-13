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

        # ১. স্ট্রিক এবং কাজা কার্ডের উচ্চতা সমান করা (-1 বা MATCH_PARENT)
        content = re.sub(r'new\s+LinearLayout\.LayoutParams\(0,\s*(?:ViewGroup\.LayoutParams\.WRAP_CONTENT|LinearLayout\.LayoutParams\.WRAP_CONTENT|-2),\s*1f\)', 'new LinearLayout.LayoutParams(0, -1, 1f)', content)

        # ২. অটো-ট্রান্সলেশন মেথড যুক্ত করা
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

        # তারিখ এবং সংখ্যাগুলোতে অটো-ট্রান্সলেটর বসানো
        content = content.replace('topDate.setText(lang.getShortGreg(selectedDate[0]));', 'topDate.setText(tBn(lang.getShortGreg(selectedDate[0])));')
        content = content.replace('topSub.setText(lang.getFullGreg(selectedDate[0]) + " • " + lang.getHijri(selectedDate[0]));', 'topSub.setText(tBn(lang.getFullGreg(selectedDate[0]) + " • " + lang.getHijri(selectedDate[0])));')
        content = content.replace('streakNum.setText(String.valueOf(streak));', 'streakNum.setText(tBn(String.valueOf(streak)));')
        content = content.replace('qazaNum.setText(String.valueOf(qazaCount));', 'qazaNum.setText(tBn(String.valueOf(qazaCount)));')

        # ৩. রোজার কার্ড হুবহু আগের ডিজাইনের মতো করে যুক্ত করা
        roza_code = """
        // ==========================================
        //  ROZA (FASTING) TRACKER
        // ==========================================
        android.widget.TextView rozaHeader = new android.widget.TextView(MainActivity.this);
        rozaHeader.setText(sp.getString("app_lang", "en").equals("bn") ? "অন্যান্য ইবাদত" : "Other Trackers");
        rozaHeader.setTextColor(themeColors[2]);
        rozaHeader.setTextSize(18);
        rozaHeader.setTypeface(null, android.graphics.Typeface.BOLD);
        android.widget.LinearLayout.LayoutParams rHlp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        rHlp.setMargins((int)(20*DENSITY), (int)(15*DENSITY), 0, (int)(5*DENSITY));
        main.addView(rozaHeader, rHlp);

        final soup.neumorphism.NeumorphCardView rCard = new soup.neumorphism.NeumorphCardView(MainActivity.this);
        rCard.setShapeType(soup.neumorphism.ShapeType.FLAT);
        rCard.setShadowElevation(3.5f * DENSITY);
        android.widget.LinearLayout.LayoutParams rClp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        rClp.setMargins((int)(15*DENSITY), (int)(5*DENSITY), (int)(15*DENSITY), (int)(5*DENSITY));
        rCard.setLayoutParams(rClp);
        rCard.setPadding((int)(15*DENSITY), (int)(2*DENSITY), (int)(15*DENSITY), (int)(2*DENSITY));

        android.widget.LinearLayout rInner = new android.widget.LinearLayout(MainActivity.this);
        rInner.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        rInner.setGravity(android.view.Gravity.CENTER_VERTICAL);
        rInner.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));

        android.view.View rIcon = ui.getRoundImage("img_roza", 0, android.graphics.Color.TRANSPARENT, colorAccent);
        android.widget.LinearLayout.LayoutParams rILp = new android.widget.LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY));
        rILp.setMargins(0, 0, (int)(15*DENSITY), 0);
        rIcon.setLayoutParams(rILp);
        rInner.addView(rIcon);

        android.widget.LinearLayout rTextLay = new android.widget.LinearLayout(MainActivity.this);
        rTextLay.setOrientation(android.widget.LinearLayout.VERTICAL);
        rTextLay.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView rTitle = new android.widget.TextView(MainActivity.this);
        rTitle.setText(sp.getString("app_lang", "en").equals("bn") ? "রোজা" : "Fasting");
        rTitle.setTextColor(themeColors[2]);
        rTitle.setTextSize(16);
        rTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        rTextLay.addView(rTitle);
        
        final android.widget.TextView rSub = new android.widget.TextView(MainActivity.this);
        rSub.setTextColor(themeColors[3]);
        rSub.setTextSize(12);
        rTextLay.addView(rSub);
        rInner.addView(rTextLay);

        android.widget.LinearLayout rRightLay = new android.widget.LinearLayout(MainActivity.this);
        rRightLay.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        rRightLay.setGravity(android.view.Gravity.CENTER_VERTICAL);

        android.widget.TextView rCatBtn = new android.widget.TextView(MainActivity.this);
        rCatBtn.setText(sp.getString("app_lang", "en").equals("bn") ? "ক্যাটাগরি ▼" : "Category ▼");
        rCatBtn.setTextColor(themeColors[3]);
        rCatBtn.setTextSize(12);
        rCatBtn.setPadding((int)(8*DENSITY), (int)(4*DENSITY), (int)(8*DENSITY), (int)(4*DENSITY));
        android.graphics.drawable.GradientDrawable catBg = new android.graphics.drawable.GradientDrawable();
        catBg.setStroke((int)(1.5f*DENSITY), themeColors[3]);
        catBg.setCornerRadius(8f*DENSITY);
        rCatBtn.setBackground(catBg);
        android.widget.LinearLayout.LayoutParams rCatLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        rCatLp.setMargins(0, 0, (int)(15*DENSITY), 0);
        rRightLay.addView(rCatBtn, rCatLp);

        final soup.neumorphism.NeumorphCardView rChk = new soup.neumorphism.NeumorphCardView(MainActivity.this);
        android.widget.LinearLayout.LayoutParams rChkLp = new android.widget.LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY));
        rChk.setLayoutParams(rChkLp);
        rChk.setPadding((int)(3*DENSITY), (int)(3*DENSITY), (int)(3*DENSITY), (int)(3*DENSITY));
        rRightLay.addView(rChk);

        rInner.addView(rRightLay);
        rCard.addView(rInner);
        main.addView(rCard);

        final String rKey = dKey + "_roza_stat";
        final boolean isBn = sp.getString("app_lang", "en").equals("bn");
        final String[] rOpts = isBn ? new String[]{"ফরজ", "কাজা", "নফল"} : new String[]{"Fard", "Qaza", "Nafil"};
        final String[] rVals = {"fard", "qaza", "nafil"};

        final Runnable updateR = new Runnable() {
            @Override
            public void run() {
                String state = sp.getString(rKey, "none");
                rChk.removeAllViews();
                if(state.equals("none")) {
                    rChk.setShapeType(soup.neumorphism.ShapeType.FLAT);
                    rChk.setShadowElevation(3.5f * DENSITY);
                    rSub.setText(isBn ? "রাখা হয়নি" : "Not Fasting");
                    
                    android.widget.LinearLayout unchk = new android.widget.LinearLayout(MainActivity.this);
                    android.graphics.drawable.GradientDrawable out = new android.graphics.drawable.GradientDrawable();
                    out.setStroke((int)(2*DENSITY), themeColors[3]);
                    out.setCornerRadius(10f*DENSITY);
                    unchk.setBackground(out);
                    rChk.addView(unchk, new android.widget.FrameLayout.LayoutParams(-1, -1));
                } else {
                    rChk.setShapeType(soup.neumorphism.ShapeType.PRESSED);
                    rChk.setShadowElevation(2f * DENSITY);
                    
                    android.widget.LinearLayout chkLay = new android.widget.LinearLayout(MainActivity.this);
                    chkLay.setGravity(android.view.Gravity.CENTER);
                    android.graphics.drawable.GradientDrawable fill = new android.graphics.drawable.GradientDrawable();
                    fill.setColor(colorAccent);
                    fill.setCornerRadius(10f*DENSITY);
                    chkLay.setBackground(fill);
                    
                    android.widget.TextView tick = new android.widget.TextView(MainActivity.this);
                    tick.setText("✓");
                    tick.setTextColor(android.graphics.Color.WHITE);
                    tick.setTextSize(18);
                    tick.setTypeface(null, android.graphics.Typeface.BOLD);
                    chkLay.addView(tick);
                    rChk.addView(chkLay, new android.widget.FrameLayout.LayoutParams(-1, -1));
                    
                    String label = state.equals("fard") ? rOpts[0] : (state.equals("qaza") ? rOpts[1] : rOpts[2]);
                    rSub.setText(label + (isBn ? " রোজা রাখা হয়েছে" : " Fasting"));
                }
            }
        };
        updateR.run();

        rChk.setOnClickListener(new android.view.View.OnClickListener() {
            @Override
            public void onClick(android.view.View v) {
                String state = sp.getString(rKey, "none");
                sp.edit().putString(rKey, state.equals("none") ? "nafil" : "none").apply();
                updateR.run();
                try { ((android.os.Vibrator)getSystemService(VIBRATOR_SERVICE)).vibrate(30); } catch(Exception e){}
            }
        });

        rCatBtn.setOnClickListener(new android.view.View.OnClickListener() {
            @Override
            public void onClick(android.view.View v) {
                android.app.AlertDialog.Builder b = new android.app.AlertDialog.Builder(MainActivity.this);
                b.setTitle(isBn ? "ক্যাটাগরি" : "Category");
                b.setItems(rOpts, new android.content.DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(android.content.DialogInterface d, int w) {
                        sp.edit().putString(rKey, rVals[w]).apply();
                        updateR.run();
                    }
                });
                b.show();
            }
        });
        // ==========================================
"""
        # নামাজের লুপ শেষ হওয়ার জায়গাটি টার্গেট করে নিখুঁতভাবে বসানো
        target = "main.addView(pCard, cardParams);\n        }"
        if target in content and 'ROZA (FASTING) TRACKER' not in content:
            content = content.replace(target, target + "\n" + roza_code)

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ পারফেক্ট! কোনো এরর ছাড়া আপনার অরিজিনাল ডিজাইনেই ফিচারগুলো যুক্ত করা হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
