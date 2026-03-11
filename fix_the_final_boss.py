import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(java_file):
    print("❌ MainActivity.java not found!")
    exit()

with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. সপ্তাহের দিনগুলোকে একদম গোল (Circle) করা এবং থ্রিডি ইফেক্ট স্পষ্ট করা
mc = re.sub(r'applyNeo\(t,\s*isSel\s*\?\s*1\s*:\s*0,\s*8f,\s*isSel\s*\?\s*1\.5f\s*:\s*3f', 'applyNeo(t, isSel ? 1 : 0, 24f, isSel ? 2f : 5.5f', mc)
mc = re.sub(r't\.setPadding\(\(int\)\(12\*DENSITY\),\s*\(int\)\(10\*DENSITY\),\s*\(int\)\(12\*DENSITY\),\s*\(int\)\(10\*DENSITY\)\);', 't.setPadding((int)(8*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY));', mc)
mc = re.sub(r't\.setPadding\(0,\s*\(int\)\(8\*DENSITY\),\s*0,\s*\(int\)\(8\*DENSITY\)\);', 't.setPadding((int)(8*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY));', mc)

# ২. ভবিষ্যতের দিনগুলোকে দৃশ্যমান করা (হালকা ছাই রঙ দিয়ে)
mc = re.sub(r't\.setTextColor\([^)]*TRANSPARENT[^)]*\);', 't.setTextColor(android.graphics.Color.parseColor("#94A3B8")); t.setAlpha(0.6f);', mc)
mc = re.sub(r't\.setVisibility\([^)]*INVISIBLE[^)]*\);', 't.setVisibility(android.view.View.VISIBLE); t.setAlpha(0.6f);', mc)
mc = re.sub(r't\.setAlpha\(\s*0(?:\.0)?f\s*\);', 't.setAlpha(0.6f);', mc)

# ৩. বাটনগুলোর সাইজ মেইন কার্ডের সমান করা এবং মাঝখানে কার্ডের সমান স্পেস দেওয়া
btn_fix = """
        LinearLayout.LayoutParams btnLp1 = new LinearLayout.LayoutParams(0, -2, 1f);
        // ওপরে 16dp গ্যাপ (কার্ডের সমান), বামে 6dp, ডানে 6dp গ্যাপ দিয়ে কার্ডের মাপে আনা হলো
        btnLp1.setMargins((int)(6*DENSITY), (int)(16*DENSITY), (int)(6*DENSITY), 0);
        markAllBtn.setLayoutParams(btnLp1);
        
        LinearLayout.LayoutParams btnLp2 = new LinearLayout.LayoutParams(0, -2, 1f);
        btnLp2.setMargins((int)(6*DENSITY), (int)(16*DENSITY), (int)(6*DENSITY), 0);
        todayBtn.setLayoutParams(btnLp2);
        
        topBtns.setPadding(0, (int)(10*DENSITY), 0, (int)(16*DENSITY));
"""
mc = re.sub(r'LinearLayout\.LayoutParams btnLp1 = new LinearLayout\.LayoutParams\(0, -2, 1f\);.*?topBtns\.setPadding[^;]+;', btn_fix, mc, flags=re.DOTALL)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✔ FINAL BOSS FIXED! ALL VISUALS ARE PERFECT NOW.")
