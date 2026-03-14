import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    if 'MainActivity.java' in f:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ফরজের কার্ডের জন্য নতুন জামাত/একাকী লজিক
        new_jamaat_logic = r'''
            // --- NEW JAMAAT LOGIC START ---
            if (!stat.equals("excused")) {
                TextView jamaatBtn = new TextView(this);
                final String jKey = selectedDate[0] + "_" + name + "_jamaat";
                String jStat = sp.getString(jKey, "jamaat"); // "jamaat" or "alone"
                boolean isDone = stat.equals("yes");
                
                boolean isBn = sp.getString("app_lang", "en").equals("bn");
                String sText = jStat.equals("jamaat") ? (isBn ? "জামাতের সাথে" : "Jamaat") : (isBn ? "একাকী" : "Alone");
                jamaatBtn.setText(sText); 
                jamaatBtn.setTextSize(11); 
                jamaatBtn.setSingleLine(true);
                jamaatBtn.setTextColor(isDone ? android.graphics.Color.WHITE : themeColors[2]);
                
                applyNeo(jamaatBtn, 1, 10f, 2f, isDone ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0")), isDarkTheme);
                
                jamaatBtn.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY) + (int)(2f*DENSITY));
                LinearLayout.LayoutParams cLp2 = new LinearLayout.LayoutParams(-2, -2); 
                cLp2.setMargins(0, 0, (int)(15*DENSITY), 0); 
                jamaatBtn.setLayoutParams(cLp2);
                
                jamaatBtn.setOnClickListener(new View.OnClickListener() { 
                    @Override public void onClick(View v) { 
                        if (!stat.equals("yes")) return;
                        v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                        showJamaatDialog(jKey);
                    } 
                }); 
                innerCard.addView(jamaatBtn);
            }
            // --- NEW JAMAAT LOGIC END ---
            '''
        
        # আগের সুন্নতের লজিকগুলো সরিয়ে জামাতের লজিক বসানো হচ্ছে
        pattern = r'if\s*\(\s*AppConstants\.SUNNAHS\[i\]\.length\s*>\s*0\s*&&\s*!stat\.equals\("excused"\)\s*\)\s*\{.*?\}\s*(?=final\s*View\s*chk\s*=\s*getNeoCheckbox)'
        c = re.sub(pattern, new_jamaat_logic, c, flags=re.DOTALL)
        
        # জামাত বা একাকী সিলেক্ট করার পপ-আপ ডায়ালগ
        jamaat_dialog_method = r'''
    private void showJamaatDialog(final String jKey) {
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
        title.setText(isBn ? "কিভাবে পড়েছেন?" : "How did you pray?"); 
        title.setTextColor(colorAccent); title.setTextSize(20); 
        title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title); 
        
        android.widget.ScrollView sv = new android.widget.ScrollView(this);
        android.widget.LinearLayout list = new android.widget.LinearLayout(this); 
        list.setOrientation(android.widget.LinearLayout.VERTICAL);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); 
        
        String[] opts = isBn ? new String[]{"জামাতের সাথে", "একাকী"} : new String[]{"Jamaat", "Alone"};
        final String[] vals = {"jamaat", "alone"};
        String curType = sp.getString(jKey, "jamaat");
        
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
            tv.setTextSize(16); tv.setTypeface(android.graphics.Typeface.DEFAULT); 
            tv.setTypeface(sChecked ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT);
            tv.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
            final android.view.View chk = ui.getPremiumCheckbox(sChecked ? "yes" : "no", colorAccent); 
            row.addView(tv); row.addView(chk); list.addView(row);
            row.setOnClickListener(new android.view.View.OnClickListener() { 
                @Override public void onClick(final android.view.View v) { 
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); 
                    sp.edit().putString(jKey, sVal).apply(); 
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
        closeBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { ad.dismiss(); } });
        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }
'''
        if "showJamaatDialog" not in c:
            c = c.replace('public class MainActivity extends Activity {', 'public class MainActivity extends Activity {\n' + jamaat_dialog_method)

        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ ধাপ ২: ফরজের কার্ডে জামাত/একাকী অপশন যুক্ত করা হয়েছে!")
