import os
sp = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
sc = open(sp).read()

old_pdf = "doc.finishPage(pg); java.io.File dir=android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS);"
new_pdf = """doc.finishPage(pg); 
            int p2H = (tD*35)+150; android.graphics.pdf.PdfDocument.PageInfo pi2=new android.graphics.pdf.PdfDocument.PageInfo.Builder(pw,p2H,2).create(); android.graphics.pdf.PdfDocument.Page pg2=doc.startPage(pi2); android.graphics.Canvas cv2=pg2.getCanvas(); pt.setColor(android.graphics.Color.WHITE); cv2.drawRect(0,0,pw,p2H,pt); pt.setColor(colorAccent); pt.setTextSize(22); pt.setTypeface(android.graphics.Typeface.create(appFonts[1],1)); pt.setTextAlign(android.graphics.Paint.Align.CENTER); cv2.drawText(isBn?"বিস্তারিত দৈনিক রিপোর্ট":"Detailed Daily Report",pw/2f,50,pt); float tY=100; float cW2=pw/8f; String[] hdrs=isBn?new String[]{"তারিখ","ফজর","যোহর","আসর","মাগ","এশা","বিতর","অবস্থা"}:new String[]{"Date","Fajr","Dhr","Asr","Mag","Isha","Witr","Stat"}; pt.setColor(android.graphics.Color.parseColor("#333333")); pt.setTextSize(14); for(int i=0;i<8;i++)cv2.drawText(hdrs[i],(i*cW2)+(cW2/2f),tY,pt); tY+=15; pt.setStrokeWidth(1f); pt.setColor(android.graphics.Color.parseColor("#DDDDDD")); cv2.drawLine(20,tY,pw-20,tY,pt); tY+=25; cal.set(5,1); for(int i=1;i<=tD;i++){ cal.set(5,i); String dK=sdf.format(cal.getTime()); SalahRecord r=getRoomRecord(dK); if(cal.after(now)&&!dK.equals(sdf.format(now.getTime())))continue; pt.setColor(android.graphics.Color.parseColor("#555555")); pt.setTypeface(appFonts[0]); cv2.drawText(isBn?lang.bnNum(i):String.valueOf(i),(cW2/2f),tY,pt); boolean aD=true; if(r!=null){ for(int p=0;p<6;p++){ String st=getFardStat(r,prayers[p]); if(st.equals("yes")){pt.setColor(android.graphics.Color.parseColor("#22C55E"));cv2.drawText("✓",(p+1)*cW2+(cW2/2f),tY,pt);}else if(st.equals("excused")){pt.setColor(android.graphics.Color.parseColor("#8B5CF6"));cv2.drawText("🌸",(p+1)*cW2+(cW2/2f),tY,pt);}else{pt.setColor(android.graphics.Color.parseColor("#FF5252"));cv2.drawText("✕",(p+1)*cW2+(cW2/2f),tY,pt);aD=false;} } }else{ for(int p=0;p<6;p++){pt.setColor(android.graphics.Color.parseColor("#FF5252"));cv2.drawText("✕",(p+1)*cW2+(cW2/2f),tY,pt);aD=false;} } pt.setColor(aD?android.graphics.Color.parseColor("#22C55E"):android.graphics.Color.parseColor("#FF5252")); cv2.drawText(aD?(isBn?"★":"★"):(isBn?"⚠":"⚠"),7*cW2+(cW2/2f),tY,pt); tY+=35; } doc.finishPage(pg2);
            java.io.File dir=android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS);"""

if "pi2" not in sc and old_pdf in sc:
    sc = sc.replace(old_pdf, new_pdf)
    open(sp,'w').write(sc)
    print("✅ Detailed Table Page added to PDF successfully!")
else:
    print("⚠️ PDF was already updated or pattern not found.")
