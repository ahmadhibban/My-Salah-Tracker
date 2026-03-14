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

public class StatsHelper
{
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

    public StatsHelper(Activity activity, float DENSITY, int[] themeColors, int colorAccent,
        LanguageEngine lang, UIComponents ui, SharedPreferences sp, String[] prayers,
        Typeface[] appFonts)
    {
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

    // ✨ ROOM DATABASE HELPERS FOR SUPERFAST STATS ✨
    private SalahRecord getRoomRecord(String date)
    {
        return SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(date);
    }

    private String getFardStat(SalahRecord r, String p)
    {
        if (r == null)
            return "no";
        switch (p) {
            case "Fajr":
                return r.fajr;
            case "Dhuhr":
                return r.dhuhr;
            case "Asr":
                return r.asr;
            case "Maghrib":
                return r.maghrib;
            case "Isha":
                return r.isha;
            case "Witr":
                return r.witr;
            default:
                return "no";
        }
    }

    private boolean getQazaStat(SalahRecord r, String p)
    {
        if (r == null)
            return false;
        switch (p) {
            case "Fajr":
                return r.fajr_qaza;
            case "Dhuhr":
                return r.dhuhr_qaza;
            case "Asr":
                return r.asr_qaza;
            case "Maghrib":
                return r.maghrib_qaza;
            case "Isha":
                return r.isha_qaza;
            case "Witr":
                return r.witr_qaza;
            default:
                return false;
        }
    }

    private int getTotalExtras(String dKey)
    {
        int c = 0;
        for (int p = 0; p < prayers.length; p++) {
            String pr = prayers[p];
            for (String sn : AppConstants.SUNNAHS[p])
                if ("yes".equals(sp.getString(dKey + "_" + pr + "_Sunnah_" + sn, "no")))
                    c++;
            String cStr = sp.getString("custom_nafl_" + pr, "");
            if (!cStr.isEmpty()) {
                for (String cN : cStr.split(",")) {
                    if (cN.contains(":"))
                        cN = cN.split(":")[0];
                    if ("yes".equals(sp.getString(dKey + "_" + pr + "_Custom_" + cN, "no")))
                        c++;
                }
            }
        }
        return c;
    }

    private void applyFont(View v, Typeface reg, Typeface bold)
    {
        if (v instanceof TextView) {
            TextView tv = (TextView) v;
            if (tv.getTypeface() != null && tv.getTypeface().isBold())
                tv.setTypeface(bold);
            else
                tv.setTypeface(reg);
        } else if (v instanceof ViewGroup) {
            ViewGroup vg = (ViewGroup) v;
            for (int i = 0; i < vg.getChildCount(); i++) applyFont(vg.getChildAt(i), reg, bold);
        }
    }

    public void exportXls()
    {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            java.io.File dir =
                activity.getExternalFilesDir(android.os.Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists())
                dir.mkdirs();
            java.io.File file = new java.io.File(
                dir, "Salah_Premium_Report_" + System.currentTimeMillis() + ".xls");
            java.io.PrintWriter pw = new java.io.PrintWriter(
                new java.io.OutputStreamWriter(new java.io.FileOutputStream(file), "UTF-8"));
            int tD = 0, tDn = 0, tM = 0, tE = 0, tQ = 0, tExt = 0;
            java.util.Calendar sumCal = (java.util.Calendar) statsCalPointer.clone();
            sumCal.set(5, 1);
            int mDays = sumCal.getActualMaximum(5);
            java.util.Calendar nowSum = java.util.Calendar.getInstance();
            java.text.SimpleDateFormat sdf =
                new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US);
            for (int j = 1; j <= mDays; j++) {
                sumCal.set(5, j);
                String dk = sdf.format(sumCal.getTime());
                if (sumCal.after(nowSum) && !dk.equals(sdf.format(nowSum.getTime())))
                    continue;
                tD++;
                SalahRecord rec = getRoomRecord(dk);
                if (rec != null) {
                    for (String p : prayers) {
                        String st = getFardStat(rec, p);
                        if (st.equals("yes"))
                            tDn++;
                        else if (st.equals("excused"))
                            tE++;
                        else {
                            if (getQazaStat(rec, p))
                                tQ++;
                            else
                                tM++;
                        }
                    }
                }
                tExt += getTotalExtras(dk);
            }
            int streak = ui.calculateStreak(sp, prayers);
            String title = (isBn ? "মাসিক রিপোর্ট • " : "Monthly Report • ")
                + new java.text.SimpleDateFormat("MMMM yyyy", java.util.Locale.US)
                      .format(statsCalPointer.getTime());
            StringBuilder xml = new StringBuilder();
            xml.append(
                "<?xml version=\"1.0\" encoding=\"UTF-8\"?><?mso-application progid=\"Excel.Sheet\"?><Workbook xmlns=\"urn:schemas-microsoft-com:office:spreadsheet\" xmlns:ss=\"urn:schemas-microsoft-com:office:spreadsheet\"><Styles><Style ss:ID=\"Default\" ss:Name=\"Normal\"><Alignment ss:Vertical=\"Center\"/></Style>");
            xml.append(
                "<Style ss:ID=\"sTitle\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"22\" ss:Bold=\"1\" ss:Color=\"#FFFFFF\"/><Interior ss:Color=\"#10B981\" ss:Pattern=\"Solid\"/></Style>");
            xml.append(
                "<Style ss:ID=\"sSumH\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"13\" ss:Bold=\"1\" ss:Color=\"#5F6368\"/><Interior ss:Color=\"#F8F9FA\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append(
                "<Style ss:ID=\"sSumV\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"16\" ss:Bold=\"1\" ss:Color=\"#202124\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\" ss:Color=\"#10B981\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append(
                "<Style ss:ID=\"sHead\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"14\" ss:Bold=\"1\" ss:Color=\"#FFFFFF\"/><Interior ss:Color=\"#334155\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\" ss:Color=\"#0F172A\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append(
                "<Style ss:ID=\"sDate\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#334155\"/><Interior ss:Color=\"#F8FAFC\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/></Borders></Style>");
            xml.append(
                "<Style ss:ID=\"sYes\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#059669\"/><Interior ss:Color=\"#D1FAE5\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/></Borders></Style>");
            xml.append(
                "<Style ss:ID=\"sNo\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#DC2626\"/><Interior ss:Color=\"#FEE2E2\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/></Borders></Style>");
            xml.append(
                "<Style ss:ID=\"sExc\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#7C3AED\"/><Interior ss:Color=\"#EDE9FE\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/></Borders></Style>");
            xml.append(
                "<Style ss:ID=\"sExt\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#D97706\"/><Interior ss:Color=\"#FEF3C7\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E2E8F0\"/></Borders></Style>");
            xml.append("</Styles><Worksheet ss:Name=\"Report\"><Table><Column ss:Width=\"150\"/>");
            for (int i = 0; i < 6; i++) xml.append("<Column ss:Width=\"115\"/>");
            xml.append("<Column ss:Width=\"130\"/><Column ss:Width=\"160\"/>");
            xml.append(
                "<Row ss:Height=\"70\"><Cell ss:MergeAcross=\"8\" ss:StyleID=\"sTitle\"><Data ss:Type=\"String\">"
                + title + "</Data></Cell></Row>");
            String em = sp.getString("user_email", "guest@salah.com");
            xml.append(
                "<Row ss:Height=\"30\"><Cell ss:MergeAcross=\"8\" ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">"
                + em
                + "</Data></Cell></Row><Row ss:Height=\"20\"><Cell><Data ss:Type=\"String\"></Data></Cell></Row>");
            xml.append("<Row ss:Height=\"40\"><Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">"
                + (isBn ? "মোট দিন" : "Total Days")
                + "</Data></Cell><Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">"
                + (isBn ? "আদায়কৃত" : "Done")
                + "</Data></Cell><Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">"
                + (isBn ? "কাজা" : "Missed")
                + "</Data></Cell><Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">"
                + (isBn ? "অপেক্ষমান কাজা" : "Pending Qaza")
                + "</Data></Cell><Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">"
                + (isBn ? "ছুটি" : "Excused")
                + "</Data></Cell><Cell ss:MergeAcross=\"1\" ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">"
                + (isBn ? "নফল/সুন্নাহ" : "Extras")
                + "</Data></Cell><Cell ss:MergeAcross=\"1\" ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">"
                + (isBn ? "স্ট্রিক" : "Streak") + "</Data></Cell></Row>");
            xml.append("<Row ss:Height=\"50\"><Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">"
                + lang.bnNum(tD)
                + "</Data></Cell><Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">"
                + lang.bnNum(tDn)
                + "</Data></Cell><Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">"
                + lang.bnNum(tM)
                + "</Data></Cell><Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">"
                + lang.bnNum(tQ)
                + "</Data></Cell><Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">"
                + lang.bnNum(tE)
                + "</Data></Cell><Cell ss:MergeAcross=\"1\" ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">"
                + lang.bnNum(tExt)
                + "</Data></Cell><Cell ss:MergeAcross=\"1\" ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">"
                + lang.bnNum(streak)
                + " ★</Data></Cell></Row><Row ss:Height=\"25\"><Cell><Data ss:Type=\"String\"></Data></Cell></Row>");
            xml.append("<Row ss:Height=\"45\">");
            String[] hdrs = isBn ? new String[] {"তারিখ", "ফজর", "যোহর", "আসর", "মাগরিব", "এশা",
                                "বিতর", "অতিরিক্ত (নফল)", "সারসংক্ষেপ"}
                                 : new String[] {"Date", "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha",
                                     "Witr", "Extras (Nafl)", "Status"};
            for (String h : hdrs)
                xml.append(
                    "<Cell ss:StyleID=\"sHead\"><Data ss:Type=\"String\">" + h + "</Data></Cell>");
            xml.append("</Row>");
            java.util.Calendar cal = (java.util.Calendar) statsCalPointer.clone();
            cal.set(5, 1);
            for (int i = 1; i <= mDays; i++) {
                cal.set(5, i);
                String dK = sdf.format(cal.getTime());
                SalahRecord r = getRoomRecord(dK);
                String dDisp = isBn ? lang.bnNum(i) + " "
                        + lang.get(new java.text.SimpleDateFormat("MMM", java.util.Locale.US)
                                       .format(cal.getTime()))
                        + ", " + lang.bnNum(cal.get(1))
                                    : dK;
                xml.append(
                    "<Row ss:Height=\"40\"><Cell ss:StyleID=\"sDate\"><Data ss:Type=\"String\">"
                    + dDisp + "</Data></Cell>");
                boolean aD = true;
                for (String p : prayers) {
                    String s = getFardStat(r, p);
                    String sty = s.equals("yes") ? "sYes" : (s.equals("excused") ? "sExc" : "sNo");
                    String txt = s.equals("yes")
                        ? "\u2713 " + (isBn ? "সম্পন্ন" : "Done")
                        : (s.equals("excused") ? "\u273F " + (isBn ? "ছুটি" : "Excused")
                                               : "\u2715 " + (isBn ? "কাজা" : "Missed"));
                    xml.append("<Cell ss:StyleID=\"" + sty + "\"><Data ss:Type=\"String\">" + txt
                        + "</Data></Cell>");
                    if (!s.equals("yes") && !s.equals("excused"))
                        aD = false;
                }
                int dEx = getTotalExtras(dK);
                String exTxt = dEx > 0 ? "+ " + lang.bnNum(dEx) : "-";
                xml.append("<Cell ss:StyleID=\"sExt\"><Data ss:Type=\"String\">" + exTxt
                    + "</Data></Cell>");
                String sSt = aD ? "sYes" : "sNo";
                String sTxt = aD ? (isBn ? "★ আলহামদুলিল্লাহ" : "★ Perfect")
                                 : (isBn ? "⚠ অসম্পূর্ণ" : "⚠ Incomplete");
                xml.append("<Cell ss:StyleID=\"" + sSt + "\"><Data ss:Type=\"String\">" + sTxt
                    + "</Data></Cell></Row>");
            }
            xml.append("</Table></Worksheet></Workbook>");
            pw.write(xml.toString());
            pw.close();
            final java.io.File fF = file;
            ui.showSmartBanner(
                (android.widget.FrameLayout) activity.findViewById(android.R.id.content),
                isBn ? "সফল" : "Success",
                isBn ? "XLS ফাইল সেভ হয়েছে (ওপেন করতে ক্লিক)" : "XLS Saved", "img_tick", colorAccent,
                () -> {
                    android.content.Intent i =
                        new android.content.Intent(android.content.Intent.ACTION_VIEW);
                    i.setDataAndType(androidx.core.content.FileProvider.getUriForFile(
                                         activity, activity.getPackageName() + ".provider", fF),
                        "application/vnd.ms-excel");
                    i.addFlags(1);
                    activity.startActivity(android.content.Intent.createChooser(i, "Open with..."));
                });
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void showStatsOptionsDialog()
    {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        FrameLayout wrap = new FrameLayout(activity);
        wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout main = new LinearLayout(activity);
        main.setOrientation(LinearLayout.VERTICAL);
        main.setPadding(
            (int) (25 * DENSITY), (int) (30 * DENSITY), (int) (25 * DENSITY), (int) (30 * DENSITY));
        GradientDrawable gd = new GradientDrawable();
        gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY);
        main.setBackground(gd);
        TextView title = new TextView(activity);
        title.setText(isBn ? "উন্নত পরিসংখ্যান" : "Advanced Statistics");
        title.setTextColor(themeColors[2]);
        title.setTextSize(20);
        title.setTypeface(Typeface.DEFAULT_BOLD);
        title.setPadding(0, 0, 0, (int) (20 * DENSITY));
        main.addView(title);
        final AlertDialog ad = new AlertDialog.Builder(activity).setView(wrap).create();
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(Gravity.CENTER);

        class BtnMaker
        {
            void add(String t, final Runnable act)
            {
                LinearLayout btn = new LinearLayout(activity);
                btn.setOrientation(LinearLayout.HORIZONTAL);
                btn.setGravity(Gravity.CENTER_VERTICAL);
                btn.setPadding((int) (15 * DENSITY), (int) (15 * DENSITY), (int) (15 * DENSITY),
                    (int) (15 * DENSITY));
                GradientDrawable bg = new GradientDrawable();
                bg.setColor(themeColors[4]);
                bg.setCornerRadius(15f * DENSITY);
                btn.setBackground(bg);
                LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2);
                lp.setMargins(0, 0, 0, (int) (10 * DENSITY));
                btn.setLayoutParams(lp);
                View dot = new View(activity);
                GradientDrawable dBg = new GradientDrawable();
                dBg.setShape(GradientDrawable.OVAL);
                dBg.setColor(colorAccent);
                dot.setBackground(dBg);
                dot.setLayoutParams(
                    new LinearLayout.LayoutParams((int) (10 * DENSITY), (int) (10 * DENSITY)));
                btn.addView(dot);
                TextView tv = new TextView(activity);
                tv.setText(t);
                tv.setTextColor(themeColors[2]);
                tv.setTextSize(16);
                tv.setTypeface(Typeface.DEFAULT_BOLD);
                tv.setPadding((int) (15 * DENSITY), 0, 0, 0);
                btn.addView(tv);
                btn.setOnClickListener(new View.OnClickListener() {
                    @Override public void onClick(View v)
                    {
                        ad.dismiss();
                        act.run();
                    }
                });
                main.addView(btn);
            }
        }
        BtnMaker bm = new BtnMaker();
        bm.add(isBn ? "সাপ্তাহিক পরিসংখ্যান" : "Weekly Statistics", new Runnable() {
            @Override public void run()
            {
                showStats(true);
            }
        });
        bm.add(isBn ? "মাসিক পরিসংখ্যান" : "Monthly Statistics", new Runnable() {
            @Override public void run()
            {
                showStats(false);
            }
        });
        bm.add(isBn ? "রিপোর্ট শেয়ার (ছবি)" : "Share Report (Image)", new Runnable() {
            @Override public void run()
            {
                showShareTypeDialog();
            }
        });
        bm.add(isBn ? "প্রিমিয়াম এক্সেল (XLS) এক্সপোর্ট" : "Export Premium XLS", new Runnable() {
            @Override public void run()
            {
                exportXls();
            }
        });
        bm.add(isBn ? "প্রিমিয়াম পিডিএফ এক্সপোর্ট" : "Export Premium PDF", new Runnable() {
            @Override public void run()
            {
                exportPdf();
            }
        });

        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int) (300 * DENSITY), -2);
        flp.gravity = Gravity.CENTER;
        wrap.addView(main, flp);
        applyFont(main, appFonts[0], appFonts[1]);
        if (!activity.isFinishing())
            ad.show();
    }

    private void showShareTypeDialog()
    {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        FrameLayout wrap = new FrameLayout(activity);
        wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout main = new LinearLayout(activity);
        main.setOrientation(LinearLayout.VERTICAL);
        main.setPadding(
            (int) (25 * DENSITY), (int) (30 * DENSITY), (int) (25 * DENSITY), (int) (30 * DENSITY));
        GradientDrawable gd = new GradientDrawable();
        gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY);
        main.setBackground(gd);
        TextView title = new TextView(activity);
        title.setText(isBn ? "রিপোর্টের ধরন নির্বাচন করুন" : "Select Report Type");
        title.setTextColor(themeColors[2]);
        title.setTextSize(20);
        title.setTypeface(Typeface.DEFAULT_BOLD);
        title.setGravity(Gravity.CENTER);
        title.setPadding(0, 0, 0, (int) (20 * DENSITY));
        main.addView(title);
        final AlertDialog ad = new AlertDialog.Builder(activity).setView(wrap).create();
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(Gravity.CENTER);

        View.OnClickListener clicker = new View.OnClickListener() {
            @Override public void onClick(View v)
            {
                ad.dismiss();
                boolean isWeekly = (boolean) v.getTag();
                shareImageReport(isWeekly);
            }
        };

        LinearLayout btn1 = new LinearLayout(activity);
        btn1.setPadding(
            (int) (15 * DENSITY), (int) (15 * DENSITY), (int) (15 * DENSITY), (int) (15 * DENSITY));
        btn1.setGravity(Gravity.CENTER);
        GradientDrawable bg1 = new GradientDrawable();
        bg1.setColor(colorAccent);
        bg1.setCornerRadius(15f * DENSITY);
        btn1.setBackground(bg1);
        btn1.setTag(true);
        btn1.setOnClickListener(clicker);
        TextView t1 = new TextView(activity);
        t1.setText(isBn ? "সাপ্তাহিক রিপোর্ট" : "Weekly Report");
        t1.setTextColor(android.graphics.Color.WHITE);
        t1.setTypeface(Typeface.DEFAULT_BOLD);
        btn1.addView(t1);
        main.addView(btn1);

        LinearLayout btn2 = new LinearLayout(activity);
        btn2.setPadding(
            (int) (15 * DENSITY), (int) (15 * DENSITY), (int) (15 * DENSITY), (int) (15 * DENSITY));
        btn2.setGravity(Gravity.CENTER);
        GradientDrawable bg2 = new GradientDrawable();
        bg2.setColor(themeColors[4]);
        bg2.setCornerRadius(15f * DENSITY);
        btn2.setBackground(bg2);
        btn2.setTag(false);
        btn2.setOnClickListener(clicker);
        LinearLayout.LayoutParams lp2 = new LinearLayout.LayoutParams(-1, -2);
        lp2.setMargins(0, (int) (10 * DENSITY), 0, 0);
        btn2.setLayoutParams(lp2);
        TextView t2 = new TextView(activity);
        t2.setText(isBn ? "মাসিক রিপোর্ট" : "Monthly Report");
        t2.setTextColor(themeColors[2]);
        t2.setTypeface(Typeface.DEFAULT_BOLD);
        btn2.addView(t2);
        main.addView(btn2);

        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int) (300 * DENSITY), -2);
        flp.gravity = Gravity.CENTER;
        wrap.addView(main, flp);
        applyFont(main, appFonts[0], appFonts[1]);
        if (!activity.isFinishing())
            ad.show();
    }

    public void shareImageReport(boolean isWeekly)
    {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            int w = 2160, h = 2850;
            android.graphics.Bitmap bm =
                android.graphics.Bitmap.createBitmap(w, h, android.graphics.Bitmap.Config.RGB_565);
            android.graphics.Canvas cv = new android.graphics.Canvas(bm);
            android.graphics.Paint pt = new android.graphics.Paint(1);
            pt.setColor(themeColors[0]);
            cv.drawRect(0, 0, w, h, pt);
            android.graphics.Path ph = new android.graphics.Path();
            ph.moveTo(0, 0);
            ph.lineTo(w, 0);
            ph.lineTo(w, 550);
            ph.cubicTo(w / 2f, 750, w / 2f, 350, 0, 550);
            ph.close();
            pt.setColor(colorAccent);
            cv.drawPath(ph, pt);
            pt.setColor(android.graphics.Color.WHITE);
            pt.setTextAlign(android.graphics.Paint.Align.CENTER);
            pt.setTextSize(120);
            pt.setTypeface(android.graphics.Typeface.create(appFonts[1], 1));
            cv.drawText("My Salah Tracker", w / 2f, 220, pt);
            pt.setTextSize(60);
            pt.setTypeface(appFonts[0]);
            String em = sp.getString("user_email", "guest@salah.com");
            if (em.length() > 25)
                em = em.substring(0, 22) + "...";
            cv.drawText(em, w / 2f, 320, pt);
            pt.setTextSize(70);
            pt.setTypeface(appFonts[1]);
            cv.drawText(isWeekly ? (isBn ? "সাপ্তাহিক রিপোর্ট" : "Weekly Report")
                                 : (isBn ? "মাসিক রিপোর্ট" : "Monthly Report"),
                w / 2f, 440, pt);
            java.util.Calendar eC = (java.util.Calendar) statsCalPointer.clone(),
                               sC = (java.util.Calendar) statsCalPointer.clone(),
                               now = java.util.Calendar.getInstance();
            if (isWeekly) {
                while (sC.get(7) != 7) sC.add(5, -1);
                eC = (java.util.Calendar) sC.clone();
                eC.add(5, 6);
                if (eC.after(now))
                    eC = now;
            } else {
                sC.set(5, 1);
                eC.set(5, sC.getActualMaximum(5));
                if (eC.after(now))
                    eC = now;
            }
            java.text.SimpleDateFormat sk = new java.text.SimpleDateFormat(
                                           "yyyy-MM-dd", java.util.Locale.US),
                                       sd = new java.text.SimpleDateFormat(
                                           "EEEE", java.util.Locale.US);
            String gR = lang.getShortGreg(sC.getTime()) + " - " + lang.getShortGreg(eC.getTime()),
                   hR = ui.getHijriDate(sC.getTime(), sp.getInt("hijri_offset", 0)) + " - "
                + ui.getHijriDate(eC.getTime(), sp.getInt("hijri_offset", 0));
            String sDy = lang.get(sd.format(sC.getTime())), eDy = lang.get(sd.format(eC.getTime()));
            if (isBn) {
                String[] bD = {
                    "রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার"};
                sDy = bD[sC.get(7) - 1];
                eDy = bD[eC.get(7) - 1];
            }
            pt.setColor(themeColors[2]);
            pt.setTextSize(55);
            pt.setTypeface(appFonts[1]);
            cv.drawText(gR, w / 2f, 750, pt);
            pt.setColor(themeColors[3]);
            pt.setTextSize(45);
            pt.setTypeface(appFonts[0]);
            cv.drawText(hR, w / 2f, 830, pt);
            cv.drawText(sDy + " - " + eDy, w / 2f, 900, pt);
            int tD = 0, tDn = 0, tM = 0, tE = 0, tQ = 0;
            java.util.Calendar lC = (java.util.Calendar) sC.clone();
            java.util.ArrayList<Float> dFV = new java.util.ArrayList<>(),
                                       dSV = new java.util.ArrayList<>();
            java.util.ArrayList<Integer> dC = new java.util.ArrayList<>();
            java.util.ArrayList<String> dL = new java.util.ArrayList<>();
            while (!lC.after(eC)) {
                tD++;
                String dK = sk.format(lC.getTime());
                SalahRecord r = getRoomRecord(dK);
                int dyDn = 0, dyE = 0, sC_cnt = 0;
                if (r != null) {
                    for (int p = 0; p < prayers.length; p++) {
                        String st = getFardStat(r, prayers[p]);
                        if (st.equals("yes")) {
                            tDn++;
                            dyDn++;
                        } else if (st.equals("excused")) {
                            tE++;
                            dyE++;
                        } else {
                            if (getQazaStat(r, prayers[p]))
                                tQ++;
                            else
                                tM++;
                        }
                    }
                    if (isWeekly)
                        sC_cnt += getTotalExtras(dK);
                }
                dFV.add((float) (dyDn + dyE));
                dSV.add((float) sC_cnt);
                if (lC.after(now) && !dK.equals(sk.format(now.getTime())))
                    dC.add(android.graphics.Color.TRANSPARENT);
                else if (dyDn + dyE == 0)
                    dC.add(android.graphics.Color.TRANSPARENT);
                else if (dyE > 0)
                    dC.add(android.graphics.Color.parseColor("#8B5CF6"));
                else
                    dC.add(android.graphics.Color.parseColor("#22C55E"));
                dL.add(isWeekly ? lang.get(sd.format(lC.getTime())).substring(0, 3)
                                : lang.bnNum(lC.get(5)));
                lC.add(5, 1);
            }
            float sY = 1050, pd = 80, cW = (w - (pd * 3)) / 2f, cH = 280;
            drawReportCard(cv, pt, pd, sY, cW, cH, colorAccent, isBn ? "মোট দিন" : "Total Days",
                lang.bnNum(tD));
            drawReportCard(cv, pt, pd * 2 + cW, sY, cW, cH,
                android.graphics.Color.parseColor("#3B82F6"),
                isBn ? "আদায়কৃত নামাজ" : "Prayers Done", lang.bnNum(tDn));
            drawReportCard(cv, pt, pd, sY + cH + 60, cW, cH,
                android.graphics.Color.parseColor("#FF5252"), isBn ? "কাজা হয়েছে" : "Missed",
                lang.bnNum(tM));
            drawReportCard(cv, pt, pd * 2 + cW, sY + cH + 60, cW, cH,
                android.graphics.Color.parseColor("#FF9500"),
                isBn ? "অপেক্ষমান কাজা" : "Pending Qaza", lang.bnNum(tQ));
            drawReportCard(cv, pt, pd, sY + (cH * 2) + 120, cW, cH,
                android.graphics.Color.parseColor("#8B5CF6"), isBn ? "পিরিয়ড/ছুটি" : "Excused Mode",
                lang.bnNum(tE));
            drawReportCard(cv, pt, pd * 2 + cW, sY + (cH * 2) + 120, cW, cH,
                android.graphics.Color.parseColor("#9B59B6"),
                isBn ? "বর্তমান স্ট্রিক" : "Current Streak",
                lang.bnNum(ui.calculateStreak(sp, prayers)));
            float cyY = sY + (cH * 3) + 200, cyH = 480;
            pt.setColor(themeColors[1]);
            cv.drawRoundRect(new android.graphics.RectF(pd, cyY, w - pd, cyY + cyH), 50, 50, pt);
            float cIW = w - (pd * 2) - 80, cCol = cIW / dFV.size(), mBH = cyH - 140;
            for (int i = 0; i < dFV.size(); i++) {
                float cx = pd + 40 + (i * cCol) + (cCol / 2f), fH = (dFV.get(i) / 6f) * mBH,
                      sH = (dSV.get(i) / 12f) * mBH;
                float bW = isWeekly ? 35 : 12;
                float gap = isWeekly ? 5 : 2;
                if (fH > 0) {
                    pt.setColor(dC.get(i));
                    cv.drawRoundRect(new android.graphics.RectF(cx - bW - gap, cyY + 60 + mBH - fH,
                                         cx - gap, cyY + 60 + mBH),
                        bW / 2f, bW / 2f, pt);
                }
                if (sH > 0) {
                    pt.setColor(android.graphics.Color.parseColor("#F59E0B"));
                    cv.drawRoundRect(new android.graphics.RectF(cx + gap, cyY + 60 + mBH - sH,
                                         cx + gap + bW, cyY + 60 + mBH),
                        bW / 2f, bW / 2f, pt);
                }
                pt.setColor(themeColors[3]);
                pt.setTextSize(isWeekly ? 35 : 24);
                pt.setTextAlign(android.graphics.Paint.Align.CENTER);
                pt.setTypeface(appFonts[0]);
                cv.drawText(dL.get(i), cx, cyY + cyH - 40, pt);
            }
            pt.setColor(themeColors[3]);
            pt.setTextAlign(android.graphics.Paint.Align.CENTER);
            pt.setTextSize(45);
            cv.drawText(
                isBn ? "My Salah Tracker অ্যাপের মাধ্যমে তৈরি" : "Generated by My Salah Tracker",
                w / 2f, h - 80, pt);
            java.io.File dir =
                activity.getExternalFilesDir(android.os.Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists())
                dir.mkdirs();
            java.io.File file =
                new java.io.File(dir, "Salah_Report_" + System.currentTimeMillis() + ".png");
            java.io.FileOutputStream fos = new java.io.FileOutputStream(file);
            bm.compress(android.graphics.Bitmap.CompressFormat.PNG, 100, fos);
            fos.flush();
            fos.close();
            android.os.StrictMode.VmPolicy.Builder b = new android.os.StrictMode.VmPolicy.Builder();
            android.os.StrictMode.setVmPolicy(b.build());
            android.content.Intent i =
                new android.content.Intent(android.content.Intent.ACTION_SEND);
            i.setType("image/png");
            i.putExtra(android.content.Intent.EXTRA_STREAM, android.net.Uri.fromFile(file));
            i.putExtra(
                android.content.Intent.EXTRA_TEXT, "Alhamdulillah! Check out my Salah progress.");
            activity.startActivity(android.content.Intent.createChooser(i, "Share via"));
        } catch (Exception e) {
            ui.showSmartBanner(
                (android.widget.FrameLayout) activity.findViewById(android.R.id.content),
                lang.get("Share Failed"), lang.get("Storage permission required."), "img_warning",
                colorAccent, null);
        }
    }

    private void drawReportCard(Canvas canvas, Paint paint, float x, float y, float w, float h,
        int accentColor, String title, String value)
    {
        paint.setColor(themeColors[1]);
        canvas.drawRoundRect(new RectF(x, y, x + w, y + h), 50, 50, paint);
        paint.setColor(accentColor);
        canvas.drawRoundRect(new RectF(x, y, x + 40, y + h), 50, 50, paint);
        canvas.drawRect(x + 20, y, x + 40, y + h, paint);
        paint.setColor(themeColors[3]);
        paint.setTextAlign(Paint.Align.LEFT);
        paint.setTextSize(50);
        paint.setTypeface(appFonts[0]);
        canvas.drawText(title, x + 90, y + 110, paint);
        paint.setColor(accentColor);
        paint.setTextSize(110);
        paint.setTypeface(appFonts[1]);
        canvas.drawText(value, x + 90, y + 230, paint);
    }

    // ✨ THE SUPERFAST PDF ENGINE WITH ROOM ✨
    public void syncDate(java.util.Date d)
    {
        if (d != null)
            statsCalPointer.setTime(d);
    }

    public void exportPdf()
    {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            int pw = 650, ph = 2500;
            android.graphics.pdf.PdfDocument doc = new android.graphics.pdf.PdfDocument();
            android.graphics.pdf.PdfDocument.PageInfo pi =
                new android.graphics.pdf.PdfDocument.PageInfo.Builder(pw, ph, 1).create();
            android.graphics.pdf.PdfDocument.Page pg = doc.startPage(pi);
            android.graphics.Canvas cv = pg.getCanvas();
            android.graphics.Paint pt = new android.graphics.Paint(1);
            pt.setColor(android.graphics.Color.WHITE);
            cv.drawRect(0, 0, pw, ph, pt);
            pt.setColor(colorAccent);
            android.graphics.Path hp = new android.graphics.Path();
            hp.moveTo(0, 0);
            hp.lineTo(pw, 0);
            hp.lineTo(pw, 180);
            hp.cubicTo(pw / 2f, 220, 0, 180, 0, 180);
            hp.close();
            cv.drawPath(hp, pt);
            pt.setColor(android.graphics.Color.WHITE);
            pt.setTextSize(38);
            pt.setTypeface(android.graphics.Typeface.create(appFonts[1], 1));
            pt.setTextAlign(android.graphics.Paint.Align.CENTER);
            cv.drawText("My Salah Tracker", pw / 2f, 65, pt);
            String em = sp.getString("user_email", "guest@salah.com");
            pt.setTextSize(16);
            pt.setTypeface(appFonts[0]);
            cv.drawText(em, pw / 2f, 95, pt);
            String mNm = new java.text.SimpleDateFormat("MMMM yyyy", java.util.Locale.US)
                             .format(statsCalPointer.getTime());
            if (isBn)
                mNm = lang.get(new java.text.SimpleDateFormat("MMMM", java.util.Locale.US)
                                   .format(statsCalPointer.getTime()))
                    + " " + lang.bnNum(statsCalPointer.get(java.util.Calendar.YEAR));
            pt.setTextSize(18);
            pt.setAlpha(220);
            cv.drawText((isBn ? "মাসিক রিপোর্ট • " : "Monthly Report • ") + mNm, pw / 2f, 135, pt);
            pt.setAlpha(255);
            java.util.Calendar cal = (java.util.Calendar) statsCalPointer.clone();
            cal.set(5, 1);
            int tD = cal.getActualMaximum(5);
            int dP = 0, tDn = 0, tM = 0, tE = 0, tQ = 0;
            java.util.Calendar now = java.util.Calendar.getInstance();
            java.text.SimpleDateFormat sdf =
                new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US);
            for (int i = 1; i <= tD; i++) {
                cal.set(5, i);
                String dK = sdf.format(cal.getTime());
                if (cal.after(now) && !dK.equals(sdf.format(now.getTime())))
                    continue;
                dP++;
                SalahRecord r = getRoomRecord(dK);
                if (r != null) {
                    for (String p : prayers) {
                        String st = getFardStat(r, p);
                        boolean isQ = getQazaStat(r, p);
                        if (st.equals("yes"))
                            tDn++;
                        else if (st.equals("excused"))
                            tE++;
                        else {
                            if (isQ)
                                tQ++;
                            else
                                tM++;
                        }
                    }
                }
            }
            float sY = 200, pd = 30, cW = (pw - (pd * 4)) / 3f, cH = 75;
            drawPdfCardBig(cv, pt, pd, sY, cW, cH, colorAccent, isBn ? "মোট দিন" : "Total Days",
                lang.bnNum(dP));
            drawPdfCardBig(cv, pt, pd * 2 + cW, sY, cW, cH,
                android.graphics.Color.parseColor("#3B82F6"), isBn ? "আদায়কৃত" : "Prayers Done",
                lang.bnNum(tDn));
            drawPdfCardBig(cv, pt, pd * 3 + cW * 2, sY, cW, cH,
                android.graphics.Color.parseColor("#FF5252"), isBn ? "কাজা হয়েছে" : "Missed",
                lang.bnNum(tM));
            drawPdfCardBig(cv, pt, pd, sY + cH + 20, cW, cH,
                android.graphics.Color.parseColor("#FF9500"),
                isBn ? "অপেক্ষমান কাজা" : "Pending Qaza", lang.bnNum(tQ));
            drawPdfCardBig(cv, pt, pd * 2 + cW, sY + cH + 20, cW, cH,
                android.graphics.Color.parseColor("#FF4081"), isBn ? "পিরিয়ড/ছুটি" : "Excused Mode",
                lang.bnNum(tE));
            drawPdfCardBig(cv, pt, pd * 3 + cW * 2, sY + cH + 20, cW, cH,
                android.graphics.Color.parseColor("#9B59B6"),
                isBn ? "বর্তমান স্ট্রিক" : "Current Streak",
                lang.bnNum(ui.calculateStreak(sp, prayers)));
            float cSY = sY + (cH * 2) + 70;
            pt.setColor(android.graphics.Color.parseColor("#333333"));
            pt.setTextSize(22);
            pt.setTypeface(android.graphics.Typeface.create(appFonts[1], 1));
            pt.setTextAlign(android.graphics.Paint.Align.LEFT);
            cv.drawText(
                isBn ? "মাসিক ক্যালেন্ডার ওভারভিউ" : "Monthly Calendar Overview", pd, cSY, pt);
            String[] ds = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
            if (isBn)
                ds = new String[] {"রবি", "সোম", "মঙ্গল", "বুধ", "বৃহঃ", "শুক্র", "শনি"};
            float clW = 460, clCol = clW / 7f, clX = (pw - clW) / 2f, rH = 50;
            pt.setTextSize(14);
            pt.setTypeface(appFonts[0]);
            pt.setColor(android.graphics.Color.parseColor("#888888"));
            pt.setTextAlign(android.graphics.Paint.Align.CENTER);
            for (int i = 0; i < 7; i++)
                cv.drawText(ds[i], clX + (i * clCol) + (clCol / 2f), cSY + 45, pt);
            cal.set(5, 1);
            int off = cal.get(7) - 1;
            float gY = cSY + 75;
            for (int i = 1; i <= tD; i++) {
                int r = (off + i - 1) / 7, c = (off + i - 1) % 7;
                float cx = clX + (c * clCol) + (clCol / 2f), cy = gY + (r * rH);
                cal.set(5, i);
                String dK = sdf.format(cal.getTime());
                SalahRecord rec = getRoomRecord(dK);
                int cArc = 0;
                boolean hEx = false;
                if (rec != null) {
                    for (String p : prayers) {
                        String st = getFardStat(rec, p);
                        if (st.equals("yes"))
                            cArc++;
                        else if (st.equals("excused")) {
                            cArc++;
                            hEx = true;
                        }
                    }
                }
                pt.setStyle(android.graphics.Paint.Style.STROKE);
                pt.setStrokeWidth(2f);
                pt.setColor(android.graphics.Color.parseColor("#F1F5F9"));
                cv.drawCircle(cx, cy, 18f, pt);
                if (cArc > 0 && !(cal.after(now) && !dK.equals(sdf.format(now.getTime())))) {
                    pt.setColor(cArc == 6 ? android.graphics.Color.parseColor("#22C55E")
                                          : (hEx ? android.graphics.Color.parseColor("#8B5CF6")
                                                 : android.graphics.Color.parseColor("#10B981")));
                    cv.drawArc(new android.graphics.RectF(cx - 18f, cy - 18f, cx + 18f, cy + 18f),
                        -90, 360f * (cArc / 6f), false, pt);
                }
                pt.setStyle(android.graphics.Paint.Style.FILL);
                pt.setColor(android.graphics.Color.parseColor("#333333"));
                pt.setTextSize(14);
                pt.setTypeface(android.graphics.Typeface.create(appFonts[1], 1));
                cv.drawText(lang.bnNum(i), cx, cy + 5, pt);
            }
            int tR = (int) Math.ceil((tD + off) / 7.0);
            float wSY = gY + (tR * rH) + 40;
            pt.setColor(android.graphics.Color.parseColor("#333333"));
            pt.setTextSize(22);
            pt.setTypeface(android.graphics.Typeface.create(appFonts[1], 1));
            pt.setTextAlign(android.graphics.Paint.Align.LEFT);
            cv.drawText(
                isBn ? "সাপ্তাহিক বিস্তারিত (ফজর থেকে বিতর)" : "Weekly Detail (Fard & Sunnah)", pd,
                wSY, pt);
            float wY = wSY + 30, wCH = 170f, bG = 20f;
            for (int w = 1; w <= tR; w++) {
                int sD = (w == 1) ? 1 : ((w - 1) * 7 - off + 1), eD = Math.min(w * 7 - off, tD);
                if (sD > tD)
                    break;
                java.util.Calendar tmpS = (java.util.Calendar) statsCalPointer.clone();
                tmpS.set(5, sD);
                java.util.Calendar tmpE = (java.util.Calendar) statsCalPointer.clone();
                tmpE.set(5, eD);
                java.text.SimpleDateFormat sm =
                    new java.text.SimpleDateFormat("MMM", java.util.Locale.US);
                String sDS = isBn ? (lang.bnNum(sD) + " " + lang.get(sm.format(tmpS.getTime())))
                                  : (sm.format(tmpS.getTime()) + " "
                                      + String.format(java.util.Locale.US, "%02d", sD));
                String eDS = isBn ? (lang.bnNum(eD) + " " + lang.get(sm.format(tmpE.getTime())))
                                  : (sm.format(tmpE.getTime()) + " "
                                      + String.format(java.util.Locale.US, "%02d", eD));
                String wT =
                    (isBn ? "সপ্তাহ " : "Week ") + lang.bnNum(w) + " (" + sDS + " - " + eDS + ")";
                pt.setColor(android.graphics.Color.parseColor("#FAFAFC"));
                cv.drawRoundRect(new android.graphics.RectF(pd, wY, pw - pd, wY + wCH), 15, 15, pt);
                pt.setColor(android.graphics.Color.parseColor("#555555"));
                pt.setTextSize(14);
                pt.setTypeface(android.graphics.Typeface.create(appFonts[1], 1));
                pt.setTextAlign(android.graphics.Paint.Align.LEFT);
                cv.drawText(wT, pd + 20, wY + 30, pt);
                float cAW = pw - (pd * 2) - 40, cCW = cAW / 7f, cXS = pd + 20;
                for (int d = sD; d <= eD; d++) {
                    cal.set(5, d);
                    int dw = cal.get(7) - 1;
                    String dK = sdf.format(cal.getTime());
                    float cx = cXS + (dw * cCW) + (cCW / 2f);
                    int fD = 0, sD_cnt = 0;
                    boolean hB = false;
                    if (cal.before(now) || dK.equals(sdf.format(now.getTime()))) {
                        SalahRecord rec = getRoomRecord(dK);
                        if (rec != null) {
                            for (int p = 0; p < prayers.length; p++) {
                                String fS = getFardStat(rec, prayers[p]);
                                if (fS.equals("yes"))
                                    fD++;
                                else if (fS.equals("excused")) {
                                    fD++;
                                    hB = true;
                                }
                            }
                            sD_cnt += getTotalExtras(dK);
                        }
                    }
                    float mBH = 90f, lH = (fD / 6f) * mBH, rH_b = (sD_cnt / 12f) * mBH,
                          bY = wY + 135f;
                    if (!(cal.after(now) && !dK.equals(sdf.format(now.getTime())))) {
                        if (fD > 0) {
                            pt.setColor(hB ? android.graphics.Color.parseColor("#8B5CF6")
                                           : android.graphics.Color.parseColor("#22C55E"));
                            cv.drawRoundRect(
                                new android.graphics.RectF(cx - 10, bY - lH, cx - 1, bY), 4.5f,
                                4.5f, pt);
                        }
                        if (sD_cnt > 0) {
                            pt.setColor(android.graphics.Color.parseColor("#F59E0B"));
                            cv.drawRoundRect(
                                new android.graphics.RectF(cx + 1, bY - rH_b, cx + 10, bY), 4.5f,
                                4.5f, pt);
                        }
                    }
                    pt.setColor(android.graphics.Color.parseColor("#AAAAAA"));
                    pt.setTextSize(10);
                    pt.setTypeface(appFonts[0]);
                    pt.setTextAlign(android.graphics.Paint.Align.CENTER);
                    cv.drawText(ds[dw] + " " + lang.bnNum(d), cx, bY + 18, pt);
                }
                wY += wCH + bG;
            }
            pt.setColor(android.graphics.Color.parseColor("#AAAAAA"));
            pt.setTextSize(12);
            pt.setTypeface(appFonts[0]);
            pt.setTextAlign(android.graphics.Paint.Align.CENTER);
            cv.drawText(
                isBn ? "My Salah Tracker অ্যাপের মাধ্যমে তৈরি" : "Generated by My Salah Tracker",
                pw / 2f, ph - 40, pt);
            doc.finishPage(pg);

            java.io.File dir =
                activity.getExternalFilesDir(android.os.Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists())
                dir.mkdirs();
            java.io.File file =
                new java.io.File(dir, "Salah_Report_" + System.currentTimeMillis() + ".pdf");
            doc.writeTo(new java.io.FileOutputStream(file));
            doc.close();
            final java.io.File fF = file;
            if (activity instanceof MainActivity) {
                android.widget.FrameLayout r = activity.findViewById(android.R.id.content);
                if (r != null && ui != null) {
                    ui.showSmartBanner(r, isBn ? "সফল" : "Success",
                        isBn ? "পিডিএফ সেভ হয়েছে (দেখতে ক্লিক করুন)" : "PDF Saved (Click to view)",
                        "img_tick", colorAccent, () -> {
                            android.content.Intent i =
                                new android.content.Intent(android.content.Intent.ACTION_VIEW);
                            android.net.Uri u = androidx.core.content.FileProvider.getUriForFile(
                                activity, activity.getPackageName() + ".provider", fF);
                            i.setDataAndType(u, "application/pdf");
                            i.addFlags(1);
                            i.setFlags(1073741824 | 1);
                            try {
                                activity.startActivity(i);
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        });
                }
            }
        } catch (Exception e) {
            if (activity instanceof MainActivity) {
                android.widget.FrameLayout r = activity.findViewById(android.R.id.content);
                if (r != null && ui != null)
                    ui.showSmartBanner(r, "Error", "Storage permission required.", "img_warning",
                        colorAccent, null);
            }
        }
    }

    private void drawPdfCardBig(Canvas canvas, Paint paint, float x, float y, float w, float h,
        int accent, String title, String val)
    {
        paint.setColor(Color.parseColor("#F8F9F9"));
        canvas.drawRoundRect(new RectF(x, y, x + w, y + h), 14, 14, paint);
        paint.setColor(accent);
        canvas.drawRoundRect(new RectF(x, y, x + 8, y + h), 14, 14, paint);
        canvas.drawRect(x + 4, y, x + 8, y + h, paint);
        paint.setColor(Color.parseColor("#7F8C8D"));
        paint.setTextSize(14);
        paint.setTypeface(appFonts[0]);
        paint.setTextAlign(Paint.Align.LEFT);
        canvas.drawText(title, x + 22, y + 30, paint);
        paint.setColor(accent);
        paint.setTextSize(26);
        paint.setTypeface(appFonts[1]);
        canvas.drawText(val, x + 22, y + 60, paint);
    }

    public void showStats(final boolean isWeekly)
    {
        // statsCalPointer.setTime(new Date()); Removed to keep history
        AlertDialog.Builder builder = new AlertDialog.Builder(activity);
        final LinearLayout wrap = new LinearLayout(activity);
        wrap.setGravity(Gravity.CENTER);
        wrap.setPadding(
            (int) (20 * DENSITY), (int) (20 * DENSITY), (int) (20 * DENSITY), (int) (20 * DENSITY));
        final LinearLayout card = new LinearLayout(activity);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(
            (int) (25 * DENSITY), (int) (30 * DENSITY), (int) (25 * DENSITY), (int) (30 * DENSITY));
        card.setGravity(Gravity.CENTER_HORIZONTAL);
        GradientDrawable cardBg = new GradientDrawable();
        cardBg.setColor(themeColors[1]);
        cardBg.setCornerRadius(30f * DENSITY);
        card.setBackground(cardBg);
        wrap.addView(card, new LinearLayout.LayoutParams(-1, -2));
        final AlertDialog dialog = builder.setView(wrap).create();
        dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        dialog.getWindow().setGravity(Gravity.CENTER);
        renderStats(card, dialog, isWeekly);
        if (!activity.isFinishing())
            dialog.show();
    }

    private void renderStats(final android.widget.LinearLayout card,
        final android.app.AlertDialog dialog, final boolean isWeekly)
    {
        card.removeAllViews();
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        android.widget.LinearLayout nav = new android.widget.LinearLayout(activity);
        nav.setGravity(android.view.Gravity.CENTER_VERTICAL);
        nav.setPadding(0, 0, 0, (int) (25 * DENSITY));
        android.widget.TextView prev = new android.widget.TextView(activity);
        prev.setText("❮");
        prev.setTextSize(22);
        prev.setPadding(
            (int) (15 * DENSITY), (int) (10 * DENSITY), (int) (15 * DENSITY), (int) (10 * DENSITY));
        prev.setTextColor(colorAccent);
        ui.addClickFeedback(prev);
        prev.setOnClickListener(v -> {
            java.util.Calendar check = (java.util.Calendar) statsCalPointer.clone();
            if (isWeekly)
                check.add(java.util.Calendar.DATE, -7);
            else
                check.add(java.util.Calendar.MONTH, -1);
            if (check.get(java.util.Calendar.YEAR)
                >= java.util.Calendar.getInstance().get(java.util.Calendar.YEAR) - 100) {
                if (isWeekly)
                    statsCalPointer.add(java.util.Calendar.DATE, -7);
                else
                    statsCalPointer.add(java.util.Calendar.MONTH, -1);
                renderStats(card, dialog, isWeekly);
            } else {
                ui.showSmartBanner(
                    (android.widget.FrameLayout) activity.findViewById(android.R.id.content),
                    lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."),
                    "img_warning", colorAccent, null);
            }
        });
        final java.util.Calendar temp = (java.util.Calendar) statsCalPointer.clone();
        final int totalDays = isWeekly ? 7 : temp.getActualMaximum(java.util.Calendar.DAY_OF_MONTH);
        if (isWeekly)
            while (temp.get(java.util.Calendar.DAY_OF_WEEK) != java.util.Calendar.SATURDAY)
                temp.add(java.util.Calendar.DATE, -1);
        else
            temp.set(java.util.Calendar.DAY_OF_MONTH, 1);
        final java.util.Calendar startCal = (java.util.Calendar) temp.clone();
        java.util.Calendar endCal = (java.util.Calendar) startCal.clone();
        endCal.add(java.util.Calendar.DATE, totalDays - 1);

        android.widget.TextView title = new android.widget.TextView(activity);
        java.text.SimpleDateFormat mF = new java.text.SimpleDateFormat("MMMM", java.util.Locale.US);
        title.setText(isWeekly ? "📊 " + lang.getShortGreg(startCal.getTime()) + " - "
                    + lang.getShortGreg(endCal.getTime())
                               : "📊 " + lang.get(mF.format(statsCalPointer.getTime())) + " "
                    + lang.bnNum(statsCalPointer.get(java.util.Calendar.YEAR)));
        title.setTextColor(themeColors[2]);
        title.setTextSize(16);
        title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        title.setGravity(android.view.Gravity.CENTER);
        title.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));

        android.widget.TextView next = new android.widget.TextView(activity);
        next.setText("❯");
        next.setTextSize(22);
        next.setPadding(
            (int) (15 * DENSITY), (int) (10 * DENSITY), (int) (15 * DENSITY), (int) (10 * DENSITY));
        final java.util.Calendar now = java.util.Calendar.getInstance();
        final boolean isFuture = isWeekly
            ? (startCal.after(now))
            : ((statsCalPointer.get(java.util.Calendar.YEAR) > now.get(java.util.Calendar.YEAR))
                || (statsCalPointer.get(java.util.Calendar.YEAR) == now.get(java.util.Calendar.YEAR)
                    && statsCalPointer.get(java.util.Calendar.MONTH)
                        >= now.get(java.util.Calendar.MONTH)));
        next.setTextColor(isFuture ? themeColors[4] : colorAccent);
        ui.addClickFeedback(next);
        next.setOnClickListener(v -> {
            if (!isFuture) {
                if (isWeekly)
                    statsCalPointer.add(java.util.Calendar.DATE, 7);
                else
                    statsCalPointer.add(java.util.Calendar.MONTH, 1);
                renderStats(card, dialog, isWeekly);
            } else {
                ui.showPremiumLocked(colorAccent);
            }
        });
        nav.addView(prev);
        nav.addView(title);
        nav.addView(next);
        card.addView(nav);

        java.util
            .ArrayList<com.github.mikephil.charting.data.BarEntry> fE = new java.util.ArrayList<>(),
                                                                   sE = new java.util.ArrayList<>();
        java.util.ArrayList<Integer> fC = new java.util.ArrayList<>();
        String[] lbls = new String[totalDays];
        java.text.SimpleDateFormat sdf =
            new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US);
        int tDone = 0, tExc = 0, tSun = 0, daysPassed = 0;

        for (int i = 0; i < totalDays; i++) {
            String dK = sdf.format(startCal.getTime());
            int d = 0, e = 0, s = 0;
            SalahRecord sR = getRoomRecord(dK);
            if (startCal.before(now) || dK.equals(sdf.format(now.getTime()))) {
                daysPassed++;
                if (sR != null) {
                    for (int j = 0; j < 6; j++) {
                        String st = getFardStat(sR, prayers[j]);
                        if ("yes".equals(st))
                            d++;
                        else if ("excused".equals(st))
                            e++;
                    }
                    if (isWeekly)
                        s += getTotalExtras(dK);
                }
                tDone += d;
                tExc += e;
                tSun += s;
            }
            float fVal = d + e;
            fE.add(new com.github.mikephil.charting.data.BarEntry(
                (Math.min(6f, s * (6f / 10f)) == 0) ? i : i - 0.2f, fVal));
            sE.add(new com.github.mikephil.charting.data.BarEntry(
                i + 0.2f, Math.min(6f, s * (6f / 10f))));
            fC.add(fVal == 0 ? android.graphics.Color.TRANSPARENT
                             : ((MainActivity) activity).getStatusColor(dK));
            lbls[i] = isWeekly ? new java.text.SimpleDateFormat("E", java.util.Locale.US)
                                     .format(startCal.getTime())
                                     .substring(0, 1)
                               : (isBn ? lang.bnNum(i + 1) : "" + (i + 1));
            if (isBn && isWeekly)
                lbls[i] = new String[] {"র", "সো", "ম", "বু", "বৃ", "শু",
                    "শ"}[startCal.get(java.util.Calendar.DAY_OF_WEEK) - 1];
            startCal.add(java.util.Calendar.DATE, 1);
        }

        com.github.mikephil.charting.charts.BarChart bc =
            new com.github.mikephil.charting.charts.BarChart(activity);
        bc.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, (int) (180 * DENSITY)));
        com.github.mikephil.charting.data.BarDataSet fs =
            new com.github.mikephil.charting.data.BarDataSet(fE, "Fard");
        fs.setColors(fC);
        fs.setDrawValues(false);
        com.github.mikephil.charting.data.BarData bd;
        com.github.mikephil.charting.data.BarDataSet ss =
            new com.github.mikephil.charting.data.BarDataSet(sE, "Sunnah");
        ss.setColor(android.graphics.Color.parseColor("#F59E0B"));
        ss.setDrawValues(false);
        bd = new com.github.mikephil.charting.data.BarData(fs, ss);
        bd.setBarWidth(0.3f);
        bc.getXAxis().setAxisMinimum(-0.5f);
        bc.getXAxis().setAxisMaximum(totalDays - 0.5f);
        bc.setData(bd);
        bc.setRenderer(new com.github.mikephil.charting.renderer.BarChartRenderer(
            bc, bc.getAnimator(), bc.getViewPortHandler()) {
            @Override
            public void drawDataSet(android.graphics.Canvas c,
                com.github.mikephil.charting.interfaces.datasets.IBarDataSet dataSet, int index)
            {
                for (int j = 0; j < dataSet.getEntryCount(); j++) {
                    com.github.mikephil.charting.data.BarEntry e = dataSet.getEntryForIndex(j);
                    if (e.getY() <= 0)
                        continue;
                    float[] pos = new float[] {e.getX() - 0.15f, e.getY(), e.getX() + 0.15f, 0};
                    mChart.getTransformer(dataSet.getAxisDependency()).pointValuesToPixel(pos);
                    mRenderPaint.setColor(dataSet.getColor(j));
                    c.drawRoundRect(new android.graphics.RectF(pos[0], pos[1], pos[2], pos[3]),
                        8f * DENSITY, 8f * DENSITY, mRenderPaint);
                }
            }
        });
        bc.getAxisLeft().setAxisMinimum(0);
        bc.getAxisLeft().setAxisMaximum(6.2f);
        bc.getAxisLeft().setGranularity(1f);
        bc.getXAxis().setPosition(
            com.github.mikephil.charting.components.XAxis.XAxisPosition.BOTTOM);
        bc.getXAxis().setDrawGridLines(false);
        bc.getXAxis().setTextColor(themeColors[3]);
        bc.getXAxis().setValueFormatter(
            new com.github.mikephil.charting.formatter.ValueFormatter() {
                @Override public String getFormattedValue(float v)
                {
                    int idx = Math.round(v);
                    return (idx >= 0 && idx < lbls.length) ? lbls[idx] : "";
                }
            });
        bc.getLegend().setEnabled(false);
        bc.getDescription().setEnabled(false);
        bc.getAxisRight().setEnabled(false);

        final java.util.Calendar sCalClick = (java.util.Calendar) temp.clone();
        if (isWeekly)
            while (sCalClick.get(java.util.Calendar.DAY_OF_WEEK) != java.util.Calendar.SATURDAY)
                sCalClick.add(java.util.Calendar.DATE, -1);
        else
            sCalClick.set(java.util.Calendar.DAY_OF_MONTH, 1);
        bc.setOnChartValueSelectedListener(
            new com.github.mikephil.charting.listener.OnChartValueSelectedListener() {
                @Override
                public void onValueSelected(com.github.mikephil.charting.data.Entry e,
                    com.github.mikephil.charting.highlight.Highlight h)
                {
                    int idx = Math.round(e.getX());
                    final java.util.Calendar tCal = (java.util.Calendar) sCalClick.clone();
                    tCal.add(java.util.Calendar.DATE, idx);
                    java.util.Calendar n = java.util.Calendar.getInstance();
                    if (tCal.after(n)
                        && !sdf.format(tCal.getTime()).equals(sdf.format(n.getTime()))) {
                        ui.showPremiumLocked(colorAccent);
                    } else if (tCal.get(java.util.Calendar.YEAR)
                        < n.get(java.util.Calendar.YEAR) - 100) {
                        android.widget.FrameLayout r = activity.findViewById(android.R.id.content);
                        if (r != null)
                            ui.showSmartBanner(r, lang.get("Limit Reached"),
                                lang.get("Cannot go back more than 100 years."), "img_warning",
                                colorAccent, null);
                    } else {
                        new android.os.Handler(android.os.Looper.getMainLooper())
                            .postDelayed(() -> {
                                dialog.dismiss();
                                if (activity instanceof MainActivity) {
                                    try {
                                        java.lang.reflect.Field f =
                                            MainActivity.class.getDeclaredField("selectedDate");
                                        f.setAccessible(true);
                                        String[] arr = (String[]) f.get(activity);
                                        arr[0] = sdf.format(tCal.getTime());
                                        java.lang.reflect.Method m =
                                            MainActivity.class.getDeclaredMethod("loadTodayPage");
                                        m.setAccessible(true);
                                        m.invoke(activity);
                                    } catch (Exception ex) {
                                        android.util.Log.e("SalahTracker", "Error", ex);
                                    }
                                }
                            }, 150);
                    }
                }
                @Override public void onNothingSelected() {}
            });
        card.addView(bc);

        android.widget.LinearLayout legBox = new android.widget.LinearLayout(activity);
        legBox.setGravity(android.view.Gravity.CENTER);
        legBox.setPadding(0, (int) (15 * DENSITY), 0, (int) (5 * DENSITY));
        String[] lN = isBn ? new String[] {"ফরজ", "সুন্নাহ", "ছুটি"}
                           : new String[] {"Fard", "Sunnah", "Excused"};
        int[] lC = new int[] {android.graphics.Color.parseColor("#22C55E"),
            android.graphics.Color.parseColor("#F59E0B"),
            android.graphics.Color.parseColor("#8B5CF6")};
        for (int i = 0; i < lN.length; i++) {
            android.widget.LinearLayout item = new android.widget.LinearLayout(activity);
            item.setGravity(android.view.Gravity.CENTER);
            item.setPadding((int) (10 * DENSITY), 0, (int) (10 * DENSITY), 0);
            android.view.View dot = new android.view.View(activity);
            dot.setLayoutParams(new android.widget.LinearLayout.LayoutParams(
                (int) (12 * DENSITY), (int) (12 * DENSITY)));
            android.graphics.drawable.GradientDrawable dGd =
                new android.graphics.drawable.GradientDrawable();
            dGd.setColor(lC[i]);
            dGd.setCornerRadius(6 * DENSITY);
            dot.setBackground(dGd);
            android.widget.TextView txt = new android.widget.TextView(activity);
            txt.setText(lN[i]);
            txt.setTextColor(themeColors[3]);
            txt.setTextSize(12);
            txt.setPadding((int) (5 * DENSITY), 0, 0, 0);
            item.addView(dot);
            item.addView(txt);
            legBox.addView(item);
        }
        card.addView(legBox);

        int tMiss = (daysPassed * 6) - tDone - tExc;
        if (tMiss < 0)
            tMiss = 0;
        android.widget.LinearLayout dRow = new android.widget.LinearLayout(activity);
        dRow.setPadding(0, (int) (25 * DENSITY), 0, (int) (10 * DENSITY));
        android.widget.LinearLayout b1 = new android.widget.LinearLayout(activity);
        b1.setOrientation(1);
        b1.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView t1 = new android.widget.TextView(activity);
        t1.setText(lang.bnNum(tDone));
        t1.setTextSize(24);
        t1.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        t1.setTextColor(android.graphics.Color.parseColor("#22C55E"));
        android.widget.TextView l1 = new android.widget.TextView(activity);
        l1.setText(isBn ? "ফরজ" : "Fard");
        l1.setTextSize(11);
        l1.setTextColor(themeColors[3]);
        b1.addView(t1);
        b1.addView(l1);
        dRow.addView(b1);
        android.widget.LinearLayout b3 = new android.widget.LinearLayout(activity);
        b3.setOrientation(1);
        b3.setGravity(17);
        b3.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView t3 = new android.widget.TextView(activity);
        t3.setText(lang.bnNum(tSun));
        t3.setTextSize(24);
        t3.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        t3.setTextColor(android.graphics.Color.parseColor("#F59E0B"));
        t3.setGravity(17);
        android.widget.TextView l3 = new android.widget.TextView(activity);
        l3.setText(isBn ? "সুন্নাহ" : "Sunnah");
        l3.setTextSize(11);
        l3.setTextColor(themeColors[3]);
        l3.setGravity(17);
        b3.addView(t3);
        b3.addView(l3);
        dRow.addView(b3);
        android.widget.LinearLayout b2 = new android.widget.LinearLayout(activity);
        b2.setOrientation(1);
        b2.setGravity(5);
        b2.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView t2 = new android.widget.TextView(activity);
        t2.setText(lang.bnNum(tMiss));
        t2.setTextSize(24);
        t2.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        t2.setTextColor(android.graphics.Color.parseColor("#FF5252"));
        t2.setGravity(5);
        android.widget.TextView l2 = new android.widget.TextView(activity);
        l2.setText(lang.get("Missed"));
        l2.setTextSize(11);
        l2.setTextColor(themeColors[3]);
        l2.setGravity(5);
        b2.addView(t2);
        b2.addView(l2);
        dRow.addView(b2);
        card.addView(dRow);

        android.widget.TextView close = new android.widget.TextView(activity);
        close.setText(lang.get("CLOSE"));
        close.setTextColor(themeColors[3]);
        close.setPadding(
            (int) (15 * DENSITY), (int) (15 * DENSITY), (int) (15 * DENSITY), (int) (5 * DENSITY));
        close.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        close.setGravity(17);
        ui.addClickFeedback(close);
        close.setOnClickListener(v -> {
            if (dialog != null)
                dialog.dismiss();
        });
        card.addView(close);
        applyFont(card, appFonts[0], appFonts[1]);
    }
}