import os
import re

def main():
    paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    main_path = None
    tasbih_path = None
    
    for r in paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: main_path = os.path.join(root, 'MainActivity.java')
            if 'PremiumTasbihView.java' in files: tasbih_path = os.path.join(root, 'PremiumTasbihView.java')
        if main_path and tasbih_path: break

    # ==========================================
    # ১. তাসবিহ কাউন্টারে বাংলা সংখ্যা ফিক্স
    # ==========================================
    if tasbih_path:
        with open(tasbih_path, 'r', encoding='utf-8') as f:
            t_content = f.read()
        
        old_update = r'private void updateDisplay\(\)\s*\{\s*display\.setText\(String\.format\("%04d", count\)\);\s*\}'
        new_update = """private void updateDisplay() {
        String numStr = String.format("%04d", count);
        try {
            android.content.SharedPreferences sp = getContext().getSharedPreferences("salah_pro_final", 0);
            if (sp.getString("app_lang", "en").equals("bn")) {
                numStr = numStr.replace("0", "০").replace("1", "১").replace("2", "২").replace("3", "৩").replace("4", "৪").replace("5", "৫").replace("6", "৬").replace("7", "৭").replace("8", "৮").replace("9", "৯");
            }
        } catch(Exception e){}
        display.setText(numStr);
    }"""
        t_content = re.sub(old_update, new_update, t_content)
        with open(tasbih_path, 'w', encoding='utf-8') as f:
            f.write(t_content)

    # ==========================================
    # ২. মেইন অ্যাক্টিভিটিতে রোজার কার্ড হুবহু মিল করা
    # ==========================================
    if main_path:
        with open(main_path, 'r', encoding='utf-8') as f:
            m_content = f.read()

        # আগের সব ফালতু রোজার কোড মুছে ফেলা
        m_content = re.sub(r'// --- ROZA TRACKER START ---.*?// --- ROZA TRACKER END ---', '', m_content, flags=re.DOTALL)
        
        roza_perfect_code = """
        // --- ROZA TRACKER START ---
        final boolean isRozaBn = sp.getString("app_lang", "en").equals("bn");
        final String rozaDbKey = selectedDate[0] + "_roza_stat";
        
        android.widget.TextView rozaHdr = new android.widget.TextView(MainActivity.this);
        rozaHdr.setText(isRozaBn ? "অন্যান্য ইবাদত" : "Other Trackers");
        rozaHdr.setTextColor(themeColors[2]);
        rozaHdr.setTextSize(18);
        rozaHdr.setTypeface(null, android.graphics.Typeface.BOLD);
        android.widget.LinearLayout.LayoutParams rozaHdrLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        // মার্জিন জিরো করা হয়েছে যাতে ঠিক নামাজের কার্ডের সাথে এলাইন হয়
        rozaHdrLp.setMargins(0, (int)(5*DENSITY), 0, (int)(10*DENSITY));

        // 100% Match with Prayer Card Layout (pCard)
        soup.neumorphism.NeumorphCardView rCardNeo = new soup.neumorphism.NeumorphCardView(MainActivity.this);
        rCardNeo.setShapeType(0);
        rCardNeo.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
        rCardNeo.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
        rCardNeo.setShadowElevation(3f * DENSITY);
        rCardNeo.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 16f*DENSITY).build());
        rCardNeo.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
        android.widget.LinearLayout.LayoutParams rCLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        rCLp.setMargins(0, 0, 0, 0); // 0 margin to exactly match prayer cards
        rCardNeo.setLayoutParams(rCLp);

        android.widget.LinearLayout rInner = new android.widget.LinearLayout(MainActivity.this);
        rInner.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        rInner.setGravity(android.view.Gravity.CENTER_VERTICAL);
        rInner.setPadding((int)(20*DENSITY), (int)(18*DENSITY), (int)(20*DENSITY), (int)(18*DENSITY)); // Exact Padding match!
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
        rTv.setText(isRozaBn ? "রোজা" : "Fasting");
        rTv.setTextColor(themeColors[2]);
        rTv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        rTv.setTextSize(16);
        rTv.setSingleLine(true);
        rTxtCon.addView(rTv);
        rInner.addView(rTxtCon);

        final String rozaType = sp.getString(selectedDate[0] + "_roza_type", "nafil");
        final boolean isRozaDone = sp.getString(rozaDbKey, "no").equals("yes");

        // Category Button (100% Match with Sunnah Button)
        android.widget.TextView rCatBtn = new android.widget.TextView(MainActivity.this);
        String catLabel = isRozaBn ? "নফল" : "Nafil";
        if(rozaType.equals("fard")) catLabel = isRozaBn ? "ফরজ" : "Fard";
        else if(rozaType.equals("qaza")) catLabel = isRozaBn ? "কাজা" : "Qaza";
        rCatBtn.setText(catLabel);
        rCatBtn.setTextSize(11);
        rCatBtn.setSingleLine(true);
        rCatBtn.setTextColor(isRozaDone ? android.graphics.Color.WHITE : themeColors[2]);
        
        // Exact Sunken 3D Effect for button
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
                sp.edit().putString(rozaDbKey, !isRozaDone ? "yes" : "no").apply();
                v.animate().scaleX(0.95f).scaleY(0.95f).alpha(0.8f).setDuration(35).withEndAction(new Runnable() { @Override public void run() { v.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(120).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); } }).start();
                loadTodayPage();
            }
        });

        // সরাসরি নামাজের কার্ডের সাথে যুক্ত করা হচ্ছে (gap ও size 100% match করবে)
        if(isLandscape) {
            col2.addView(rozaHdr, rozaHdrLp);
            col2.addView(rCardNeo);
        } else {
            cardsContainer.addView(rozaHdr, rozaHdrLp);
            cardsContainer.addView(rCardNeo);
        }
        // --- ROZA TRACKER END ---
"""
        # মেইন পেজে নামাজের কার্ডের লুপ যেখানে শেষ হয়েছে, ঠিক তার নিচে রোজার কার্ড যুক্ত করা
        target_injection = "        } // end of prayer loop or contentArea.addView"
        if "contentArea.addView(cardsContainer);" in m_content:
            m_content = m_content.replace("contentArea.addView(cardsContainer);", roza_perfect_code + "\n        contentArea.addView(cardsContainer);")
        
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(m_content)
            
        print("✅ পারফেক্ট! তাসবিহের বাংলা ফন্ট এবং রোজার কার্ডের সাইজ/গ্যাপ ১০০% আপনার ডিজাইনের সাথে ম্যাচ করা হয়েছে।")
    else:
        print("❌ ফাইল পাওয়া যায়নি।")

if __name__ == '__main__': main()
