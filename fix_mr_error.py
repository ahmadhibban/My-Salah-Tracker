import os, re

for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ১. ভুল জায়গায় বসা mr.render(); গুলো মুছে ফেলা
        c = c.replace('mr.render(); ', '')
        
        # ২. MenuRow ক্লাসকে স্মার্ট করা (যেন আলাদা করে mr.render() কল করতে না হয়)
        menu_class_self_sorting = r'''class MenuRow {
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
                
                // অটো-সর্টিং লজিক (render কল করার কোনো দরকার নেই)
                java.util.Collections.sort(items, new java.util.Comparator<MenuItem>() {
                    @Override public int compare(MenuItem m1, MenuItem m2) { return m1.title.compareTo(m2.title); }
                });
                mainLayout.removeAllViews();
                for(MenuItem m : items) { mainLayout.addView(m.view); }
            }
        }'''
        
        # আগের ভেজাল করা মেনু ক্লাসকে নতুন অটো-সর্টিং মেনু ক্লাস দিয়ে রিপ্লেস করা
        c = re.sub(r'class\s+MenuRow\s*\{.*?void\s+render\(\)\s*\{.*?\}\s*\}', menu_class_self_sorting, c, flags=re.DOTALL)
        
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ mr.render এরর ফিক্স এবং অটো-সর্টিং সম্পন্ন হয়েছে!")
