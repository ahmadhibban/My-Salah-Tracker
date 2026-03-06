import os

path = 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # ১. কাস্টম ফন্ট ভেরিয়েবল যুক্ত করা
    if 'Typeface tfReg;' not in content:
        content = content.replace('private Runnable onDateSelected;', 'private Runnable onDateSelected;\n    private android.graphics.Typeface tfReg, tfBold;')
        
        init_fonts = """        this.hijriViewCal = Calendar.getInstance();
        tfReg = android.graphics.Typeface.DEFAULT; tfBold = android.graphics.Typeface.DEFAULT_BOLD;
        try { if (sp.getString("app_lang", "en").equals("bn")) { tfReg = android.graphics.Typeface.createFromAsset(activity.getAssets(), "fonts/hind_reg.ttf"); tfBold = android.graphics.Typeface.createFromAsset(activity.getAssets(), "fonts/hind_bold.ttf"); } else { tfReg = android.graphics.Typeface.createFromAsset(activity.getAssets(), "fonts/poppins_reg.ttf"); tfBold = android.graphics.Typeface.createFromAsset(activity.getAssets(), "fonts/poppins_bold.ttf"); } } catch(Exception e){}"""
        content = content.replace('this.hijriViewCal = Calendar.getInstance();', init_fonts)

    # ২. applyFont মেথড ইনজেক্ট করা
    if 'private void applyFont(' not in content:
        apply_font_method = """
    private void applyFont(android.view.View v) {
        if (v instanceof android.widget.TextView) { 
            android.widget.TextView tv = (android.widget.TextView) v;
            if (tv.getTypeface() != null && tv.getTypeface().isBold()) tv.setTypeface(tfBold); else tv.setTypeface(tfReg); 
        } else if (v instanceof android.view.ViewGroup) { 
            android.view.ViewGroup vg = (android.view.ViewGroup) v;
            for (int i = 0; i < vg.getChildCount(); i++) applyFont(vg.getChildAt(i));
        }
    }
    public void showGregorian"""
        content = content.replace('public void showGregorian', apply_font_method)

    # ৩. সব ডায়ালগে ফন্ট অ্যাপ্লাই করা
    content = content.replace('dialog.show();', 'applyFont(wrap); dialog.show();')
    content = content.replace('yearDialog[0].show();', 'applyFont(wrap); yearDialog[0].show();')
    content = content.replace('ad.show();', 'applyFont(wrap); ad.show();')
    content = content.replace('yAd.show();', 'applyFont(yWrap); yAd.show();')

    # ৪. ইংরেজি ক্যালেন্ডারে হাইলাইট লজিক (আরবি ক্যালেন্ডারের মতো)
    old_greg_highlight = """                    GradientDrawable bgD = new GradientDrawable(); bgD.setShape(GradientDrawable.OVAL);
                    if(sp.getString(dKey+"_"+prayers[0], "no").equals("excused")) { bgD.setColor(Color.parseColor("#FF4081")); tv.setTextColor(Color.WHITE);
                    } 
                    else if(dKey.equals(selectedDate[0])) { bgD.setColor(colorAccent);
                    tv.setTextColor(Color.WHITE); } 
                    else { bgD.setColor(themeColors[1]);
                    }
                    tv.setBackground(isFuture ? bgD : (dKey.equals(selectedDate[0]) ? bgD : ui.getRainbowBorder(dKey, 3)));"""
                
    new_greg_highlight = """                    GradientDrawable bgD = new GradientDrawable(); bgD.setShape(GradientDrawable.OVAL);
                    SalahRecord dRec = SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(dKey);
                    boolean isAllDone = true;
                    if(dRec != null){
                        for(String pName : prayers){
                            String sStat = "no";
                            if(pName.equals("Fajr")) sStat=dRec.fajr; else if(pName.equals("Dhuhr")) sStat=dRec.dhuhr;
                            else if(pName.equals("Asr")) sStat=dRec.asr; else if(pName.equals("Maghrib")) sStat=dRec.maghrib;
                            else if(pName.equals("Isha")) sStat=dRec.isha; else if(pName.equals("Witr")) sStat=dRec.witr;
                            if(!sStat.equals("yes") && !sStat.equals("excused")){ isAllDone = false; break; }
                        }
                    } else { isAllDone = false; }
                    
                    tv.setTextColor(dKey.equals(selectedDate[0]) ? android.graphics.Color.WHITE : (isFuture ? themeColors[4] : (isAllDone ? colorAccent : themeColors[2])));
                    if (dKey.equals(selectedDate[0])) { bgD.setColor(colorAccent); tv.setBackground(bgD); }
                    else if (isAllDone && !isFuture) { bgD.setColor(themeColors[5]); tv.setBackground(bgD); }
                    else { bgD.setColor(android.graphics.Color.TRANSPARENT); tv.setBackground(bgD); }"""

    content = content.replace(old_greg_highlight, new_greg_highlight)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Calendar Helper Updated Successfully! Fonts and Highlights are active.")
else:
    print("❌ Calendar Helper file not found!")

