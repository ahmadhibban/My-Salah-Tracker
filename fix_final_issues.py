import os
import re

def main():
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    # 1. Fix MainActivity (Menu Sorting & Card Shrinking)
    main_path = None
    for r in search_paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: main_path = os.path.join(root, 'MainActivity.java'); break
        if main_path: break

    if main_path:
        with open(main_path, 'r', encoding='utf-8') as f:
            c = f.read()
        
        # --- A. Menu A-Z Sorting ---
        targets = ["Choose Theme", "Change Language", "Backup & Sync", "View Qaza List", "Advanced Statistics", "Adjust Hijri Date"]
        lines = c.split('\n')
        menu_lines = {}
        for i, line in enumerate(lines):
            for t in targets:
                # addImg বা add যেকোনো মেথডেই কাজ করবে
                if t in line and "add" in line:
                    menu_lines[t] = line
                    lines[i] = "---TO_DELETE---"
        
        if len(menu_lines) == 6:
            # A-Z অনুযায়ী সিরিয়াল
            sorted_keys = ["Adjust Hijri Date", "Advanced Statistics", "Backup & Sync", "Change Language", "Choose Theme", "View Qaza List"]
            sorted_block = "\n".join([menu_lines[k] for k in sorted_keys])
            
            inserted = False
            final_lines = []
            for line in lines:
                if line == "---TO_DELETE---":
                    if not inserted:
                        final_lines.append(sorted_block)
                        inserted = True
                else:
                    final_lines.append(line)
            c = "\n".join(final_lines)
            print("✅ সেটিংস মেনু A-Z সর্টিং করা হয়েছে।")
        else:
            print("⚠️ সেটিংস মেনুর সবগুলো অপশন স্বয়ংক্রিয়ভাবে সাজানো যায়নি (হয়তো আগেই সাজানো আছে)।")

        # --- B. Shrink Percentage Card (এক পেজে ফিট করার জন্য) ---
        # pCard এর প্যাডিং এবং মার্জিন একদম মিনিমাম করে দেওয়া হলো
        c = re.sub(r'pCard\.setPadding\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\);', 'pCard.setPadding(30, 8, 30, 8);', c)
        c = re.sub(r'headerParams\.setMargins\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\);', 'headerParams.setMargins(30, 8, 30, 8);', c)
        
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(c)
            print("✅ পার্সেন্টেজ কার্ডের সাইজ ছোট করে এক পেজে ফিট করা হয়েছে।")

    # 2. Shrink PremiumTasbihView (পার্সেন্টেজ কার্ডের ভেতরের স্পেস কমানো)
    tasbih_path = None
    for r in search_paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            if 'PremiumTasbihView.java' in files: tasbih_path = os.path.join(root, 'PremiumTasbihView.java'); break
        if tasbih_path: break
        
    if tasbih_path:
        with open(tasbih_path, 'r', encoding='utf-8') as f:
            tc = f.read()
        # ওপর-নিচের স্পেস 20 থেকে কমিয়ে 2 করে দেওয়া হলো
        tc = re.sub(r'setPadding\(\s*60\s*,\s*\d+\s*,\s*20\s*,\s*\d+\s*\);', 'setPadding(60, 2, 20, 2);', tc)
        with open(tasbih_path, 'w', encoding='utf-8') as f:
            f.write(tc)

    # 3. Chart Center Alignment (StatsHelper.java বা MainActivity.java)
    for r in search_paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            for file_name in files:
                if file_name.endswith('.java'):
                    f_path = os.path.join(root, file_name)
                    try:
                        with open(f_path, 'r', encoding='utf-8') as f:
                            chart_c = f.read()
                        
                        # ডাইনামিক রেজেক্স যা ফরজ এবং সুন্নতের ভ্যালু ক্যাপচার করে
                        pattern = r'fE\.add\(\s*new\s+(?:[a-zA-Z0-9_.]+\.)?BarEntry\(\s*(?:i\s*-\s*0\.2f|i)\s*,\s*([^)]+)\)\s*\);\s*sE\.add\(\s*new\s+(?:[a-zA-Z0-9_.]+\.)?BarEntry\(\s*(?:i\s*\+\s*0\.2f|i)\s*,\s*([^)]+)\)\s*\);'
                        
                        def chart_repl(m):
                            f_y = m.group(1) # ফরজের ভ্যালু
                            s_y = m.group(2) # সুন্নতের ভ্যালু
                            # লজিক: সুন্নত 0 হলে ফরজ সেন্টারে (i), নইলে বামে (i - 0.2f)
                            return f"fE.add(new com.github.mikephil.charting.data.BarEntry(({s_y}) == 0 ? i : i - 0.2f, {f_y}));\n                        sE.add(new com.github.mikephil.charting.data.BarEntry(({f_y}) == 0 ? i : i + 0.2f, {s_y}));"
                        
                        new_chart_c = re.sub(pattern, chart_repl, chart_c)
                        
                        if new_chart_c != chart_c:
                            with open(f_path, 'w', encoding='utf-8') as f:
                                f.write(new_chart_c)
                            print(f"✅ চার্ট সেন্টার অ্যালাইনমেন্ট একদম পারফেক্ট করা হয়েছে ({file_name})।")
                    except Exception as e:
                        pass

if __name__ == '__main__': main()
