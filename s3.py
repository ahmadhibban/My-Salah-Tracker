f='app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
z2=r'''
    class ZikrCanvasView extends android.view.View {
        private float startX, beadOff = 0f; private boolean isSwiping = false; private android.graphics.Bitmap rBmp, sOn, sOff;
        private int[][] bCols = { {0xFFA5D6A7,0xFF2E7D32,0xFF1B5E20}, {0xFFFFE082,0xFFFF8F00,0xFFE65100}, {0xFFFFFFFF,0xFFE0E0E0,0xFF9E9E9E}, {0xFFBCAAA4,0xFF795548,0xFF4E342E}, {0xFFEF9A9A,0xFFC62828,0xFFB71C1C}, {0xFF9E9E9E,0xFF424242,0xFF212121} };
        public ZikrCanvasView(android.content.Context ctx) { super(ctx); if(zikrMan==null){zikrMan=new ZikrManager();zikrMan.init(ctx);} rBmp=ld("img_zikr_reset"); sOn=ld("img_zikr_sound_on"); sOff=ld("img_zikr_sound_off"); }
        private android.graphics.Bitmap ld(String n){ int id=getResources().getIdentifier(n,"drawable",getContext().getPackageName()); return id!=0?android.graphics.BitmapFactory.decodeResource(getResources(),id):null; }
        private String tB(int n) { String o=String.valueOf(n); String[] e={"0","1","2","3","4","5","6","7","8","9"}, b={"০","১","২","৩","৪","৫","৬","৭","৮","৯"}; for(int i=0;i<10;i++) o=o.replace(e[i],b[i]); return o; }
        private void dB(android.graphics.Canvas cv, float cx, float cy, float r, int t, android.graphics.Paint p) { p.setShader(new android.graphics.RadialGradient(cx-r/3, cy-r/3, r*1.2f, bCols[t], null, android.graphics.Shader.TileMode.CLAMP)); p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(10,0,5,0x44000000); cv.drawCircle(cx,cy,r,p); p.clearShadowLayer(); p.setShader(null); }
        @Override protected void onDraw(android.graphics.Canvas cv) {
            super.onDraw(cv); boolean iB = sp.getString("app_lang","en").equals("bn"); float w=getWidth(), cx=w/2f; android.graphics.Paint p=new android.graphics.Paint(1);
            int idx=zikrMan.currentIdx; ZikrManager.TasbihData d=zikrMan.tasbihList.get(idx); int cur=zikrMan.indCounts[idx];
            p.setColor(themeColors[2]); p.setTextSize(65f); p.setTypeface(appFonts[1]); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText("Round "+(iB?tB(zikrMan.indRounds[idx]):zikrMan.indRounds[idx]), cx, 120f, p);
            float cY=480f, rad=w*0.33f; float swp=d.target>0?((float)cur/d.target)*360f:0f;
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(40f); p.setStrokeCap(android.graphics.Paint.Cap.ROUND); p.setColor(themeColors[4]); cv.drawCircle(cx,cY,rad,p);
            p.setColor(colorAccent); cv.drawArc(new android.graphics.RectF(cx-rad,cY-rad,cx+rad,cY+rad),-90,swp,false,p);
            double rD=Math.toRadians(swp-90); float bX=(float)(cx+rad*Math.cos(rD)), bY=(float)(cY+rad*Math.sin(rD)); p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(30,0,0,colorAccent); p.setColor(colorAccent); cv.drawCircle(bX,bY,32f,p); p.clearShadowLayer(); p.setColor(android.graphics.Color.WHITE); cv.drawCircle(bX,bY,14f,p);
            p.setTypeface(appFonts[1]); p.setColor(themeColors[2]); p.setTextAlign(android.graphics.Paint.Align.LEFT);
            String mS=iB?tB(cur):String.valueOf(cur); String tS=d.target>0?(" / "+(iB?tB(d.target):d.target)):""; float mF=250f, tF=60f; p.setTextSize(mF); float mW=p.measureText(mS); android.graphics.Paint tP=new android.graphics.Paint(p); tP.setTextSize(tF); tP.setColor(themeColors[3]); tP.setTypeface(appFonts[0]); float tW=tP.measureText(tS);
            while(mW+tW>rad*1.7f){ mF-=5f; tF-=1.2f; p.setTextSize(mF); tP.setTextSize(tF); mW=p.measureText(mS); tW=tP.measureText(tS); }
            float sXT=cx-(mW+tW)/2f; cv.drawText(mS,sXT,cY+(mF/3.2f),p); cv.drawText(tS,sXT+mW,cY+(mF/3.2f),tP);
            float strY = cY+rad+140f, gap=165f, spc=85f, bR=38f; p.setColor(themeColors[3]); p.setStrokeWidth(4f); cv.drawLine(60f, strY, w-60f, strY, p);
            float acX=beadOff<0?cx+gap/2+beadOff:(beadOff>0?cx-gap/2+beadOff:0f);
            for(int i=0;i<4;i++){ if(!(beadOff>0&&i==0)) dB(cv,cx-gap/2-(i*spc),strY,bR,zikrMan.beadTheme,p); if(!(beadOff<0&&i==0)) dB(cv,cx+gap/2+(i*spc),strY,bR,zikrMan.beadTheme,p); }
            if(beadOff!=0) dB(cv,acX,strY,bR,zikrMan.beadTheme,p);
            float bT=strY+130f, bH=320f, bB=bT+bH; p.setColor(themeColors[1]); p.setShadowLayer(15,0,8,0x15000000); cv.drawRoundRect(new android.graphics.RectF(50,bT,w-50,bB), 45f, 45f, p); p.clearShadowLayer();
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(4f); p.setColor(colorAccent); cv.drawRoundRect(new android.graphics.RectF(50,bT,w-50,bB), 45f, 45f, p);
            p.setStyle(android.graphics.Paint.Style.FILL); android.text.TextPaint tp=new android.text.TextPaint(p); tp.setTypeface(getArabicFont()); tp.setColor(themeColors[2]);
            int layW=(int)(w-140); float fS=95f; android.text.StaticLayout sl;
            while(true){ tp.setTextSize(fS); sl=new android.text.StaticLayout(d.arabic,tp,layW,android.text.Layout.Alignment.ALIGN_CENTER,1.2f,0,false); if(sl.getLineCount()<=2){ if(sl.getLineCount()==2){ String l2=d.arabic.substring(sl.getLineStart(1),sl.getLineEnd(1)).trim(); if(!l2.contains(" ")&&fS>40f){fS-=2f;continue;} } break; } if(fS<=35f) break; fS-=2f; }
            cv.save(); cv.translate(cx-(layW/2f), bT+(bH-sl.getHeight())/2f); sl.draw(cv); cv.restore();
            float iY=bB+110f, mrg=130f; if(rBmp!=null) cv.drawBitmap(rBmp,null,new android.graphics.RectF(mrg-40,iY-40,mrg+40,iY+40),p); else{ p.setColor(themeColors[1]); cv.drawCircle(mrg,iY,55f,p); p.setColor(themeColors[3]); p.setTextSize(45f); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText("↺",mrg,iY+15f,p); }
            android.graphics.Bitmap sb=zikrMan.soundOn?sOn:sOff; p.setAlpha(zikrMan.soundOn?255:120); if(sb!=null) cv.drawBitmap(sb,null,new android.graphics.RectF(w-mrg-40,iY-40,w-mrg+40,iY+40),p); else{ p.setColor(themeColors[1]); cv.drawCircle(w-mrg,iY,55f,p); p.setColor(colorAccent); p.setTextSize(45f); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText(zikrMan.soundOn?"🔊":"🔇",w-mrg,iY+15f,p); } p.setAlpha(255);
            float thY=iY+160f; for(int i=0;i<6;i++){ float cxT=cx-250f+(i*100f); dB(cv,cxT,thY,35f,i,p); if(zikrMan.beadTheme==i){ p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(6f); p.setColor(colorAccent); cv.drawCircle(cxT,thY,48f,p); } }
        }
    //_TOUCH_
'''
open(f,'w').write(open(f).read().replace('//_UI_', z2))
print("✅ Step 3: UI Engine Injected!")
