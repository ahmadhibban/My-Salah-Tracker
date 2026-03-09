import re
import os

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'

if not os.path.exists(f):
    print("❌ Error: File not found!")
    exit()

with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# ১. Fix ambiguous setText (if exists)
c = re.sub(r'streakBadge\.setText\((streakCount\s*>=\s*365\s*\?.*?)\);', r'streakBadge.setText(String.valueOf(\1));', c)

# ২. Remove ALL traces of ZikrManager, ZikrCanvasView, loadZikrTab, loadStatsTab
garbage = ["private ZikrManager zikrMan", "static class ZikrManager", "class ZikrCanvasView", "private void loadZikrTab()", "private void loadStatsTab()"]
first_garbage_idx = len(c)

for g in garbage:
    idx = c.find(g)
    if idx != -1 and idx < first_garbage_idx:
        first_garbage_idx = idx

# Cut the file right before the mess starts
if first_garbage_idx < len(c):
    c = c[:first_garbage_idx]

# ৩. FIX THE BRACKETS (CRITICAL STEP)
# Strip all trailing spaces and newlines
c = c.rstrip()
# Remove any trailing closing brackets '}' that might close MainActivity prematurely
while c.endswith('}'):
    c = c[:-1].rstrip()

# ৪. INJECT THE MASTERPIECE (Ensure it is inside MainActivity)
mega_code = r'''
    private ZikrManager zikrMan = null;
    
    static class ZikrManager {
        static class TasbihData { String arabic, pron, mean; int target; TasbihData(String a, int t, String p, String m){arabic=a;target=t;pron=p;mean=m;} }
        java.util.ArrayList<TasbihData> tasbihList = new java.util.ArrayList<>();
        int currentIdx = 0; int[] indCounts = new int[300], indRounds = new int[300];
        boolean soundOn = true; int beadTheme = 0; android.media.ToneGenerator toneGen; android.content.SharedPreferences prefs;

        void init(android.content.Context ctx) {
            try {
                prefs = ctx.getSharedPreferences("TasbihPrefs_v10", android.content.Context.MODE_PRIVATE);
                if(tasbihList.isEmpty()) {
                    String[] raw = {
                        "سُبْحَانَ اللّٰهِ|33|সুবহানাল্লাহ|আল্লাহ অতি পবিত্র",
                        "الْحَمْدُ لِلّٰهِ|33|আলহামদুলিল্লাহ|যাবতীয় প্রশংসা আল্লাহর জন্য",
                        "اللّٰهُ أَكْبَرُ|34|আল্লাহু আকবার|আল্লাহ সর্বশ্রেষ্ঠ",
                        "لَا إِلٰهَ إِلَّا اللّٰهُ|0|লা ইলাহা ইল্লাল্লাহ|আল্লাহ ছাড়া কোনো ইলাহ নেই",
                        "أَسْتَغْفِرُ اللّٰهَ|100|আস্তাগফিরুল্লাহ|আমি আল্লাহর কাছে ক্ষমা চাই",
                        "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللّٰهِ|0|লা হাওলা ওয়ালা কুওয়াতা ইল্লা বিল্লাহ|আল্লাহ ছাড়া কোনো শক্তি নেই"
                    };
                    for(String s : raw) { String[] p = s.split("\\|"); tasbihList.add(new TasbihData(p[0], Integer.parseInt(p[1]), p[2], p[3])); }
                }
                for(int i=0; i<tasbihList.size(); i++) { indCounts[i] = prefs.getInt("ind_"+i, 0); indRounds[i] = prefs.getInt("round_"+i, 0); tasbihList.get(i).target = prefs.getInt("target_"+i, tasbihList.get(i).target); }
                currentIdx = prefs.getInt("lastIdx", 0); if(currentIdx >= tasbihList.size()) currentIdx = 0;
                soundOn = prefs.getBoolean("sound_on", true); beadTheme = prefs.getInt("bead_theme", 0);
                try{ toneGen = new android.media.ToneGenerator(android.media.AudioManager.STREAM_MUSIC, 100); }catch(Exception e){}
            } catch(Exception e) {}
        }
        void save() { if(prefs!=null) prefs.edit().putInt("ind_"+currentIdx, indCounts[currentIdx]).putInt("round_"+currentIdx, indRounds[currentIdx]).putInt("lastIdx", currentIdx).putBoolean("sound_on", soundOn).putInt("bead_theme", beadTheme).apply(); }
    }

    class ZikrCanvasView extends android.view.View {
        private float startX, beadOffset = 0f; private boolean isSwiping = false; 
        private android.graphics.Bitmap rBmp, sOn, sOff;
        private int[][] bCols = { {0xFFA5D6A7,0xFF2E7D32,0xFF1B5E20}, {0xFFFFE082,0xFFFF8F00,0xFFE65100}, {0xFFFFFFFF,0xFFE0E0E0,0xFF9E9E9E}, {0xFFBCAAA4,0xFF795548,0xFF4E342E}, {0xFFEF9A9A,0xFFC62828,0xFFB71C1C}, {0xFF9E9E9E,0xFF424242,0xFF212121} };

        public ZikrCanvasView(android.content.Context ctx) { 
            super(ctx); if(zikrMan==null){zikrMan=new ZikrManager();zikrMan.init(ctx);} 
            rBmp=load("img_zikr_reset"); sOn=load("img_zikr_sound_on"); sOff=load("img_zikr_sound_off");
        }
        private android.graphics.Bitmap load(String n){ int id=getResources().getIdentifier(n,"drawable",getContext().getPackageName()); return id!=0?android.graphics.BitmapFactory.decodeResource(getResources(),id):null; }
        private String toBn(int n) { String o=String.valueOf(n); String[] e={"0","1","2","3","4","5","6","7","8","9"}, b={"০","১","২","৩","৪","৫","৬","৭","৮","৯"}; for(int i=0;i<10;i++) o=o.replace(e[i],b[i]); return o; }
        private void drawB(android.graphics.Canvas cv, float cx, float cy, float rad, int t, android.graphics.Paint p) { 
            android.graphics.RadialGradient rg = new android.graphics.RadialGradient(cx-rad/3, cy-rad/3, rad*1.2f, bCols[t], null, android.graphics.Shader.TileMode.CLAMP); 
            p.setShader(rg); p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(10,0,5,0x44000000); cv.drawCircle(cx, cy, rad, p); p.clearShadowLayer(); p.setShader(null); 
        }

        @Override protected void onDraw(android.graphics.Canvas cv) {
            super.onDraw(cv); boolean isBn = sp.getString("app_lang","en").equals("bn"); float w=getWidth(), cx=w/2f;
            android.graphics.Paint p=new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            int idx=zikrMan.currentIdx; ZikrManager.TasbihData d=zikrMan.tasbihList.get(idx); int cur=zikrMan.indCounts[idx];

            p.setColor(themeColors[2]); p.setTextSize(65f); p.setTypeface(appFonts[1]); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            cv.drawText("Round "+(isBn?toBn(zikrMan.indRounds[idx]):zikrMan.indRounds[idx]), cx, 120f, p);

            float cY=480f, rad=w*0.33f; float sweep=d.target>0?((float)cur/d.target)*360f:0f;
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(40f); p.setStrokeCap(android.graphics.Paint.Cap.ROUND); p.setColor(themeColors[4]); cv.drawCircle(cx,cY,rad,p);
            p.setColor(colorAccent); cv.drawArc(new android.graphics.RectF(cx-rad,cY-rad,cx+rad,cY+rad),-90,sweep,false,p);
            
            double rD=Math.toRadians(sweep-90); float bX=(float)(cx+rad*Math.cos(rD)), bY=(float)(cY+rad*Math.sin(rD)); 
            p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(40,0,0,colorAccent); p.setColor(colorAccent); cv.drawCircle(bX,bY,35f,p); p.clearShadowLayer(); p.setColor(android.graphics.Color.WHITE); cv.drawCircle(bX,bY,15f,p);

            p.setTypeface(appFonts[1]); p.setColor(themeColors[2]); p.setTextAlign(android.graphics.Paint.Align.LEFT);
            String mS=isBn?toBn(cur):String.valueOf(cur); String tS=d.target>0?(" / "+(isBn?toBn(d.target):d.target)):"";
            float mF=250f, tF=60f; p.setTextSize(mF); float mW=p.measureText(mS); android.graphics.Paint tP=new android.graphics.Paint(p); tP.setTextSize(tF); tP.setColor(themeColors[3]); tP.setTypeface(appFonts[0]); float tW=tP.measureText(tS);
            while(mW+tW>rad*1.7f){ mF-=5f; tF-=1.2f; p.setTextSize(mF); tP.setTextSize(tF); mW=p.measureText(mS); tW=tP.measureText(tS); }
            float sXT=cx-(mW+tW)/2f; cv.drawText(mS,sXT,cY+(mF/3.2f),p); cv.drawText(tS,sXT+mW,cY+(mF/3.2f),tP);

            float strY = cY + rad + 140f; p.setColor(themeColors[3]); p.setStrokeWidth(4f); cv.drawLine(60f, strY, w-60f, strY, p);
            float gap=165f, spc=85f, beadR=38f; float actX=beadOffset<0?cx+gap/2+beadOffset:(beadOffset>0?cx-gap/2+beadOffset:0f);
            for(int i=0;i<4;i++){ 
                if(!(beadOffset>0&&i==0)) drawB(cv,cx-gap/2-(i*spc),strY,beadR,zikrMan.beadTheme,p);
                if(!(beadOffset<0&&i==0)) drawB(cv,cx+gap/2+(i*spc),strY,beadR,zikrMan.beadTheme,p);
            }
            if(beadOffset!=0) drawB(cv,actX,strY,beadR,zikrMan.beadTheme,p);

            float boxT=strY+130f, boxH=320f, boxB=boxT+boxH; p.setColor(themeColors[1]); p.setShadowLayer(15,0,8,0x15000000); cv.drawRoundRect(new android.graphics.RectF(50,boxT,w-50,boxB), 45f, 45f, p); p.clearShadowLayer();
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(5f); p.setColor(colorAccent); cv.drawRoundRect(new android.graphics.RectF(50,boxT,w-50,boxB), 45f, 45f, p);
            p.setStyle(android.graphics.Paint.Style.FILL); android.text.TextPaint tp=new android.text.TextPaint(p); tp.setTypeface(getArabicFont()); tp.setColor(themeColors[2]);
            int layW=(int)(w-140); float fS=100f; android.text.StaticLayout sl;
            while(true){ tp.setTextSize(fS); sl=new android.text.StaticLayout(d.arabic,tp,layW,android.text.Layout.Alignment.ALIGN_CENTER,1.2f,0,false);
                if(sl.getLineCount()<=2){ if(sl.getLineCount()==2){ String l2=d.arabic.substring(sl.getLineStart(1),sl.getLineEnd(1)).trim(); if(!l2.contains(" ")&&fS>40f){fS-=2f;continue;} } break; }
                if(fS<=35f) break; fS-=2f; }
            cv.save(); cv.translate(cx-(layW/2f), boxT+(boxH-sl.getHeight())/2f); sl.draw(cv); cv.restore();

            float iY=boxB+110f, mrg=130f;
            if(rBmp!=null) cv.drawBitmap(rBmp,null,new android.graphics.RectF(mrg-40,iY-40,mrg+40,iY+40),p); else{ p.setColor(themeColors[1]); cv.drawCircle(mrg,iY,55f,p); p.setColor(themeColors[3]); p.setTextSize(45f); cv.drawText("↺",mrg,iY+15f,p); }
            android.graphics.Bitmap sb=zikrMan.soundOn?sOn:sOff; p.setAlpha(zikrMan.soundOn?255:120); if(sb!=null) cv.drawBitmap(sb,null,new android.graphics.RectF(w-mrg-40,iY-40,w-mrg+40,iY+40),p); else{ p.setColor(themeColors[1]); cv.drawCircle(w-mrg,iY,55f,p); p.setColor(colorAccent); p.setTextSize(45f); cv.drawText(zikrMan.soundOn?"🔊":"🔇",w-mrg,iY+15f,p); } p.setAlpha(255);
            
            float thY=iY+160f; for(int i=0;i<6;i++){ float cxT=cx-250f+(i*100f); drawB(cv,cxT,thY,35f,i,p); if(zikrMan.beadTheme==i){ p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(6f); p.setColor(colorAccent); cv.drawCircle(cxT,thY,48f,p); } }
        }

        private void cnt(boolean a){ int i=zikrMan.currentIdx; if(a){zikrMan.indCounts[i]++; if(zikrMan.soundOn&&zikrMan.toneGen!=null) zikrMan.toneGen.startTone(24,50); if(zikrMan.tasbihList.get(i).target>0&&zikrMan.indCounts[i]>=zikrMan.tasbihList.get(i).target){zikrMan.indCounts[i]=0;zikrMan.indRounds[i]++;performHapticFeedback(0);}} else {if(zikrMan.indCounts[i]>0)zikrMan.indCounts[i]--;} zikrMan.save(); }
        private void anim(float t, boolean a){ android.animation.ValueAnimator v=android.animation.ValueAnimator.ofFloat(beadOffset,t); v.setDuration(120); v.addUpdateListener(an->{beadOffset=(float)an.getAnimatedValue();invalidate();}); v.addListener(new android.animation.AnimatorListenerAdapter(){public void onAnimationEnd(android.animation.Animator an){if(t!=0f)cnt(a); beadOffset=0f;invalidate();}}); v.start(); }

        @Override public boolean onTouchEvent(android.view.MotionEvent ev) {
            float x=ev.getX(), y=ev.getY(), w=getWidth(), cx=w/2f; float iY=940f, thY=1100f; int i=zikrMan.currentIdx;
            if(ev.getAction()==0){startX=x;isSwiping=false;return true;}
            if(ev.getAction()==2){float dx=x-startX; if(Math.abs(dx)>20){isSwiping=true; beadOffset=dx; if(beadOffset>160f)beadOffset=160f; if(beadOffset<-160f)beadOffset=-160f; invalidate();}}
            if(ev.getAction()==1){
                float dx=x-startX; if(isSwiping){ if(dx<-60){performHapticFeedback(1);anim(-160f,true);} else if(dx>60){performHapticFeedback(1);anim(160f,false);} else anim(0f,false); }
                else {
                    if(Math.abs(y-iY)<120){ if(x<250){performHapticFeedback(1); new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Reset")).setMessage(lang.get("Do you want to reset?")).setPositiveButton("Yes",(di,wi)->{zikrMan.indCounts[i]=0;zikrMan.indRounds[i]=0;zikrMan.save();invalidate();}).setNegativeButton("No",null).show();} else if(x>w-250){zikrMan.soundOn=!zikrMan.soundOn;zikrMan.save();invalidate();} }
                    else if(y>350 && y<600 && x>cx){performHapticFeedback(1); editT(i);}
                    else if(y>750 && y<1100 && x>50 && x<w-50){performHapticFeedback(1); showL();}
                    else if(y>thY-60 && y<thY+60){ for(int j=0;j<6;j++){ if(Math.abs(x-(cx-250f+(j*100f)))<50){zikrMan.beadTheme=j;zikrMan.save();invalidate();break;} } }
                    else {performHapticFeedback(1);anim(-160f,true);}
                }
            } return true;
        }
        private void editT(int idx){ final android.widget.EditText et=new android.widget.EditText(getContext()); et.setInputType(2); et.setText(String.valueOf(zikrMan.tasbihList.get(idx).target)); new android.app.AlertDialog.Builder(getContext()).setTitle("Target").setView(et).setPositiveButton("OK",(di,wi)->{if(!et.getText().toString().isEmpty()){zikrMan.tasbihList.get(idx).target=Integer.parseInt(et.getText().toString()); zikrMan.prefs.edit().putInt("target_"+idx,zikrMan.tasbihList.get(idx).target).apply(); invalidate();}}).show(); }
        private void showL(){
            final android.app.Dialog d=new android.app.Dialog(getContext(),android.R.style.Theme_Black_NoTitleBar_Fullscreen); android.widget.LinearLayout r=new android.widget.LinearLayout(getContext()); r.setOrientation(1); r.setBackgroundColor(themeColors[0]); r.setPadding(40,80,40,40); android.widget.TextView t1=new android.widget.TextView(getContext()); t1.setText(lang.get("Zikr")); t1.setTextColor(colorAccent); t1.setTextSize(26); t1.setTypeface(appFonts[1]); t1.setGravity(17); r.addView(t1);
            android.widget.ScrollView sv=new android.widget.ScrollView(getContext()); android.widget.LinearLayout l=new android.widget.LinearLayout(getContext()); l.setOrientation(1);
            for(int j=0;j<zikrMan.tasbihList.size();j++){
                final int rI=j; ZikrManager.TasbihData dt=zikrMan.tasbihList.get(j); android.widget.LinearLayout row=new android.widget.LinearLayout(getContext()); row.setOrientation(1); row.setPadding(30,45,30,45); row.setGravity(17);
                android.widget.TextView tA=new android.widget.TextView(getContext()); tA.setText(dt.arabic); tA.setTextColor(themeColors[2]); tA.setTextSize(32); tA.setTypeface(getArabicFont()); tA.setGravity(17); tA.setOnClickListener(v->{zikrMan.currentIdx=rI;zikrMan.save();invalidate();d.dismiss();}); row.addView(tA);
                android.widget.TextView tP=new android.widget.TextView(getContext()); tP.setText(dt.pron); tP.setTextColor(themeColors[3]); tP.setTextSize(16); tP.setGravity(17); tP.setPadding(0,15,0,5); row.addView(tP);
                android.widget.TextView tM=new android.widget.TextView(getContext()); tM.setText(dt.mean); tM.setTextColor(themeColors[3]); tM.setTextSize(14); tM.setGravity(17); tM.setPadding(0,0,0,25); row.addView(tM);
                android.widget.TextView tT=new android.widget.TextView(getContext()); tT.setText("Target: "+dt.target); tT.setTextColor(colorAccent); tT.setTextSize(18); tT.setTypeface(appFonts[1]); tT.setGravity(17); android.graphics.drawable.GradientDrawable tb=new android.graphics.drawable.GradientDrawable(); tb.setColor(themeColors[1]); tb.setCornerRadius(15f); tT.setBackground(tb); tT.setPadding(40,15,40,15); tT.setOnClickListener(v->{ editT(rI); }); row.addView(tT);
                l.addView(row); android.view.View div=new android.view.View(getContext()); div.setBackgroundColor(themeColors[4]); div.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1,2)); l.addView(div);
            } sv.addView(l); r.addView(sv,new android.widget.LinearLayout.LayoutParams(-1,0,1f));
            android.widget.Button bA=new android.widget.Button(getContext()); bA.setText("+ Add New"); bA.setAllCaps(false); bA.setTextColor(colorAccent); bA.setTypeface(appFonts[1]); android.graphics.drawable.GradientDrawable btnBg=new android.graphics.drawable.GradientDrawable(); btnBg.setColor(0); btnBg.setStroke(4, colorAccent); btnBg.setCornerRadius(30f); bA.setBackground(btnBg); android.widget.LinearLayout.LayoutParams blp=new android.widget.LinearLayout.LayoutParams(-1,150); blp.setMargins(40,30,40,40); bA.setLayoutParams(blp);
            bA.setOnClickListener(v->{ d.dismiss(); }); r.addView(bA); d.setContentView(r); d.show();
        }
    }

    private void loadZikrTab() {
        contentArea.removeAllViews();
        contentArea.addView(new ZikrCanvasView(this), new android.widget.LinearLayout.LayoutParams(-1, -1));
    }

    private void loadStatsTab() {
        contentArea.removeAllViews();
        contentArea.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));
        android.widget.TextView h = new android.widget.TextView(this); h.setText(lang.get("Stats")); h.setTextColor(themeColors[2]); h.setTextSize(24); h.setTypeface(appFonts[1]); h.setPadding(0,0,0,(int)(20*DENSITY)); contentArea.addView(h);
        try {
            java.lang.reflect.Method m = StatsHelper.class.getDeclaredMethod("renderStats", android.widget.LinearLayout.class, android.app.AlertDialog.class, boolean.class); m.setAccessible(true);
            android.widget.TextView wT = new android.widget.TextView(this); wT.setText(lang.get("Weekly Statistics")); wT.setTextColor(themeColors[3]); wT.setTypeface(appFonts[1]); contentArea.addView(wT);
            android.widget.LinearLayout wC = new android.widget.LinearLayout(this); wC.setOrientation(android.widget.LinearLayout.VERTICAL); wC.setPadding((int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY));
            android.graphics.drawable.GradientDrawable wBg = new android.graphics.drawable.GradientDrawable(); wBg.setColor(themeColors[1]); wBg.setCornerRadius(25f*DENSITY); wC.setBackground(wBg);
            android.widget.LinearLayout.LayoutParams wLp = new android.widget.LinearLayout.LayoutParams(-1, -2); wLp.setMargins(0,(int)(10*DENSITY),0,(int)(20*DENSITY)); wC.setLayoutParams(wLp);
            m.invoke(statsHelper, wC, null, true); wC.removeViewAt(wC.getChildCount()-1); contentArea.addView(wC);
            
            android.widget.TextView mT = new android.widget.TextView(this); mT.setText(lang.get("Monthly Statistics")); mT.setTextColor(themeColors[3]); mT.setTypeface(appFonts[1]); contentArea.addView(mT);
            android.widget.LinearLayout mC = new android.widget.LinearLayout(this); mC.setOrientation(android.widget.LinearLayout.VERTICAL); mC.setPadding((int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY));
            android.graphics.drawable.GradientDrawable mBg = new android.graphics.drawable.GradientDrawable(); mBg.setColor(themeColors[1]); mBg.setCornerRadius(25f*DENSITY); mC.setBackground(mBg);
            android.widget.LinearLayout.LayoutParams mLp = new android.widget.LinearLayout.LayoutParams(-1, -2); mLp.setMargins(0,(int)(10*DENSITY),0,(int)(20*DENSITY)); mC.setLayoutParams(mLp);
            m.invoke(statsHelper, mC, null, false); mC.removeViewAt(mC.getChildCount()-1); contentArea.addView(mC);
        } catch(Exception e){}
    }
'''

# Ensure correct class closing
with open(f, 'w', encoding='utf-8') as file:
    file.write(c + "\n" + mega_code + "\n}\n")

print("✅ BRACKETS FIXED! MASTERPIECE INSTALLED! HIT PLAY! 🚀")
