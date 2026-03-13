import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    
    # ১. ইংরেজি ক্যালেন্ডারের বর্ডার রিমুভ (ফাঁকা থাকলে)
    if 'CalendarHelper.java' in f:
        p = os.path.join(r, 'CalendarHelper.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        c = re.sub(
            r'else\s*\{\s*bgD\.setColor\(android\.graphics\.Color\.TRANSPARENT\);\s*tv\.setBackground\([^;]+;\s*\}',
            r'else { tv.setBackground(null); }',
            c, flags=re.DOTALL
        )
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

    # ২. সেটিংসের পপ-আপে A-Z সর্টিং সিস্টেম
    if 'MainActivity.java' in f:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        menu_class_new = r'''class MenuRow {
            class MenuItem { String title; android.widget.LinearLayout view; }
            java.util.List<MenuItem> items = new java.util.ArrayList<>();
            void addImg(String titleStr, String imgName, final Runnable action) {
                MenuItem item = new MenuItem(); 
                item.title = lang.get(titleStr);
                
                android.widget.LinearLayout btn = new android.widget.LinearLayout(MainActivity.this);
                btn.setOrientation(android.widget.LinearLayout.HORIZONTAL); btn.setGravity(android.view.Gravity.CENTER_VERTICAL); btn.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
                android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable(); bg.setColor(themeColors[4]); bg.setCornerRadius(15f*DENSITY); btn.setBackground(bg);
                android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams(-1, -2);
                lp.setMargins(0, 0, 0, (int)(10*DENSITY)); btn.setLayoutParams(lp);
                android.view.View icon = ui.getRoundImage(imgName, 0, android.graphics.Color.TRANSPARENT, colorAccent); 
                android.widget.LinearLayout.LayoutParams icLp = new android.widget.LinearLayout.LayoutParams((int)(28*DENSITY), (int)(28*DENSITY)); icLp.setMargins(0,0,(int)(15*DENSITY),0); icon.setLayoutParams(icLp);
                btn.addView(icon);
                android.widget.TextView t1 = new android.widget.TextView(MainActivity.this); t1.setText(item.title); t1.setTextColor(themeColors[2]); t1.setTextSize(16); t1.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btn.addView(t1);
                btn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { ad.dismiss(); action.run(); } }); 
                item.view = btn; items.add(item);
            }
            void render() {
                java.util.Collections.sort(items, new java.util.Comparator<MenuItem>() {
                    @Override public int compare(MenuItem m1, MenuItem m2) { return m1.title.compareTo(m2.title); }
                });
                for(MenuItem m : items) { mainLayout.addView(m.view); }
            }
        }'''
        c = re.sub(r'class\s+MenuRow\s*\{.*?mainLayout\.addView\(btn\);\s*\}\s*\}', menu_class_new, c, flags=re.DOTALL)
        
        # অপশনগুলো রেন্ডার করার কমান্ড যুক্ত করা
        if 'mr.render();' not in c:
            c = re.sub(r'(FrameLayout\.LayoutParams\s+flp\s*=\s*new\s+FrameLayout\.LayoutParams)', r'mr.render(); \1', c)
        
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ ধাপ ২: ক্যালেন্ডার বর্ডার রিমুভ এবং সেটিংস A-Z সর্টিং সম্পন্ন হয়েছে!")
