f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(f, 'r', encoding='utf-8').read()

canvas = r'''class ZikrCanvasView extends android.view.View {
        private float startX, startY, beadOffset = 0f; private boolean isSwiping = false; private android.graphics.Bitmap rBmp, sOn, sOff;
        private int[][] beadColors = { {0xFFA5D6A7, 0xFF2E7D32, 0xFF1B5E20}, {0xFFFFE082, 0xFFFF8F00, 0xFFE65100}, {0xFFFFFFFF, 0xFFE0E0E0, 0xFF9E9E9E}, {0xFFBCAAA4, 0xFF795548, 0xFF4E342E}, {0xFFEF9A9A, 0xFFC62828, 0xFFB71C1C}, {0xFF9E9E9E, 0xFF424242, 0xFF212121} };
        public ZikrCanvasView(android.content.Context ctx) { super(ctx); if(zikrMan==null){zikrMan=new ZikrManager();zikrMan.init(ctx);} try{ rBmp=load("img_zikr_reset"); sOn=load("img_zikr_sound_on"); sOff=load("img_zikr_sound_off"); }catch(Exception e){} }
        private android.graphics.Bitmap load(String n){ int id=getResources().getIdentifier(n,"drawable",getContext().getPackageName()); return id!=0?android.graphics.BitmapFactory.decodeResource(getResources(),id):null; }
        private String toBn(int n) { String o=String.valueOf(n); String[] e={"0","1","2","3","4","5","6","7","8","9"}, b={"০","১","২","৩","৪","৫","৬","৭","৮","৯"}; for(int i=0;i<10;i++) o=o.replace(e[i],b[i]); return o; }
        private void drawBead(android.graphics.Canvas cv, float cx, float cy, float rad, int t, android.graphics.Paint p) { android.graphics.RadialGradient rg = new android.graphics.RadialGradient(cx-rad/3, cy-rad/3, rad*1.2f, beadColors[t], null, android.graphics.Shader.TileMode.CLAMP); p.setShader(rg); p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(10,0,5,0x44000000); cv.drawCircle(cx, cy, rad, p); p.clearShadowLayer(); p.setShader(null); }
        
        @Override protected void onDraw(android.graphics.Canvas cv) {
            super.onDraw(cv); boolean isBn = sp.getString("app_lang","en").equals("bn"); float w=getWidth(), cx=w/2f;
            android.graphics.Paint p=new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            int idx=zikrMan.currentIdx; ZikrManager.TasbihData d=zikrMan.tasbihList.get(idx); int cur=zikrMan.indCounts[idx];
            
            float topY=100f; p.setColor(themeColors[2]); p.setTextSize(65f); p.setTypeface(appFonts[1]); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText("Round "+(isBn?toBn(zikrMan.indRounds[idx]):zikrMan.indRounds[idx]), cx, topY+20f, p);
            
            float cY=topY+380f, rad=w*0.33f; float sweep=d.target>0?((float)cur/d.target)*360f:0f;
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(40f); p.setStrokeCap(android.graphics.Paint.Cap.ROUND); p.setColor(themeColors[4]); cv.drawCircle(cx,cY,rad,p); p.setColor(colorAccent); cv.drawArc(new android.graphics.RectF(cx-rad,cY-rad,cx+rad,cY+rad),-90,sweep,false,p);
            double rD=Math.toRadians(sweep-90); float bX=(float)(cx+rad*Math.cos(rD)), bY=(float)(cY+rad*Math.sin(rD)); p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(35,0,0,colorAccent); p.setColor(colorAccent); cv.drawCircle(bX,bY,32f,p); p.clearShadowLayer(); p.setColor(android.graphics.Color.WHITE); cv.drawCircle(bX,bY,12f,p);
            
            p.setTypeface(appFonts[1]); p.setColor(themeColors[2]); p.setTextAlign(android.graphics.Paint.Align.LEFT);
            String mS=isBn?toBn(cur):String.valueOf(cur); String tS=d.target>0?(" / "+(isBn?toBn(d.target):d.target)):"";
            float mF=250f, tF=60f; p.setTextSize(mF); float mW=p.measureText(mS); android.graphics.Paint tP=new android.graphics.Paint(p); tP.setTextSize(tF); tP.setColor(themeColors[3]); tP.setTypeface(appFonts[0]); float tW=tP.measureText(tS);
            while(mW+tW>rad*1.7f){ mF-=5f; tF-=1.2f; p.setTextSize(mF); tP.setTextSize(tF); mW=p.measureText(mS); tW=tP.measureText(tS); }
            float sXT=cx-(mW+tW)/2f; cv.drawText(mS,sXT,cY+(mF/3.2f),p); cv.drawText(tS,sXT+mW,cY+(mF/3.2f),tP);
            
            float strY=cY+rad+100f; p.setColor(themeColors[3]); p.setStrokeWidth(3f); cv.drawLine(50f,strY,w-50f,strY,p);
            float gap=160f, spc=85f, beadR=38f; float aX=beadOffset<0?cx+gap/2+beadOffset:(beadOffset>0?cx-gap/2+beadOffset:0f);
            for(int i=0;i<4;i++){ if(!(beadOffset>0&&i==0)) drawBead(cv,cx-gap/2-(i*spc),strY,beadR,zikrMan.beadTheme,p); if(!(beadOffset<0&&i==0)) drawBead(cv,cx+gap/2+(i*spc),strY,beadR,zikrMan.beadTheme,p); }
            if(beadOffset!=0) drawBead(cv,aX,strY,beadR,zikrMan.beadTheme,p);
            
            float boxT=strY+100f, boxH=320f, boxB=boxT+boxH; p.setColor(themeColors[1]); p.setShadowLayer(15,0,8,0x15000000); cv.drawRoundRect(new android.graphics.RectF(50,boxT,w-50,boxB), 40f, 40f, p); p.clearShadowLayer();
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(4f); p.setColor(colorAccent); cv.drawRoundRect(new android.graphics.RectF(50,boxT,w-50,boxB), 40f, 40f, p);
            
            p.setStyle(android.graphics.Paint.Style.FILL); android.text.TextPaint tp=new android.text.TextPaint(p); tp.setTypeface(getArabicFont()); tp.setColor(themeColors[2]);
            int layW=(int)(w-140); float fS=95f; android.text.StaticLayout sl;
            while(true){ tp.setTextSize(fS); sl=new android.text.StaticLayout(d.arabic,tp,layW,android.text.Layout.Alignment.ALIGN_CENTER,1.2f,0,false);
                if(sl.getLineCount()<=2){ if(sl.getLineCount()==2){ String l2=d.arabic.substring(sl.getLineStart(1),sl.getLineEnd(1)).trim(); if(!l2.contains(" ")&&fS>40f){fS-=2f;continue;} } break; }
                if(fS<=35f) break; fS-=2f; }
            cv.save(); cv.translate(cx-(layW/2f), boxT+(boxH-sl.getHeight())/2f); sl.draw(cv); cv.restore();
            
            float iY=boxB+110f; float mrg=130f; if(rBmp!=null) cv.drawBitmap(rBmp,null,new android.graphics.RectF(mrg-40,iY-40,mrg+40,iY+40),p); else{ p.setColor(themeColors[1]); cv.drawCircle(mrg,iY,55f,p); p.setColor(themeColors[3]); p.setTextSize(45f); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText("↺",mrg,iY+15f,p); }
            android.graphics.Bitmap sB=zikrMan.soundOn?sOn:sOff; p.setAlpha(zikrMan.soundOn?255:120); if(sB!=null) cv.drawBitmap(sB,null,new android.graphics.RectF(w-mrg-40,iY-40,w-mrg+40,iY+40),p); else{ p.setColor(themeColors[1]); cv.drawCircle(w-mrg,iY,55f,p); p.setColor(colorAccent); p.setTextSize(45f); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText(zikrMan.soundOn?"🔊":"🔇",w-mrg,iY+15f,p); } p.setAlpha(255);
            
            float thY=iY+160f; for(int i=0;i<6;i++){ float cxT=cx-250f+(i*100f); drawBead(cv,cxT,thY,35f,i,p); if(zikrMan.beadTheme==i){ p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(6f); p.setColor(colorAccent); cv.drawCircle(cxT,thY,48f,p); } }
        }
        
        private void count(boolean add) { int i=zikrMan.currentIdx; ZikrManager.TasbihData d=zikrMan.tasbihList.get(i); if(add){ zikrMan.indCounts[i]++; if(zikrMan.soundOn&&zikrMan.toneGen!=null) zikrMan.toneGen.startTone(24,50); if(d.target>0&&zikrMan.indCounts[i]>=d.target){zikrMan.indCounts[i]=0; zikrMan.indRounds[i]++; performHapticFeedback(0);} } else { if(zikrMan.indCounts[i]>0){zikrMan.indCounts[i]--;} } zikrMan.save(); }
        private void anim(float t, boolean a) { android.animation.ValueAnimator v=android.animation.ValueAnimator.ofFloat(beadOffset,t); v.setDuration(120); v.addUpdateListener(an->{beadOffset=(float)an.getAnimatedValue();invalidate();}); v.addListener(new android.animation.AnimatorListenerAdapter(){public void onAnimationEnd(android.animation.Animator an){if(t!=0f)count(a); beadOffset=0f;invalidate();}}); v.start(); }
        
        @Override public boolean onTouchEvent(android.view.MotionEvent ev) {
            float x=ev.getX(), y=ev.getY(), w=getWidth(), cx=w/2f; float topY=100f, cY=topY+380f, rad=w*0.33f, strY=cY+rad+100f, boxT=strY+100f, boxB=boxT+320f, iY=boxB+110f, thY=iY+160f; int i=zikrMan.currentIdx;
            if(ev.getAction()==0){startX=x;startY=y;isSwiping=false;return true;}
            if(ev.getAction()==2){float dx=x-startX; if(Math.abs(dx)>20){isSwiping=true; beadOffset=dx; if(beadOffset>160f)beadOffset=160f; if(beadOffset<-160f)beadOffset=-160f; invalidate();}}
            if(ev.getAction()==1){
                float dx=x-startX; if(isSwiping){ if(dx<-60){performHapticFeedback(1);anim(-160f,true);} else if(dx>60){performHapticFeedback(1);anim(160f,false);} else anim(0f,false); }
                else {
                    if(Math.abs(y-iY)<80){ if(x<200){performHapticFeedback(1); new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Reset")).setMessage(lang.get("Do you want to reset counts for this Dua?")).setPositiveButton("Yes",(di,wi)->{zikrMan.indCounts[i]=0;zikrMan.indRounds[i]=0;zikrMan.save();invalidate();}).setNegativeButton("No",null).show();} else if(x>w-200){performHapticFeedback(1);zikrMan.soundOn=!zikrMan.soundOn;zikrMan.save();invalidate();} }
                    else if(y>cY-80 && y<cY+80 && x>cx){performHapticFeedback(1); final android.widget.EditText et=new android.widget.EditText(getContext()); et.setInputType(2); et.setText(String.valueOf(zikrMan.tasbihList.get(i).target)); new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Target")).setView(et).setPositiveButton("OK",(di,wi)->{if(!et.getText().toString().isEmpty()){zikrMan.tasbihList.get(i).target=Integer.parseInt(et.getText().toString()); zikrMan.prefs.edit().putInt("target_"+i,zikrMan.tasbihList.get(i).target).apply(); invalidate();}}).show();}
                    else if(y>boxT && y<boxB && x>40 && x<w-40){performHapticFeedback(1); showList();}
                    else if(y>thY-60 && y<thY+60){ float sX=cx-250f; for(int j=0;j<6;j++){ if(Math.abs(x-(sX+(j*100f)))<50){performHapticFeedback(1);zikrMan.beadTheme=j;zikrMan.save();invalidate();break;} } }
                    else {performHapticFeedback(1);anim(-160f,true);}
                }
            } return true;
        }
        
        private void showList(){
            final android.app.Dialog d=new android.app.Dialog(getContext(),android.R.style.Theme_Black_NoTitleBar_Fullscreen); android.widget.LinearLayout r=new android.widget.LinearLayout(getContext()); r.setOrientation(1); r.setBackgroundColor(themeColors[0]); r.setPadding(40,80,40,40); android.widget.TextView t1=new android.widget.TextView(getContext()); t1.setText(lang.get("Zikr")); t1.setTextColor(colorAccent); t1.setTextSize(26); t1.setTypeface(appFonts[1]); t1.setGravity(1); r.addView(t1);
            android.widget.ScrollView sv=new android.widget.ScrollView(getContext()); android.widget.LinearLayout l=new android.widget.LinearLayout(getContext()); l.setOrientation(1);
            for(int j=0;j<zikrMan.tasbihList.size();j++){
                final int rI=j; ZikrManager.TasbihData dt=zikrMan.tasbihList.get(j); android.widget.LinearLayout row=new android.widget.LinearLayout(getContext()); row.setOrientation(1); row.setPadding(30,45,30,45); row.setGravity(17);
                android.widget.TextView tA=new android.widget.TextView(getContext()); tA.setText(dt.arabic); tA.setTextColor(themeColors[2]); tA.setTextSize(32); tA.setTypeface(getArabicFont()); tA.setGravity(17); tA.setOnClickListener(v->{zikrMan.currentIdx=rI;zikrMan.save();invalidate();d.dismiss();}); row.addView(tA);
                android.widget.TextView tP=new android.widget.TextView(getContext()); tP.setText(dt.pron); tP.setTextColor(themeColors[3]); tP.setTextSize(16); tP.setTypeface(appFonts[0]); tP.setGravity(17); tP.setPadding(0,15,0,5); row.addView(tP);
                android.widget.TextView tM=new android.widget.TextView(getContext()); tM.setText(dt.mean); tM.setTextColor(themeColors[3]); tM.setTextSize(14); tM.setTypeface(appFonts[0]); tM.setGravity(17); tM.setPadding(0,0,0,25); row.addView(tM);
                android.widget.TextView tT=new android.widget.TextView(getContext()); tT.setText("Target: "+dt.target); tT.setTextColor(colorAccent); tT.setTextSize(18); tT.setTypeface(appFonts[1]); tT.setGravity(17); android.graphics.drawable.GradientDrawable tb=new android.graphics.drawable.GradientDrawable(); tb.setColor(themeColors[1]); tb.setCornerRadius(15f); tT.setBackground(tb); tT.setPadding(40,15,40,15); tT.setOnClickListener(v->{ final android.widget.EditText et=new android.widget.EditText(getContext()); et.setInputType(2); et.setText(String.valueOf(zikrMan.tasbihList.get(rI).target)); new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Target")).setView(et).setPositiveButton("OK",(di,wi)->{if(!et.getText().toString().isEmpty()){zikrMan.tasbihList.get(rI).target=Integer.parseInt(et.getText().toString()); tT.setText("Target: "+et.getText().toString()); zikrMan.prefs.edit().putInt("target_"+rI, zikrMan.tasbihList.get(rI).target).apply(); invalidate();}}).show(); }); row.addView(tT);
                l.addView(row); android.view.View div=new android.view.View(getContext()); div.setBackgroundColor(themeColors[4]); div.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1,2)); l.addView(div);
            } sv.addView(l); r.addView(sv,new android.widget.LinearLayout.LayoutParams(-1,0,1f));
            android.widget.Button bA=new android.widget.Button(getContext()); bA.setText("+ Add New"); bA.setAllCaps(false); bA.setTextColor(colorAccent); bA.setTypeface(appFonts[1]); android.graphics.drawable.GradientDrawable btnBg=new android.graphics.drawable.GradientDrawable(); btnBg.setColor(android.graphics.Color.TRANSPARENT); btnBg.setStroke(4, colorAccent); btnBg.setCornerRadius(30f); bA.setBackground(btnBg); android.widget.LinearLayout.LayoutParams blp=new android.widget.LinearLayout.LayoutParams(-1,150); blp.setMargins(40,30,40,40); bA.setLayoutParams(blp);
            bA.setOnClickListener(v->{ android.widget.LinearLayout lay=new android.widget.LinearLayout(getContext()); lay.setOrientation(1); lay.setPadding(50,20,50,20); final android.widget.EditText eD=new android.widget.EditText(getContext()); eD.setHint("Arabic Dua"); final android.widget.EditText eP=new android.widget.EditText(getContext()); eP.setHint("উচ্চারণ"); final android.widget.EditText eM=new android.widget.EditText(getContext()); eM.setHint("অর্থ"); final android.widget.EditText eT=new android.widget.EditText(getContext()); eT.setHint("Target"); eT.setInputType(2); lay.addView(eD); lay.addView(eP); lay.addView(eM); lay.addView(eT); new android.app.AlertDialog.Builder(getContext()).setTitle("Add").setView(lay).setPositiveButton("OK",(di,wi)->{if(!eD.getText().toString().isEmpty()){zikrMan.tasbihList.add(new ZikrManager.TasbihData(eD.getText().toString(),Integer.parseInt(eT.getText().toString().isEmpty()?"0":eT.getText().toString()),eP.getText().toString(),eM.getText().toString())); zikrMan.save(); invalidate(); d.dismiss();}}).show(); }); r.addView(bA); d.setContentView(r); d.show();
        }
    }
    private void loadZikrTab() { contentArea.removeAllViews(); contentArea.addView(new ZikrCanvasView(this), new android.widget.LinearLayout.LayoutParams(-1,-1)); }
    private void loadStatsTab() {
        contentArea.removeAllViews(); contentArea.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY)); android.widget.TextView h = new android.widget.TextView(this); h.setText(lang.get("Stats")); h.setTextColor(themeColors[2]); h.setTextSize(24); h.setTypeface(appFonts[1]); h.setPadding(0,0,0,(int)(20*DENSITY)); contentArea.addView(h);
        try { java.lang.reflect.Method m = StatsHelper.class.getDeclaredMethod("renderStats", android.widget.LinearLayout.class, android.app.AlertDialog.class, boolean.class); m.setAccessible(true); android.widget.TextView wT = new android.widget.TextView(this); wT.setText(lang.get("Weekly Statistics")); wT.setTextColor(themeColors[3]); wT.setTypeface(appFonts[1]); contentArea.addView(wT); android.widget.LinearLayout wC = new android.widget.LinearLayout(this); wC.setOrientation(android.widget.LinearLayout.VERTICAL); wC.setPadding((int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY)); android.graphics.drawable.GradientDrawable wBg = new android.graphics.drawable.GradientDrawable(); wBg.setColor(themeColors[1]); wBg.setCornerRadius(25f*DENSITY); wC.setBackground(wBg); android.widget.LinearLayout.LayoutParams wLp = new android.widget.LinearLayout.LayoutParams(-1, -2); wLp.setMargins(0,(int)(10*DENSITY),0,(int)(20*DENSITY)); wC.setLayoutParams(wLp); m.invoke(statsHelper, wC, null, true); wC.removeViewAt(wC.getChildCount()-1); contentArea.addView(wC); android.widget.TextView mT = new android.widget.TextView(this); mT.setText(lang.get("Monthly Statistics")); mT.setTextColor(themeColors[3]); mT.setTypeface(appFonts[1]); contentArea.addView(mT); android.widget.LinearLayout mC = new android.widget.LinearLayout(this); mC.setOrientation(android.widget.LinearLayout.VERTICAL); mC.setPadding((int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY)); android.graphics.drawable.GradientDrawable mBg = new android.graphics.drawable.GradientDrawable(); mBg.setColor(themeColors[1]); mBg.setCornerRadius(25f*DENSITY); mC.setBackground(mBg); android.widget.LinearLayout.LayoutParams mLp = new android.widget.LinearLayout.LayoutParams(-1, -2); mLp.setMargins(0,(int)(10*DENSITY),0,(int)(20*DENSITY)); mC.setLayoutParams(mLp); m.invoke(statsHelper, mC, null, false); mC.removeViewAt(mC.getChildCount()-1); contentArea.addView(mC); } catch(Exception e){}
    }'''

c = c.replace('// CANVAS_PLACEHOLDER', canvas)
open(f, 'w', encoding='utf-8').write(c)
print("✅ Step 3: UI & Canvas Injected successfully! Build now.")
