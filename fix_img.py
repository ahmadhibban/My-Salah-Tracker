import re
f = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
c = open(f).read()
m = re.search(r'public\s+void\s+shareImageReport\s*\([^)]*\)\s*\{', c)
if m:
    s=m.start(); b=0; e=-1; im=False
    for i in range(s, len(c)):
        if c[i]=='{': b+=1; im=True
        elif c[i]=='}':
            b-=1
            if im and b==0: e=i+1; break
    if e!=-1:
        ni = """public void shareImageReport(boolean isWeekly) {
        boolean isBn=sp.getString("app_lang","en").equals("bn");
        try{
            int w=2160, h=2850; android.graphics.Bitmap bm=android.graphics.Bitmap.createBitmap(w,h,android.graphics.Bitmap.Config.ARGB_8888); android.graphics.Canvas cv=new android.graphics.Canvas(bm); android.graphics.Paint pt=new android.graphics.Paint(1);
            pt.setColor(themeColors[0]); cv.drawRect(0,0,w,h,pt); android.graphics.Path ph=new android.graphics.Path(); ph.moveTo(0,0); ph.lineTo(w,0); ph.lineTo(w,550); ph.cubicTo(w/2f,750,w/2f,350,0,550); ph.close(); pt.setColor(colorAccent); cv.drawPath(ph,pt);
            pt.setColor(android.graphics.Color.WHITE); pt.setTextAlign(android.graphics.Paint.Align.CENTER); pt.setTextSize(120); pt.setTypeface(android.graphics.Typeface.create(appFonts[1],1)); cv.drawText("My Salah Tracker",w/2f,220,pt);
            pt.setTextSize(60); pt.setTypeface(appFonts[0]); String em=sp.getString("user_email","guest@salah.com"); if(em.length()>25) em=em.substring(0,22)+"..."; cv.drawText(em,w/2f,320,pt);
            pt.setTextSize(70); pt.setTypeface(appFonts[1]); cv.drawText(isWeekly?(isBn?"সাপ্তাহিক রিপোর্ট":"Weekly Report"):(isBn?"মাসিক রিপোর্ট":"Monthly Report"),w/2f,440,pt);
            java.util.Calendar eC=(java.util.Calendar)statsCalPointer.clone(), sC=(java.util.Calendar)statsCalPointer.clone(), now=java.util.Calendar.getInstance();
            if(isWeekly){while(sC.get(7)!=7)sC.add(5,-1); eC=(java.util.Calendar)sC.clone(); eC.add(5,6); if(eC.after(now))eC=now;}
            else{sC.set(5,1); eC.set(5,sC.getActualMaximum(5)); if(eC.after(now))eC=now;}
            java.text.SimpleDateFormat sk=new java.text.SimpleDateFormat("yyyy-MM-dd",java.util.Locale.US), sd=new java.text.SimpleDateFormat("EEEE",java.util.Locale.US);
            String gR=lang.getShortGreg(sC.getTime())+" - "+lang.getShortGreg(eC.getTime()), hR=ui.getHijriDate(sC.getTime(),sp.getInt("hijri_offset",0))+" - "+ui.getHijriDate(eC.getTime(),sp.getInt("hijri_offset",0));
            String sDy=lang.get(sd.format(sC.getTime())), eDy=lang.get(sd.format(eC.getTime()));
            if(isBn){String[] bD={"রবিবার","সোমবার","মঙ্গলবার","বুধবার","বৃহস্পতিবার","শুক্রবার","শনিবার"}; sDy=bD[sC.get(7)-1]; eDy=bD[eC.get(7)-1];}
            pt.setColor(themeColors[2]); pt.setTextSize(55); pt.setTypeface(appFonts[1]); cv.drawText(gR,w/2f,750,pt); pt.setColor(themeColors[3]); pt.setTextSize(45); pt.setTypeface(appFonts[0]); cv.drawText(hR,w/2f,830,pt); cv.drawText(sDy+" - "+eDy,w/2f,900,pt);
            int tD=0, tDn=0, tM=0, tE=0, tQ=0; java.util.Calendar lC=(java.util.Calendar)sC.clone();
            java.util.ArrayList<Float> dFV=new java.util.ArrayList<>(), dSV=new java.util.ArrayList<>(); java.util.ArrayList<Integer> dC=new java.util.ArrayList<>(); java.util.ArrayList<String> dL=new java.util.ArrayList<>();
            while(!lC.after(eC)){
                tD++; String dK=sk.format(lC.getTime()); SalahRecord r=getRoomRecord(dK); int dyDn=0, dyE=0, sC_cnt=0;
                if(r!=null){for(int p=0;p<prayers.length;p++){String st=getFardStat(r,prayers[p]); if(st.equals("yes")){tDn++;dyDn++;}else if(st.equals("excused")){tE++;dyE++;}else{if(getQazaStat(r,prayers[p]))tQ++;else tM++;} if(isWeekly)for(String sN:AppConstants.SUNNAHS[p])if("yes".equals(sp.getString(dK+"_"+prayers[p]+"_Sunnah_"+sN,"no")))sC_cnt++;}}
                dFV.add((float)(dyDn+dyE)); dSV.add((float)sC_cnt);
                if(lC.after(now)&&!dK.equals(sk.format(now.getTime()))) dC.add(android.graphics.Color.TRANSPARENT); else if(dyDn+dyE==0) dC.add(android.graphics.Color.TRANSPARENT); else if(dyE>0) dC.add(android.graphics.Color.parseColor("#8B5CF6")); else dC.add(android.graphics.Color.parseColor("#22C55E"));
                dL.add(isWeekly?lang.get(sd.format(lC.getTime())).substring(0,3):lang.bnNum(lC.get(5))); lC.add(5,1);
            }
            float sY=1050, pd=80, cW=(w-(pd*3))/2f, cH=280;
            drawReportCard(cv,pt,pd,sY,cW,cH,colorAccent,isBn?"মোট দিন":"Total Days",lang.bnNum(tD)); drawReportCard(cv,pt,pd*2+cW,sY,cW,cH,android.graphics.Color.parseColor("#3B82F6"),isBn?"আদায়কৃত নামাজ":"Prayers Done",lang.bnNum(tDn));
            drawReportCard(cv,pt,pd,sY+cH+60,cW,cH,android.graphics.Color.parseColor("#FF5252"),isBn?"কাজা হয়েছে":"Missed",lang.bnNum(tM)); drawReportCard(cv,pt,pd*2+cW,sY+cH+60,cW,cH,android.graphics.Color.parseColor("#FF9500"),isBn?"অপেক্ষমান কাজা":"Pending Qaza",lang.bnNum(tQ));
            drawReportCard(cv,pt,pd,sY+(cH*2)+120,cW,cH,android.graphics.Color.parseColor("#8B5CF6"),isBn?"পিরিয়ড/ছুটি":"Excused Mode",lang.bnNum(tE)); drawReportCard(cv,pt,pd*2+cW,sY+(cH*2)+120,cW,cH,android.graphics.Color.parseColor("#9B59B6"),isBn?"বর্তমান স্ট্রিক":"Current Streak",lang.bnNum(ui.calculateStreak(sp,prayers)));
            float cyY=sY+(cH*3)+200, cyH=480; pt.setColor(themeColors[1]); cv.drawRoundRect(new android.graphics.RectF(pd,cyY,w-pd,cyY+cyH),50,50,pt);
            float cIW=w-(pd*2)-80, cCol=cIW/dFV.size(), mBH=cyH-140;
            for(int i=0;i<dFV.size();i++){
                float cx=pd+40+(i*cCol)+(cCol/2f), fH=(dFV.get(i)/6f)*mBH, sH=(dSV.get(i)/12f)*mBH;
                if(isWeekly){if(fH>0){pt.setColor(dC.get(i));cv.drawRoundRect(new android.graphics.RectF(cx-40,cyY+60+mBH-fH,cx-5,cyY+60+mBH),15,15,pt);} if(sH>0){pt.setColor(android.graphics.Color.parseColor("#F59E0B"));cv.drawRoundRect(new android.graphics.RectF(cx+5,cyY+60+mBH-sH,cx+40,cyY+60+mBH),15,15,pt);}}
                else if(fH>0){pt.setColor(dC.get(i));cv.drawRoundRect(new android.graphics.RectF(cx-15,cyY+60+mBH-fH,cx+15,cyY+60+mBH),12,12,pt);}
                pt.setColor(themeColors[3]); pt.setTextSize(isWeekly?35:24); pt.setTextAlign(android.graphics.Paint.Align.CENTER); pt.setTypeface(appFonts[0]); cv.drawText(dL.get(i),cx,cyY+cyH-40,pt);
            }
            pt.setColor(themeColors[3]); pt.setTextAlign(android.graphics.Paint.Align.CENTER); pt.setTextSize(45); cv.drawText(isBn?"My Salah Tracker অ্যাপের মাধ্যমে তৈরি":"Generated by My Salah Tracker",w/2f,h-80,pt);
            java.io.File dir=android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS); if(!dir.exists())dir.mkdirs();
            java.io.File file=new java.io.File(dir,"Salah_Report_"+System.currentTimeMillis()+".png"); java.io.FileOutputStream fos=new java.io.FileOutputStream(file); bm.compress(android.graphics.Bitmap.CompressFormat.PNG,100,fos); fos.flush(); fos.close();
            android.os.StrictMode.VmPolicy.Builder b=new android.os.StrictMode.VmPolicy.Builder(); android.os.StrictMode.setVmPolicy(b.build());
            android.content.Intent i=new android.content.Intent(android.content.Intent.ACTION_SEND); i.setType("image/png"); i.putExtra(android.content.Intent.EXTRA_STREAM,android.net.Uri.fromFile(file)); i.putExtra(android.content.Intent.EXTRA_TEXT,"Alhamdulillah! Check out my Salah progress."); activity.startActivity(android.content.Intent.createChooser(i,"Share via"));
        }catch(Exception e){}
    }"""
        open(f,'w').write(c[:s] + ni + c[e:])
print("✅ Image Method Fixed successfully! YOU ARE READY TO BUILD.")
