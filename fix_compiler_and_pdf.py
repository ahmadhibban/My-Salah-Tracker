import os
import re

def main():
    target_main = None
    target_stats = None
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    for r in search_paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: target_main = os.path.join(root, 'MainActivity.java')
            if 'StatsHelper.java' in files: target_stats = os.path.join(root, 'StatsHelper.java')
        if target_main and target_stats: break

    # ১. MainActivity.java ফিক্স (Compile Error + A-Z Menu Sorting)
    if target_main:
        with open(target_main, 'r', encoding='utf-8') as f:
            content = f.read()

        # ভাঙা কোড ব্লকটি সিলেক্ট করে ফ্রেশ কোড দিয়ে রিপ্লেস করা হচ্ছে
        pattern = r'private void showSettingsMenu\(\).*?(?=private void showMarkOptions\(\))'
        
        clean_code = """private void showSettingsMenu() {
        FrameLayout wrap = new FrameLayout(this);
        wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout mainLayout = new LinearLayout(this); mainLayout.setOrientation(LinearLayout.VERTICAL); mainLayout.setPadding((int)(20*DENSITY), (int)(25*DENSITY), (int)(20*DENSITY), (int)(25*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); mainLayout.setBackground(gd);
        TextView title = new TextView(this); title.setText(lang.get("Settings & Options")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); mainLayout.addView(title);
        final AlertDialog ad = new AlertDialog.Builder(this).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(Gravity.CENTER); 

        class MenuRow {
            void addImg(String titleStr, String imgName, final Runnable action) {
                LinearLayout btn = new LinearLayout(MainActivity.this);
                btn.setOrientation(LinearLayout.HORIZONTAL); btn.setGravity(Gravity.CENTER_VERTICAL); btn.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
                GradientDrawable bg = new GradientDrawable(); bg.setColor(themeColors[4]); bg.setCornerRadius(15f*DENSITY); btn.setBackground(bg);
                LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2);
                lp.setMargins(0, 0, 0, (int)(10*DENSITY)); btn.setLayoutParams(lp);
                View icon = ui.getRoundImage(imgName, 0, Color.TRANSPARENT, colorAccent); 
                LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(28*DENSITY), (int)(28*DENSITY)); icLp.setMargins(0,0,(int)(15*DENSITY),0); icon.setLayoutParams(icLp);
                btn.addView(icon);
                TextView t1 = new TextView(MainActivity.this); t1.setText(lang.get(titleStr)); t1.setTextColor(themeColors[2]); t1.setTextSize(16); t1.setTypeface(Typeface.DEFAULT_BOLD); btn.addView(t1);
                btn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { ad.dismiss(); action.run(); } }); mainLayout.addView(btn);
            }
        }
        MenuRow mr = new MenuRow();
        
        // একদম পারফেক্ট A-Z সর্টিং
        mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "হিজরি তারিখ সেটিং" : "Adjust Hijri Date", "img_moon", new Runnable() { @Override public void run() { boolean isBn = sp.getString("app_lang", "en").equals("bn"); FrameLayout wrap = new FrameLayout(MainActivity.this); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1)); LinearLayout main = new LinearLayout(MainActivity.this); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd); TextView title = new TextView(MainActivity.this); title.setText(isBn ? "হিজরি তারিখ সেটিং" : "Adjust Hijri Date"); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title); final AlertDialog ad = new AlertDialog.Builder(MainActivity.this).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(Gravity.CENTER); String[] opts = isBn ? new String[]{"-১ দিন", "ডিফল্ট (০)", "+১ দিন"} : new String[]{"-1 Day", "Default (0)", "+1 Day"}; final int[] vals = {-1, 0, 1}; int current = sp.getInt("hijri_offset", 0); for(int i=0; i<3; i++) { final int idx = i; LinearLayout btn = new LinearLayout(MainActivity.this); btn.setOrientation(LinearLayout.HORIZONTAL); btn.setGravity(Gravity.CENTER); btn.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY)); GradientDrawable bg = new GradientDrawable(); bg.setColor(vals[i] == current ? colorAccent : themeColors[4]); bg.setCornerRadius(15f*DENSITY); btn.setBackground(bg); LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2); lp.setMargins(0, 0, 0, (int)(10*DENSITY)); btn.setLayoutParams(lp); TextView tv = new TextView(MainActivity.this); tv.setText(opts[i]); tv.setTextColor(vals[i] == current ? Color.WHITE : themeColors[2]); tv.setTextSize(16); tv.setTypeface(Typeface.DEFAULT_BOLD); tv.setGravity(Gravity.CENTER); tv.setLayoutParams(new LinearLayout.LayoutParams(-1, -2)); btn.addView(tv); btn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { sp.edit().putInt("hijri_offset", vals[idx]).apply(); ad.dismiss(); loadTodayPage(); refreshWidget(); } }); main.addView(btn); } FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp); applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show(); }});
        mr.addImg("Advanced Statistics", "img_stats", new Runnable() { @Override public void run() { try{statsHelper.syncDate(sdf.parse(selectedDate[0]));}catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); } statsHelper.showStatsOptionsDialog(); }});
        mr.addImg("Backup & Sync", "img_cloud", new Runnable() { @Override public void run() { backupHelper.showProfileDialog(new Runnable() { @Override public void run() { loadTodayPage(); refreshWidget(); }}); }});
        mr.addImg("Change Language", "img_lang", new Runnable() { @Override public void run() { String nextL = sp.getString("app_lang", "en").equals("en") ? "bn" : "en"; sp.edit().putString("app_lang", nextL).apply(); finish(); Intent intent = new Intent(MainActivity.this, MainActivity.class); try { intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime()); } catch(Exception e){} startActivity(intent); overridePendingTransition(0, 0); }});
        mr.addImg("Choose Theme", "img_theme", new Runnable() { @Override public void run() { sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply(); finish(); Intent intent = new Intent(MainActivity.this, MainActivity.class); try { intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime()); } catch(Exception e){} startActivity(intent); overridePendingTransition(0, 0); }});
        mr.addImg("View Qaza List", "img_custom_qaza", new Runnable() { @Override public void run() { showQazaListDialog(); }});

        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(320*DENSITY), -2);
        flp.gravity = Gravity.CENTER; wrap.addView(mainLayout, flp);
        applyFont(mainLayout, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }

    private void showQazaListDialog() {
        FrameLayout wrap = new FrameLayout(this);
        wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout main = new LinearLayout(this); main.setOrientation(LinearLayout.VERTICAL); main.setPadding(0, (int)(30*DENSITY), 0, (int)(30*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        TextView title = new TextView(this); title.setText(lang.get("View Qaza List")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); title.setPadding(0, 0, 0, (int)(20*DENSITY));
        main.addView(title);
        
        final AlertDialog ad = new AlertDialog.Builder(this).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(Gravity.CENTER); 
        
        ScrollView scroll = new ScrollView(this); final LinearLayout list = new LinearLayout(this);
        list.setOrientation(LinearLayout.VERTICAL); list.setPadding((int)(20*DENSITY), 0, (int)(20*DENSITY), 0);
        Calendar cal = Calendar.getInstance(); int qazaCount = 0;
        
        SalahDao dao = SalahDatabase.getDatabase(this).salahDao();
        for(int i=0; i<365; i++) { 
            final String dK = sdf.format(cal.getTime());
            final SalahRecord r = dao.getRecordByDate(dK);
            
            if (r != null) {
                for(final String p : AppConstants.PRAYERS) {
                    if(getQazaStat(r, p) && getFardStat(r, p).equals("no")) {
                        qazaCount++;
                        final LinearLayout row = new LinearLayout(this); row.setOrientation(LinearLayout.HORIZONTAL); row.setGravity(Gravity.CENTER_VERTICAL); row.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
                        GradientDrawable bg = new GradientDrawable(); bg.setColor(themeColors[4]); bg.setCornerRadius(15f*DENSITY); row.setBackground(bg);
                        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2); lp.setMargins(0, 0, 0, (int)(10*DENSITY)); row.setLayoutParams(lp);
                        LinearLayout tLay = new LinearLayout(this); tLay.setOrientation(LinearLayout.VERTICAL);
                        tLay.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
                        TextView t1 = new TextView(this); t1.setText(lang.get(p)); t1.setTextColor(themeColors[2]); t1.setTextSize(16); t1.setTypeface(Typeface.DEFAULT_BOLD);
                        TextView t2 = new TextView(this); t2.setText(lang.getShortGreg(cal.getTime())); t2.setTextColor(themeColors[3]);
                        t2.setTextSize(12);
                        tLay.addView(t1); tLay.addView(t2); row.addView(tLay);
                        TextView btn = new TextView(this); btn.setText(lang.get("Done")); btn.setTextColor(colorAccent); btn.setTypeface(Typeface.DEFAULT_BOLD); btn.setPadding((int)(15*DENSITY), (int)(8*DENSITY), (int)(15*DENSITY), (int)(8*DENSITY));
                        GradientDrawable bBg = new GradientDrawable(); bBg.setColor(themeColors[5]); bBg.setCornerRadius(10f*DENSITY); btn.setBackground(bBg); row.addView(btn);
                        btn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { 
                            setQazaStat(r, p, false); setFardStat(r, p, "yes"); updateRoomRecord(r);
                            sp.edit().putBoolean(dK+"_"+p+"_qaza", false).putString(dK+"_"+p, "yes").apply(); 
                            list.removeView(row); loadTodayPage(); refreshWidget(); 
                        } });
                        list.addView(row);
                    }
                }
            }
            cal.add(Calendar.DATE, -1);
        }
        
        if(qazaCount == 0) { 
            View customEmptyIcon = ui.getRoundImage("img_empty_qaza", 0, android.graphics.Color.TRANSPARENT, colorAccent);
            LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(80*DENSITY), (int)(80*DENSITY)); icLp.gravity = Gravity.CENTER; icLp.setMargins(0, (int)(20*DENSITY), 0, (int)(10*DENSITY)); customEmptyIcon.setLayoutParams(icLp); list.addView(customEmptyIcon);
            TextView empty = new TextView(this);
            empty.setText(lang.get("Alhamdulillah! No pending Qaza.")); empty.setTextColor(themeColors[3]); empty.setGravity(Gravity.CENTER);
            empty.setPadding(0, 0, 0, (int)(20*DENSITY)); list.addView(empty);
        }
        
        scroll.addView(list);
        main.addView(scroll, new LinearLayout.LayoutParams(-1, (int)(300*DENSITY)));
        TextView closeBtn = new TextView(this); closeBtn.setText(lang.get("CLOSE")); closeBtn.setTextColor(themeColors[3]); closeBtn.setGravity(Gravity.CENTER); closeBtn.setTypeface(Typeface.DEFAULT_BOLD); closeBtn.setPadding(0, (int)(20*DENSITY), 0, 0); main.addView(closeBtn);
        closeBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { ad.dismiss(); } });
        FrameLayout.LayoutParams flp2 = new FrameLayout.LayoutParams((int)(320*DENSITY), -2);
        flp2.gravity = Gravity.CENTER; wrap.addView(main, flp2);
        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }
"""

        content = re.sub(pattern, clean_code, content, flags=re.DOTALL)
        
        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ MainActivity.java এর কম্পাইল এরর ফিক্স করা হয়েছে এবং A-Z সর্টিং সফল হয়েছে!")
            
    # ২. StatsHelper.java ফিক্স (Image এবং PDF এ সেন্টার অ্যালাইনমেন্ট)
    if target_stats:
        with open(target_stats, 'r', encoding='utf-8') as f:
            c2 = f.read()

        # Image Report ফিক্স
        c2 = c2.replace('float fX=gX-(bW/2f)-(sV>0?spc/2f:0); float sX=gX+(bW/2f)+(sV>0?spc/2f:0);',
                        'float fX = (sV > 0) ? (gX - bW - spc/2f) : (gX - bW/2f); float sX = (fV > 0) ? (gX + spc/2f) : (gX - bW/2f);')
        
        # PDF ফিক্স
        c2 = c2.replace('float fX=cx-(bW/2f)-(sV>0?spc/2f:0); float sX=cx+(bW/2f)+(sV>0?spc/2f:0);',
                        'float fX = (sV > 0) ? (cx - bW - spc/2f) : (cx - bW/2f); float sX = (fV > 0) ? (cx + spc/2f) : (cx - bW/2f);')

        with open(target_stats, 'w', encoding='utf-8') as f:
            f.write(c2)
        print("✅ Image এবং PDF চার্টে 'ফরজ' এর দাগ সেন্টার করা হয়েছে!")

if __name__ == '__main__': main()
