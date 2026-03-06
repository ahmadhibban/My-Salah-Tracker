package com.my.salah.tracker.app;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.graphics.pdf.PdfDocument;
import android.net.Uri;
import android.os.Environment;
import android.os.StrictMode;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import java.io.File;
import java.io.FileOutputStream;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public class StatsHelper {
    private Activity activity; private float DENSITY; private int[] themeColors; private int colorAccent; private LanguageEngine lang; private UIComponents ui; private SharedPreferences sp; private String[] prayers; private Typeface[] appFonts; private Calendar statsCalPointer;

    public StatsHelper(Activity activity, float DENSITY, int[] themeColors, int colorAccent, LanguageEngine lang, UIComponents ui, SharedPreferences sp, String[] prayers, Typeface[] appFonts) {
        this.activity = activity; this.DENSITY = DENSITY; this.themeColors = themeColors; this.colorAccent = colorAccent; this.lang = lang; this.ui = ui; this.sp = sp; this.prayers = prayers; this.appFonts = appFonts; this.statsCalPointer = Calendar.getInstance();
    }

    // ✨ ROOM DATABASE HELPERS FOR SUPERFAST STATS ✨
    private SalahRecord getRoomRecord(String date) {
        return SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(date);
    }
    
    private String getFardStat(SalahRecord r, String p) {
        if(r==null) return "no";
        switch(p){ case "Fajr":return r.fajr; case "Dhuhr":return r.dhuhr; case "Asr":return r.asr; case "Maghrib":return r.maghrib; case "Isha":return r.isha; case "Witr":return r.witr; default:return "no";}
    }
    
    private boolean getQazaStat(SalahRecord r, String p) {
        if(r==null) return false;
        switch(p){ case "Fajr":return r.fajr_qaza; case "Dhuhr":return r.dhuhr_qaza; case "Asr":return r.asr_qaza; case "Maghrib":return r.maghrib_qaza; case "Isha":return r.isha_qaza; case "Witr":return r.witr_qaza; default:return false;}
    }

    private void applyFont(View v, Typeface reg, Typeface bold) {
        if (v instanceof TextView) { TextView tv = (TextView) v; if (tv.getTypeface() != null && tv.getTypeface().isBold()) tv.setTypeface(bold); else tv.setTypeface(reg); } 
        else if (v instanceof ViewGroup) { ViewGroup vg = (ViewGroup) v; for (int i = 0; i < vg.getChildCount(); i++) applyFont(vg.getChildAt(i), reg, bold); }
    }

    
    public void exportXls() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            java.io.File dir = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists()) dir.mkdirs();
            java.io.File file = new java.io.File(dir, "Salah_Premium_Report_" + System.currentTimeMillis() + ".xls");
            java.io.PrintWriter pw = new java.io.PrintWriter(new java.io.OutputStreamWriter(new java.io.FileOutputStream(file), "UTF-8"));
            
            int tDays = 0, tDone = 0, tMissed = 0, tExcused = 0, tQaza = 0;
            java.util.Calendar sumCal = (java.util.Calendar) statsCalPointer.clone(); sumCal.set(java.util.Calendar.DAY_OF_MONTH, 1);
            int mDays = sumCal.getActualMaximum(java.util.Calendar.DAY_OF_MONTH);
            java.util.Calendar nowSum = java.util.Calendar.getInstance();
            java.text.SimpleDateFormat sdf = new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US);
            
            for(int j=1; j<=mDays; j++) {
                sumCal.set(java.util.Calendar.DAY_OF_MONTH, j);
                String dk = sdf.format(sumCal.getTime());
                if(sumCal.after(nowSum) && !dk.equals(sdf.format(nowSum.getTime()))) continue;
                tDays++;
                SalahRecord rec = getRoomRecord(dk);
                for(String p : prayers) {
                    String st = getFardStat(rec, p); boolean isQz = getQazaStat(rec, p);
                    if(st.equals("yes")) tDone++; else if(st.equals("excused")) tExcused++; else { if(isQz) tQaza++; else tMissed++; }
                }
            }
            int streak = ui.calculateStreak(sp, prayers);
            String title = (isBn ? "মাসিক রিপোর্ট • " : "Monthly Report • ") + new java.text.SimpleDateFormat("MMMM yyyy", java.util.Locale.US).format(statsCalPointer.getTime());
            
            StringBuilder xml = new StringBuilder();
            xml.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
            xml.append("<?mso-application progid=\"Excel.Sheet\"?>");
            xml.append("<Workbook xmlns=\"urn:schemas-microsoft-com:office:spreadsheet\" xmlns:ss=\"urn:schemas-microsoft-com:office:spreadsheet\">");
            
            xml.append("<Styles>");
            xml.append("<Style ss:ID=\"Default\" ss:Name=\"Normal\"><Alignment ss:Vertical=\"Center\"/></Style>");
            xml.append("<Style ss:ID=\"sTitle\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"20\" ss:Bold=\"1\" ss:Color=\"#FFFFFF\"/><Interior ss:Color=\"#FF9800\" ss:Pattern=\"Solid\"/></Style>");
            xml.append("<Style ss:ID=\"sSumH\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#5F6368\"/><Interior ss:Color=\"#F8F9FA\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sSumV\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"16\" ss:Bold=\"1\" ss:Color=\"#202124\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\" ss:Color=\"#FF9800\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sHead\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"13\" ss:Bold=\"1\" ss:Color=\"#FFFFFF\"/><Interior ss:Color=\"#3C4043\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\" ss:Color=\"#202124\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sDate\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#3C4043\"/><Interior ss:Color=\"#F1F3F4\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sYes\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#137333\"/><Interior ss:Color=\"#E6F4EA\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sNo\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#C5221F\"/><Interior ss:Color=\"#FCE8E6\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sExc\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#B80672\"/><Interior ss:Color=\"#FCE4EC\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("</Styles>");
            
            xml.append("<Worksheet ss:Name=\"Report\"><Table>");
            
            xml.append("<Column ss:Width=\"140\"/>");
            for(int i=0; i<6; i++) xml.append("<Column ss:Width=\"110\"/>");
            xml.append("<Column ss:Width=\"150\"/>");
            
            xml.append("<Row ss:Height=\"60\"><Cell ss:MergeAcross=\"7\" ss:StyleID=\"sTitle\"><Data ss:Type=\"String\">" + title + "</Data></Cell></Row>");
            xml.append("<Row ss:Height=\"20\"><Cell><Data ss:Type=\"String\"></Data></Cell></Row>");
            
            xml.append("<Row ss:Height=\"35\">");
            xml.append("<Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"মোট দিন":"Total Days") + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"আদায়কৃত":"Done") + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"কাজা":"Missed") + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"অপেক্ষমান কাজা":"Pending Qaza") + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"ছুটি":"Excused") + "</Data></Cell>");
            xml.append("<Cell ss:MergeAcross=\"2\" ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"স্ট্রিক":"Streak") + "</Data></Cell>");
            xml.append("</Row>");
            
            xml.append("<Row ss:Height=\"45\">");
            xml.append("<Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(tDays) + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(tDone) + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(tMissed) + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(tQaza) + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(tExcused) + "</Data></Cell>");
            xml.append("<Cell ss:MergeAcross=\"2\" ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(streak) + " ★</Data></Cell>");
            xml.append("</Row>");
            xml.append("<Row ss:Height=\"25\"><Cell><Data ss:Type=\"String\"></Data></Cell></Row>");

            xml.append("<Row ss:Height=\"40\">");
            String[] headers = isBn ? new String[]{"তারিখ", "ফজর", "যোহর", "আসর", "মাগরিব", "এশা", "বিতর", "সারসংক্ষেপ"} : new String[]{"Date", "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr", "Status"};
            for(String h : headers) xml.append("<Cell ss:StyleID=\"sHead\"><Data ss:Type=\"String\">" + h + "</Data></Cell>");
            xml.append("</Row>");
            
            java.util.Calendar cal = (java.util.Calendar) statsCalPointer.clone(); cal.set(java.util.Calendar.DAY_OF_MONTH, 1);
            for(int i=1; i<=mDays; i++) {
                cal.set(java.util.Calendar.DAY_OF_MONTH, i);
                String dKey = sdf.format(cal.getTime());
                SalahRecord r = getRoomRecord(dKey);
                
                String dateDisplay = isBn ? lang.bnNum(i) + " " + lang.get(new java.text.SimpleDateFormat("MMM", java.util.Locale.US).format(cal.getTime())) + ", " + lang.bnNum(cal.get(java.util.Calendar.YEAR)) : dKey;
                
                xml.append("<Row ss:Height=\"35\">");
                xml.append("<Cell ss:StyleID=\"sDate\"><Data ss:Type=\"String\">" + dateDisplay + "</Data></Cell>");
                
                boolean allDone = true;
                for(String p : prayers) {
                    String s = getFardStat(r, p);
                    String style = s.equals("yes") ? "sYes" : (s.equals("excused") ? "sExc" : "sNo");
                    String txt = s.equals("yes") ? "\u2713 " + (isBn?"সম্পন্ন":"Done") : (s.equals("excused") ? "\u273F " + (isBn?"ছুটি":"Excused") : "\u2715 " + (isBn?"কাজা":"Missed"));
                    xml.append("<Cell ss:StyleID=\"" + style + "\"><Data ss:Type=\"String\">" + txt + "</Data></Cell>");
                    if(!s.equals("yes") && !s.equals("excused")) allDone = false;
                }
                String sStyle = allDone ? "sYes" : "sNo";
                String sTxt = allDone ? (isBn ? "★ আলহামদুলিল্লাহ" : "★ Perfect") : (isBn ? "⚠ অসম্পূর্ণ" : "⚠ Incomplete");
                xml.append("<Cell ss:StyleID=\"" + sStyle + "\"><Data ss:Type=\"String\">" + sTxt + "</Data></Cell>");
                xml.append("</Row>");
            }
            xml.append("</Table></Worksheet></Workbook>");
            pw.write(xml.toString());
            pw.close();
            
            final java.io.File finalFile = file;
            ui.showSmartBanner((android.widget.FrameLayout) activity.findViewById(android.R.id.content), isBn?"সফল":"Success", isBn?"XLS ফাইল সেভ হয়েছে (ওপেন করতে ক্লিক)":"XLS Saved (Click to open)", "img_tick", colorAccent, new Runnable() {
                @Override public void run() {
                    android.content.Intent intent = new android.content.Intent(android.content.Intent.ACTION_VIEW);
                    android.net.Uri uri = androidx.core.content.FileProvider.getUriForFile(activity, activity.getPackageName() + ".provider", finalFile);
                    intent.setDataAndType(uri, "application/vnd.ms-excel");
                    intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    activity.startActivity(android.content.Intent.createChooser(intent, "Open with..."));
                }
            });
        } catch(Exception e) {}
    }

    public void showStatsOptionsDialog() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        FrameLayout wrap = new FrameLayout(activity); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout main = new LinearLayout(activity); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        TextView title = new TextView(activity); title.setText(isBn ? "উন্নত পরিসংখ্যান" : "Advanced Statistics"); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
        final AlertDialog ad = new AlertDialog.Builder(activity).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(Gravity.CENTER); 
        
        class BtnMaker {
            void add(String t, final Runnable act) {
                LinearLayout btn = new LinearLayout(activity); btn.setOrientation(LinearLayout.HORIZONTAL); btn.setGravity(Gravity.CENTER_VERTICAL); btn.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
                GradientDrawable bg = new GradientDrawable(); bg.setColor(themeColors[4]); bg.setCornerRadius(15f*DENSITY); btn.setBackground(bg); LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2); lp.setMargins(0, 0, 0, (int)(10*DENSITY)); btn.setLayoutParams(lp);
                View dot = new View(activity); GradientDrawable dBg = new GradientDrawable(); dBg.setShape(GradientDrawable.OVAL); dBg.setColor(colorAccent); dot.setBackground(dBg); dot.setLayoutParams(new LinearLayout.LayoutParams((int)(10*DENSITY), (int)(10*DENSITY))); btn.addView(dot);
                TextView tv = new TextView(activity); tv.setText(t); tv.setTextColor(themeColors[2]); tv.setTextSize(16); tv.setTypeface(Typeface.DEFAULT_BOLD); tv.setPadding((int)(15*DENSITY), 0, 0, 0); btn.addView(tv);
                btn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { ad.dismiss(); act.run(); } }); main.addView(btn);
            }
        }
        BtnMaker bm = new BtnMaker();
        bm.add(isBn ? "সাপ্তাহিক পরিসংখ্যান" : "Weekly Statistics", new Runnable() { @Override public void run() { showStats(true); } });
        bm.add(isBn ? "মাসিক পরিসংখ্যান" : "Monthly Statistics", new Runnable() { @Override public void run() { showStats(false); } });
        bm.add(isBn ? "রিপোর্ট শেয়ার (ছবি)" : "Share Report (Image)", new Runnable() { @Override public void run() { showShareTypeDialog(); } });
        bm.add(isBn ? "প্রিমিয়াম এক্সেল (XLS) এক্সপোর্ট" : "Export Premium XLS", new Runnable() { @Override public void run() { exportXls(); } });
        bm.add(isBn ? "প্রিমিয়াম পিডিএফ এক্সপোর্ট" : "Export Premium PDF", new Runnable() { @Override public void run() { exportPdf(); } });
        
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp); applyFont(main, appFonts[0], appFonts[1]); ad.show();
    }

    private void showShareTypeDialog() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        FrameLayout wrap = new FrameLayout(activity); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout main = new LinearLayout(activity); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        TextView title = new TextView(activity); title.setText(isBn ? "রিপোর্টের ধরন নির্বাচন করুন" : "Select Report Type"); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
        final AlertDialog ad = new AlertDialog.Builder(activity).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(Gravity.CENTER);
        
        View.OnClickListener clicker = new View.OnClickListener() { @Override public void onClick(View v) { ad.dismiss(); boolean isWeekly = (boolean) v.getTag(); shareImageReport(isWeekly); } };
        
        LinearLayout btn1 = new LinearLayout(activity); btn1.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY)); btn1.setGravity(Gravity.CENTER);
        GradientDrawable bg1 = new GradientDrawable(); bg1.setColor(colorAccent); bg1.setCornerRadius(15f*DENSITY); btn1.setBackground(bg1); btn1.setTag(true); btn1.setOnClickListener(clicker);
        TextView t1 = new TextView(activity); t1.setText(isBn ? "সাপ্তাহিক রিপোর্ট" : "Weekly Report"); t1.setTextColor(Color.WHITE); t1.setTypeface(Typeface.DEFAULT_BOLD); btn1.addView(t1); main.addView(btn1);
        
        LinearLayout btn2 = new LinearLayout(activity); btn2.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY)); btn2.setGravity(Gravity.CENTER);
        GradientDrawable bg2 = new GradientDrawable(); bg2.setColor(themeColors[4]); bg2.setCornerRadius(15f*DENSITY); btn2.setBackground(bg2); btn2.setTag(false); btn2.setOnClickListener(clicker);
        LinearLayout.LayoutParams lp2 = new LinearLayout.LayoutParams(-1, -2); lp2.setMargins(0, (int)(10*DENSITY), 0, 0); btn2.setLayoutParams(lp2);
        TextView t2 = new TextView(activity); t2.setText(isBn ? "মাসিক রিপোর্ট" : "Monthly Report"); t2.setTextColor(themeColors[2]); t2.setTypeface(Typeface.DEFAULT_BOLD); btn2.addView(t2); main.addView(btn2);
        
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp); applyFont(main, appFonts[0], appFonts[1]); ad.show();
    }

    public void shareImageReport(boolean isWeekly) {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            int width = 2160;
            int height = 2850; // ⬆️ ক্যানভাসের সাইজ বড় করা হয়েছে চার্টের জন্য 
            Bitmap bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888); Canvas canvas = new Canvas(bitmap); Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
            paint.setColor(themeColors[0]); canvas.drawRect(0, 0, width, height, paint); Path path = new Path(); path.moveTo(0,0); path.lineTo(width, 0); path.lineTo(width, 550);
            path.cubicTo(width/2f, 750, width/2f, 350, 0, 550); path.close(); paint.setColor(colorAccent); canvas.drawPath(path, paint);
            paint.setColor(Color.WHITE); paint.setTextAlign(Paint.Align.CENTER); paint.setTextSize(120); paint.setTypeface(Typeface.create(appFonts[1], Typeface.BOLD));
            canvas.drawText("My Salah Tracker", width/2f, 220, paint);
            paint.setTextSize(60); paint.setTypeface(appFonts[0]); String email = sp.getString("user_email", "guest@salah.com"); canvas.drawText(email, width/2f, 320, paint);
            paint.setTextSize(70); paint.setTypeface(appFonts[1]);
            String reportTitle = isWeekly ? (isBn ? "সাপ্তাহিক রিপোর্ট" : "Weekly Report") : (isBn ? "মাসিক রিপোর্ট" : "Monthly Report");
            canvas.drawText(reportTitle, width/2f, 440, paint);
            
            Calendar endCal = (Calendar) statsCalPointer.clone(); Calendar startCal = (Calendar) statsCalPointer.clone();
            if (isWeekly) { 
                while (startCal.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) startCal.add(Calendar.DATE, -1);
                endCal = (Calendar) startCal.clone(); endCal.add(Calendar.DATE, 6);
                if(endCal.after(Calendar.getInstance())) endCal = Calendar.getInstance();
            } else { 
                startCal.set(Calendar.DAY_OF_MONTH, 1); endCal.set(Calendar.DAY_OF_MONTH, startCal.getActualMaximum(Calendar.DAY_OF_MONTH)); 
                if(endCal.after(Calendar.getInstance())) endCal = Calendar.getInstance();
            }
            
            SimpleDateFormat sdfKey = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
            SimpleDateFormat sdfDay = new SimpleDateFormat("EEEE", Locale.US);
            String gregDateRange = lang.getShortGreg(startCal.getTime()) + " - " + lang.getShortGreg(endCal.getTime());
            String hijriDateRange = ui.getHijriDate(startCal.getTime(), sp.getInt("hijri_offset", 0)) + " - " + ui.getHijriDate(endCal.getTime(), sp.getInt("hijri_offset", 0));
            String startDay = lang.get(sdfDay.format(startCal.getTime()));
            String endDay = lang.get(sdfDay.format(endCal.getTime()));
            if(isBn) { String[] bnDays = {"রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার"}; startDay = bnDays[startCal.get(Calendar.DAY_OF_WEEK)-1]; endDay = bnDays[endCal.get(Calendar.DAY_OF_WEEK)-1]; }
            
            paint.setColor(themeColors[2]);
            paint.setTextSize(55); paint.setTypeface(appFonts[1]); canvas.drawText(gregDateRange, width/2f, 750, paint); paint.setColor(themeColors[3]); paint.setTextSize(45); paint.setTypeface(appFonts[0]); canvas.drawText(hijriDateRange, width/2f, 830, paint);
            canvas.drawText(startDay + " - " + endDay, width/2f, 900, paint);
            
            int totalDays = 0, totalDone = 0, totalMissed = 0, totalExcused = 0, totalQaza = 0;
            Calendar loopCal = (Calendar) startCal.clone();
            java.util.ArrayList<Float> dailyValues = new java.util.ArrayList<>();
            java.util.ArrayList<Integer> dailyColors = new java.util.ArrayList<>();
            java.util.ArrayList<String> dailyLabels = new java.util.ArrayList<>();
            
            while(!loopCal.after(endCal)) { 
                totalDays++;
                String dKey = sdfKey.format(loopCal.getTime()); 
                SalahRecord r = getRoomRecord(dKey);
                int dayDone = 0; int dayExcused = 0;
                for(String p : prayers) { 
                    String stat = getFardStat(r, p);
                    boolean isQaza = getQazaStat(r, p); 
                    if(stat.equals("yes")) { totalDone++; dayDone++; }
                    else if(stat.equals("excused")) { totalExcused++; dayExcused++; }
                    else { if(isQaza) totalQaza++; else totalMissed++; } 
                } 
                float totalDayVal = dayDone + dayExcused;
                dailyValues.add(totalDayVal);
                if (loopCal.after(Calendar.getInstance()) && !dKey.equals(sdfKey.format(Calendar.getInstance().getTime()))) dailyColors.add(themeColors[4]);
                else if (totalDayVal == 0) dailyColors.add(Color.parseColor("#FF5252"));
                else if (dayExcused > 0) dailyColors.add(Color.parseColor("#FF4081"));
                else dailyColors.add(colorAccent);
                
                if (isWeekly) dailyLabels.add(lang.get(sdfDay.format(loopCal.getTime())).substring(0, 3));
                else dailyLabels.add(lang.bnNum(loopCal.get(Calendar.DAY_OF_MONTH)));
                
                loopCal.add(Calendar.DATE, 1);
            }
            
            float startY = 1050;
            float padding = 80; float cardW = (width - (padding*3)) / 2f; float cardH = 280;
            drawReportCard(canvas, paint, padding, startY, cardW, cardH, colorAccent, isBn?"মোট দিন":"Total Days", lang.bnNum(totalDays));
            drawReportCard(canvas, paint, padding*2 + cardW, startY, cardW, cardH, Color.parseColor("#3B82F6"), isBn?"আদায়কৃত নামাজ":"Prayers Done", lang.bnNum(totalDone));
            drawReportCard(canvas, paint, padding, startY + cardH + 60, cardW, cardH, Color.parseColor("#FF5252"), isBn?"কাজা হয়েছে":"Missed", lang.bnNum(totalMissed));
            drawReportCard(canvas, paint, padding*2 + cardW, startY + cardH + 60, cardW, cardH, Color.parseColor("#FF9500"), isBn?"অপেক্ষমান কাজা":"Pending Qaza", lang.bnNum(totalQaza));
            drawReportCard(canvas, paint, padding, startY + (cardH*2) + 120, cardW, cardH, Color.parseColor("#FF4081"), isBn?"পিরিয়ড / ছুটির মোড":"Excused Mode", lang.bnNum(totalExcused));
            drawReportCard(canvas, paint, padding*2 + cardW, startY + (cardH*2) + 120, cardW, cardH, Color.parseColor("#9B59B6"), isBn?"বর্তমান স্ট্রিক":"Current Streak", lang.bnNum(ui.calculateStreak(sp, prayers)));
            
            // ✨ চার্ট আঁকার লজিক (Weekly / Monthly) ✨
            float chartY = startY + (cardH*3) + 200;
            float chartH = 480;
            paint.setColor(themeColors[1]);
            canvas.drawRoundRect(new RectF(padding, chartY, width - padding, chartY + chartH), 50, 50, paint);
            
            float chartInnerW = width - (padding*2) - 80;
            float colW = chartInnerW / dailyValues.size();
            float maxBarH = chartH - 140;
            
            for(int i=0; i<dailyValues.size(); i++) {
                float cx = padding + 40 + (i*colW) + (colW/2f);
                float valH = (dailyValues.get(i) / 6f) * maxBarH;
                if (valH < 10 && dailyValues.get(i) > 0) valH = 10;
                
                float barW = isWeekly ? 50f : 15f; // সাপ্তাহিক হলে মোটা বার, মাসিক হলে চিকন বার
                
                paint.setColor(themeColors[4]);
                canvas.drawRoundRect(new RectF(cx - barW, chartY + 60 + maxBarH - maxBarH, cx + barW, chartY + 60 + maxBarH), barW/2f, barW/2f, paint);
                
                paint.setColor(dailyColors.get(i));
                canvas.drawRoundRect(new RectF(cx - barW, chartY + 60 + maxBarH - valH, cx + barW, chartY + 60 + maxBarH), barW/2f, barW/2f, paint);
                
                paint.setColor(themeColors[3]); paint.setTextSize(isWeekly ? 35 : 24); paint.setTextAlign(Paint.Align.CENTER); paint.setTypeface(appFonts[0]);
                canvas.drawText(dailyLabels.get(i), cx, chartY + chartH - 40, paint);
            }
            
            // ফুটার টেক্সট সেফ জোনে বসানো
            paint.setColor(themeColors[3]); paint.setTextAlign(Paint.Align.CENTER);
            paint.setTextSize(45); canvas.drawText(isBn ? "My Salah Tracker অ্যাপের মাধ্যমে তৈরি" : "Generated by My Salah Tracker", width/2f, height - 80, paint);
            
            java.io.File dir = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS); if (!dir.exists()) dir.mkdirs();
            java.io.File file = new java.io.File(dir, "Salah_Report_" + System.currentTimeMillis() + ".png");
            java.io.FileOutputStream fos = new java.io.FileOutputStream(file); bitmap.compress(Bitmap.CompressFormat.PNG, 100, fos); fos.flush(); fos.close();
            android.os.StrictMode.VmPolicy.Builder builder = new android.os.StrictMode.VmPolicy.Builder(); android.os.StrictMode.setVmPolicy(builder.build());
            Intent intent = new Intent(Intent.ACTION_SEND); intent.setType("image/png"); intent.putExtra(Intent.EXTRA_STREAM, android.net.Uri.fromFile(file)); intent.putExtra(Intent.EXTRA_TEXT, "Alhamdulillah! Check out my Salah progress."); activity.startActivity(Intent.createChooser(intent, "Share via"));
        } catch (Exception e) {}
    }

    private void drawReportCard(Canvas canvas, Paint paint, float x, float y, float w, float h, int accentColor, String title, String value) {
        paint.setColor(themeColors[1]); canvas.drawRoundRect(new RectF(x, y, x+w, y+h), 50, 50, paint); 
        paint.setColor(accentColor); canvas.drawRoundRect(new RectF(x, y, x+40, y+h), 50, 50, paint); canvas.drawRect(x+20, y, x+40, y+h, paint); 
        paint.setColor(themeColors[3]); paint.setTextAlign(Paint.Align.LEFT); paint.setTextSize(50); paint.setTypeface(appFonts[0]); canvas.drawText(title, x+90, y+110, paint); 
        paint.setColor(accentColor); paint.setTextSize(110); paint.setTypeface(appFonts[1]); canvas.drawText(value, x+90, y+230, paint);
    }

    // ✨ THE SUPERFAST PDF ENGINE WITH ROOM ✨
    public void syncDate(java.util.Date d) { if(d != null) statsCalPointer.setTime(d); }

    public void exportPdf() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            int pdfWidth = 650;
            int pdfHeight = 1950;
            
            PdfDocument document = new PdfDocument();
            PdfDocument.PageInfo pageInfo = new PdfDocument.PageInfo.Builder(pdfWidth, pdfHeight, 1).create(); 
            PdfDocument.Page page = document.startPage(pageInfo);
            Canvas canvas = page.getCanvas(); Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);

            // Background
            paint.setColor(Color.WHITE); canvas.drawRect(0, 0, pdfWidth, pdfHeight, paint);

            // Beautiful Large Header
            paint.setColor(colorAccent);
            Path headerPath = new Path(); headerPath.moveTo(0, 0); headerPath.lineTo(pdfWidth, 0); headerPath.lineTo(pdfWidth, 180);
            headerPath.cubicTo(pdfWidth/2f, 220, 0, 180, 0, 180); headerPath.close();
            canvas.drawPath(headerPath, paint);

            // Title
            paint.setColor(Color.WHITE); paint.setTextSize(38); paint.setTypeface(Typeface.create(appFonts[1], Typeface.BOLD)); paint.setTextAlign(Paint.Align.CENTER);
            canvas.drawText("My Salah Tracker", pdfWidth/2f, 75, paint);
            
            String monthName = new SimpleDateFormat("MMMM yyyy", Locale.US).format(statsCalPointer.getTime());
            if(isBn) { monthName = lang.get(new SimpleDateFormat("MMMM", Locale.US).format(statsCalPointer.getTime())) + " " + lang.bnNum(statsCalPointer.get(Calendar.YEAR)); }
            paint.setTextSize(18); paint.setTypeface(appFonts[0]); paint.setAlpha(220);
            canvas.drawText((isBn ? "মাসিক রিপোর্ট • " : "Monthly Report • ") + monthName, pdfWidth/2f, 115, paint); paint.setAlpha(255);

            Calendar cal = (Calendar) statsCalPointer.clone(); cal.set(Calendar.DAY_OF_MONTH, 1);
            int totalDaysInMonth = cal.getActualMaximum(Calendar.DAY_OF_MONTH);
            int totalDaysPassed = 0, totalDone = 0, totalMissed = 0, totalExcused = 0, totalQaza = 0;
            Calendar now = Calendar.getInstance(); SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);

            for(int i=1; i<=totalDaysInMonth; i++) {
                cal.set(Calendar.DAY_OF_MONTH, i); String dKey = sdf.format(cal.getTime());
                if(cal.after(now) && !dKey.equals(sdf.format(now.getTime()))) continue;
                totalDaysPassed++;
                
                SalahRecord r = getRoomRecord(dKey);
                for(String p : prayers) {
                    String stat = getFardStat(r, p); boolean isQaza = getQazaStat(r, p);
                    if(stat.equals("yes")) totalDone++; else if(stat.equals("excused")) totalExcused++; else { if(isQaza) totalQaza++; else totalMissed++; }
                }
            }

            // 3 Columns Cards Layout
            float startY = 200; float padding = 30; float cardW = (pdfWidth - (padding*4)) / 3f; float cardH = 75;
            drawPdfCardBig(canvas, paint, padding, startY, cardW, cardH, colorAccent, isBn?"মোট দিন":"Total Days", lang.bnNum(totalDaysPassed));
            drawPdfCardBig(canvas, paint, padding*2 + cardW, startY, cardW, cardH, Color.parseColor("#3B82F6"), isBn?"আদায়কৃত":"Prayers Done", lang.bnNum(totalDone));
            drawPdfCardBig(canvas, paint, padding*3 + cardW*2, startY, cardW, cardH, Color.parseColor("#FF5252"), isBn?"কাজা হয়েছে":"Missed", lang.bnNum(totalMissed));
            
            drawPdfCardBig(canvas, paint, padding, startY + cardH + 20, cardW, cardH, Color.parseColor("#FF9500"), isBn?"অপেক্ষমান কাজা":"Pending Qaza", lang.bnNum(totalQaza));
            drawPdfCardBig(canvas, paint, padding*2 + cardW, startY + cardH + 20, cardW, cardH, Color.parseColor("#FF4081"), isBn?"পিরিয়ড/ছুটি":"Excused Mode", lang.bnNum(totalExcused));
            drawPdfCardBig(canvas, paint, padding*3 + cardW*2, startY + cardH + 20, cardW, cardH, Color.parseColor("#9B59B6"), isBn?"বর্তমান স্ট্রিক":"Current Streak", lang.bnNum(ui.calculateStreak(sp, prayers)));

            // 1. Centered Monthly Calendar Grid
            float calStartY = startY + (cardH*2) + 70;
            paint.setColor(Color.parseColor("#333333")); paint.setTextSize(22); paint.setTypeface(Typeface.create(appFonts[1], Typeface.BOLD)); paint.setTextAlign(Paint.Align.LEFT);
            canvas.drawText(isBn ? "মাসিক ক্যালেন্ডার ওভারভিউ" : "Monthly Calendar Overview", padding, calStartY, paint);

            String[] daysStr = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
            if(isBn) daysStr = new String[]{"রবি", "সোম", "মঙ্গল", "বুধ", "বৃহঃ", "শুক্র", "শনি"};
            
            float calWidth = 460; float colW = calWidth / 7f; float calX = (pdfWidth - calWidth) / 2f; float rowH = 50;
            paint.setTextSize(14); paint.setTypeface(appFonts[0]); paint.setColor(Color.parseColor("#888888")); paint.setTextAlign(Paint.Align.CENTER);
            for(int i=0; i<7; i++) canvas.drawText(daysStr[i], calX + (i*colW) + (colW/2f), calStartY + 45, paint);

            cal.set(Calendar.DAY_OF_MONTH, 1); int offset = cal.get(Calendar.DAY_OF_WEEK) - 1;
            float gridY = calStartY + 75;

            for(int i=1; i<=totalDaysInMonth; i++) {
                int r = (offset + i - 1) / 7; int c = (offset + i - 1) % 7;
                float cx = calX + (c*colW) + (colW/2f); float cy = gridY + (r*rowH);
                cal.set(Calendar.DAY_OF_MONTH, i); String dKey = sdf.format(cal.getTime());
                
                SalahRecord rec = getRoomRecord(dKey);
                boolean allDone = true; boolean hasMissed = false; boolean hasExcused = false;
                for(String p : prayers) { String st = getFardStat(rec, p); if(st.equals("no")) { allDone = false; hasMissed = true; } if(st.equals("excused")) hasExcused = true; }
                
                float radius = 18f;
                if(cal.after(now) && !dKey.equals(sdf.format(now.getTime()))) { 
                    paint.setColor(Color.parseColor("#F5F6FA")); paint.setStyle(Paint.Style.FILL); canvas.drawCircle(cx, cy, radius, paint); 
                } 
                else if (allDone || hasExcused) { 
                    paint.setColor(colorAccent); paint.setStyle(Paint.Style.STROKE); paint.setStrokeWidth(3f); canvas.drawCircle(cx, cy, radius, paint); paint.setStyle(Paint.Style.FILL);
                } 
                else { 
                    paint.setColor(Color.parseColor("#FFEBEE")); paint.setStyle(Paint.Style.FILL); canvas.drawCircle(cx, cy, radius, paint); 
                }

                paint.setColor(Color.parseColor("#333333")); paint.setTextSize(14); paint.setTypeface(Typeface.create(appFonts[1], Typeface.BOLD)); canvas.drawText(lang.bnNum(i), cx, cy+5, paint);
            }

            // 2. Weekly Detail (Charts!)
            int totalRows = (int) Math.ceil((totalDaysInMonth + offset) / 7.0);
            float weekStartY = gridY + (totalRows * rowH) + 40;
            paint.setColor(Color.parseColor("#333333")); paint.setTextSize(22); paint.setTypeface(Typeface.create(appFonts[1], Typeface.BOLD)); paint.setTextAlign(Paint.Align.LEFT);
            canvas.drawText(isBn ? "সাপ্তাহিক বিস্তারিত (ফজর থেকে বিতর)" : "Weekly Detail (Fard & Sunnah)", padding, weekStartY, paint);

            float wY = weekStartY + 30; 
            float weekCardH = 120f; 
            float barGap = 20f;
            
            for(int w=1; w<=totalRows; w++) {
                int sDay = (w==1) ? 1 : ((w-1)*7 - offset + 1); int eDay = Math.min(w*7 - offset, totalDaysInMonth);
                if(sDay > totalDaysInMonth) break;

                Calendar tempS = (Calendar) statsCalPointer.clone(); tempS.set(Calendar.DAY_OF_MONTH, sDay);
                Calendar tempE = (Calendar) statsCalPointer.clone(); tempE.set(Calendar.DAY_OF_MONTH, eDay);
                SimpleDateFormat sdfMMM = new SimpleDateFormat("MMM", Locale.US);
                String sDateStr = isBn ? (lang.bnNum(sDay) + " " + lang.get(sdfMMM.format(tempS.getTime()))) : (sdfMMM.format(tempS.getTime()) + " " + String.format("%02d", sDay));
                String eDateStr = isBn ? (lang.bnNum(eDay) + " " + lang.get(sdfMMM.format(tempE.getTime()))) : (sdfMMM.format(tempE.getTime()) + " " + String.format("%02d", eDay));
                String wTitle = (isBn ? "সপ্তাহ " : "Week ") + lang.bnNum(w) + " (" + sDateStr + " - " + eDateStr + ")";

                paint.setColor(Color.parseColor("#FAFAFC")); canvas.drawRoundRect(new RectF(padding, wY, pdfWidth-padding, wY+weekCardH), 15, 15, paint);
                paint.setColor(Color.parseColor("#555555")); paint.setTextSize(14); paint.setTypeface(Typeface.create(appFonts[1], Typeface.BOLD)); paint.setTextAlign(Paint.Align.LEFT);
                canvas.drawText(wTitle, padding+20, wY+30, paint);

                float chartAreaW = pdfWidth - (padding * 2) - 40; float colW_Chart = chartAreaW / 7f; float chartXStart = padding + 20;
                
                for(int d=sDay; d<=eDay; d++) {
                    cal.set(Calendar.DAY_OF_MONTH, d); int dayOfWeek = cal.get(Calendar.DAY_OF_WEEK) - 1; 
                    String dK = sdf.format(cal.getTime());
                    float cx = chartXStart + (dayOfWeek * colW_Chart) + (colW_Chart/2f);
                    
                    int fardDone = 0; int sunnahDone = 0;
                    if(cal.before(now) || dK.equals(sdf.format(now.getTime()))) {
                        SalahRecord r = getRoomRecord(dK);
                        for(int p=0; p<prayers.length; p++) { 
                            String fardSt = getFardStat(r, prayers[p]);
                            if(fardSt.equals("yes") || fardSt.equals("excused")) fardDone++; 
                            for(String sName : AppConstants.SUNNAHS[p]) { if(sp.getString(dK+"_"+prayers[p]+"_Sunnah_"+sName, "no").equals("yes")) sunnahDone++; }
                        }
                    }
                    
                    float maxBarH = 50f; float leftH = (fardDone / 6f) * maxBarH; float rightH = (sunnahDone / 12f) * maxBarH;
                    if(leftH < 3 && fardDone > 0) leftH = 3; if(rightH < 3 && sunnahDone > 0) rightH = 3;
                    
                    int leftColor = colorAccent; int rightColor = Color.parseColor("#FFCA28"); 
                    if(cal.after(now) && !dK.equals(sdf.format(now.getTime()))) { leftColor = Color.parseColor("#EAECEE"); rightColor = Color.parseColor("#EAECEE"); leftH = maxBarH; rightH = maxBarH; }
                    else if(fardDone == 0 && sunnahDone == 0) { leftColor = Color.parseColor("#E2E8F0"); rightColor = Color.parseColor("#F1F5F9"); leftH=maxBarH; rightH=maxBarH*0.7f; }

                    float baseLineY = wY + 90f;

                    paint.setColor(leftColor); canvas.drawRoundRect(new RectF(cx - 8, baseLineY - leftH, cx - 2, baseLineY), 3f, 3f, paint);
                    paint.setColor(rightColor); canvas.drawRoundRect(new RectF(cx + 2, baseLineY - rightH, cx + 8, baseLineY), 3f, 3f, paint);
                    
                    paint.setColor(Color.parseColor("#AAAAAA")); paint.setTextSize(10); paint.setTypeface(appFonts[0]); paint.setTextAlign(Paint.Align.CENTER);
                    String dayLabel = daysStr[dayOfWeek] + " " + lang.bnNum(d); canvas.drawText(dayLabel, cx, baseLineY + 18, paint);
                }
                wY += weekCardH + barGap;
            }

            paint.setColor(Color.parseColor("#AAAAAA")); paint.setTextSize(12); paint.setTypeface(appFonts[0]); paint.setTextAlign(Paint.Align.CENTER);
            canvas.drawText(isBn ? "My Salah Tracker অ্যাপের মাধ্যমে তৈরি" : "Generated by My Salah Tracker", pdfWidth/2f, pdfHeight - 40, paint);

            document.finishPage(page);
            File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS); if (!dir.exists()) dir.mkdirs();
            File file = new File(dir, "Salah_Report_" + System.currentTimeMillis() + ".pdf"); document.writeTo(new FileOutputStream(file)); document.close();
            
            final File finalFile = file;
            
            ui.showSmartBanner((android.widget.FrameLayout) activity.findViewById(android.R.id.content), isBn?"সফল":"Success", isBn?"পিডিএফ সেভ হয়েছে (দেখতে ক্লিক করুন)":"PDF Saved (Click to view)", "img_tick", colorAccent, new Runnable() {
                @Override public void run() {
                    Intent intent = new Intent(Intent.ACTION_VIEW);
                    Uri contentUri = androidx.core.content.FileProvider.getUriForFile(activity, activity.getPackageName() + ".provider", finalFile);
                    intent.setDataAndType(contentUri, "application/pdf");
                    intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    intent.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY | Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    try { activity.startActivity(intent); } catch (Exception e) {}
                }
            });
        } catch(Exception e) {  ui.showSmartBanner((android.widget.FrameLayout) activity.findViewById(android.R.id.content), "Error", "Storage permission required.", "img_warning", colorAccent, null); }
    }

    private void drawPdfCardBig(Canvas canvas, Paint paint, float x, float y, float w, float h, int accent, String title, String val) {
        paint.setColor(Color.parseColor("#F8F9F9")); canvas.drawRoundRect(new RectF(x, y, x+w, y+h), 14, 14, paint);
        paint.setColor(accent); canvas.drawRoundRect(new RectF(x, y, x+8, y+h), 14, 14, paint); canvas.drawRect(x+4, y, x+8, y+h, paint);
        paint.setColor(Color.parseColor("#7F8C8D")); paint.setTextSize(14); paint.setTypeface(appFonts[0]); paint.setTextAlign(Paint.Align.LEFT); canvas.drawText(title, x+22, y+30, paint);
        paint.setColor(accent); paint.setTextSize(26); paint.setTypeface(appFonts[1]); canvas.drawText(val, x+22, y+60, paint);
    }

    public void showStats(final boolean isWeekly) {
        // statsCalPointer.setTime(new Date()); Removed to keep history 
        AlertDialog.Builder builder = new AlertDialog.Builder(activity);
        final LinearLayout wrap = new LinearLayout(activity); wrap.setGravity(Gravity.CENTER); wrap.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));
        final LinearLayout card = new LinearLayout(activity); 
        card.setOrientation(LinearLayout.VERTICAL); card.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); card.setGravity(Gravity.CENTER_HORIZONTAL);
        GradientDrawable cardBg = new GradientDrawable(); cardBg.setColor(themeColors[1]); cardBg.setCornerRadius(30f * DENSITY); card.setBackground(cardBg); wrap.addView(card, new LinearLayout.LayoutParams(-1, -2));
        final AlertDialog dialog = builder.setView(wrap).create(); dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent); dialog.getWindow().setGravity(Gravity.CENTER); 
        renderStats(card, dialog, isWeekly); dialog.show();
    }
    
    private void renderStats(final LinearLayout card, final AlertDialog dialog, final boolean isWeekly) {
        card.removeAllViews();
        LinearLayout nav = new LinearLayout(activity); nav.setGravity(Gravity.CENTER_VERTICAL); nav.setPadding(0, 0, 0, (int)(25*DENSITY));
        TextView prev = new TextView(activity); prev.setText("❮"); prev.setTextSize(22); prev.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY)); prev.setTextColor(colorAccent);
        prev.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { if(isWeekly) statsCalPointer.add(Calendar.DATE, -7); else statsCalPointer.add(Calendar.MONTH, -1); renderStats(card, dialog, isWeekly); } });
        final Calendar temp = (Calendar) statsCalPointer.clone(); final int totalDays = isWeekly ? 7 : temp.getActualMaximum(Calendar.DAY_OF_MONTH);
        if(isWeekly) while (temp.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) temp.add(Calendar.DATE, -1); else temp.set(Calendar.DAY_OF_MONTH, 1);
        final Calendar startCal = (Calendar) temp.clone(); Calendar endCal = (Calendar) startCal.clone(); endCal.add(Calendar.DATE, 6);
        
        TextView title = new TextView(activity); SimpleDateFormat mF = new SimpleDateFormat("MMMM", Locale.US);
        String titleStr = isWeekly ? "📊 " + lang.getShortGreg(startCal.getTime()) + " - " + lang.getShortGreg(endCal.getTime()) : "📊 " + lang.get(mF.format(statsCalPointer.getTime())) + " " + lang.bnNum(statsCalPointer.get(Calendar.YEAR));
        title.setText(titleStr); title.setTextColor(themeColors[2]); title.setTextSize(16); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); title.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
        
        TextView next = new TextView(activity); next.setText("❯"); next.setTextSize(22); next.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));
        final Calendar now = Calendar.getInstance(); final boolean isFuture; if(isWeekly) { Calendar nextWeekStart = (Calendar) startCal.clone(); nextWeekStart.add(Calendar.DATE, 7); isFuture = nextWeekStart.after(now); } else { isFuture = (statsCalPointer.get(Calendar.YEAR) > now.get(Calendar.YEAR)) || (statsCalPointer.get(Calendar.YEAR) == now.get(Calendar.YEAR) && statsCalPointer.get(Calendar.MONTH) >= now.get(Calendar.MONTH)); }
        next.setTextColor(isFuture ? themeColors[4] : colorAccent);
        next.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { if(!isFuture){ if(isWeekly) statsCalPointer.add(Calendar.DATE, 7); else statsCalPointer.add(Calendar.MONTH, 1); renderStats(card, dialog, isWeekly); } } });
        nav.addView(prev); nav.addView(title); nav.addView(next); card.addView(nav);

        final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
        int daysPassed = 0; int totalCompleted = 0; int totalExcused = 0; Calendar calcCal = (Calendar) startCal.clone(); String todayStr = sdf.format(now.getTime());
        java.util.ArrayList<com.github.mikephil.charting.data.BarEntry> entries = new java.util.ArrayList<>(); java.util.ArrayList<Integer> colors = new java.util.ArrayList<>(); String[] labelsArr = new String[totalDays];

        for(int i=0; i<totalDays; i++) { 
            String dK = sdf.format(calcCal.getTime()); int count = 0; int excCount = 0;
            if(calcCal.before(now) || dK.equals(todayStr)) { 
                daysPassed++; 
                SalahRecord r = getRoomRecord(dK);
                for(String p : prayers) { String st = getFardStat(r, p); if(st.equals("yes")) count++; else if(st.equals("excused")) excCount++; } 
                totalCompleted += count; totalExcused += excCount;
            } 
            float total = count + excCount; entries.add(new com.github.mikephil.charting.data.BarEntry((float)i, total));
            if (calcCal.after(now) && !dK.equals(todayStr)) { colors.add(themeColors[4]); } else if (total == 0) { colors.add(Color.parseColor("#FF5252")); } else if (excCount > 0) { colors.add(Color.parseColor("#FF4081")); } else { colors.add(colorAccent); } 
            labelsArr[i] = lang.bnNum(i+1); calcCal.add(Calendar.DATE, 1); 
        }

        int totalPossible = daysPassed * 6; int totalMissed = totalPossible - totalCompleted - totalExcused; if(totalMissed < 0) totalMissed = 0;
        com.github.mikephil.charting.charts.BarChart barChart = new com.github.mikephil.charting.charts.BarChart(activity); barChart.setLayoutParams(new LinearLayout.LayoutParams(-1, (int)(180 * DENSITY)));
        com.github.mikephil.charting.data.BarDataSet dataSet = new com.github.mikephil.charting.data.BarDataSet(entries, "Prayers"); dataSet.setColors(colors); dataSet.setDrawValues(false);
        com.github.mikephil.charting.data.BarData barData = new com.github.mikephil.charting.data.BarData(dataSet); barData.setBarWidth(0.5f); barChart.setData(barData);
        barChart.getDescription().setEnabled(false); barChart.getLegend().setEnabled(false); barChart.getAxisRight().setEnabled(false); barChart.getXAxis().setPosition(com.github.mikephil.charting.components.XAxis.XAxisPosition.BOTTOM); barChart.getXAxis().setDrawGridLines(false); barChart.getXAxis().setTextColor(themeColors[3]); barChart.getXAxis().setValueFormatter(new com.github.mikephil.charting.formatter.IndexAxisValueFormatter(labelsArr)); barChart.getAxisLeft().setDrawGridLines(true); barChart.getAxisLeft().setGridColor(themeColors[4]); barChart.getAxisLeft().setTextColor(themeColors[3]); barChart.getAxisLeft().setAxisMinimum(0f); barChart.getAxisLeft().setAxisMaximum(6f); barChart.getAxisLeft().setLabelCount(6, true); barChart.animateY(1000); card.addView(barChart);

        LinearLayout detailsRow = new LinearLayout(activity); detailsRow.setOrientation(LinearLayout.HORIZONTAL); detailsRow.setPadding(0, (int)(25*DENSITY), 0, (int)(10*DENSITY)); 
        LinearLayout b1 = new LinearLayout(activity); b1.setOrientation(LinearLayout.VERTICAL); b1.setGravity(Gravity.START | Gravity.CENTER_VERTICAL); b1.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
        TextView t1 = new TextView(activity); t1.setText(lang.bnNum(totalCompleted)); t1.setTextSize(24); t1.setTypeface(Typeface.DEFAULT_BOLD); t1.setTextColor(colorAccent); TextView l1 = new TextView(activity); l1.setText(lang.get("Prayers Done")); l1.setTextSize(11); l1.setTextColor(themeColors[3]); b1.addView(t1); b1.addView(l1);
        View space = new View(activity); space.setLayoutParams(new LinearLayout.LayoutParams(0, 0, 1f)); 
        LinearLayout b2 = new LinearLayout(activity); b2.setOrientation(LinearLayout.VERTICAL); b2.setGravity(Gravity.END | Gravity.CENTER_VERTICAL); b2.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
        TextView t2 = new TextView(activity); t2.setText(lang.bnNum(totalMissed)); t2.setTextSize(24); t2.setTypeface(Typeface.DEFAULT_BOLD); t2.setTextColor(Color.parseColor("#FF5252")); t2.setGravity(Gravity.END); TextView l2 = new TextView(activity); l2.setText(lang.get("Missed")); l2.setTextSize(11); l2.setTextColor(themeColors[3]); l2.setGravity(Gravity.END); b2.addView(t2); b2.addView(l2);
        detailsRow.addView(b1); detailsRow.addView(space); detailsRow.addView(b2); card.addView(detailsRow);
        
        TextView close = new TextView(activity); close.setText(lang.get("CLOSE")); close.setTextColor(themeColors[3]); close.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(5*DENSITY)); close.setTypeface(Typeface.DEFAULT_BOLD); close.setGravity(Gravity.CENTER); close.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { dialog.dismiss(); } }); card.addView(close); applyFont(card, appFonts[0], appFonts[1]);
    }
}