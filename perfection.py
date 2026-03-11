import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(java_file):
    print("❌ MainActivity.java not found!")
    exit()

with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. একপাশে বেশি সাদা কমানো (শ্যাডো ব্যালেন্স করে পারফেক্ট সফট করা হলো)
mc = mc.replace('android.graphics.Color.WHITE', 'android.graphics.Color.parseColor("#F1F5F9")')

# ২. সপ্তাহের ঘরগুলোর দুই পাশের তীর চিহ্নে থ্রিডি ইফেক্ট (সাধারণত এগুলো leftBtn, rightBtn নামে থাকে)
arrows = ["leftBtn", "rightBtn", "prevBtn", "nextBtn", "btnLeft", "btnRight", "leftArrow", "rightArrow"]
for arr in arrows:
    mc = re.sub(rf'{arr}\.setBackground\(.*?\);', rf'applyNeo({arr}, 0, 15f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); {arr}.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY));', mc)

# ৩. চেকবক্সের "উঁচা" (Flat) স্টাইলটাকে আরও সুন্দর ও প্রিমিয়াম করা হলো
mc = mc.replace('nd.setShadowElevation((isChk ? 2f : 5f) * DENSITY);', 'nd.setShadowElevation((isChk ? 2f : 6f) * DENSITY);')
mc = mc.replace('nd.setShadowElevation(3f * DENSITY);', 'nd.setShadowElevation((isChk ? 2f : 5.5f) * DENSITY);')
mc = mc.replace('nd.setPadding((int)(12*DENSITY), (int)(12*DENSITY), (int)(12*DENSITY), (int)(12*DENSITY));', 'nd.setPadding((int)(14*DENSITY), (int)(14*DENSITY), (int)(14*DENSITY), (int)(14*DENSITY));')

# ৪. নামাজের আইকনগুলোতে সুন্দর সফট থ্রিডি ইফেক্ট যুক্ত করা
if 'applyNeo(iconView' not in mc:
    mc = mc.replace('innerCard.addView(iconView);', 'applyNeo(iconView, 0, 12f, 2.5f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); iconView.setPadding((int)(10*DENSITY),(int)(10*DENSITY),(int)(10*DENSITY),(int)(10*DENSITY)); innerCard.addView(iconView);')

# ৫. পার্সেন্টেজের ঘর অ্যাপের বর্তমান কালার (colorAccent) দিয়ে ফিল করা এবং ইফেক্ট আরও ফোটানো
mc = re.sub(r'int tSur = [^;]+;', 'int tSur = colorAccent;', mc)
mc = re.sub(r'int tShd = [^;]+;', 'int tShd = isDarkTheme ? android.graphics.Color.rgb((int)(android.graphics.Color.red(colorAccent)*0.4f), (int)(android.graphics.Color.green(colorAccent)*0.4f), (int)(android.graphics.Color.blue(colorAccent)*0.4f)) : android.graphics.Color.rgb((int)(android.graphics.Color.red(colorAccent)*0.75f), (int)(android.graphics.Color.green(colorAccent)*0.75f), (int)(android.graphics.Color.blue(colorAccent)*0.75f));', mc)
mc = mc.replace('applyNeo(pCard, 0, 20f, 6f', 'applyNeo(pCard, 0, 20f, 12f') # ইফেক্ট আরও ফুটিয়ে তোলা হলো

# ৬. ভবিষ্যতের দিনগুলো গায়েব না করে হালকা (Faded) করে দেখানো
mc = re.sub(r't\.setTextColor\([^)]*Color\.TRANSPARENT[^)]*\);', 't.setAlpha(0.35f);', mc)
mc = mc.replace('t.setVisibility(View.INVISIBLE);', 't.setVisibility(View.VISIBLE); t.setAlpha(0.35f);')
mc = mc.replace('t.setAlpha(0f);', 't.setAlpha(0.35f);')
mc = mc.replace('t.setAlpha(0.0f);', 't.setAlpha(0.35f);')

# সপ্তাহের ঘরগুলোর প্যাডিং চারদিকে সমান করে ব্যালেন্স করা হলো
mc = mc.replace('t.setPadding(0, (int)(8*DENSITY), 0, (int)(8*DENSITY));', 't.setPadding((int)(12*DENSITY), (int)(10*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY));')

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✔ ALL 6 PERFECTIONS APPLIED SUCCESSFULLY!")
