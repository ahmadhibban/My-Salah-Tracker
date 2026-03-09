f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(f, 'r', encoding='utf-8').read()
manager = r'''static class ZikrManager {
        static class TasbihData { String arabic, pron, mean; int target; TasbihData(String a, int t, String p, String m){arabic=a;target=t;pron=p;mean=m;} }
        java.util.ArrayList<TasbihData> tasbihList = new java.util.ArrayList<>();
        int currentIdx = 0; int[] indCounts = new int[300], indRounds = new int[300], indTotals = new int[300];
        boolean soundOn = true; int beadTheme = 0; android.media.ToneGenerator toneGen; android.content.SharedPreferences prefs;
        void init(android.content.Context ctx) {
            try {
                prefs = ctx.getSharedPreferences("TasbihPrefs_v6", android.content.Context.MODE_PRIVATE);
                if(tasbihList.isEmpty()) {
                    String[] raw = {"سُبْحَانَ اللّٰهِ|33|সুবহানাল্লাহ|আল্লাহ পবিত্র ও মহিমান্বিত", "الْحَمْدُ لِلّٰهِ|33|আলহামদুলিল্লাহ|যাবতীয় প্রশংসা আল্লাহর জন্য", "اللّٰهُ أَكْبَرُ|34|আল্লাহু আকবার|আল্লাহ সর্বশ্রেষ্ঠ", "لَا إِلٰهَ إِلَّا اللّٰهُ مُحَمَّدٌ رَسُولُ اللّٰهِ|0|লা ইলাহা ইল্লাল্লাহু মুহাম্মাদুর রাসুলুল্লাহ|আল্লাহ ছাড়া কোনো ইলাহ নেই..."};
                    for(String s : raw) { String[] p = s.split("\\\\|"); tasbihList.add(new TasbihData(p[0], Integer.parseInt(p[1]), p.length>2?p[2]:"উচ্চারণ যুক্ত করুন", p.length>3?p[3]:"অর্থ যুক্ত করুন")); }
                }
                for(int i=0; i<tasbihList.size(); i++) { indCounts[i] = prefs.getInt("ind_"+i, 0); indRounds[i] = prefs.getInt("round_"+i, 0); tasbihList.get(i).target = prefs.getInt("target_"+i, tasbihList.get(i).target); }
                currentIdx = prefs.getInt("lastIdx", 0); if(currentIdx >= tasbihList.size()) currentIdx = 0;
                soundOn = prefs.getBoolean("sound_on", true); beadTheme = prefs.getInt("bead_theme", 0);
                try{ toneGen = new android.media.ToneGenerator(android.media.AudioManager.STREAM_MUSIC, 100); }catch(Exception e){}
            } catch(Exception e) {}
        }
        void save() { if(prefs!=null) prefs.edit().putInt("ind_"+currentIdx, indCounts[currentIdx]).putInt("round_"+currentIdx, indRounds[currentIdx]).putInt("lastIdx", currentIdx).putBoolean("sound_on", soundOn).putInt("bead_theme", beadTheme).apply(); }
    }
    // ZIKR_CANVAS_PLACEHOLDER'''
c = c.replace('// ZIKR_MGR_PLACEHOLDER', manager)
open(f, 'w', encoding='utf-8').write(c)
print("✅ Step 2: ZikrManager Added with Pronunciation & Meaning.")
