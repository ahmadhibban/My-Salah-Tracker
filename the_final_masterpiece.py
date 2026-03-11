import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(java_file):
    print("❌ MainActivity.java not found!")
    exit()

with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. সপ্তাহের ঘরগুলো সবসময় ডেবে (Pressed = Type 1) থাকবে এবং সুন্দর গোল হবে
mc = re.sub(r'applyNeo\(t,\s*[^,]+,\s*[^,]+,\s*[^,]+,\s*isSel\s*\?\s*colorAccent[^)]+\);', 'applyNeo(t, 1, 24f, 3f, isSel ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0")), isDarkTheme);', mc)

# ২. ভবিষ্যতের দিনগুলোকে একদম ১০০% স্পষ্ট করে দেওয়া (কোনো আলফা বা স্বচ্ছতা থাকবে না)
mc = re.sub(r't\.setAlpha\([^)]+\);', '', mc)  # সব Alpha রিমুভ
mc = re.sub(r't\.setTextColor\([^)]*TRANSPARENT[^)]*\);', 't.setTextColor(themeColors[2]);', mc)
mc = re.sub(r't\.setTextColor\([^)]*#94A3B8[^)]*\);', 't.setTextColor(themeColors[2]);', mc)
mc = re.sub(r't\.setVisibility\([^)]*INVISIBLE[^)]*\);', 't.setVisibility(android.view.View.VISIBLE);', mc)

# ৩. মার্ক অল এবং টুডে বাটনকে একদম মেইন কার্ডের সমান করা এবং ওপরে-নিচে পারফেক্ট গ্যাপ দেওয়া
btn_fix = """
        LinearLayout.LayoutParams btnLp1 = new LinearLayout.LayoutParams(0, -2, 1f);
        // ওপরে 24dp (বিশাল গ্যাপ), বামে 16dp (কার্ডের সমান করতে), ডানে 8dp, নিচে 16dp গ্যাপ
        btnLp1.setMargins((int)(16*DENSITY), (int)(24*DENSITY), (int)(8*DENSITY), (int)(16*DENSITY));
        markAllBtn.setLayoutParams(btnLp1);
        
        LinearLayout.LayoutParams btnLp2 = new LinearLayout.LayoutParams(0, -2, 1f);
        // ওপরে 24dp, বামে 8dp, ডানে 16dp (কার্ডের সমান করতে), নিচে 16dp গ্যাপ
        btnLp2.setMargins((int)(8*DENSITY), (int)(24*DENSITY), (int)(16*DENSITY), (int)(16*DENSITY));
        todayBtn.setLayoutParams(btnLp2);
"""
mc = re.sub(r'LinearLayout\.LayoutParams btnLp1 = new LinearLayout\.LayoutParams\(0, -2, 1f\);.*?todayBtn\.setLayoutParams\(btnLp2\);', btn_fix.strip(), mc, flags=re.DOTALL)

# এক্সট্রা প্যাডিং থাকলে মুছে ফেলা (যাতে মার্জিন পারফেক্টলি কাজ করে)
mc = re.sub(r'topBtns\.setPadding[^;]+;', 'topBtns.setPadding(0, 0, 0, 0);', mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✔ ALL ADJUSTMENTS DONE! SPACING AND SIZING ARE NOW PERFECT.")
