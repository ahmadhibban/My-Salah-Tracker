import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# ১. ZikrManager এ সঠিক সর্টিং (সুবহানাল্লাহ, আলহামদুলিল্লাহ, আল্লাহু আকবার সবার আগে)
old_init = r'if\(tasbihList\.isEmpty\(\)\) \{.*?for\(String s : raw\) \{ String\[\] p = s\.split\("\\\\\\\\|"\); tasbihList\.add\(new TasbihData\(p\[0\], Integer\.parseInt\(p\[1\]\)\)\); \}'
new_init = r'''if(tasbihList.isEmpty()) {
                String[] raw = {"سُبْحَانَ اللّٰهِ|33", "الْحَمْدُ لِلّٰهِ|33", "اللّٰهُ أَكْبَرُ|34", "لَا إِلٰهَ إِلَّا اللّٰهُ مُحَمَّدٌ רَسُولُ اللّٰهِ|0", "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ كُلَّمَا ذَكَرَهُ الذَّاكِرُونَ وَصَلِّ عَلَى مُحَمَّدٍ كُلَّمَا غَفَلَ عَنْ ذِكْرِهِ الْغَافِلُونَ|0", "صَلَّى اللّٰهُ عَلَيْهِ وَسَلَّمَ|0", "جَزَى اللهُ عَنَّا مُحَمَّدًا مَا هُوَ أَهْلُهُ|0", "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ النَّبِيِّ الْأُمِّيِّ وَعَلَى آلِهِ وَسَلِّمْ تَسْلِيمًا|0", "اَللّٰهُمَّ صَلِّ عَلَىٰ سَيِّدِنَا وَنَبِيِّনَا وَشَفِيعِنَا وَحَبِيبِنَا وَمَوْلَانَا مُحَمَّدٍ ، صَلَّى اللّٰهُ عَلَيْهِ وَعَلَىٰ آلِهِ وَأَصْحَابِهِ وَبَارِكْ وَسَلِّমْ|0", "أَسْتَغْفِرُ اللّٰهَ وَأَتُوبُ إِلَيْهِ|100", "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللّٰهِ|0", "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ|0", "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْجَنَّةَ وَأَعُوذُ بِكَ مِنَ النَّارِ|0", "اللَّهُمَّ إِنَّكَ عَفُوٌّ كَرِيمٌ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي|0", "لَا إِلَهَ إِلَّا اللهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ يُحْيِي وَيُمِيتُ وَهُوة عَلَى كُلِّ شَيْءٍ قَدِيرٌ|100", "اللَّهُمَّ اهْدِنَا وَاهْدِ بِنَا وَاهْدِ النَّاسَ جَمِيعًا|0", "اللَّهُمَّ لَا مَانِعَ لِمَا أَعْطَيْتَ، وَلَا مُعْطِيَ لِمَا مَنَعْتَ।", "أَسْتَغْفِرُ اللهَ|3", "إِلَّا اللهُ|0", "أَعُوذُ بِاللهِ السَّمِيعِ الْعَلِيمِ مِنَ الشَّيْطَانِ الرَّجِيمِ|0", "حَسْبِيَ اللهُ لَا إِلَهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ|7", "أَعُوذُ بِكَلِمَاتِ اللهِ التَّامَّاتِ مِنْ غَضَبِهِ وَعِقَابِهِ وَشَرِّ عِبَادِهِ|0", "حَسْبُنَا اللهُ، وَنِعْمَ الْوَكِيلُ|0", "أَسْتَغْفِرُ اللَّهَ الَّذِي لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ وَأَتُوبُ إِلَيْهِ|0"};
                for(String s : raw) { String[] p = s.split("\\\\|"); tasbihList.add(new TasbihData(p[0], Integer.parseInt(p[1]))); }
                java.util.ArrayList<TasbihData> sorted = new java.util.ArrayList<>();
                for(int i=0; i<3 && i<tasbihList.size(); i++) sorted.add(tasbihList.get(i));
                if(tasbihList.size() > 3) {
                    java.util.List<TasbihData> sub = new java.util.ArrayList<>(tasbihList.subList(3, tasbihList.size()));
                    java.util.Collections.sort(sub, (a, b) -> Integer.compare(a.arabic.length(), b.arabic.length()));
                    sorted.addAll(sub);
                } tasbihList = sorted;
            }'''
c = re.sub(old_init, new_init, c, flags=re.DOTALL)

# ২. ZikrCanvasView ক্লাস পুরোপুরি রি-ডিজাইন করা
start_idx = c.find("class ZikrCanvasView")
end_idx = c.find("private void loadZikrTab()")

if start_idx != -1 and end_idx != -1:
    new_canvas = """class ZikrCanvasView extends android.view.View {
        private float startX, startY; private android.graphics.Bitmap resetBmp, sOnBmp, sOffBmp;
        public ZikrCanvasView(android.content.Context context) {
            super(context); if(zikrMan == null) { zikrMan = new ZikrManager(); zikrMan.init(context); }
            resetBmp = loadBmp("img_zikr_reset"); sOnBmp = loadBmp("img_zikr_sound_on"); sOffBmp = loadBmp("img_zikr_sound_off");
        }
        private android.graphics.Bitmap loadBmp(String n){ int id=getResources().getIdentifier(n,"drawable",getContext().getPackageName()); return id!=0?android.graphics.BitmapFactory.decodeResource(getResources(),id):null; }
        private String toBn(int n) { String o=String.valueOf(n); String[] e={"0","1","2","3","4","5","6","7","8","9"}, b={"০","১","২","৩","৪","৫","৬","৭","৮","৯"}; for(int i=0;i<10;i++) o=o.replace(e[i],b[i]); return o; }

        @Override protected void onDraw(android.graphics.Canvas cv) {
            super.onDraw(cv); boolean isBn = sp.getString("app_lang","en").equals("bn"); float w=getWidth(), centerX=w/2f;
            android.graphics.Paint p = new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            int idx=zikrMan.currentIdx; ZikrManager.TasbihData d=zikrMan.tasbihList.get(idx); int cur=zikrMan.indCounts[idx];

            // 1. Dua Box (Original High-Res Style)
            float boxT=70f, boxH=380f, boxB=boxT+boxH;
            p.setColor(themeColors[1]); p.setShadowLayer(20,0,10,android.graphics.Color.parseColor("#15000000"));
            cv.drawRoundRect(new android.graphics.RectF(50,boxT,w-50,boxB), 45f, 45f, p); p.clearShadowLayer();
            
            android.text.TextPaint tp = new android.text.TextPaint(p); tp.setTypeface(getArabicFont()); tp.setColor(themeColors[2]);
            int layW=(int)(w-160); float fSize=100f; android.text.StaticLayout sl;
            while(true) {
                tp.setTextSize(fSize); sl = new android.text.StaticLayout(d.arabic, tp, layW, android.text.Layout.Alignment.ALIGN_CENTER, 1.2f, 0, false);
                if(sl.getLineCount() <= 2) {
                    if(sl.getLineCount() == 2) {
                        String l2 = d.arabic.substring(sl.getLineStart(1), sl.getLineEnd(1)).trim();
                        if(!l2.contains(" ") && fSize > 40f) { fSize -= 2f; continue; } // One word on 2nd line -> Shrink to fit 1 line
                    }
                    break;
                }
                if(fSize <= 35f) break; fSize -= 2f;
            }
            cv.save(); cv.translate(centerX-(layW/2f), boxT+(boxH-sl.getHeight())/2f); sl.draw(cv); cv.restore();

            // 2. Navigation & Instruction
            p.setColor(themeColors[3]); p.setTextSize(34f); p.setTextAlign(android.graphics.Paint.Align.CENTER); p.setTypeface(appFonts[0]);
            cv.drawText(lang.get("Tap box to change Dua or Target"), centerX, boxB+75f, p);

            // 3. Middle Icons (Below Box, Above Circle)
            float iconY = boxB + 190f; float margin=130f;
            if(resetBmp!=null) cv.drawBitmap(resetBmp, null, new android.graphics.RectF(margin-45, iconY-45, margin+45, iconY+45), p);
            else { p.setColor(themeColors[1]); cv.drawCircle(margin, iconY, 65f, p); p.setColor(themeColors[3]); p.setTextSize(50f); cv.drawText("↺", margin, iconY+18f, p); }
            
            android.graphics.Bitmap sB = zikrMan.soundOn ? sOnBmp : sOffBmp;
            if(sB!=null) cv.drawBitmap(sB, null, new android.graphics.RectF(w-margin-45, iconY-45, w-margin+45, iconY+45), p);
            else { p.setColor(themeColors[1]); cv.drawCircle(w-margin, iconY, 65f, p); p.setColor(zikrMan.soundOn?colorAccent:themeColors[3]); p.setTextSize(50f); cv.drawText(zikrMan.soundOn?"🔊":"🔇", w-margin, iconY+18f, p); }

            // 4. Progress Circle & Glowing Ball
            float cY = iconY + 450f, rad = w*0.37f; float sweep = d.target>0 ? ((float)cur/d.target)*360f : 0f;
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(50f); p.setStrokeCap(android.graphics.Paint.Cap.ROUND);
            p.setColor(themeColors[4]); cv.drawCircle(centerX, cY, rad, p);
            p.setColor(colorAccent); cv.drawArc(new android.graphics.RectF(centerX-rad, cY-rad, centerX+rad, cY+rad), -90, sweep, false, p);
            
            double rD = Math.toRadians(sweep-90); float ballX=(float)(centerX+rad*Math.cos(rD)), ballY=(float)(cY+rad*Math.sin(rD));
            p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(45,0,0,colorAccent); p.setColor(colorAccent); cv.drawCircle(ballX, ballY, 36f, p); p.clearShadowLayer();
            p.setColor(android.graphics.Color.WHITE); cv.drawCircle(ballX, ballY, 15f, p);

            // 5. Perfect Number Centering (Large + Target)
            p.setTypeface(appFonts[1]); p.setColor(themeColors[2]); p.setTextAlign(android.graphics.Paint.Align.LEFT);
            String mS = isBn?toBn(cur):String.valueOf(cur); String tS = d.target>0 ? (" / "+(isBn?toBn(d.target):d.target)) : "";
            float mF=260f, tF=60f; p.setTextSize(mF); float mW=p.measureText(mS);
            android.graphics.Paint tP = new android.graphics.Paint(p); tP.setTextSize(tF); tP.setColor(themeColors[3]); tP.setTypeface(appFonts[0]); float tW=tP.measureText(tS);
            while(mW+tW > rad*1.7f) { mF-=5f; tF-=1.2f; p.setTextSize(mF); tP.setTextSize(tF); mW=p.measureText(mS); tW=tP.measureText(tS); }
            float startXT = centerX - (mW+tW)/2f; float txtY = cY + (mF/3.2f);
            cv.drawText(mS, startXT, txtY, p); cv.drawText(tS, startXT+mW, txtY, tP);

            // 6. Bottom UI (Minus & Rounds)
            float bY_coord = cY + rad + 155f; float mX=centerX-rad+25f, sX=centerX+rad-25f;
            drawRoundBtn(cv, mX, bY_coord, "-", android.graphics.Color.parseColor("#EF4444"), 110f);
            drawRoundBtn(cv, sX, bY_coord, isBn?toBn(zikrMan.indRounds[idx]):String.valueOf(zikrMan.indRounds[idx]), colorAccent, 70f);
            p.setColor(themeColors[3]); p.setTextSize(34f); p.setTypeface(appFonts[0]); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText(lang.get("Rounds"), sX, bY_coord+130f, p);

            // 7. Total Card
            String totTxt = lang.get("Total") + ": " + (isBn?toBn(zikrMan.indTotals[idx]):zikrMan.indTotals[idx]);
            p.setTextSize(48f); p.setTypeface(appFonts[1]); float totW = p.measureText(totTxt)+110f;
            p.setColor(themeColors[1]); p.setShadowLayer(15,0,8,android.graphics.Color.parseColor("#12000000"));
            cv.drawRoundRect(new android.graphics.RectF(centerX-totW/2, bY_coord+220, centerX+totW/2, bY_coord+320), 35f, 35f, p); p.clearShadowLayer();
            p.setColor(themeColors[2]); cv.drawText(totTxt, centerX, bY_coord+288f, p);
        }

        private void drawRoundBtn(android.graphics.Canvas cv, float x, float y, String t, int c, float s) {
            android.graphics.Paint p = new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            p.setColor(themeColors[1]); p.setShadowLayer(15,0,8,android.graphics.Color.parseColor("#15000000")); cv.drawCircle(x,y,90f,p); p.clearShadowLayer();
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(5f); p.setColor(themeColors[4]); cv.drawCircle(x,y,90f,p);
            p.setStyle(android.graphics.Paint.Style.FILL); p.setColor(c); p.setTextSize(s); p.setTypeface(appFonts[1]); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText(t, x, y+s/3.3f, p);
        }

        @Override public boolean onTouchEvent(android.view.MotionEvent ev) {
            float x=ev.getX(), y=ev.getY(), w=getWidth(), centerX=w/2f;
            float boxT=70f, boxB=boxT+380f, iconY=boxB+190f, cY=iconY+450f, rad=w*0.37f, bY_c=cY+rad+155f, mX=centerX-rad+25f, margin=130f; int idx=zikrMan.currentIdx;
            if(ev.getAction()==android.view.MotionEvent.ACTION_DOWN){ startX=x; return true; }
            if(ev.getAction()==android.view.MotionEvent.ACTION_UP){
                if(Math.abs(y-iconY)<100) {
                    if(Math.abs(x-margin)<100) { performHapticFeedback(1); showResetD(idx); return true; }
                    if(Math.abs(x-(w-margin))<100) { performHapticFeedback(1); zikrMan.soundOn=!zikrMan.soundOn; zikrMan.save(); invalidate(); return true; }
                }
                if(x>50 && x<w-50 && y>boxT && y<boxB) { performHapticFeedback(1); showZList(); return true; }
                if(Math.abs(x-mX)<105 && Math.abs(y-bY_c)<105) { performHapticFeedback(1); if(zikrMan.indCounts[idx]>0){ zikrMan.indCounts[idx]--; zikrMan.indTotals[idx]--; zikrMan.save(); invalidate(); } return true; }
                double dist = Math.sqrt(Math.pow(x-centerX,2)+Math.pow(y-cY,2));
                if(dist<=rad+60) { performHapticFeedback(1); zikrMan.indCounts[idx]++; zikrMan.indTotals[idx]++; if(zikrMan.soundOn && zikrMan.toneGen!=null) zikrMan.toneGen.startTone(android.media.ToneGenerator.TONE_PROP_BEEP, 50); if(zikrMan.tasbihList.get(idx).target>0 && zikrMan.indCounts[idx]>=zikrMan.tasbihList.get(idx).target){ zikrMan.indCounts[idx]=0; zikrMan.indRounds[idx]++; performHapticFeedback(0); } zikrMan.save(); invalidate(); return true; }
                float dX=x-startX; if(Math.abs(dX)>150){ if(dX<0) zikrMan.currentIdx=(zikrMan.currentIdx+1)%zikrMan.tasbihList.size(); else zikrMan.currentIdx=(zikrMan.currentIdx-1+zikrMan.tasbihList.size())%zikrMan.tasbihList.size(); zikrMan.save(); invalidate(); return true; }
            } invalidate(); return true;
        }
        private void showResetD(int i){ new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Reset")).setMessage(lang.get("Do you want to reset counts for this Dua?")).setPositiveButton(lang.get("Yes"), (di,wi)->{ zikrMan.indCounts[i]=0; zikrMan.indTotals[i]=0; zikrMan.indRounds[i]=0; zikrMan.save(); invalidate(); }).setNegativeButton(lang.get("No"),null).show(); }
        private void showZList(){ final android.app.Dialog d=new android.app.Dialog(getContext(),android.R.style.Theme_Black_NoTitleBar_Fullscreen); android.widget.LinearLayout r=new android.widget.LinearLayout(getContext()); r.setOrientation(1); r.setBackgroundColor(themeColors[0]); r.setPadding(40,80,40,40); android.widget.TextView t1=new android.widget.TextView(getContext()); t1.setText(lang.get("Zikr")); t1.setTextColor(colorAccent); t1.setTextSize(26); t1.setTypeface(appFonts[1]); t1.setGravity(1); r.addView(t1); android.widget.ScrollView sv=new android.widget.ScrollView(getContext()); android.widget.LinearLayout l=new android.widget.LinearLayout(getContext()); l.setOrientation(1); for(int i=0;i<zikrMan.tasbihList.size();i++){ final int rI=i; android.widget.LinearLayout row=new android.widget.LinearLayout(getContext()); row.setPadding(20,35,20,35); row.setGravity(16); android.widget.TextView tvD=new android.widget.TextView(getContext()); tvD.setText(zikrMan.tasbihList.get(rI).arabic); tvD.setTextColor(themeColors[2]); tvD.setTextSize(26); tvD.setTypeface(getArabicFont()); tvD.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,-2,7.5f)); tvD.setOnClickListener(v->{ zikrMan.currentIdx=rI; zikrMan.save(); invalidate(); d.dismiss(); }); android.widget.TextView tvT=new android.widget.TextView(getContext()); tvT.setText(String.valueOf(zikrMan.tasbihList.get(rI).target)); tvT.setTextColor(colorAccent); tvT.setTextSize(22); tvT.setTypeface(appFonts[0]); tvT.setGravity(1); tvT.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,-2,2.5f)); tvT.setOnClickListener(v->{ editT(rI,tvT); }); row.addView(tvD); row.addView(tvT); l.addView(row); } sv.addView(l); r.addView(sv,new android.widget.LinearLayout.LayoutParams(-1,0,1f)); android.widget.Button bA=new android.widget.Button(getContext()); bA.setText("+ Add New"); bA.setAllCaps(false); bA.setBackgroundColor(themeColors[1]); bA.setTextColor(themeColors[2]); bA.setOnClickListener(v->{ android.widget.LinearLayout lay=new android.widget.LinearLayout(getContext()); lay.setOrientation(1); lay.setPadding(50,20,50,20); final android.widget.EditText eD=new android.widget.EditText(getContext()); eD.setHint("Arabic Dua"); final android.widget.EditText eT=new android.widget.EditText(getContext()); eT.setHint("Target"); eT.setInputType(2); lay.addView(eD); lay.addView(eT); new android.app.AlertDialog.Builder(getContext()).setTitle("Add").setView(lay).setPositiveButton("OK",(di,wi)->{ if(!eD.getText().toString().isEmpty()){ zikrMan.tasbihList.add(new ZikrManager.TasbihData(eD.getText().toString(),Integer.parseInt(eT.getText().toString().isEmpty()?"0":eT.getText().toString()))); zikrMan.save(); invalidate(); d.dismiss(); } }).show(); }); r.addView(bA); d.setContentView(r); d.show(); }
        private void editT(int i, android.widget.TextView tv){ final android.widget.EditText et=new android.widget.EditText(getContext()); et.setInputType(2); et.setText(String.valueOf(zikrMan.tasbihList.get(i).target)); new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Target")).setView(et).setPositiveButton("OK",(di,wi)->{ if(!et.getText().toString().isEmpty()){ int n=Integer.parseInt(et.getText().toString()); zikrMan.tasbihList.get(i).target=n; tv.setText(String.valueOf(n)); zikrMan.prefs.edit().putInt("target_"+i,n).apply(); invalidate(); } }).show(); }
    }
"""
c = c[:start_idx] + new_canvas + c[end_idx:]

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Zikr Masterpiece RESTORED! Centered numbers, Smart Scaling, and Fixed Icons!")
