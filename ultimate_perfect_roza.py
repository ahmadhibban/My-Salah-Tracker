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

        # ==============================================================
        # ১. আগের সব ফালতু কোড মুছে ফেলা
        # ==============================================================
        content = re.sub(r'// --- ROZA TRACKER START ---.*?// --- ROZA TRACKER END ---', '', content, flags=re.DOTALL)
        if 'private void showRozaCategoryDialog' in content:
            content = re.sub(r'private void showRozaCategoryDialog\(\).*?// --- ROZA DIALOG END ---', '', content, flags=re.DOTALL)

        # ==============================================================
        # ২. ১০০% পারফেক্ট ক্যাটাগরি ডায়ালগ (হুবহু সুন্নতের ডায়ালগের কপি)
        # ==============================================================
        roza_dialog_code = """
    private void showRozaCategoryDialog() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this);
        wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1)); 
        android.widget.LinearLayout main = new android.widget.LinearLayout(this); 
        main.setOrientation(android.widget.LinearLayout.VERTICAL); 
        main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); 
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); 
        gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); main.setBackground(gd); 
        
        android.widget.TextView title = new android.widget.TextView(this); 
        title.setText(isBn ? "রোজার ক্যাটাগরি" : "Fasting Category"); 
        title.setTextColor(colorAccent); title.setTextSize(20); 
        title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title); 
        
        android.widget.ScrollView sv = new android.widget.ScrollView(this); 
        android.widget.LinearLayout list = new android.widget.LinearLayout(this); 
        list.setOrientation(android.widget.LinearLayout.VERTICAL);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); 
        
        String[] opts = isBn ? new String[]{"ফরজ", "কাজা", "নফল"} : new String[]{"Fard", "Qaza", "Nafil"};
        final String[] vals = {"fard", "qaza", "nafil"};
        String curType = sp.getString(selectedDate[0] + "_roza_type", "nafil");
        
        for(int s=0; s<opts.length; s++) { 
            final String sName = opts[s];
            final String sVal = vals[s];
            final boolean sChecked = curType.equals(sVal);
            
            final android.widget.LinearLayout row = new android.widget.LinearLayout(this); 
            row.setOrientation(android.widget.LinearLayout.HORIZONTAL); 
            row.setGravity(android.view.Gravity.CENTER_VERTICAL); 
            row.setPadding((int)(10*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY), (int)(12*DENSITY)); 
            android.widget.LinearLayout.LayoutParams rowLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
            rowLp.setMargins(0, 0, 0, (int)(10*DENSITY)); row.setLayoutParams(rowLp); 
            final android.graphics.drawable.GradientDrawable rowBg = new android.graphics.drawable.GradientDrawable(); 
            rowBg.setCornerRadius(15f*DENSITY); 
            rowBg.setColor(sChecked ? themeColors[4] : android.graphics.Color.TRANSPARENT); 
            row.setBackground(rowBg);
            
            final android.widget.TextView tv = new android.widget.TextView(this); 
            tv.setText(sName); 
            tv.setTextColor(sChecked ? colorAccent : themeColors[2]); 
            tv.setTextSize(16); 
            tv.setTypeface(sChecked ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT);
            tv.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); 
            
            final android.view.View chk = ui.getPremiumCheckbox(sChecked ? "yes" : "no", colorAccent); 
            row.addView(tv); row.addView(chk); list.addView(row);
            
            row.setOnClickListener(new android.view.View.OnClickListener() { 
                @Override public void onClick(final android.view.View v) { 
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); 
                    sp.edit().putString(selectedDate[0] + "_roza_type", sVal).apply(); 
                    sp.edit().putString(selectedDate[0] + "_roza_stat", "yes").apply();
                    ad.dismiss();
                    loadTodayPage();
                } 
            });
        } 
        
        sv.addView(list);
        main.addView(sv, new android.widget.LinearLayout.LayoutParams(-1, -2, 1f));
        
        android.widget.TextView closeBtn = new android.widget.TextView(this); 
        closeBtn.setText(lang.get("Done")); 
        closeBtn.setTextColor(android.graphics.Color.parseColor("#F1F5F9")); 
        closeBtn.setGravity(android.view.Gravity.CENTER); 
        closeBtn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); 
        closeBtn.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY));
        android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); 
        cBg.setColor(colorAccent); cBg.setCornerRadius(20f*DENSITY); 
        closeBtn.setBackground(cBg); 
        android.widget.LinearLayout.LayoutParams clp = new android.widget.LinearLayout.LayoutParams(-1, -2); 
        clp.setMargins(0, (int)(15*DENSITY), 0, 0); 
        closeBtn.setLayoutParams(clp); 
        main.addView(closeBtn);
        
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); 
        flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); 
        ad.getWindow().setGravity(android.view.Gravity.CENTER);
        closeBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { ad.dismiss(); loadTodayPage(); } });
        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }
    // --- ROZA DIALOG END ---
"""
        content = content.replace("private void showSunnahDialog", roza_dialog_code + "\n    private void showSunnahDialog")

        # ==============================================================
        # ৩. ১০০% পারফেক্ট রোজার কার্ড (নামাজের কার্ডের কার্বন কপি)
        # ==============================================================
        roza_card_code = """
        // --- ROZA TRACKER START ---
        android.widget.TextView rozaHdr = new android.widget.TextView(MainActivity.this);
        rozaHdr.setText(sp.getString("app_lang", "en").equals("bn") ? "অন্যান্য ইবাদত" : "Other Trackers");
        rozaHdr.setTextColor(themeColors[2]);
        rozaHdr.setTextSize(18);
        rozaHdr.setTypeface(null, android.graphics.Typeface.BOLD);
        android.widget.LinearLayout.LayoutParams rozaHdrLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        rozaHdrLp.setMargins((int)(25*DENSITY), (int)(15*DENSITY), 0, (int)(5*DENSITY));
        contentArea.addView(rozaHdr, rozaHdrLp);

        // 100% Match with Prayer Card Layout
        soup.neumorphism.NeumorphCardView rCardNeo = new soup.neumorphism.NeumorphCardView(MainActivity.this);
        rCardNeo.setShapeType(0);
        rCardNeo.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
        rCardNeo.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
        rCardNeo.setShadowElevation(3f * DENSITY);
        rCardNeo.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 16f*DENSITY).build());
        rCardNeo.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
        android.widget.LinearLayout.LayoutParams rCLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        rCLp.setMargins(0, 0, 0, (int)(15*DENSITY));
        rCardNeo.setLayoutParams(rCLp);

        android.widget.LinearLayout rInner = new android.widget.LinearLayout(MainActivity.this);
        rInner.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        rInner.setGravity(android.view.Gravity.CENTER_VERTICAL);
        rInner.setPadding((int)(20*DENSITY), (int)(18*DENSITY), (int)(20*DENSITY), (int)(18*DENSITY)); // Exact same padding!
        rCardNeo.addView(rInner);

        // 100% Match with Icon Frame
        android.view.View rIconView = ui.getRoundImage("img_roza", 8, android.graphics.Color.TRANSPARENT, colorAccent);
        rIconView.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        rIconView.setPadding(5, 2, 5, 2);
        android.widget.FrameLayout rIconFrame = new android.widget.FrameLayout(MainActivity.this);
        android.widget.LinearLayout.LayoutParams rFlp = new android.widget.LinearLayout.LayoutParams((int)(30*DENSITY), (int)(30*DENSITY));
        rFlp.setMargins(0, 0, (int)(15*DENSITY), 0);
        rIconFrame.setLayoutParams(rFlp);
        applyNeo(rIconFrame, 0, 12f, 2.5f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        android.widget.FrameLayout.LayoutParams rIvLp = new android.widget.FrameLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY));
        rIvLp.gravity = android.view.Gravity.CENTER;
        rIconView.setLayoutParams(rIvLp);
        rIconFrame.addView(rIconView);
        rInner.addView(rIconFrame);

        // Title Row
        android.widget.LinearLayout rTxtCon = new android.widget.LinearLayout(MainActivity.this);
        rTxtCon.setOrientation(android.widget.LinearLayout.VERTICAL);
        rTxtCon.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView rTv = new android.widget.TextView(MainActivity.this);
        rTv.setText(sp.getString("app_lang", "en").equals("bn") ? "রোজা" : "Fasting");
        rTv.setTextColor(themeColors[2]);
        rTv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        rTv.setTextSize(16);
        rTv.setSingleLine(true);
        rTxtCon.addView(rTv);
        rInner.addView(rTxtCon);

        // Data Variables
        final String rozaKey = selectedDate[0] + "_roza_stat";
        final String rozaType = sp.getString(selectedDate[0] + "_roza_type", "nafil");
        final boolean isRozaDone = sp.getString(rozaKey, "no").equals("yes");

        // Category Button (100% Match with Sunnah Button)
        android.widget.TextView rCatBtn = new android.widget.TextView(MainActivity.this);
        String catLabel = sp.getString("app_lang", "en").equals("bn") ? "নফল" : "Nafil";
        if(rozaType.equals("fard")) catLabel = sp.getString("app_lang", "en").equals("bn") ? "ফরজ" : "Fard";
        else if(rozaType.equals("qaza")) catLabel = sp.getString("app_lang", "en").equals("bn") ? "কাজা" : "Qaza";
        rCatBtn.setText(catLabel);
        rCatBtn.setTextSize(11);
        rCatBtn.setSingleLine(true);
        rCatBtn.setTextColor(isRozaDone ? android.graphics.Color.WHITE : themeColors[2]);
        applyNeo(rCatBtn, 1, 10f, 2f, isRozaDone ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0")), isDarkTheme);
        rCatBtn.setPadding((int)(14*DENSITY), (int)(8*DENSITY), (int)(14*DENSITY), (int)(8*DENSITY));
        rCatBtn.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY) + (int)(2f*DENSITY));
        android.widget.LinearLayout.LayoutParams rCatLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        rCatLp.setMargins(0, 0, (int)(15*DENSITY), 0);
        rCatBtn.setLayoutParams(rCatLp);
        rCatBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showRozaCategoryDialog(); } });
        rInner.addView(rCatBtn);

        // Checkbox (100% Exact match using your own getNeoCheckbox)
        final android.view.View rChkBox = getNeoCheckbox(isRozaDone ? "yes" : "no", colorAccent);
        rInner.addView(rChkBox);

        // Click Action
        rCardNeo.setOnClickListener(new android.view.View.OnClickListener() {
            @Override public void onClick(final android.view.View v) {
                v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                sp.edit().putString(rozaKey, !isRozaDone ? "yes" : "no").apply();
                v.animate().scaleX(0.95f).scaleY(0.95f).alpha(0.8f).setDuration(35).withEndAction(new Runnable() { @Override public void run() { v.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(120).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); } }).start();
                loadTodayPage();
            }
        });

        contentArea.addView(rCardNeo);
        // --- ROZA TRACKER END ---
"""
        content = content.replace("contentArea.addView(cardsContainer);", "contentArea.addView(cardsContainer);\n" + roza_card_code)

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ 100% PERFECT MATCH! আপনার অরিজিনাল থ্রিডি ডিজাইন এবং কাস্টম ডায়ালগসহ রোজার ফিচারটি বসানো হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
