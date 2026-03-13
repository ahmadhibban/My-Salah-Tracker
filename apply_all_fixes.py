import os
import re

def main():
    target_main = None
    target_stats = None
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    for root_path in search_paths:
        if not os.path.exists(root_path): continue
        for root, dirs, files in os.walk(root_path):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: target_main = os.path.join(root, 'MainActivity.java')
            if 'StatsHelper.java' in files: target_stats = os.path.join(root, 'StatsHelper.java')
        if target_main and target_stats: break

    # ==========================================
    # 1. MainActivity.java - UI & Dynamic Updates
    # ==========================================
    if target_main:
        with open(target_main, 'r', encoding='utf-8') as f:
            content = f.read()

        # --- A. মাগরিব আইকনের সাইজ ফিক্স (Padding 0 থেকে 8 করা) ---
        content = content.replace('int[] pPaddings = {8, 8, 8, 0, 8, 8};', 'int[] pPaddings = {8, 8, 8, 8, 8, 8};')

        # --- B. কাজা লিস্টের এম্পটি আইকন কালারফুল করা ---
        content = content.replace('ui.getRoundImage("img_empty_qaza", 0, android.graphics.Color.TRANSPARENT, 0)', 'ui.getRoundImage("img_empty_qaza", 0, android.graphics.Color.TRANSPARENT, colorAccent)')

        # --- C. হোয়াইট মোডে সুন্নত বক্স থিম কালারে ফিল করা ---
        content = content.replace('if (type == 1 && !isDark) {', 'if (type == 1 && !isDark && bgColor != colorAccent) {')

        # --- D. সেটিংস মেনু A-Z সর্টিং ---
        m_theme = re.search(r'mr\.addImg\("Choose Theme".*?\}\);', content, re.DOTALL)
        m_lang = re.search(r'mr\.addImg\("Change Language".*?\}\);', content, re.DOTALL)
        m_sync = re.search(r'mr\.addImg\("Backup & Sync".*?\}\);', content, re.DOTALL)
        m_qaza = re.search(r'mr\.addImg\("View Qaza List".*?\}\);', content, re.DOTALL)
        m_stats = re.search(r'mr\.addImg\("Advanced Statistics".*?\}\);', content, re.DOTALL)
        m_hijri = re.search(r'mr\.addImg\(sp\.getString\("app_lang", "en"\)\.equals\("bn"\) \? "হিজরি তারিখ সেটিং" : "Adjust Hijri Date".*?\}\);', content, re.DOTALL)
        
        if m_theme and m_hijri:
            full_menu = f"{m_theme.group(0)}\n        {m_lang.group(0)}\n        {m_sync.group(0)}\n        {m_qaza.group(0)}\n        {m_stats.group(0)}\n        {m_hijri.group(0)}"
            sorted_menu = f"{m_hijri.group(0)}\n        {m_stats.group(0)}\n        {m_sync.group(0)}\n        {m_lang.group(0)}\n        {m_theme.group(0)}\n        {m_qaza.group(0)}"
            content = content.replace(full_menu, sorted_menu)

        # --- E. লাইভ ডাইনামিক আপডেট (No Reload) ---
        if 'setTag("PERCENT_TEXT")' not in content:
            content = content.replace('pT.setText(lang.bnNum(countCompleted*100/6) + "%");', 'pT.setText(lang.bnNum(countCompleted*100/6) + "%"); pT.setTag("PERCENT_TEXT");')
            content = content.replace('subBtm.setText(statusMsgs[countCompleted]);', 'subBtm.setText(statusMsgs[countCompleted]); subBtm.setTag("SUB_TEXT");')

        dynamic_code = """v.postDelayed(new Runnable() { @Override public void run() { 
                        soup.neumorphism.NeumorphCardView chkCard = (soup.neumorphism.NeumorphCardView) chk;
                        chkCard.setShapeType(newVal.equals("yes") ? 0 : 1);
                        chkCard.setShadowElevation((newVal.equals("yes") ? 2f : 5.5f) * DENSITY);
                        chkCard.removeAllViews();
                        if (newVal.equals("yes")) {
                            TextView inner = new TextView(MainActivity.this);
                            inner.setText("✓");
                            inner.setTextColor(colorAccent);
                            inner.setTextSize(18);
                            inner.setTypeface(null, Typeface.BOLD);
                            inner.setGravity(Gravity.CENTER);
                            inner.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
                            chkCard.addView(inner);
                        }
                        
                        TextView pText = getWindow().getDecorView().findViewWithTag("PERCENT_TEXT");
                        TextView sText = getWindow().getDecorView().findViewWithTag("SUB_TEXT");
                        if (pText != null) {
                            int nC = 0;
                            SalahRecord nR = getRoomRecord(selectedDate[0]);
                            for(String pr : AppConstants.PRAYERS) {
                                String s = getFardStat(nR, pr);
                                if(s.equals("yes") || s.equals("excused")) nC++;
                            }
                            pText.setText(lang.bnNum(nC*100/6) + "%");
                            if(sText != null) sText.setText(statusMsgs[nC]);
                        }
                        refreshWidget(); 
                    }}, 20);"""
        
        # Replacing both possibilities (if old optimization ran or not)
        content = content.replace('v.postDelayed(new Runnable() { @Override public void run() { loadTodayPage(); refreshWidget(); }}, 20);', dynamic_code)
        content = content.replace('v.postDelayed(new Runnable() { @Override public void run() { loadTodayPage(); refreshWidget(); }}, 150);', dynamic_code)

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ MainActivity: UI Fixes & Dynamic State Appled.")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

    # ==========================================
    # 2. StatsHelper.java - Chart Center Alignment
    # ==========================================
    if target_stats:
        with open(target_stats, 'r', encoding='utf-8') as f:
            content = f.read()

        old_chart_code = """float fVal = d+e; fE.add(new com.github.mikephil.charting.data.BarEntry(i-0.2f, fVal));
sE.add(new com.github.mikephil.charting.data.BarEntry(i+0.2f, Math.min(6f, s*(6f/10f))));"""
        
        new_chart_code = """float fVal = d+e;
float sunnahVal = Math.min(6f, s*(6f/10f));
fE.add(new com.github.mikephil.charting.data.BarEntry(sunnahVal == 0 ? i : i - 0.2f, fVal));
sE.add(new com.github.mikephil.charting.data.BarEntry(fVal == 0 ? i : i + 0.2f, sunnahVal));"""
        
        content = content.replace(old_chart_code, new_chart_code)
        
        with open(target_stats, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ StatsHelper: Chart Bar Centered.")
    else:
        print("❌ StatsHelper.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
