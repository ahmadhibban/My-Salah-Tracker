import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# ১. ডাবল পেজ ভাইরাস ধ্বংস করা (পেজ লোডের আগে স্ক্রিন ক্লিন করা)
c = c.replace('private void loadRozaTab() {', 'private void loadRozaTab() { contentArea.removeAllViews();')
c = c.replace('private void loadQuranTab() {', 'private void loadQuranTab() { contentArea.removeAllViews();')
c = c.replace('private void loadZikrTab() {', 'private void loadZikrTab() { contentArea.removeAllViews();')
c = c.replace('private void loadStatsTab() {', 'private void loadStatsTab() { contentArea.removeAllViews();')

# ২. অদৃশ্য আরবি লেখাকে দৃশ্যমান করা (বক্সের উচ্চতা ঠিক করা)
c = c.replace('svDua.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,(int)(130*DENSITY),1f));', 'svDua.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, -2));')
c = c.replace('duaWrap.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,-1,1f));', 'duaWrap.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));')
c = c.replace('tvDua.setTextSize(30);', 'tvDua.setTextSize(35); tvDua.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY));')

# ৩. মেইন পেজ থেকে জোর করে "অতিরিক্ত নফল" বাটন মুছে ফেলা
c = re.sub(r'android\.widget\.LinearLayout\s+addBtn\s*=\s*new\s+android\.widget\.LinearLayout\(this\);.*?cardsContainer\.addView\(addBtn\);', '', c, flags=re.DOTALL)
c = re.sub(r'LinearLayout\s+addBtn\s*=\s*new\s+LinearLayout\(this\);.*?cardsContainer\.addView\(addBtn\);', '', c, flags=re.DOTALL)

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ RESCUE COMPLETE! Double UI Fixed, Text is Visible, Home is Clean!")
