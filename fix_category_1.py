import re

def rep(f, old, new):
    c = open(f).read()
    if old in c: open(f,'w').write(c.replace(old, new))

# 1. LanguageEngine: Add New Words
le = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
c = open(le).read()
if '"Wipe All Data"' not in c:
    c = c.replace('bnMap.put("Settings & Options", "সেটিংস এবং অপশন");',
                  'bnMap.put("Settings & Options", "সেটিংস এবং অপশন");\n        bnMap.put("Wipe All Data", "সব ডাটা মুছে ফেলুন");\n        bnMap.put("Are you sure? This will delete all your local data permanently.", "আপনি কি নিশ্চিত? এটি আপনার ফোনের সব লোকাল ডাটা চিরতরে মুছে ফেলবে।");\n        bnMap.put("Deleting...", "মুছে ফেলা হচ্ছে...");\n        bnMap.put("Offline Data", "অফলাইন ডাটা");\n        bnMap.put("Data will sync when internet is available.", "ইন্টারনেট কানেকশন এলে ডাটা অটোম্যাটিক সিঙ্ক হবে।");\n        bnMap.put("Delete", "মুছে ফেলুন");')
    open(le,'w').write(c)

# 2. MainActivity: Landscape Lock, Offline Icon, Multi-device Sync, 1s Anim, Wipe Data
ma = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(ma).read()

# Portrait Lock & Auto-Sync on Resume
c = c.replace('protected void onCreate(Bundle savedInstanceState) {',
              '@Override protected void onResume() { super.onResume(); if(sp!=null && !sp.getString("user_email", "").isEmpty() && sp.getString("offline_q", "").isEmpty()) { fbHelper.fetchAndLoad(null, new Runnable() { @Override public void run() { loadTodayPage(); refreshWidget(); } }, null); } }\n\n    @Override\n    protected void onCreate(Bundle savedInstanceState) {')
c = c.replace('setContentView(root);', 'setRequestedOrientation(android.content.pm.ActivityInfo.SCREEN_ORIENTATION_PORTRAIT); setContentView(root);')

# Animation Time (2s -> 1s)
c = c.replace('}, 2000);', '}, 1000);')

# Offline Icon Setup
o_icon = 'View periodBtn = ui.getRoundImage("img_period"'
n_icon = 'View offBtn = ui.getRoundImage("img_offline_warning", 6, themeColors[5], android.graphics.Color.parseColor("#FF5252")); LinearLayout.LayoutParams offLp = new LinearLayout.LayoutParams((int)(34 * DENSITY), (int)(34 * DENSITY)); offLp.setMargins(0,0,(int)(8*DENSITY),0); offBtn.setLayoutParams(offLp); if(sp.getString("offline_q", "").isEmpty()) offBtn.setVisibility(View.GONE); offBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { ui.showSmartBanner(root, lang.get("Offline Data"), lang.get("Data will sync when internet is available."), "img_offline_warning", colorAccent, null); } }); rightHeader.addView(offBtn);\n        View periodBtn = ui.getRoundImage("img_period"'
if 'img_offline_warning' not in c: c = c.replace(o_icon, n_icon)

# Wipe Data Option
o_wipe = 'mr.addImg("Advanced Statistics", "img_stats", new Runnable() { @Override public void run() { try{statsHelper.syncDate(sdf.parse(selectedDate[0]));}catch(Exception e){} statsHelper.showStatsOptionsDialog(); }});'
n_wipe = 'mr.addImg("Advanced Statistics", "img_stats", new Runnable() { @Override public void run() { try{statsHelper.syncDate(sdf.parse(selectedDate[0]));}catch(Exception e){} statsHelper.showStatsOptionsDialog(); }});\n        mr.addImg("Wipe All Data", "img_offline_warning", new Runnable() { @Override public void run() { showWipeDataDialog(); }});'
if '"Wipe All Data"' not in c: c = c.replace(o_wipe, n_wipe)

wipe_func = """private void showWipeDataDialog() {
        FrameLayout wrap = new FrameLayout(this); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        LinearLayout main = new LinearLayout(this); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        View icon = ui.getRoundImage("img_offline_warning", 0, android.graphics.Color.TRANSPARENT, android.graphics.Color.parseColor("#FF5252")); 
        LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(50*DENSITY), (int)(50*DENSITY)); icLp.gravity = Gravity.CENTER_HORIZONTAL; icLp.setMargins(0, 0, 0, (int)(15*DENSITY)); icon.setLayoutParams(icLp); main.addView(icon);
        TextView title = new TextView(this); title.setText(lang.get("Wipe All Data")); title.setTextColor(android.graphics.Color.parseColor("#FF5252")); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); main.addView(title);
        TextView sub = new TextView(this); sub.setText(lang.get("Are you sure? This will delete all your local data permanently.")); sub.setTextColor(themeColors[3]); sub.setTextSize(14); sub.setGravity(Gravity.CENTER); sub.setPadding(0, (int)(10*DENSITY), 0, (int)(25*DENSITY)); main.addView(sub);
        LinearLayout row = new LinearLayout(this); row.setOrientation(LinearLayout.HORIZONTAL);
        Button btnC = new Button(this); btnC.setText(lang.get("CANCEL")); btnC.setTextColor(themeColors[2]); btnC.setAllCaps(false); btnC.setTypeface(Typeface.DEFAULT_BOLD);
        GradientDrawable bgC = new GradientDrawable(); bgC.setColor(themeColors[4]); bgC.setCornerRadius(15f*DENSITY); btnC.setBackground(bgC);
        LinearLayout.LayoutParams lpC = new LinearLayout.LayoutParams(0, (int)(50*DENSITY), 1f); lpC.setMargins(0,0,(int)(10*DENSITY),0); row.addView(btnC, lpC);
        Button btnD = new Button(this); btnD.setText(lang.get("Delete")); btnD.setTextColor(android.graphics.Color.WHITE); btnD.setAllCaps(false); btnD.setTypeface(Typeface.DEFAULT_BOLD);
        GradientDrawable bgD = new GradientDrawable(); bgD.setColor(android.graphics.Color.parseColor("#FF5252")); bgD.setCornerRadius(15f*DENSITY); btnD.setBackground(bgD);
        LinearLayout.LayoutParams lpD = new LinearLayout.LayoutParams(0, (int)(50*DENSITY), 1f); row.addView(btnD, lpD); main.addView(row);
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp);
        final AlertDialog ad = new AlertDialog.Builder(this).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(Gravity.CENTER);
        applyFont(main, appFonts[0], appFonts[1]); btnC.setOnClickListener(new View.OnClickListener(){@Override public void onClick(View v){ad.dismiss();}});
        btnD.setOnClickListener(new View.OnClickListener(){@Override public void onClick(View v){
            ad.dismiss(); ui.showSmartBanner(root, lang.get("Deleting..."), "", "img_offline_warning", android.graphics.Color.parseColor("#FF5252"), null);
            new Thread(new Runnable(){@Override public void run(){
                SalahDatabase.getDatabase(MainActivity.this).clearAllTables(); sp.edit().clear().apply();
                runOnUiThread(new Runnable(){@Override public void run(){ finish(); startActivity(getIntent()); }});
            }}).start();
        }}); ad.show();
    }\n}"""
if 'showWipeDataDialog()' not in c: c = c[:c.rfind('}')] + wipe_func
open(ma,'w').write(c)

print("✅ Category 1 Updates Applied Successfully! Now you can Build.")
