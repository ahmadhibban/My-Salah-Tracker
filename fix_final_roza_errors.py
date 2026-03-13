import os

def main():
    target_main = None
    for r in ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']:
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

        start_marker = '// --- ROZA TRACKER START ---'
        end_marker = '// --- ROZA TRACKER END ---'
        
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            # একদম ক্লিন এবং ফ্রেশ কোড, কোনো ভেরিয়েবল কনফ্লিক্ট ছাড়া
            clean_roza_block = """// --- ROZA TRACKER START ---
        android.content.SharedPreferences spR = getSharedPreferences("salah_pro_final", 0);
        final boolean isBnLangRoza = spR.getString("app_lang", "en").equals("bn");
        final String rKey = selectedDate[0] + "_roza_stat";
        
        android.widget.TextView rHdr = new android.widget.TextView(MainActivity.this);
        rHdr.setText(isBnLangRoza ? "অন্যান্য ইবাদত" : "Other Trackers");
        rHdr.setTextColor(themeColors[2]);
        rHdr.setTextSize(18);
        rHdr.setTypeface(null, android.graphics.Typeface.BOLD);
        android.widget.LinearLayout.LayoutParams rHdrLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        rHdrLp.setMargins((int)(15*DENSITY), (int)(15*DENSITY), 0, (int)(5*DENSITY));
        main.addView(rHdr, rHdrLp);

        final soup.neumorphism.NeumorphCardView rCard = new soup.neumorphism.NeumorphCardView(MainActivity.this);
        rCard.setShapeType(soup.neumorphism.ShapeType.FLAT);
        rCard.setShadowElevation(3.5f * DENSITY);
        android.widget.LinearLayout.LayoutParams rCardLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        rCardLp.setMargins((int)(15*DENSITY), 0, (int)(15*DENSITY), 0);
        rCard.setLayoutParams(rCardLp);
        rCard.setPadding((int)(15*DENSITY), (int)(2*DENSITY), (int)(15*DENSITY), (int)(2*DENSITY));

        android.widget.LinearLayout rInner = new android.widget.LinearLayout(MainActivity.this);
        rInner.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        rInner.setGravity(android.view.Gravity.CENTER_VERTICAL);
        rInner.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));

        android.view.View rIcon = ui.getRoundImage("img_roza", 0, android.graphics.Color.TRANSPARENT, colorAccent);
        android.widget.LinearLayout.LayoutParams rIconLp = new android.widget.LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY));
        rIconLp.setMargins(0, 0, (int)(15*DENSITY), 0);
        rIcon.setLayoutParams(rIconLp);
        rInner.addView(rIcon);

        android.widget.LinearLayout rTxtLay = new android.widget.LinearLayout(MainActivity.this);
        rTxtLay.setOrientation(android.widget.LinearLayout.VERTICAL);
        rTxtLay.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView rTitle = new android.widget.TextView(MainActivity.this);
        rTitle.setText(isBnLangRoza ? "রোজা" : "Fasting");
        rTitle.setTextColor(themeColors[2]);
        rTitle.setTextSize(16);
        rTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        rTxtLay.addView(rTitle);
        
        final android.widget.TextView rSub = new android.widget.TextView(MainActivity.this);
        rSub.setTextColor(themeColors[3]);
        rSub.setTextSize(12);
        rTxtLay.addView(rSub);
        rInner.addView(rTxtLay);

        android.widget.LinearLayout rRightLay = new android.widget.LinearLayout(MainActivity.this);
        rRightLay.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        rRightLay.setGravity(android.view.Gravity.CENTER_VERTICAL);

        android.widget.TextView rCatBtn = new android.widget.TextView(MainActivity.this);
        rCatBtn.setText(isBnLangRoza ? "ক্যাটাগরি ▼" : "Category ▼");
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

        final String[] rOpts = isBnLangRoza ? new String[]{"ফরজ", "কাজা", "নফল"} : new String[]{"Fard", "Qaza", "Nafil"};
        final String[] rVals = {"fard", "qaza", "nafil"};

        final Runnable updateR = new Runnable() {
            @Override
            public void run() {
                String state = spR.getString(rKey, "none");
                rChk.removeAllViews();
                if(state.equals("none")) {
                    rChk.setShapeType(soup.neumorphism.ShapeType.FLAT);
                    rChk.setShadowElevation(3.5f * DENSITY);
                    rSub.setText(isBnLangRoza ? "রাখা হয়নি" : "Not Fasting");
                    
                    android.widget.LinearLayout unchk = new android.widget.LinearLayout(MainActivity.this);
                    android.graphics.drawable.GradientDrawable out = new android.graphics.drawable.GradientDrawable();
                    out.setStroke((int)(2*DENSITY), themeColors[3]); out.setCornerRadius(10f*DENSITY);
                    unchk.setBackground(out);
                    rChk.addView(unchk, new android.widget.FrameLayout.LayoutParams(-1, -1));
                } else {
                    rChk.setShapeType(soup.neumorphism.ShapeType.PRESSED);
                    rChk.setShadowElevation(2f * DENSITY);
                    
                    android.widget.LinearLayout chkLay = new android.widget.LinearLayout(MainActivity.this);
                    chkLay.setGravity(android.view.Gravity.CENTER);
                    android.graphics.drawable.GradientDrawable fill = new android.graphics.drawable.GradientDrawable();
                    fill.setColor(colorAccent); fill.setCornerRadius(10f*DENSITY);
                    chkLay.setBackground(fill);
                    
                    android.widget.TextView tick = new android.widget.TextView(MainActivity.this);
                    tick.setText("✓"); tick.setTextColor(android.graphics.Color.WHITE); tick.setTextSize(18); tick.setTypeface(null, android.graphics.Typeface.BOLD);
                    chkLay.addView(tick);
                    rChk.addView(chkLay, new android.widget.FrameLayout.LayoutParams(-1, -1));
                    
                    String label = state.equals("fard") ? rOpts[0] : (state.equals("qaza") ? rOpts[1] : rOpts[2]);
                    rSub.setText(label + (isBnLangRoza ? " রোজা রাখা হয়েছে" : " Fasting"));
                }
            }
        };
        updateR.run();

        rChk.setOnClickListener(new android.view.View.OnClickListener() {
            @Override
            public void onClick(android.view.View v) {
                String state = spR.getString(rKey, "none");
                spR.edit().putString(rKey, state.equals("none") ? "nafil" : "none").apply();
                updateR.run();
                try { ((android.os.Vibrator)getSystemService(VIBRATOR_SERVICE)).vibrate(30); } catch(Exception e){}
            }
        });

        rCatBtn.setOnClickListener(new android.view.View.OnClickListener() {
            @Override
            public void onClick(android.view.View v) {
                android.app.AlertDialog.Builder b = new android.app.AlertDialog.Builder(MainActivity.this);
                b.setTitle(isBnLangRoza ? "রোজার ধরন" : "Fasting Type");
                b.setItems(rOpts, new android.content.DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(android.content.DialogInterface d, int w) {
                        spR.edit().putString(rKey, rVals[w]).apply();
                        updateR.run();
                    }
                });
                b.show();
            }
        });
        // --- ROZA TRACKER END ---"""
            
            content = content[:start_idx] + clean_roza_block + content[end_idx + len(end_marker):]

            with open(target_main, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ শেষ! সমস্ত কনফ্লিক্ট এবং এরর চিরতরে মুছে ফ্রেশ কোড বসানো হয়েছে।")
        else:
            print("❌ রোজার কোড ব্লকটি খুঁজে পাওয়া যায়নি।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
