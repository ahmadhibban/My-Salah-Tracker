import re
f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(f).read()

# 1. Language Update
le = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
lc = open(le).read()
if '"Tap box to change Dua or Target"' not in lc:
    lc = lc.replace('bnMap.put("Reset", "রিসেট");', 'bnMap.put("Reset", "রিসেট");\n        bnMap.put("Tap box to change Dua or Target", "দোয়া পরিবর্তন করতে বা টার্গেট সেট করতে বক্সে ট্যাপ করুন");\n        bnMap.put("Do you want to reset counts for this Dua?", "আপনি কি এই দোয়ার হিসাব জিরো (০) করতে চান?");')
    open(le, 'w').write(lc)

# 2. ZikrManager Sorting Logic
old_init = '''for(String s : raw) { String[] p = s.split("\\\\|"); tasbihList.add(new TasbihData(p[0], Integer.parseInt(p[1]))); }'''
new_init = '''for(String s : raw) { String[] p = s.split("\\\\|"); tasbihList.add(new TasbihData(p[0], Integer.parseInt(p[1]))); }
                    java.util.ArrayList<TasbihData> temp = new java.util.ArrayList<>();
                    for(int i=0; i<3; i++) temp.add(tasbihList.get(i));
                    java.util.List<TasbihData> sub = new java.util.ArrayList<>(tasbihList.subList(3, tasbihList.size()));
                    java.util.Collections.sort(sub, new java.util.Comparator<TasbihData>() { public int compare(TasbihData a, TasbihData b) { return Integer.compare(a.arabic.length(), b.arabic.length()); } });
                    temp.addAll(sub); tasbihList = temp;'''
c = c.replace(old_init, new_init)
open(f, 'w').write(c)
print("✅ Part 1 Done: Language and Sorting injected.")
