f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(f, 'r', encoding='utf-8').read()

start_idx = c.find("class ZikrCanvasView")
end_idx = c.find("private void loadZikrTab()")

if start_idx != -1 and end_idx != -1:
    new_canvas = r'''class ZikrCanvasView extends android.view.View {
        private float startX, startY, beadOffset = 0f; private boolean isSwiping = false; private long startTime;
        private android.graphics.Bitmap resetBmp, sOnBmp, sOffBmp;
        
        // Premium 3D Bead Themes: Emerald, Amber, Pearl, Wood, Ruby, Onyx
        private int[][] beadColors = {
            {0xFFA5D6A7, 0xFF2E7D32, 0xFF1B5E20}, {0xFFFFE082, 0xFFFF8F00, 0xFFE65100},
            {0xFFFFFFFF, 0xFFE0E0E0, 0xFF9E9E9E}, {0xFFBCAAA4, 0xFF795548, 0xFF4E342E},
            {0xFFEF9A9A, 0xFFC62828, 0xFFB71C1C}, {0xFF9E9E9E, 0xFF424242, 0xFF212121}
        };

        public ZikrCanvasView(android.content.Context context) {
            super(context); if(zikrMan == null) { zikrMan = new ZikrManager(); zikrMan.init(context); }
            try { resetBmp=loadBmp("img_zikr_reset"); sOnBmp=loadBmp("img_zikr_sound_on"); sOffBmp=loadBmp("img_zikr_sound_off"); } catch(Exception e){}
        }
        private android.graphics.Bitmap loadBmp(String n){ int id=getResources().getIdentifier(n,"drawable",getContext().getPackageName()); return id!=0?android.graphics.BitmapFactory.decodeResource(getResources(),id):null; }
        private String toBn(int n) { String o=String.valueOf(n); String[] e={"0","1","2","3","4","5","6","7","8","9"}, b={"০","১","২","৩","৪","৫","৬","৭","৮","৯"}; for(int i=0;i<10;i++) o=o.replace(e[i],b[i]); return o; }

        @Override protected void onDraw(android.graphics.Canvas cv) {
            super.onDraw(cv); boolean isBn = sp.getString("app_lang","en").equals("bn"); float w=getWidth(), centerX=w/2f;
            android.graphics.Paint p = new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            int idx=zikrMan.currentIdx; ZikrManager.TasbihData d=zikrMan.tasbihList.get(idx); int cur=zikrMan.indCounts[idx];

            // 1. Top Icons & Round Counter
            float topY = 120f, margin = 120f;
            if(resetBmp!=null) cv.drawBitmap(resetBmp, null, new android.graphics.RectF(margin-45, topY-45, margin+45, topY+45), p);
            else { p.setColor(themeColors[1]); cv.drawCircle(margin, topY, 65f, p); p.setColor(themeColors[3]); p.setTextSize(50f); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText("↺", margin, topY+18f, p); }
            
            android.graphics.Bitmap sB = zikrMan.soundOn ? sOnBmp : sOffBmp; p.setAlpha(zikrMan.soundOn?255:120);
            if(sB!=null) cv.drawBitmap(sB, null, new android.graphics.RectF(w-margin-45, topY-45, w-margin+45, topY+45), p);
            else { p.setColor(themeColors[1]); cv.drawCircle(w-margin, topY, 65f, p); p.setColor(colorAccent); p.setTextSize(50f); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText(zikrMan.soundOn?"🔊":"🔇", w-margin, topY+18f, p); } p.setAlpha(255);

            p.setColor(themeColors[2]); p.setTextSize(65f); p.setTypeface(appFonts[1]); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            cv.drawText(lang.get("Round") + " " + (isBn?toBn(zikrMan.indRounds[idx]):zikrMan.indRounds[idx]), centerX, topY+20f, p);

            // 2. Main Circle & Numbers
            float circleY = topY + 480f, rad = w*0.42f; float sweep = d.target>0 ? ((float)cur/d.target)*360f : 0f;
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(50f); p.setStrokeCap(android.graphics.Paint.Cap.ROUND);
            p.setColor(themeColors[4]); cv.drawCircle(centerX, circleY, rad, p);
            p.setColor(colorAccent); cv.drawArc(new android.graphics.RectF(centerX-rad, circleY-rad, centerX+rad, circleY+rad), -90, sweep, false, p);
            double rD = Math.toRadians(sweep-90); float ballX=(float)(centerX+rad*Math.cos(rD)), ballY=(float)(circleY+rad*Math.sin(rD));
            p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(45,0,0,colorAccent); p.setColor(colorAccent); cv.drawCircle(ballX, ballY, 36f, p); p.clearShadowLayer(); p.setColor(android.graphics.Color.WHITE); cv.drawCircle(ballX, ballY, 15f, p);

            // Perfect Number Centering (Shifted up slightly to make room for beads)
            float numY = circleY - 40f; p.setTypeface(appFonts[1]); p.setColor(themeColors[2]); p.setTextAlign(android.graphics.Paint.Align.LEFT);
            String mS = isBn?toBn(cur):String.valueOf(cur); String tS = d.target>0 ? (" / "+(isBn?toBn(d.target):d.target)) : "";
            float mF=300f, tF=70f; p.setTextSize(mF); float mW=p.measureText(mS);
            android.graphics.Paint tP = new android.graphics.Paint(p); tP.setTextSize(tF); tP.setColor(themeColors[3]); tP.setTypeface(appFonts[0]); float tW=tP.measureText(tS);
            while(mW+tW > rad*1.8f) { mF-=5f; tF-=1.2f; p.setTextSize(mF); tP.setTextSize(tF); mW=p.measureText(mS); tW=tP.measureText(tS); }
            float startXT = centerX - (mW+tW)/2f; cv.drawText(mS, startXT, numY + (mF/3.2f), p); cv.drawText(tS, startXT+mW, numY + (mF/3.2f), tP);

            // 3. The Premium 3D Bead String (Passing horizontally)
            float stringY = circleY + 200f; p.setColor(themeColors[3]); p.setStrokeWidth(4f); cv.drawLine(centerX-rad, stringY, centerX+rad, stringY, p); // The Thread
            float bRad = 65f, spacing = 145f;
            for(int i=-4; i<=4; i++) {
                float cx = centerX + (i*spacing) + beadOffset;
                if(cx < centerX-rad+20 || cx > centerX+rad-20) continue; // Clip inside circle
                android.graphics.RadialGradient rg = new android.graphics.RadialGradient(cx-20f, stringY-20f, bRad*1.2f, beadColors[zikrMan.beadTheme], null, android.graphics.Shader.TileMode.CLAMP);
                p.setShader(rg); p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(15, 0, 10, android.graphics.Color.parseColor("#44000000"));
                cv.drawCircle(cx, stringY, bRad, p); p.clearShadowLayer(); p.setShader(null);
            }

            p.setColor(themeColors[3]); p.setTextSize(32f); p.setTypeface(appFonts[0]); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            cv.drawText("Swipe right to left to count", centerX, circleY + rad + 80f, p);

            // 4. Premium Dua Box (Exact logic requested)
            float boxTop = circleY + rad + 140f, boxH = 380f, boxB = boxTop + boxH;
            p.setColor(themeColors[1]); p.setShadowLayer(20,0,10,android.graphics.Color.parseColor("#15000000")); cv.drawRoundRect(new android.graphics.RectF(50,boxTop,w-50,boxB), 45f, 45f, p); p.clearShadowLayer();
            android.text.TextPaint tp = new android.text.TextPaint(p); tp.setTypeface(getArabicFont()); tp.setColor(themeColors[2]);
            int layW=(int)(w-140); float fSize=100f; android.text.StaticLayout sl;
            while(true) {
                tp.setTextSize(fSize); sl = new android.text.StaticLayout(d.arabic, tp, layW, android.text.Layout.Alignment.ALIGN_CENTER, 1.2f, 0, false);
                if(sl.getLineCount() <= 2) {
                    if(sl.getLineCount() == 2) { String l2 = d.arabic.substring(sl.getLineStart(1), sl.getLineEnd(1)).trim(); if(!l2.contains(" ") && fSize > 40f) { fSize -= 2f; continue; } } break;
                }
                if(fSize <= 35f) break; fSize -= 2f;
            }
            cv.save(); cv.translate(centerX-(layW/2f), boxTop+(boxH-sl.getHeight())/2f); sl.draw(cv); cv.restore();
            
            p.setColor(colorAccent); p.setTextSize(36f); p.setTypeface(appFonts[1]); cv.drawText(lang.get("Total")+": "+(isBn?toBn(zikrMan.indTotals[idx]):zikrMan.indTotals[idx]), centerX, boxB+80f, p);

            // 5. Bead Theme Selectors
            float thX = centerX - 250f, thY = boxB + 200f;
            for(int i=0; i<6; i++) {
                float cx = thX + (i*100f);
                android.graphics.RadialGradient trg = new android.graphics.RadialGradient(cx-12, thY-12, 45f, beadColors[i], null, android.graphics.Shader.TileMode.CLAMP);
                p.setShader(trg); p.setStyle(android.graphics.Paint.Style.FILL); cv.drawCircle(cx, thY, 35f, p); p.setShader(null);
                if(zikrMan.beadTheme == i) { p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(6f); p.setColor(colorAccent); cv.drawCircle(cx, thY, 48f, p); }
            }
        }

        private void animateBeads(float targetOffset) {
            android.animation.ValueAnimator a = android.animation.ValueAnimator.ofFloat(beadOffset, targetOffset); a.setDuration(150);
            a.addUpdateListener(an -> { beadOffset = (float)an.getAnimatedValue(); invalidate(); });
            a.addListener(new android.animation.AnimatorListenerAdapter() { @Override public void onAnimationEnd(android.animation.Animator an) { beadOffset = 0f; invalidate(); } }); a.start();
        }
        private void triggerCount(boolean isAdd) {
            performHapticFeedback(1); int idx=zikrMan.currentIdx; ZikrManager.TasbihData d=zikrMan.tasbihList.get(idx);
            if(isAdd) { zikrMan.indCounts[idx]++; zikrMan.indTotals[idx]++; if(zikrMan.soundOn && zikrMan.toneGen!=null) zikrMan.toneGen.startTone(android.media.ToneGenerator.TONE_PROP_BEEP, 50); if(d.target>0 && zikrMan.indCounts[idx]>=d.target){ zikrMan.indCounts[idx]=0; zikrMan.indRounds[idx]++; performHapticFeedback(0); } } 
            else { if(zikrMan.indCounts[idx]>0){ zikrMan.indCounts[idx]--; zikrMan.indTotals[idx]--; } }
            zikrMan.save(); animateBeads(isAdd ? -145f : 145f);
        }

        @Override public boolean onTouchEvent(android.view.MotionEvent ev) {
            float x=ev.getX(), y=ev.getY(), w=getWidth(), centerX=w/2f;
            float topY=120f, circleY=topY+480f, rad=w*0.42f; float boxT=circleY+rad+140f, boxB=boxT+380f, thY=boxB+200f;
            int idx=zikrMan.currentIdx;

            if(ev.getAction()==android.view.MotionEvent.ACTION_DOWN) { startX=x; startY=y; startTime=System.currentTimeMillis(); isSwiping=false; return true; }
            if(ev.getAction()==android.view.MotionEvent.ACTION_MOVE) { float dx=x-startX; if(Math.abs(dx)>30) { isSwiping=true; beadOffset=dx; if(beadOffset>160f) beadOffset=160f; if(beadOffset<-160f) beadOffset=-160f; invalidate(); } }
            if(ev.getAction()==android.view.MotionEvent.ACTION_UP) {
                float dx=x-startX; long dt=System.currentTimeMillis()-startTime;
                if(isSwiping) { if(dx < -60) triggerCount(true); else if(dx > 60) triggerCount(false); else animateBeads(0f); }
                else if(dt < 300) {
                    if(y < 250) { if(x < 250) { performHapticFeedback(1); new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Reset")).setMessage(lang.get("Do you want to reset counts for this Dua?")).setPositiveButton(lang.get("Yes"), (di,wi)->{ zikrMan.indCounts[idx]=0; zikrMan.indTotals[idx]=0; zikrMan.indRounds[idx]=0; zikrMan.save(); invalidate(); }).setNegativeButton(lang.get("No"),null).show(); } else if(x > w-250) { performHapticFeedback(1); zikrMan.soundOn=!zikrMan.soundOn; zikrMan.save(); invalidate(); } }
                    else if(y > circleY-120 && y < circleY && x > centerX) { performHapticFeedback(1); final android.widget.EditText et=new android.widget.EditText(getContext()); et.setInputType(2); et.setText(String.valueOf(zikrMan.tasbihList.get(idx).target)); new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Target")).setView(et).setPositiveButton("OK",(di,wi)->{ if(!et.getText().toString().isEmpty()){ zikrMan.tasbihList.get(idx).target=Integer.parseInt(et.getText().toString()); zikrMan.prefs.edit().putInt("target_"+idx, zikrMan.tasbihList.get(idx).target).apply(); invalidate(); } }).show(); }
                    else if(y > boxT && y < boxB && x > 40 && x < w-40) { performHapticFeedback(1); showZList(); }
                    else if(y > thY-80 && y < thY+80) { float sX=centerX-250f; for(int i=0;i<6;i++){ if(Math.abs(x-(sX+(i*100f)))<50){ performHapticFeedback(1); zikrMan.beadTheme=i; zikrMan.save(); invalidate(); break; } } }
                    else { triggerCount(true); } // Tap anywhere else to count
                }
            } return true;
        }

        private void showZList(){ final android.app.Dialog d=new android.app.Dialog(getContext(),android.R.style.Theme_Black_NoTitleBar_Fullscreen); android.widget.LinearLayout r=new android.widget.LinearLayout(getContext()); r.setOrientation(1); r.setBackgroundColor(themeColors[0]); r.setPadding(40,80,40,40); android.widget.TextView t1=new android.widget.TextView(getContext()); t1.setText(lang.get("Zikr")); t1.setTextColor(colorAccent); t1.setTextSize(26); t1.setTypeface(appFonts[1]); t1.setGravity(1); r.addView(t1); android.widget.ScrollView sv=new android.widget.ScrollView(getContext()); android.widget.LinearLayout l=new android.widget.LinearLayout(getContext()); l.setOrientation(1); for(int i=0;i<zikrMan.tasbihList.size();i++){ final int rI=i; android.widget.LinearLayout row=new android.widget.LinearLayout(getContext()); row.setPadding(20,35,20,35); row.setGravity(16); android.widget.TextView tvD=new android.widget.TextView(getContext()); tvD.setText(zikrMan.tasbihList.get(rI).arabic); tvD.setTextColor(themeColors[2]); tvD.setTextSize(26); tvD.setTypeface(getArabicFont()); tvD.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,-2,7.5f)); tvD.setOnClickListener(v->{ zikrMan.currentIdx=rI; zikrMan.save(); invalidate(); d.dismiss(); }); android.widget.TextView tvT=new android.widget.TextView(getContext()); tvT.setText(String.valueOf(zikrMan.tasbihList.get(rI).target)); tvT.setTextColor(colorAccent); tvT.setTextSize(22); tvT.setTypeface(appFonts[0]); tvT.setGravity(1); tvT.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,-2,2.5f)); tvT.setOnClickListener(v->{ final android.widget.EditText et=new android.widget.EditText(getContext()); et.setInputType(2); et.setText(String.valueOf(zikrMan.tasbihList.get(rI).target)); new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Target")).setView(et).setPositiveButton("OK",(di,wi)->{ if(!et.getText().toString().isEmpty()){ zikrMan.tasbihList.get(rI).target=Integer.parseInt(et.getText().toString()); tvT.setText(et.getText().toString()); zikrMan.prefs.edit().putInt("target_"+rI, zikrMan.tasbihList.get(rI).target).apply(); invalidate(); } }).show(); }); row.addView(tvD); row.addView(tvT); l.addView(row); } sv.addView(l); r.addView(sv,new android.widget.LinearLayout.LayoutParams(-1,0,1f)); android.widget.Button bA=new android.widget.Button(getContext()); bA.setText("+ Add New"); bA.setAllCaps(false); bA.setBackgroundColor(themeColors[1]); bA.setTextColor(themeColors[2]); bA.setOnClickListener(v->{ android.widget.LinearLayout lay=new android.widget.LinearLayout(getContext()); lay.setOrientation(1); lay.setPadding(50,20,50,20); final android.widget.EditText eD=new android.widget.EditText(getContext()); eD.setHint("Arabic Dua"); final android.widget.EditText eT=new android.widget.EditText(getContext()); eT.setHint("Target"); eT.setInputType(2); lay.addView(eD); lay.addView(eT); new android.app.AlertDialog.Builder(getContext()).setTitle("Add").setView(lay).setPositiveButton("OK",(di,wi)->{ if(!eD.getText().toString().isEmpty()){ zikrMan.tasbihList.add(new ZikrManager.TasbihData(eD.getText().toString(),Integer.parseInt(eT.getText().toString().isEmpty()?"0":eT.getText().toString()))); zikrMan.save(); invalidate(); d.dismiss(); } }).show(); }); r.addView(bA); d.setContentView(r); d.show(); }
    }
'''
    c = c[:start_idx] + new_canvas + c[end_idx:]
    open(f, 'w', encoding='utf-8').write(c)
    print("✅ 3D PHYSICS ENGINE & BEADS INJECTED SUCCESSFULLY!")
