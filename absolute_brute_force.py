import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(java_file):
    print("❌ MainActivity.java not found!")
    exit()

with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. সপ্তাহের সব ঘরকে জোর করে ডাবিয়ে (Type 1) দেওয়া
mc = re.sub(r'applyNeo\(t,\s*[^,]+,\s*[^,]+,\s*[^,]+,', 'applyNeo(t, 1, 24f, 3f,', mc)

# ২. ভবিষ্যতের দিনগুলোর সব হাইড/স্বচ্ছতা (Alpha) মুছে ফেলা
mc = re.sub(r't\.setAlpha\([^)]+\);', '', mc)
mc = mc.replace("t.setTextColor(android.graphics.Color.TRANSPARENT);", "t.setTextColor(themeColors[2]);")
mc = mc.replace("t.setTextColor(Color.TRANSPARENT);", "t.setTextColor(themeColors[2]);")
mc = re.sub(r't\.setVisibility\([^)]+\);', 't.setVisibility(android.view.View.VISIBLE);', mc)

# ৩. মার্ক অল এবং টুডে বাটনের সাইজ এবং গ্যাপ জোর করে বসানো
btn_replacement = """
        // পুরনো লেআউট প্যারামিটার মুছে নতুন করে বসানো হচ্ছে
        LinearLayout.LayoutParams btnLp1 = new LinearLayout.LayoutParams(0, -2, 1f);
        btnLp1.setMargins((int)(16*DENSITY), (int)(28*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY)); // ওপরে ২৮ ডিপি গ্যাপ!
        markAllBtn.setLayoutParams(btnLp1);

        LinearLayout.LayoutParams btnLp2 = new LinearLayout.LayoutParams(0, -2, 1f);
        btnLp2.setMargins((int)(8*DENSITY), (int)(28*DENSITY), (int)(16*DENSITY), (int)(12*DENSITY)); // ওপরে ২৮ ডিপি গ্যাপ!
        todayBtn.setLayoutParams(btnLp2);
"""

# যদি আগে থেকে লেআউট প্যারামিটার থাকে সেটাকে মুছে দেওয়া
mc = re.sub(r'LinearLayout\.LayoutParams btnLp1 = new LinearLayout\.LayoutParams\(0, -2, 1f\);.*?todayBtn\.setLayoutParams\(btnLp2\);', '', mc, flags=re.DOTALL)

# topBtns.addView(todayBtn); এর ঠিক নিচে জোর করে নতুন লেআউট প্যারামিটার ঢুকিয়ে দেওয়া
target_code = "topBtns.addView(todayBtn);"
if target_code in mc and "btnLp1.setMargins((int)(16*DENSITY)" not in mc:
    mc = mc.replace(target_code, target_code + "\n" + btn_replacement)

# এক্সট্রা প্যাডিং মুছে ফেলা
mc = re.sub(r'topBtns\.setPadding\([^)]+\);', 'topBtns.setPadding(0, 0, 0, 0);', mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✔ BRUTE FORCE APPLIED! NO EXCUSES THIS TIME.")
