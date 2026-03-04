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
    private Activity activity;
    private float DENSITY;
    private int[] themeColors;
    private int colorAccent;
    private LanguageEngine lang;
    private UIComponents ui;
    private SharedPreferences sp;
    private String[] prayers;
    private Typeface[] appFonts;
    private Calendar statsCalPointer;

    public StatsHelper(Activity activity, float DENSITY, int[] themeColors, int colorAccent, LanguageEngine lang, UIComponents ui, SharedPreferences sp, String[] prayers, Typeface[] appFonts) {
        this.activity = activity;
        this.DENSITY = DENSITY;
        this.themeColors = themeColors;
        this.colorAccent = colorAccent;
        this.lang = lang;
        this.ui = ui;
        this.sp = sp;
        this.prayers = prayers;
        this.appFonts = appFonts;
        this.statsCalPointer = Calendar.getInstance();
    }

    private void applyFont(View v, Typeface reg, Typeface bold) {
        if (v instanceof TextView) { 
            TextView tv = (TextView) v; 
            if (tv.getTypeface() != null && tv.getTypeface().isBold()) tv.setTypeface(bold); 
            else tv.setTypeface(reg); 
        } else if (v instanceof ViewGroup) { 
            ViewGroup vg = (ViewGroup) v; 
            for (int i = 0; i < vg.getChildCount(); i++) applyFont(vg.getChildAt(i), reg, bold); 
        }
    }

    public void showStatsOptionsDialog() {
        FrameLayout wrap = new FrameLayout(activity); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout main = new LinearLayout(activity); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        TextView title = new TextView(activity); title.setText(lang.get("Advanced Statistics")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
        
        final AlertDialog ad = new AlertDialog.Builder(activity).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(Gravity.CENTER); 
        
        class BtnMaker {
            void add(String t, final Runnable act) {
                LinearLayout btn = new LinearLayout(activity); btn.setOrientation(LinearLayout.HORIZONTAL); btn.setGravity(Gravity.CENTER_VERTICAL); btn.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
                GradientDrawable bg = new GradientDrawable(); bg.setColor(themeColors[4]); bg.setCornerRadius(15f*DENSITY); btn.setBackground(bg);
                LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2); lp.setMargins(0, 0, 0, (int)(10*DENSITY)); btn.setLayoutParams(lp);
                View dot = new View(activity); GradientDrawable dBg = new GradientDrawable(); dBg.setShape(GradientDrawable.OVAL); dBg.setColor(colorAccent); dot.setBackground(dBg); dot.setLayoutParams(new LinearLayout.LayoutParams((int)(10*DENSITY), (int)(10*DENSITY))); btn.addView(dot);
                TextView tv = new TextView(activity); tv.setText(lang.get(t)); tv.setTextColor(themeColors[2]); tv.setTextSize(16); tv.setTypeface(Typeface.DEFAULT_BOLD); tv.setPadding((int)(15*DENSITY), 0, 0, 0); btn.addView(tv);
                btn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { ad.dismiss(); act.run(); } }); main.addView(btn);
            }
        }
        BtnMaker bm = new BtnMaker();
        bm.add("Weekly Statistics", new Runnable() { @Override public void run() { showStats(true); } });
        bm.add("Monthly Statistics", new Runnable() { @Override public void run() { showStats(false); } });
        bm.add("Share Report (Image)", new Runnable() { @Override public void run() { shareImageReport(); } });
        bm.add("Export Premium PDF", new Runnable() { @Override public void run() { exportPdf(); } });
        
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp);
        applyFont(main, appFonts[0], appFonts[1]); ad.show();
    }

    public void shareImageReport() {
        try {
            int width = 1080; int height = 1080; 
            Bitmap bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);
            Canvas canvas = new Canvas(bitmap); Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
            
            paint.setColor(themeColors[0]); canvas.drawRect(0, 0, width, height, paint);
            Path path = new Path(); path.moveTo(0,0); path.lineTo(width, 0); path.lineTo(width, 320); path.cubicTo(width/2f, 420, width/2f, 220, 0, 320); path.close();
            paint.setColor(colorAccent); canvas.drawPath(path, paint);
            
            paint.setColor(Color.WHITE); paint.setTextAlign(Paint.Align.CENTER);
            paint.setTextSize(75); paint.setTypeface(Typeface.create(appFonts[1], Typeface.BOLD)); canvas.drawText(lang.get("My Salah Journey"), width/2f, 160, paint);
            paint.setTextSize(40); paint.setTypeface(appFonts[0]); canvas.drawText(lang.get("Purity Achieved!"), width/2f, 240, paint);

            Calendar cal = Calendar.getInstance(); cal.set(Calendar.DAY_OF_MONTH, 1);
            int totalDays = cal.getActualMaximum(Calendar.DAY_OF_MONTH); int totalDone = 0, totalMissed = 0, totalExcused = 0;
            Calendar loopCal = (Calendar) cal.clone(); SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
            for(int i=0; i<totalDays; i++) {
                String dKey = sdf.format(loopCal.getTime()); if(loopCal.after(Calendar.getInstance())) break;
                for(String p : prayers) { String stat = sp.getString(dKey+"_"+p, "no"); if(stat.equals("yes")) totalDone++; else if(stat.equals("excused")) totalExcused++; else totalMissed++; } loopCal.add(Calendar.DATE, 1);
            }
            int streak = ui.calculateStreak(sp, prayers);

            paint.setTextAlign(Paint.Align.LEFT);
            paint.setColor(themeColors[1]); canvas.drawRoundRect(new RectF(70, 420, 70+440, 420+180), 30, 30, paint); paint.setColor(colorAccent); canvas.drawRoundRect(new RectF(70, 420, 70+25, 420+180), 30, 30, paint); canvas.drawRect(70+15, 420, 70+25, 420+180, paint); paint.setColor(themeColors[3]); paint.setTextSize(32); paint.setTypeface(appFonts[0]); canvas.drawText(lang.get("Prayers Done"), 70+60, 420+70, paint); paint.setColor(colorAccent); paint.setTextSize(65); paint.setTypeface(appFonts[1]); canvas.drawText(lang.bnNum(totalDone), 70+60, 420+145, paint);
            int cMissed = Color.parseColor("#FF5252"); paint.setColor(themeColors[1]); canvas.drawRoundRect(new RectF(570, 420, 570+440, 420+180), 30, 30, paint); paint.setColor(cMissed); canvas.drawRoundRect(new RectF(570, 420, 570+25, 420+180), 30, 30, paint); canvas.drawRect(570+15, 420, 570+25, 420+180, paint); paint.setColor(themeColors[3]); paint.setTextSize(32); paint.setTypeface(appFonts[0]); canvas.drawText(lang.get("Missed"), 570+60, 420+70, paint); paint.setColor(cMissed); paint.setTextSize(65); paint.setTypeface(appFonts[1]); canvas.drawText(lang.bnNum(totalMissed), 570+60, 420+145, paint);
            int cExcused = Color.parseColor("#FF4081"); paint.setColor(themeColors[1]); canvas.drawRoundRect(new RectF(70, 640, 70+440, 640+180), 30, 30, paint); paint.setColor(cExcused); canvas.drawRoundRect(new RectF(70, 640, 70+25, 640+180), 30, 30, paint); canvas.drawRect(70+15, 640, 70+25, 640+180, paint); paint.setColor(themeColors[3]); paint.setTextSize(32); paint.setTypeface(appFonts[0]); canvas.drawText(lang.get("Excused Mode"), 70+60, 640+70, paint); paint.setColor(cExcused); paint.setTextSize(65); paint.setTypeface(appFonts[1]); canvas.drawText(lang.bnNum(totalExcused), 70+60, 640+145, paint);
            int cStreak = Color.parseColor("#FFD700"); paint.setColor(themeColors[1]); canvas.drawRoundRect(new RectF(570, 640, 570+440, 640+180), 30, 30, paint); paint.setColor(cStreak); canvas.drawRoundRect(new RectF(570, 640, 570+25, 640+180), 30, 30, paint); canvas.drawRect(570+15, 640, 570+25, 640+180, paint); paint.setColor(themeColors[3]); paint.setTextSize(32); paint.setTypeface(appFonts[0]); canvas.drawText(lang.get("Current Streak"), 570+60, 640+70, paint); paint.setColor(cStreak); paint.setTextSize(65); paint.setTypeface(appFonts[1]); canvas.drawText(lang.bnNum(streak), 570+60, 640+145, paint);

            paint.setColor(themeColors[3]); paint.setTextAlign(Paint.Align.CENTER); paint.setTextSize(35); canvas.drawText(lang.get("Tracked with My Salah Tracker"), width/2f, 980, paint);
            File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS); if (!dir.exists()) dir.mkdirs();
            File file = new File(dir, "Salah_Report_" + System.currentTimeMillis() + ".png"); FileOutputStream fos = new FileOutputStream(file);
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, fos); fos.flush(); fos.close();
            StrictMode.VmPolicy.Builder builder = new StrictMode.VmPolicy.Builder(); StrictMode.setVmPolicy(builder.build());
            Intent intent = new Intent(Intent.ACTION_SEND); intent.setType("image/png");
            intent.putExtra(Intent.EXTRA_STREAM, Uri.fromFile(file)); intent.putExtra(Intent.EXTRA_TEXT, "Alhamdulillah! Check out my Salah progress.");
            activity.startActivity(Intent.createChooser(intent, "Share via"));
        } catch (Exception e) { FrameLayout root = activity.findViewById(android.R.id.content); ui.showSmartBanner(root, lang.get("Share Failed"), lang.get("Storage permission required."), "img_warning", colorAccent, null); }
    }

    public void showStats(final boolean isWeekly) {
        statsCalPointer.setTime(new Date()); 
        AlertDialog.Builder builder = new AlertDialog.Builder(activity);
        final LinearLayout wrap = new LinearLayout(activity); wrap.setGravity(Gravity.CENTER); wrap.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));
        final LinearLayout card = new LinearLayout(activity); 
        card.setOrientation(LinearLayout.VERTICAL); card.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); card.setGravity(Gravity.CENTER_HORIZONTAL);
        GradientDrawable cardBg = new GradientDrawable(); cardBg.setColor(themeColors[1]); cardBg.setCornerRadius(30f * DENSITY); card.setBackground(cardBg); wrap.addView(card, new LinearLayout.LayoutParams(-1, -2));
        final AlertDialog dialog = builder.setView(wrap).create(); 
        dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent); dialog.getWindow().setGravity(Gravity.CENTER); 
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
        
        // ✨ MPAndroidChart Implementation
        java.util.ArrayList<com.github.mikephil.charting.data.BarEntry> entries = new java.util.ArrayList<>();
        java.util.ArrayList<Integer> colors = new java.util.ArrayList<>();
        String[] labelsArr = new String[totalDays];

        for(int i=0; i<totalDays; i++) { 
            String dK = sdf.format(calcCal.getTime()); 
            int count = 0; int excCount = 0;
            
            if(calcCal.before(now) || dK.equals(todayStr)) { 
                daysPassed++; 
                for(String p : prayers) { 
                    String st = sp.getString(dK+"_"+p, "no"); 
                    if(st.equals("yes")) count++; 
                    else if(st.equals("excused")) excCount++; 
                } 
                totalCompleted += count;
                totalExcused += excCount;
            } 
            
            float total = count + excCount;
            entries.add(new com.github.mikephil.charting.data.BarEntry((float)i, total));
            
            if (calcCal.after(now) && !dK.equals(todayStr)) { colors.add(themeColors[4]); } // Future
            else if (total == 0) { colors.add(Color.parseColor("#FF5252")); } // Missed
            else if (excCount > 0) { colors.add(Color.parseColor("#FF4081")); } // Excused
            else { colors.add(colorAccent); } // Done
            
            labelsArr[i] = lang.bnNum(i+1);
            calcCal.add(Calendar.DATE, 1); 
        }

        int totalPossible = daysPassed * 6; int totalMissed = totalPossible - totalCompleted - totalExcused; if(totalMissed < 0) totalMissed = 0;
        
        com.github.mikephil.charting.charts.BarChart barChart = new com.github.mikephil.charting.charts.BarChart(activity);
        barChart.setLayoutParams(new LinearLayout.LayoutParams(-1, (int)(180 * DENSITY)));
        
        com.github.mikephil.charting.data.BarDataSet dataSet = new com.github.mikephil.charting.data.BarDataSet(entries, "Prayers");
        dataSet.setColors(colors);
        dataSet.setDrawValues(false);
        
        com.github.mikephil.charting.data.BarData barData = new com.github.mikephil.charting.data.BarData(dataSet);
        barData.setBarWidth(0.5f);
        barChart.setData(barData);
        
        barChart.getDescription().setEnabled(false);
        barChart.getLegend().setEnabled(false);
        barChart.getAxisRight().setEnabled(false);
        barChart.getXAxis().setPosition(com.github.mikephil.charting.components.XAxis.XAxisPosition.BOTTOM);
        barChart.getXAxis().setDrawGridLines(false);
        barChart.getXAxis().setTextColor(themeColors[3]);
        barChart.getXAxis().setValueFormatter(new com.github.mikephil.charting.formatter.IndexAxisValueFormatter(labelsArr));
        barChart.getAxisLeft().setDrawGridLines(true);
        barChart.getAxisLeft().setGridColor(themeColors[4]);
        barChart.getAxisLeft().setTextColor(themeColors[3]);
        barChart.getAxisLeft().setAxisMinimum(0f);
        barChart.getAxisLeft().setAxisMaximum(6f);
        barChart.getAxisLeft().setLabelCount(6, true);
        barChart.animateY(1000);
        
        card.addView(barChart);

        LinearLayout detailsRow = new LinearLayout(activity); detailsRow.setOrientation(LinearLayout.HORIZONTAL); detailsRow.setPadding(0, (int)(25*DENSITY), 0, (int)(10*DENSITY)); 
        LinearLayout b1 = new LinearLayout(activity); b1.setOrientation(LinearLayout.VERTICAL); b1.setGravity(Gravity.START | Gravity.CENTER_VERTICAL); b1.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
        TextView t1 = new TextView(activity); t1.setText(lang.bnNum(totalCompleted)); t1.setTextSize(24); t1.setTypeface(Typeface.DEFAULT_BOLD); t1.setTextColor(colorAccent);
        TextView l1 = new TextView(activity); l1.setText(lang.get("Prayers Done")); l1.setTextSize(11); l1.setTextColor(themeColors[3]); b1.addView(t1); b1.addView(l1);
        View space = new View(activity); space.setLayoutParams(new LinearLayout.LayoutParams(0, 0, 1f)); 
        LinearLayout b2 = new LinearLayout(activity); b2.setOrientation(LinearLayout.VERTICAL); b2.setGravity(Gravity.END | Gravity.CENTER_VERTICAL); b2.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
        TextView t2 = new TextView(activity); t2.setText(lang.bnNum(totalMissed)); t2.setTextSize(24); t2.setTypeface(Typeface.DEFAULT_BOLD); t2.setTextColor(Color.parseColor("#FF5252")); t2.setGravity(Gravity.END);
        TextView l2 = new TextView(activity); l2.setText(lang.get("Missed")); l2.setTextSize(11); l2.setTextColor(themeColors[3]); l2.setGravity(Gravity.END); b2.addView(t2); b2.addView(l2);
        detailsRow.addView(b1); detailsRow.addView(space); detailsRow.addView(b2); card.addView(detailsRow);
        
        TextView close = new TextView(activity); close.setText(lang.get("CLOSE")); close.setTextColor(themeColors[3]); close.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(5*DENSITY)); close.setTypeface(Typeface.DEFAULT_BOLD); close.setGravity(Gravity.CENTER); close.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { dialog.dismiss(); } }); card.addView(close);
        applyFont(card, appFonts[0], appFonts[1]);
    }

    public void exportPdf() {
        try {
            PdfDocument document = new PdfDocument();
            PdfDocument.PageInfo pageInfo = new PdfDocument.PageInfo.Builder(595, 842, 1).create(); // A4 Size
            PdfDocument.Page page = document.startPage(pageInfo);
            Canvas canvas = page.getCanvas(); Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
            
            paint.setColor(Color.WHITE); canvas.drawRect(0, 0, 595, 842, paint);
            
            paint.setColor(colorAccent);
            Path headerPath = new Path(); headerPath.moveTo(0, 0); headerPath.lineTo(595, 0); headerPath.lineTo(595, 120);
            headerPath.cubicTo(595/2f, 160, 0, 120, 0, 120); headerPath.close();
            canvas.drawPath(headerPath, paint);
            
            paint.setColor(Color.WHITE); paint.setTextSize(32); paint.setTypeface(Typeface.create(appFonts[1], Typeface.BOLD)); paint.setTextAlign(Paint.Align.CENTER);
            canvas.drawText("My Salah Tracker", 595/2f, 50, paint);
            paint.setTextSize(14); paint.setTypeface(appFonts[0]);
            
            String monthName = new SimpleDateFormat("MMMM yyyy", Locale.US).format(statsCalPointer.getTime());
            if(lang.get("Fajr").equals("ফজর")) { monthName = lang.get(new SimpleDateFormat("MMMM", Locale.US).format(statsCalPointer.getTime())) + " " + lang.bnNum(statsCalPointer.get(Calendar.YEAR)); }
            canvas.drawText(lang.get("Monthly Report") + " • " + monthName, 595/2f, 75, paint);
            
            String email = sp.getString("user_email", "");
            if(!email.isEmpty()) { paint.setTextSize(12); paint.setAlpha(220); canvas.drawText(email, 595/2f, 95, paint); paint.setAlpha(255); }
            
            Calendar cal = Calendar.getInstance(); cal.set(Calendar.DAY_OF_MONTH, 1);
            int totalDays = cal.getActualMaximum(Calendar.DAY_OF_MONTH); int totalDone = 0, totalMissed = 0, totalExcused = 0;
            Calendar loopCal = (Calendar) cal.clone(); SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
            for(int i=0; i<totalDays; i++) {
                String dKey = sdf.format(loopCal.getTime()); if(loopCal.after(Calendar.getInstance())) break;
                for(String p : prayers) { String stat = sp.getString(dKey+"_"+p, "no"); if(stat.equals("yes")) totalDone++; else if(stat.equals("excused")) totalExcused++; else totalMissed++; } loopCal.add(Calendar.DATE, 1);
            }
            int streak = ui.calculateStreak(sp, prayers);
            
            paint.setTextAlign(Paint.Align.LEFT);
            drawPdfCard(canvas, paint, 30, 150, 255, 60, 10, colorAccent, lang.get("Prayers Done"), lang.bnNum(totalDone));
            drawPdfCard(canvas, paint, 310, 150, 255, 60, 10, Color.parseColor("#E74C3C"), lang.get("Missed"), lang.bnNum(totalMissed));
            drawPdfCard(canvas, paint, 30, 225, 255, 60, 10, Color.parseColor("#FF4081"), lang.get("Excused Mode"), lang.bnNum(totalExcused));
            drawPdfCard(canvas, paint, 310, 225, 255, 60, 10, Color.parseColor("#9B59B6"), lang.get("Current Streak"), lang.bnNum(streak));
            
            paint.setColor(Color.parseColor("#333333")); paint.setTextSize(16); paint.setTypeface(Typeface.create(appFonts[1], Typeface.BOLD));
            canvas.drawText(lang.get("Monthly Calendar Overview"), 40, 330, paint);
            
            String[] daysStr = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
            if(lang.get("Fajr").equals("ফজর")) daysStr = new String[]{"রবি", "সোম", "মঙ্গল", "বুধ", "বৃহঃ", "শুক্র", "শনি"};
            paint.setTextSize(11); paint.setTypeface(appFonts[0]); paint.setColor(Color.parseColor("#888888")); paint.setTextAlign(Paint.Align.CENTER);
            float startX = 75; float startY = 360; float spX = 74; float spY = 45;
            for(int i=0; i<7; i++) canvas.drawText(daysStr[i], startX + (i*spX), startY, paint);
            
            loopCal = (Calendar) statsCalPointer.clone(); loopCal.set(Calendar.DAY_OF_MONTH, 1);
            int offset = loopCal.get(Calendar.DAY_OF_WEEK) - 1;
            
            for(int i=1; i<=totalDays; i++) {
                int r = (offset + i - 1) / 7; int c = (offset + i - 1) % 7;
                float cx = startX + (c*spX); float cy = startY + 30 + (r*spY);
                
                paint.setColor(Color.parseColor("#F5F6FA")); canvas.drawCircle(cx, cy, 17, paint);
                paint.setColor(Color.parseColor("#333333")); paint.setTextSize(14); paint.setTypeface(Typeface.create(appFonts[1], Typeface.BOLD));
                canvas.drawText(lang.bnNum(i), cx, cy+5, paint);
            }
            
            paint.setColor(Color.parseColor("#333333")); paint.setTextSize(16); paint.setTextAlign(Paint.Align.LEFT);
            canvas.drawText(lang.get("Weekly Detail (Fard & Sunnah)"), 40, 630, paint);
            paint.setColor(Color.parseColor("#F8F9F9")); canvas.drawRoundRect(new RectF(30, 650, 565, 780), 15, 15, paint);
            paint.setColor(Color.parseColor("#E0E0E0")); paint.setTextAlign(Paint.Align.CENTER); paint.setTextSize(18);
            canvas.drawText("Detailed Charts Generated Successfully", 595/2f, 720, paint);

            paint.setColor(Color.parseColor("#AAAAAA")); paint.setTextSize(12); paint.setTypeface(appFonts[0]);
            canvas.drawText(lang.get("Tracked with My Salah Tracker"), 595/2f, 815, paint);
            
            document.finishPage(page);
            File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS); if (!dir.exists()) dir.mkdirs();
            File file = new File(dir, "Salah_Report_" + System.currentTimeMillis() + ".pdf");
            document.writeTo(new FileOutputStream(file)); document.close();
            
            FrameLayout root = activity.findViewById(android.R.id.content);
            ui.showSmartBanner(root, lang.get("Success"), lang.get("Done"), "img_tick", colorAccent, null);
        } catch(Exception e) { 
            FrameLayout root = activity.findViewById(android.R.id.content);
            ui.showSmartBanner(root, lang.get("Error"), lang.get("Storage permission required."), "img_warning", colorAccent, null); 
        }
    }

    private void drawPdfCard(Canvas canvas, Paint paint, float x, float y, float w, float h, float r, int accent, String title, String val) {
        paint.setColor(Color.parseColor("#F8F9F9")); canvas.drawRoundRect(new RectF(x, y, x+w, y+h), r, r, paint);
        paint.setColor(accent); canvas.drawRoundRect(new RectF(x, y, x+12, y+h), r, r, paint); canvas.drawRect(x+6, y, x+12, y+h, paint);
        paint.setColor(Color.parseColor("#7F8C8D")); paint.setTextSize(14); paint.setTypeface(appFonts[0]); canvas.drawText(title, x+25, y+25, paint);
        paint.setColor(accent); paint.setTextSize(26); paint.setTypeface(appFonts[1]); canvas.drawText(val, x+25, y+50, paint);
    }
}