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

    # ==========================================
    # 1. MainActivity.java - Click Bug & Layout Fit
    # ==========================================
    if target_main:
        with open(target_main, 'r', encoding='utf-8') as f:
            content = f.read()

        # --- ফিক্স ১: ক্লিক ফ্রিজ বাগ (টিক চিহ্ন না ওঠার সমাধান) ---
        # আমার আগের করা ভুল ডাইনামিক কোডটুকু মুছে ফেলে অরিজিনাল loadTodayPage() বসানো হচ্ছে
        # কিন্তু স্পিড 20ms থাকবে, তাই অ্যাপ স্ন্যাপিও লাগবে আবার ফ্রিজও হবে না!
        bad_code_pattern = r'soup\.neumorphism\.NeumorphCardView chkCard = \(soup\.neumorphism\.NeumorphCardView\) chk;.*?refreshWidget\(\);\s*\}\},\s*20\);'
        good_code = 'loadTodayPage(); refreshWidget(); }}, 20);'
        content = re.sub(bad_code_pattern, good_code, content, flags=re.DOTALL)

        # --- ফিক্স ২: এক পেইজে ফিট (খুবই এগ্রেসিভভাবে ওপর-নিচের স্পেস কমানো) ---
        # পার্সেন্টেজ কার্ডের স্পেস কমানো হলো
        content = re.sub(r'headerParams\.setMargins\([^)]+\);', 'headerParams.setMargins(45, 5, 45, 5);', content)
        content = re.sub(r'pCard\.setPadding\([^)]+\);', 'pCard.setPadding(30, 8, 30, 8);', content)
        
        # নামাজের কার্ডের স্পেস কমানো হলো
        content = re.sub(r'cardParams\.setMargins\([^)]+\);', 'cardParams.setMargins(45, 8, 45, 8);', content)
        content = re.sub(r'card\.setPadding\([^)]+\);', 'card.setPadding(35, 15, 35, 15);', content)

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ ক্লিক বাগ (টিক চিহ্ন) সমাধান হয়েছে এবং কার্ডগুলো এক পেইজে ফিট করা হয়েছে!")

    # ==========================================
    # 2. StatsHelper.java - Chart Center Alignment
    # ==========================================
    if target_stats:
        with open(target_stats, 'r', encoding='utf-8') as f:
            s_content = f.read()

        # --- ফিক্স ৩: চার্ট সেন্টার করা (যাতে সুন্নত না থাকলে ফরজ মাঝখানে থাকে) ---
        
        # 3A. Main App Chart
        s_content = re.sub(r'fE\.add\(new com\.github\.mikephil\.charting\.data\.BarEntry\([^,]+,\s*([^)]+)\)\);',
                           r'fE.add(new com.github.mikephil.charting.data.BarEntry((Math.min(6f, s*(6f/10f)) == 0) ? i : i - 0.2f, \1));', s_content)
        
        s_content = re.sub(r'sE\.add\(new com\.github\.mikephil\.charting\.data\.BarEntry\([^,]+,\s*([^)]+)\)\);',
                           r'sE.add(new com.github.mikephil.charting.data.BarEntry(((d+e) == 0) ? i : i + 0.2f, \1));', s_content)

        # 3B. Image Generation Chart
        s_content = re.sub(r'float fX\s*=\s*gX\s*-\s*\(bW\s*/\s*2f\).*?;', 
                           'float fX = (sV == 0) ? gX : (gX - bW - spc/2f);', s_content)
        s_content = re.sub(r'float sX\s*=\s*gX\s*\+\s*\(bW\s*/\s*2f\).*?;', 
                           'float sX = (fV == 0) ? gX : (gX + spc/2f);', s_content)

        # 3C. PDF Generation Chart
        s_content = re.sub(r'float fX\s*=\s*cx\s*-\s*\(bW\s*/\s*2f\).*?;', 
                           'float fX = (sV == 0) ? cx : (cx - bW - spc/2f);', s_content)
        s_content = re.sub(r'float sX\s*=\s*cx\s*\+\s*\(bW\s*/\s*2f\).*?;', 
                           'float sX = (fV == 0) ? cx : (cx + spc/2f);', s_content)

        with open(target_stats, 'w', encoding='utf-8') as f:
            f.write(s_content)
        print("✅ চার্টের দাগগুলো (অক্ষরের মাঝ বরাবর) সেন্টার অ্যালাইন করা হয়েছে!")

if __name__ == '__main__': main()
