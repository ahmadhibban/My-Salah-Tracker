import re
f = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
c = open(f).read()
m = re.search(r'public\s+void\s+exportPdf\s*\([^)]*\)\s*\{', c)
if m:
    s=m.start(); b=0; e=-1; im=False
    for i in range(s, len(c)):
        if c[i]=='{': b+=1; im=True
        elif c[i]=='}':
            b-=1
            if im and b==0: e=i+1; break
    if e!=-1:
        np = """public void exportPdf() {
        boolean isBn=sp.getString("app_lang","en").equals("bn");
        try{
            int pw=650, ph=1950; android.graphics.pdf.PdfDocument doc=new android.graphics.pdf.PdfDocument();
            android.graphics.pdf.PdfDocument.PageInfo pi=new android.graphics.pdf.PdfDocument.PageInfo.Builder(pw,ph,1).create();
            android.graphics.pdf.PdfDocument.Page pg=doc.startPage(pi); android.graphics.Canvas cv=pg.getCanvas(); android.graphics.Paint pt=new android.graphics.Paint(1);
            pt.setColor(android.graphics.Color.WHITE); cv.drawRect(0,0,pw,ph,pt); pt.setColor(colorAccent); android.graphics.Path hp=new android.graphics.Path(); hp.moveTo(0,0); hp.lineTo(pw,0); hp.lineTo(pw,180); hp.cubicTo(pw/2f,220,0,180,0,180); hp.close(); cv.drawPath(hp,pt);
            pt.setColor(android.graphics.Color.WHITE); pt.setTextSize(38); pt.setTypeface(android.graphics.Typeface.create(appFonts[1],1)); pt.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText("My Salah Tracker",pw/2f,75,pt);
            String mNm=new java.text.SimpleDateFormat("MMMM yyyy",java.util.Locale.US).format(statsCalPointer.getTime());
            if(isBn) mNm=lang.get(new java.text.SimpleDateFormat("MMMM",java.util.Locale.US).format(statsCalPointer.getTime()))+" "+lang.bnNum(statsCalPointer.get(java.util.Calendar.YEAR));
            pt.setTextSize(18); pt.setTypeface(appFonts[0]); pt.setAlpha(220); cv.drawText((isBn?"মাসিক রিপোর্ট • ":"Monthly Report • ")+mNm,pw/2f,115,pt); pt.setAlpha(255);
            java.util.Calendar cal=(java.util.Calendar)statsCalPointer.clone(); cal.set(5,1);
            int tD=cal.getActualMaximum(5); int dP=0, tDn=0, tM=0, tE=0, tQ=0; java.util.Calendar now=java.util.Calendar.getInstance(); java.text.SimpleDateFormat sdf=new java.text.SimpleDateFormat("yyyy-MM-dd",java.util.Locale.US);
            for(int i=1;i<=tD;i++){
                cal.set(5,i); String dK=sdf.format(cal.getTime()); if(cal.after(now) && !dK.equals(sdf.format(now.getTime()))) continue;
                dP++; SalahRecord r=getRoomRecord(dK);
                if(r!=null){for(String p:prayers){String st=getFardStat(r,p); boolean isQ=getQazaStat(r,p); if(st.equals("yes")) tDn++; else if(st.equals("excused")) tE++; else{if(isQ) tQ++; else tM++;}}}
            }
            float sY=200, pd=30, cW=(pw-(pd*4))/3f, cH=75;
            drawPdfCardBig(cv,pt,pd,sY,cW,cH,colorAccent,isBn?"মোট দিন":"Total Days",lang.bnNum(dP)); drawPdfCardBig(cv,pt,pd*2+cW,sY,cW,cH,android.graphics.Color.parseColor("#3B82F6"),isBn?"আদায়কৃত":"Prayers Done",lang.bnNum(tDn)); drawPdfCardBig(cv,pt,pd*3+cW*2,sY,cW,cH,android.graphics.Color.parseColor("#FF5252"),isBn?"কাজা হয়েছে":"Missed",lang.bnNum(tM));
            drawPdfCardBig(cv,pt,pd,sY+cH+20,cW,cH,android.graphics.Color.parseColor("#FF9500"),isBn?"অপেক্ষমান কাজা":"Pending Qaza",lang.bnNum(tQ)); drawPdfCardBig(cv,pt,pd*2+cW,sY+cH+20,cW,cH,android.graphics.Color.parseColor("#FF4081"),isBn?"পিরিয়ড/ছুটি":"Excused Mode",lang.bnNum(tE)); drawPdfCardBig(cv,pt,pd*3+cW*2,sY+cH+20,cW,cH,android.graphics.Color.parseColor("#9B59B6"),isBn?"বর্তমান স্ট্রিক":"Current Streak",lang.bnNum(ui.calculateStreak(sp,prayers)));
            float cSY=sY+(cH*2)+70; pt.setColor(android.graphics.Color.parseColor("#333333")); pt.setTextSize(22); pt.setTypeface(android.graphics.Typeface.create(appFonts[1],1)); pt.setTextAlign(android.graphics.Paint.Align.LEFT); cv.drawText(isBn?"মাসিক ক্যালেন্ডার ওভারভিউ":"Monthly Calendar Overview",pd,cSY,pt);
            String[] ds={"Sun","Mon","Tue","Wed","Thu","Fri","Sat"}; if(isBn) ds=new String[]{"রবি","সোম","মঙ্গল","বুধ","বৃহঃ","শুক্র","শনি"};
            float clW=460, clCol=clW/7f, clX=(pw-clW)/2f, rH=50; pt.setTextSize(14); pt.setTypeface(appFonts[0]); pt.setColor(android.graphics.Color.parseColor("#888888")); pt.setTextAlign(android.graphics.Paint.Align.CENTER);
            for(int i=0;i<7;i++) cv.drawText(ds[i],clX+(i*clCol)+(clCol/2f),cSY+45,pt);
            cal.set(5,1); int off=cal.get(7)-1; float gY=cSY+75;
            for(int i=1;i<=tD;i++){
                int r=(off+i-1)/7, c=(off+i-1)%7; float cx=clX+(c*clCol)+(clCol/2f), cy=gY+(r*rH); cal.set(5,i); String dK=sdf.format(cal.getTime()); SalahRecord rec=getRoomRecord(dK); int cArc=0; boolean hEx=false;
                if(rec!=null){for(String p:prayers){String st=getFardStat(rec,p); if(st.equals("yes")) cArc++; else if(st.equals("excused")){cArc++; hEx=true;}}}
                pt.setStyle(android.graphics.Paint.Style.STROKE); pt.setStrokeWidth(2f); pt.setColor(android.graphics.Color.parseColor("#F1F5F9")); cv.drawCircle(cx,cy,18f,pt);
                if(cArc>0 && !(cal.after(now)&&!dK.equals(sdf.format(now.getTime())))){ pt.setColor(cArc==6?android.graphics.Color.parseColor("#22C55E"):(hEx?android.graphics.Color.parseColor("#8B5CF6"):android.graphics.Color.parseColor("#10B981"))); cv.drawArc(new android.graphics.RectF(cx-18f,cy-18f,cx+18f,cy+18f),-90,360f*(cArc/6f),false,pt); }
                pt.setStyle(android.graphics.Paint.Style.FILL); pt.setColor(android.graphics.Color.parseColor("#333333")); pt.setTextSize(14); pt.setTypeface(android.graphics.Typeface.create(appFonts[1],1)); cv.drawText(lang.bnNum(i),cx,cy+5,pt);
            }
            int tR=(int)Math.ceil((tD+off)/7.0); float wSY=gY+(tR*rH)+40; pt.setColor(android.graphics.Color.parseColor("#333333")); pt.setTextSize(22); pt.setTypeface(android.graphics.Typeface.create(appFonts[1],1)); pt.setTextAlign(android.graphics.Paint.Align.LEFT); cv.drawText(isBn?"সাপ্তাহিক বিস্তারিত (ফজর থেকে বিতর)":"Weekly Detail (Fard & Sunnah)",pd,wSY,pt);
            float wY=wSY+30, wCH=120f, bG=20f;
            for(int w=1;w<=tR;w++){
                int sD=(w==1)?1:((w-1)*7-off+1), eD=Math.min(w*7-off,tD); if(sD>tD) break;
                java.util.Calendar tS=(java.util.Calendar)statsCalPointer.clone(); tS.set(5,sD); java.util.Calendar tE=(java.util.Calendar)statsCalPointer.clone(); tE.set(5,eD); java.text.SimpleDateFormat sm=new java.text.SimpleDateFormat("MMM",java.util.Locale.US);
                String sDS=isBn?(lang.bnNum(sD)+" "+lang.get(sm.format(tS.getTime()))):(sm.format(tS.getTime())+" "+String.format(java.util.Locale.US,"%02d",sD)); String eDS=isBn?(lang.bnNum(eD)+" "+lang.get(sm.format(tE.getTime()))):(sm.format(tE.getTime())+" "+String.format(java.util.Locale.US,"%02d",eD));
                String wT=(isBn?"সপ্তাহ ":"Week ")+lang.bnNum(w)+" ("+sDS+" - "+eDS+")";
                pt.setColor(android.graphics.Color.parseColor("#FAFAFC")); cv.drawRoundRect(new android.graphics.RectF(pd,wY,pw-pd,wY+wCH),15,15,pt);
                pt.setColor(android.graphics.Color.parseColor("#555555")); pt.setTextSize(14); pt.setTypeface(android.graphics.Typeface.create(appFonts[1],1)); cv.drawText(wT,pd+20,wY+30,pt);
                float cAW=pw-(pd*2)-40, cCW=cAW/7f, cXS=pd+20;
                for(int d=sD;d<=eD;d++){
                    cal.set(5,d); int dw=cal.get(7)-1; String dK=sdf.format(cal.getTime()); float cx=cXS+(dw*cCW)+(cCW/2f); int fD=0, sD_cnt=0; boolean hB=false;
                    if(cal.before(now)||dK.equals(sdf.format(now.getTime()))){ SalahRecord rec=getRoomRecord(dK); if(rec!=null){for(int p=0;p<prayers.length;p++){String fS=getFardStat(rec,prayers[p]); if(fS.equals("yes"))fD++; else if(fS.equals("excused")){fD++;hB=true;} for(String sN:AppConstants.SUNNAHS[p])if("yes".equals(sp.getString(dK+"_"+prayers[p]+"_Sunnah_"+sN,"no")))sD_cnt++;}} }
                    float lH=(fD/6f)*50f, rH_b=(sD_cnt/12f)*50f, bY=wY+90f;
                    if(!(cal.after(now)&&!dK.equals(sdf.format(now.getTime())))){
                        if(fD>0){pt.setColor(hB?android.graphics.Color.parseColor("#8B5CF6"):android.graphics.Color.parseColor("#22C55E")); cv.drawRoundRect(new android.graphics.RectF(cx-10,bY-lH,cx-1,bY),3f,3f,pt);}
                        if(sD_cnt>0){pt.setColor(android.graphics.Color.parseColor("#F59E0B")); cv.drawRoundRect(new android.graphics.RectF(cx+1,bY-rH_b,cx+10,bY),3f,3f,pt);}
                    }
                    pt.setColor(android.graphics.Color.parseColor("#AAAAAA")); pt.setTextSize(10); pt.setTypeface(appFonts[0]); pt.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText(ds[dw]+" "+lang.bnNum(d),cx,bY+18,pt);
                } wY+=wCH+bG;
            }
            pt.setColor(android.graphics.Color.parseColor("#AAAAAA")); pt.setTextSize(12); pt.setTypeface(appFonts[0]); pt.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText(isBn?"My Salah Tracker অ্যাপের মাধ্যমে তৈরি":"Generated by My Salah Tracker",pw/2f,ph-40,pt);
            doc.finishPage(pg); java.io.File dir=android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS); if(!dir.exists()) dir.mkdirs();
            java.io.File file=new java.io.File(dir,"Salah_Report_"+System.currentTimeMillis()+".pdf"); doc.writeTo(new java.io.FileOutputStream(file)); doc.close();
            final java.io.File fF=file; if(activity instanceof MainActivity){android.widget.FrameLayout r=activity.findViewById(android.R.id.content); if(r!=null&&ui!=null){ui.showSmartBanner(r,isBn?"সফল":"Success",isBn?"পিডিএফ সেভ হয়েছে (দেখতে ক্লিক করুন)":"PDF Saved (Click to view)","img_tick",colorAccent,()->{android.content.Intent i=new android.content.Intent(android.content.Intent.ACTION_VIEW); android.net.Uri u=androidx.core.content.FileProvider.getUriForFile(activity,activity.getPackageName()+".provider",fF); i.setDataAndType(u,"application/pdf"); i.addFlags(1); i.setFlags(1073741824|1); try{activity.startActivity(i);}catch(Exception e){} });}}
        }catch(Exception e){if(activity instanceof MainActivity){android.widget.FrameLayout r=activity.findViewById(android.R.id.content); if(r!=null&&ui!=null)ui.showSmartBanner(r,"Error","Storage permission required.","img_warning",colorAccent,null);}}
    }"""
        open(f,'w').write(c[:s] + np + c[e:])
print("✅ PDF Method Fixed successfully!")
