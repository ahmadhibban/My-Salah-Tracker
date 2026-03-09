import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# 1. Fix Zikr List Alignment (Center gravity)
old_tvD = r'tvD\.setLayoutParams\(new android\.widget\.LinearLayout\.LayoutParams\(0,-2,7\.5f\)\);'
new_tvD = r'tvD.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,-2,7.5f)); tvD.setGravity(android.view.Gravity.CENTER);'
c = re.sub(old_tvD, new_tvD, c)

# 2. Update Quran Tab (Para and Page separate inputs)
old_quran_tab = r'private void loadQuranTab\(\) \{.*?ui\.showSmartBanner.*?\}\);\s*\}'

new_quran_tab = r'''private void loadQuranTab() { 
        contentArea.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY)); 
        android.widget.TextView h = new android.widget.TextView(this); h.setText(lang.get("Quran")); h.setTextColor(themeColors[2]); h.setTextSize(24); h.setTypeface(appFonts[1]); h.setPadding(0,0,0,(int)(20*DENSITY)); contentArea.addView(h); 
        
        android.widget.LinearLayout ayatCard = new android.widget.LinearLayout(this); ayatCard.setOrientation(android.widget.LinearLayout.VERTICAL); ayatCard.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); 
        android.graphics.drawable.GradientDrawable aBg = new android.graphics.drawable.GradientDrawable(android.graphics.drawable.GradientDrawable.Orientation.TL_BR, new int[]{colorAccent, android.graphics.Color.parseColor("#1A2980")}); aBg.setCornerRadius(25f*DENSITY); ayatCard.setBackground(aBg); 
        android.widget.LinearLayout.LayoutParams aLp = new android.widget.LinearLayout.LayoutParams(-1, -2); aLp.setMargins(0,0,0,(int)(25*DENSITY)); ayatCard.setLayoutParams(aLp); 
        android.widget.TextView aTitle = new android.widget.TextView(this); aTitle.setText("✨ " + lang.get("Ayat of the Day")); aTitle.setTextColor(android.graphics.Color.WHITE); aTitle.setTextSize(14); aTitle.setTypeface(appFonts[1]); aTitle.setAlpha(0.8f); aTitle.setPadding(0,0,0,(int)(15*DENSITY)); ayatCard.addView(aTitle); 
        
        String[] ar = {"فَإِنَّ مَعَ الْعُسْرِ يُسْرًا", "وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ", "فَاذْكُرُونِي أَذْكُرْكُمْ"}; 
        String[] bn = {"নিশ্চয়ই কষ্টের সাথেই রয়েছে স্বস্তি। (৯৪:৫)", "তোমরা যেখানেই থাকো না কেন, তিনি তোমাদের সাথেই আছেন। (৫৭:৪)", "তোমরা আমাকে স্মরণ করো, আমিও তোমাদের স্মরণ করব। (২:১৫২)"}; 
        int rIdx = java.util.Calendar.getInstance().get(java.util.Calendar.DAY_OF_YEAR) % ar.length; 
        
        android.widget.TextView aAr = new android.widget.TextView(this); aAr.setText(ar[rIdx]); aAr.setTextColor(android.graphics.Color.WHITE); aAr.setTextSize(32); aAr.setTypeface(getArabicFont()); aAr.setGravity(android.view.Gravity.CENTER); aAr.setPadding(0,0,0,(int)(10*DENSITY)); ayatCard.addView(aAr); 
        android.widget.TextView aBn = new android.widget.TextView(this); aBn.setText(bn[rIdx]); aBn.setTextColor(android.graphics.Color.WHITE); aBn.setTextSize(16); aBn.setTypeface(appFonts[0]); aBn.setGravity(android.view.Gravity.CENTER); ayatCard.addView(aBn); 
        contentArea.addView(ayatCard); 
        
        // Input Fields Area
        android.widget.LinearLayout inputCont = new android.widget.LinearLayout(this); inputCont.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        inputCont.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, -2));
        
        // Para Input
        android.widget.LinearLayout pWrap = new android.widget.LinearLayout(this); pWrap.setOrientation(android.widget.LinearLayout.VERTICAL); pWrap.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); pWrap.setPadding(0,0,(int)(10*DENSITY),0);
        android.widget.TextView pT = new android.widget.TextView(this); pT.setText(sp.getString("app_lang","en").equals("bn") ? "পারা" : "Para"); pT.setTextColor(themeColors[3]); pT.setTextSize(14); pT.setTypeface(appFonts[0]); pT.setPadding(0,0,0,(int)(10*DENSITY)); pWrap.addView(pT); 
        final android.widget.EditText etPara = new android.widget.EditText(this); etPara.setText(sp.getString(selectedDate[0]+"_quran_para", "")); etPara.setHint("1-30"); etPara.setInputType(android.text.InputType.TYPE_CLASS_NUMBER); etPara.setTextColor(themeColors[2]); etPara.setHintTextColor(themeColors[3]); etPara.setTypeface(appFonts[1]);
        android.graphics.drawable.GradientDrawable ibg = new android.graphics.drawable.GradientDrawable(); ibg.setColor(themeColors[1]); ibg.setStroke((int)(1.5f*DENSITY), themeColors[4]); ibg.setCornerRadius(20f*DENSITY); etPara.setBackground(ibg); etPara.setPadding((int)(20*DENSITY),(int)(18*DENSITY),(int)(20*DENSITY),(int)(18*DENSITY)); pWrap.addView(etPara);
        inputCont.addView(pWrap);

        // Page Input
        android.widget.LinearLayout pgWrap = new android.widget.LinearLayout(this); pgWrap.setOrientation(android.widget.LinearLayout.VERTICAL); pgWrap.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); pgWrap.setPadding((int)(10*DENSITY),0,0,0);
        android.widget.TextView pgT = new android.widget.TextView(this); pgT.setText(sp.getString("app_lang","en").equals("bn") ? "পৃষ্ঠা" : "Page"); pgT.setTextColor(themeColors[3]); pgT.setTextSize(14); pgT.setTypeface(appFonts[0]); pgT.setPadding(0,0,0,(int)(10*DENSITY)); pgWrap.addView(pgT); 
        final android.widget.EditText etPage = new android.widget.EditText(this); etPage.setText(sp.getString(selectedDate[0]+"_quran_page", "")); etPage.setHint("Eg. 15"); etPage.setInputType(android.text.InputType.TYPE_CLASS_NUMBER); etPage.setTextColor(themeColors[2]); etPage.setHintTextColor(themeColors[3]); etPage.setTypeface(appFonts[1]);
        android.graphics.drawable.GradientDrawable ibg2 = new android.graphics.drawable.GradientDrawable(); ibg2.setColor(themeColors[1]); ibg2.setStroke((int)(1.5f*DENSITY), themeColors[4]); ibg2.setCornerRadius(20f*DENSITY); etPage.setBackground(ibg2); etPage.setPadding((int)(20*DENSITY),(int)(18*DENSITY),(int)(20*DENSITY),(int)(18*DENSITY)); pgWrap.addView(etPage);
        inputCont.addView(pgWrap);
        
        contentArea.addView(inputCont);

        android.widget.Button btn = new android.widget.Button(this); btn.setText(lang.get("Save")); btn.setTextColor(android.graphics.Color.WHITE); btn.setTypeface(appFonts[1]); android.graphics.drawable.GradientDrawable bbg = new android.graphics.drawable.GradientDrawable(); bbg.setColor(colorAccent); bbg.setCornerRadius(20f*DENSITY); btn.setBackground(bbg); btn.setAllCaps(false); 
        android.widget.LinearLayout.LayoutParams blp = new android.widget.LinearLayout.LayoutParams(-1, (int)(55*DENSITY)); blp.setMargins(0,(int)(25*DENSITY),0,0); contentArea.addView(btn, blp); 
        
        btn.setOnClickListener(v -> { 
            v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); 
            String para = etPara.getText().toString().trim(); String page = etPage.getText().toString().trim(); 
            sp.edit().putString(selectedDate[0]+"_quran_para", para).putString(selectedDate[0]+"_quran_page", page).apply(); 
            ui.showSmartBanner((android.widget.FrameLayout)findViewById(android.R.id.content), lang.get("Success"), lang.get("Progress updated."), "img_tick", colorAccent, null); 
        }); 
    }'''

c = re.sub(old_quran_tab, new_quran_tab, c, flags=re.DOTALL)

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Quran Tab (Para & Page) & Zikr List Alignment FIXED!")
