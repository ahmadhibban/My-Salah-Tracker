import os

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'

if not os.path.exists(f):
    print("❌ Error: MainActivity.java পাওয়া যায়নি!")
    exit()

with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# ১. ভেরিয়েবল যুক্ত করা
if 'private LinearLayout bottomNav;' not in c:
    c = c.replace('private SimpleDateFormat sdf;', 'private SimpleDateFormat sdf;\n    private LinearLayout bottomNav;')

# ২. Setup Method এবং Placeholder যুক্ত করা (onCreate এর ঠিক উপরে)
nav_code = r'''
    private void setupBottomNav(android.widget.LinearLayout mainLayout) {
        bottomNav = new android.widget.LinearLayout(this);
        bottomNav.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        bottomNav.setBackgroundColor(themeColors[1]);
        if (android.os.Build.VERSION.SDK_INT >= 21) bottomNav.setElevation(40f);
        
        android.widget.LinearLayout.LayoutParams navLp = new android.widget.LinearLayout.LayoutParams(-1, (int)(65*DENSITY));
        bottomNav.setLayoutParams(navLp);

        String[] titles = {lang.get("Salah"), lang.get("Fasting"), "Quran", "Zikr", lang.get("Stats")};
        String[] icons = {"img_salah", "img_moon", "img_quran", "img_zikr", "img_stats"}; 
        
        for(int i=0; i<5; i++) {
            final int index = i;
            android.widget.LinearLayout tab = new android.widget.LinearLayout(this);
            tab.setOrientation(android.widget.LinearLayout.VERTICAL);
            tab.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -1, 1f));
            tab.setGravity(android.view.Gravity.CENTER);
            
            android.widget.ImageView ic = new android.widget.ImageView(this);
            int res = getResources().getIdentifier(icons[i], "drawable", getPackageName());
            if(res != 0) ic.setImageResource(res);
            ic.setLayoutParams(new android.widget.LinearLayout.LayoutParams((int)(24*DENSITY), (int)(24*DENSITY)));
            ic.setColorFilter(index == 0 ? colorAccent : themeColors[3]);
            
            android.widget.TextView tv = new android.widget.TextView(this);
            tv.setText(titles[i]); tv.setTextSize(11); tv.setTypeface(appFonts[1]);
            tv.setTextColor(index == 0 ? colorAccent : themeColors[3]);
            tv.setGravity(android.view.Gravity.CENTER); tv.setPadding(0, (int)(4*DENSITY), 0, 0);
            
            tab.addView(ic); tab.addView(tv);
            tab.setOnClickListener(v -> {
                for(int j=0; j<5; j++) {
                    android.widget.LinearLayout t = (android.widget.LinearLayout) bottomNav.getChildAt(j);
                    ((android.widget.ImageView)t.getChildAt(0)).setColorFilter(themeColors[3]);
                    ((android.widget.TextView)t.getChildAt(1)).setTextColor(themeColors[3]);
                }
                ic.setColorFilter(colorAccent); tv.setTextColor(colorAccent);
                
                if(index == 0) loadTodayPage();
                else showPlaceholder(titles[index]);
            });
            bottomNav.addView(tab);
        }
        mainLayout.addView(bottomNav);
    }

    private void showPlaceholder(String tabName) {
        contentArea.removeAllViews();
        contentArea.setPadding((int)(20*DENSITY), (int)(50*DENSITY), (int)(20*DENSITY), (int)(100*DENSITY)); 
        android.widget.TextView tv = new android.widget.TextView(this); 
        tv.setText("🚧 " + tabName + " Tab\n\nComing Soon!"); 
        tv.setTextColor(themeColors[3]); tv.setTextSize(18); tv.setTypeface(appFonts[1]); tv.setGravity(android.view.Gravity.CENTER);
        contentArea.addView(tv);
    }

    @Override
'''
if 'setupBottomNav' not in c:
    c = c.replace('    @Override\n    protected void onCreate(Bundle savedInstanceState) {', nav_code + '    protected void onCreate(Bundle savedInstanceState) {')

# ৩. UI-তে নেভিগেশন বার কল করা
if 'setupBottomNav(mainLayout);' not in c:
    c = c.replace('mainLayout.addView(scrollView);\n        root.addView(mainLayout);', 'mainLayout.addView(scrollView);\n        setupBottomNav(mainLayout);\n        root.addView(mainLayout);')

# ৪. সালাহ পেজে প্যাডিং দেওয়া
if 'cardsContainer.animate().alpha(1f).setDuration(400).start();' in c and 'cardsContainer.setPadding' not in c:
    c = c.replace('cardsContainer.animate().alpha(1f).setDuration(400).start(); contentArea.addView(cardsContainer);', 'cardsContainer.setPadding((int)(20*DENSITY), 0, (int)(20*DENSITY), (int)(100*DENSITY));\n        cardsContainer.animate().alpha(1f).setDuration(400).start(); contentArea.addView(cardsContainer);')

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Navigation Bar successfully added!")
