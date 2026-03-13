import os
import re

def main():
    target_main = None
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
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

        # ==========================================
        # ফিক্স ১: রিস্টার্ট বন্ধ করা (Instant UI Update)
        # ==========================================
        # ক. ফরজ বক্সে ক্লিক করলে আর পেজ রিস্টার্ট হবে না
        fard_old = r'sp\.edit\(\)\.putString\(dKey \+ "_" \+ AppConstants\.PRAYERS\[finalI\], newVal\)\.apply\(\);\s*v\.postDelayed\(new Runnable\(\)\s*\{\s*@Override\s*public void run\(\)\s*\{\s*loadTodayPage\(\);\s*refreshWidget\(\);\s*\}\s*\}, \d+\);'
        fard_new = """sp.edit().putString(dKey + "_" + AppConstants.PRAYERS[finalI], newVal).apply();
                                
                                // রিলোড ছাড়া সরাসরি স্ক্রিনে টিক চিহ্ন বসানো হচ্ছে
                                chk.removeAllViews();
                                if(newVal.equals("yes")) {
                                    chk.setShapeType(soup.neumorphism.ShapeType.PRESSED);
                                    chk.setShadowElevation(2f * DENSITY);
                                    TextView tick = new TextView(MainActivity.this);
                                    tick.setText("✓"); tick.setTextColor(colorAccent); tick.setTextSize(18); tick.setTypeface(null, android.graphics.Typeface.DEFAULT_BOLD); tick.setGravity(android.view.Gravity.CENTER); tick.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
                                    chk.addView(tick);
                                } else {
                                    chk.setShapeType(soup.neumorphism.ShapeType.FLAT);
                                    chk.setShadowElevation(3.5f * DENSITY);
                                }
                                
                                int nC = 0; for(String pr : AppConstants.PRAYERS) { String s = getFardStat(r, pr); if(s.equals("yes") || s.equals("excused")) nC++; }
                                pT.setText(lang.bnNum(nC*100/6) + "%");
                                subBtm.setText(statusMsgs[nC]);
                                refreshWidget();"""
        content = re.sub(fard_old, fard_new, content)

        # খ. সুন্নাহ বক্সে ক্লিক করলেও পেজ রিস্টার্ট হবে না
        sunnah_old = r'sp\.edit\(\)\.putBoolean\(dKey \+ "_" \+ sName, !isDone\)\.apply\(\);\s*v\.postDelayed\(new Runnable\(\)\s*\{\s*@Override\s*public void run\(\)\s*\{\s*loadTodayPage\(\);\s*refreshWidget\(\);\s*\}\s*\}, \d+\);'
        sunnah_new = """sp.edit().putBoolean(dKey + "_" + sName, !isDone).apply();
                                            
                                            // রিলোড ছাড়া সরাসরি সুন্নাহ আপডেট
                                            sBox.removeAllViews();
                                            if (!isDone) {
                                                android.graphics.drawable.GradientDrawable fill = new android.graphics.drawable.GradientDrawable(); fill.setColor(colorAccent); fill.setCornerRadius(10f * DENSITY); sBox.setBackground(fill);
                                                TextView tick = new TextView(MainActivity.this); tick.setText("✓"); tick.setTextColor(android.graphics.Color.WHITE); tick.setTextSize(10); tick.setTypeface(null, android.graphics.Typeface.DEFAULT_BOLD); tick.setGravity(android.view.Gravity.CENTER); tick.setLayoutParams(new LinearLayout.LayoutParams(-1, -1)); sBox.addView(tick);
                                            } else {
                                                android.graphics.drawable.GradientDrawable out = new android.graphics.drawable.GradientDrawable(); out.setStroke(2, isDarkTheme ? themeColors[3] : android.graphics.Color.parseColor("#CCCCCC")); out.setCornerRadius(10f * DENSITY); sBox.setBackground(out);
                                            }
                                            refreshWidget();"""
        content = re.sub(sunnah_old, sunnah_new, content)

        # ==========================================
        # ফিক্স ২: কার্ডের ভেতরের হিডেন জায়গা কমানো (এক পেজে ফিট)
        # ==========================================
        # কার্ডের ভেতরের সবচেয়ে বড় জায়গাটা কমানো হলো (15 থেকে কমিয়ে 2 করা হলো)
        content = re.sub(r'inner\.setPadding\(\(int\)\(15\*DENSITY\),\s*\(int\)\(15\*DENSITY\),\s*\(int\)\(15\*DENSITY\),\s*\(int\)\(15\*DENSITY\)\);', 
                         'inner.setPadding((int)(15*DENSITY), (int)(2*DENSITY), (int)(15*DENSITY), (int)(2*DENSITY));', content)
        
        # চেকবক্সের সাইজ হালকা কমানো হলো
        content = re.sub(r'chkParams = new LinearLayout\.LayoutParams\(\(int\)\(38\*DENSITY\),\s*\(int\)\(38\*DENSITY\)\);', 
                         'chkParams = new LinearLayout.LayoutParams((int)(30*DENSITY), (int)(30*DENSITY));', content)
        
        # সুন্নাহ লিস্টের ভেতরের গ্যাপ কমানো হলো
        content = re.sub(r'sList\.setPadding\(0,\s*\(int\)\(10\*DENSITY\),\s*0,\s*0\);', 
                         'sList.setPadding(0, (int)(2*DENSITY), 0, 0);', content)
        content = re.sub(r'sLp\.setMargins\(0,\s*0,\s*0,\s*\(int\)\(8\*DENSITY\)\);', 
                         'sLp.setMargins(0, 0, 0, (int)(4*DENSITY));', content)

        # কার্ড ও হেডারের বাইরের গ্যাপ কমানো
        content = re.sub(r'cardParams\.setMargins\([^)]+\);', 
                         'cardParams.setMargins((int)(15*DENSITY), (int)(2*DENSITY), (int)(15*DENSITY), (int)(2*DENSITY));', content)
        content = re.sub(r'headerParams\.setMargins\([^)]+\);', 
                         'headerParams.setMargins((int)(15*DENSITY), (int)(2*DENSITY), (int)(15*DENSITY), (int)(2*DENSITY));', content)

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ সব সমস্যার সমাধান! রিস্টার্ট/রিলোড বাগ ফিক্স করা হয়েছে এবং কার্ডগুলো এক পেজে ফিট করা হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
