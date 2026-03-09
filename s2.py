f='app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
z1=r'''
    private ZikrManager zikrMan = null;
    static class ZikrManager {
        static class TasbihData { String arabic, pron, mean; int target; TasbihData(String a, int t, String p, String m){arabic=a;target=t;pron=p;mean=m;} }
        java.util.ArrayList<TasbihData> tasbihList = new java.util.ArrayList<>();
        int currentIdx=0; int[] indCounts=new int[300], indRounds=new int[300];
        boolean soundOn=true; int beadTheme=0; android.media.ToneGenerator toneGen; android.content.SharedPreferences prefs;
        void init(android.content.Context ctx) {
            try { prefs = ctx.getSharedPreferences("T_v11", 0);
                if(tasbihList.isEmpty()) {
                    String[] raw = {"سُبْحَانَ اللّٰهِ|33|সুবহানাল্লাহ|আল্লাহ পবিত্র ও মহিমান্বিত", "الْحَمْدُ لِلّٰهِ|33|আলহামদুলিল্লাহ|যাবতীয় প্রশংসা আল্লাহর জন্য", "اللّٰهُ أَكْبَرُ|34|আল্লাহু আকবার|আল্লাহ সর্বশ্রেষ্ঠ", "لَا إِلٰهَ إِلَّا اللّٰهُ|0|লা ইলাহা ইল্লাল্লাহ|আল্লাহ ছাড়া কোনো ইলাহ নেই", "أَسْتَغْفِرُ اللّٰهَ|100|আস্তাগফিরুল্লাহ|আমি আল্লাহর কাছে ক্ষমা চাই"};
                    for(String s:raw){ String[] p=s.split("\\|"); tasbihList.add(new TasbihData(p[0], Integer.parseInt(p[1]), p[2], p[3])); }
                }
                for(int i=0;i<tasbihList.size();i++){ indCounts[i]=prefs.getInt("c_"+i,0); indRounds[i]=prefs.getInt("r_"+i,0); tasbihList.get(i).target=prefs.getInt("t_"+i,tasbihList.get(i).target); }
                currentIdx=prefs.getInt("lI",0); soundOn=prefs.getBoolean("sO",true); beadTheme=prefs.getInt("bT",0);
                try{ toneGen=new android.media.ToneGenerator(3,100); }catch(Exception e){}
            } catch(Exception e){}
        }
        void save() { if(prefs!=null) prefs.edit().putInt("c_"+currentIdx,indCounts[currentIdx]).putInt("r_"+currentIdx,indRounds[currentIdx]).putInt("lI",currentIdx).putBoolean("sO",soundOn).putInt("bT",beadTheme).apply(); }
    }
    //_UI_
'''
open(f,'w').write(open(f).read().replace('//_ZIKR_', z1))
print("✅ Step 2: Database Injected!")
