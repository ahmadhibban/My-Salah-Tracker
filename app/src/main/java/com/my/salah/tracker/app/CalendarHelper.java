package com.my.salah.tracker.app;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.icu.util.IslamicCalendar;
import android.os.Build;
import android.view.Gravity;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public class CalendarHelper {
    private Activity activity;
    private float DENSITY;
    private int[] themeColors;
    private int colorAccent;
    private LanguageEngine lang;
    private UIComponents ui;
    private SharedPreferences sp;
    private String[] prayers;
    private String[] selectedDate;
    private Calendar calendarViewPointer;
    private Calendar hijriViewCal;
    private SimpleDateFormat sdf;
    private SimpleDateFormat monthOnlyF;
    private Runnable onDateSelected;
    private android.graphics.Typeface tfReg, tfBold;

    public CalendarHelper(Activity activity, float DENSITY, int[] themeColors, int colorAccent, LanguageEngine lang, UIComponents ui, SharedPreferences sp, String[] prayers, String[] selectedDate, Calendar calendarViewPointer, Runnable onDateSelected) {
        this.activity = activity;
        this.DENSITY = DENSITY;
        this.themeColors = themeColors;
        this.colorAccent = colorAccent;
        this.lang = lang;
        this.ui = ui;
        this.sp = sp;
        this.prayers = prayers;
        this.selectedDate = selectedDate;
        this.calendarViewPointer = calendarViewPointer;
        this.onDateSelected = onDateSelected;
        this.sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
        this.monthOnlyF = new SimpleDateFormat("MMMM", sp.getString("app_lang", "en").equals("bn") ? new Locale("bn") : Locale.US);
                this.hijriViewCal = Calendar.getInstance();
        tfReg = android.graphics.Typeface.DEFAULT; tfBold = android.graphics.Typeface.DEFAULT_BOLD;
        try { if (sp.getString("app_lang", "en").equals("bn")) { tfReg = android.graphics.Typeface.createFromAsset(activity.getAssets(), "fonts/hind_reg.ttf"); tfBold = android.graphics.Typeface.createFromAsset(activity.getAssets(), "fonts/hind_bold.ttf"); } else { tfReg = android.graphics.Typeface.createFromAsset(activity.getAssets(), "fonts/poppins_reg.ttf"); tfBold = android.graphics.Typeface.createFromAsset(activity.getAssets(), "fonts/poppins_bold.ttf"); } } catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); }
    }

    
    private void applyFont(android.view.View v) {
        if (v instanceof android.widget.TextView) { 
            android.widget.TextView tv = (android.widget.TextView) v;
            if (tv.getTypeface() != null && tv.getTypeface().isBold()) tv.setTypeface(tfBold); else tv.setTypeface(tfReg); 
        } else if (v instanceof android.view.ViewGroup) { 
            android.view.ViewGroup vg = (android.view.ViewGroup) v;
            for (int i = 0; i < vg.getChildCount(); i++) applyFont(vg.getChildAt(i));
        }
    }
    public void showGregorian() {
        calendarViewPointer.setTime(new Date()); 
        FrameLayout wrap = new FrameLayout(activity); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout calCard = new LinearLayout(activity); calCard.setOrientation(LinearLayout.VERTICAL); calCard.setPadding((int)(20*DENSITY), (int)(25*DENSITY), (int)(20*DENSITY), (int)(25*DENSITY)); calCard.setGravity(Gravity.CENTER_HORIZONTAL);
        GradientDrawable cardBg = new GradientDrawable(); cardBg.setColor(themeColors[1]); cardBg.setCornerRadius(25f * DENSITY); cardBg.setStroke((int)(1.5f*DENSITY), themeColors[4]); calCard.setBackground(cardBg); 
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams(-1, -2); flp.gravity = Gravity.CENTER; flp.setMargins((int)(20*DENSITY), 0, (int)(20*DENSITY), 0); wrap.addView(calCard, flp);
        
        final AlertDialog dialog = new AlertDialog.Builder(activity).setView(wrap).create(); 
        dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        dialog.getWindow().setGravity(Gravity.CENTER); // ডায়ালগ মাঝখানে রাখার কোড
        
        renderGregorian(calCard, dialog); 
        applyFont(wrap); dialog.show();
    }

    private void renderGregorian(final LinearLayout card, final AlertDialog dialog) {
        card.removeAllViews();
        LinearLayout yearContainer = new LinearLayout(activity); yearContainer.setGravity(Gravity.CENTER); yearContainer.setPadding(0, 0, 0, (int)(10*DENSITY));
        TextView yearBtn = new TextView(activity); yearBtn.setText("" + lang.bnNum(calendarViewPointer.get(Calendar.YEAR))); yearBtn.setTextColor(colorAccent); yearBtn.setTypeface(Typeface.DEFAULT_BOLD); yearBtn.setPadding((int)(25*DENSITY), (int)(8*DENSITY), (int)(25*DENSITY), (int)(8*DENSITY));
        GradientDrawable yBg = new GradientDrawable(); yBg.setColor(colorAccent & 0x15FFFFFF); yBg.setCornerRadius(15f * DENSITY); yearBtn.setBackground(yBg);
        yearBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showYearPicker(card, dialog); } });
        yearContainer.addView(yearBtn); card.addView(yearContainer);

        LinearLayout nav = new LinearLayout(activity); nav.setGravity(Gravity.CENTER_VERTICAL); nav.setPadding(0, (int)(2*DENSITY), 0, (int)(15*DENSITY));
        TextView prev = new TextView(activity); prev.setText("❮"); prev.setTextSize(22); prev.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY)); prev.setTextColor(colorAccent);
        prev.setOnClickListener(new View.OnClickListener() { 
            @Override public void onClick(View v) { 
                Calendar check = (Calendar) calendarViewPointer.clone(); check.add(Calendar.MONTH, -1);
                if(check.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { 
                    calendarViewPointer.add(Calendar.MONTH, -1); renderGregorian(card, dialog); 
                } else { ui.showSmartBanner((android.widget.FrameLayout)activity.findViewById(android.R.id.content), lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); }
            } 
        });
        
        TextView title = new TextView(activity); title.setText(lang.get(monthOnlyF.format(calendarViewPointer.getTime()))); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD); title.setGravity(Gravity.CENTER); title.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
        TextView next = new TextView(activity); next.setText("❯"); next.setTextSize(22); next.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));
        final Calendar now = Calendar.getInstance(); final boolean isFutureMonth = (calendarViewPointer.get(Calendar.YEAR) > now.get(Calendar.YEAR)) || (calendarViewPointer.get(Calendar.YEAR) == now.get(Calendar.YEAR) && calendarViewPointer.get(Calendar.MONTH) >= now.get(Calendar.MONTH));
        next.setTextColor(isFutureMonth ? Color.LTGRAY : colorAccent);
        next.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { if(!isFutureMonth){ calendarViewPointer.add(Calendar.MONTH, 1); renderGregorian(card, dialog); } } });
        nav.addView(prev); nav.addView(title); nav.addView(next); card.addView(nav);

        LinearLayout daysRow = new LinearLayout(activity); String[] days = {"S", "M", "T", "W", "T", "F", "S"};
        if (lang.get("Fajr").equals("ফজর")) days = new String[]{"র", "সো", "ম", "বু", "বৃ", "শু", "শ"};
        for(String d : days) { TextView tv = new TextView(activity); tv.setText(d); tv.setGravity(Gravity.CENTER); tv.setTextColor(themeColors[3]); tv.setTextSize(12); tv.setTypeface(Typeface.DEFAULT_BOLD); tv.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f)); daysRow.addView(tv); }
        card.addView(daysRow);

        Calendar temp = (Calendar) calendarViewPointer.clone(); temp.set(Calendar.DAY_OF_MONTH, 1);
        int offset = temp.get(Calendar.DAY_OF_WEEK) - 1; int totalDays = temp.getActualMaximum(Calendar.DAY_OF_MONTH); int currentDay = 1;
        int cellHeight = (int)(46 * DENSITY + 0.5f); int boxSize = (int)(36 * DENSITY + 0.5f); 

        LinearLayout gridContainer = new LinearLayout(activity); gridContainer.setOrientation(LinearLayout.VERTICAL);
        for (int row = 0; row < 6; row++) {
            LinearLayout rowLay = new LinearLayout(activity);
            for (int col = 0; col < 7; col++) {
                FrameLayout cell = new FrameLayout(activity); cell.setLayoutParams(new LinearLayout.LayoutParams(0, cellHeight, 1f));
                if (!((row == 0 && col < offset) || currentDay > totalDays)) {
                    final int dayNum = currentDay; temp.set(Calendar.DAY_OF_MONTH, dayNum); final String dKey = sdf.format(temp.getTime()); final boolean isFuture = temp.after(now); final boolean isTooOld = temp.get(Calendar.YEAR) < now.get(Calendar.YEAR) - 100;
                    TextView tv = new TextView(activity); tv.setText(lang.bnNum(dayNum)); tv.setTextColor(isFuture ? Color.LTGRAY : themeColors[2]); tv.setTextSize(13); tv.setGravity(Gravity.CENTER);
                    FrameLayout.LayoutParams boxLp = new FrameLayout.LayoutParams(boxSize, boxSize); boxLp.gravity = Gravity.CENTER; tv.setLayoutParams(boxLp);
                    boolean isAllDone = true;
                    for(String p : prayers) { if(!sp.getString(dKey+"_"+p, "no").equals("yes") && !sp.getString(dKey+"_"+p, "no").equals("excused")) { isAllDone = false; break; } }
                    tv.setTextColor(dKey.equals(selectedDate[0]) ? android.graphics.Color.WHITE : (isFuture ? android.graphics.Color.LTGRAY : (isAllDone ? colorAccent : themeColors[2])));
                    boolean isDayCompleted = true;
                    SalahRecord dRec = SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(dKey);
                    if(dRec != null) {
                        for(String p : prayers) {
                            String st = "no";
                            if(p.equals("Fajr")) st = dRec.fajr; else if(p.equals("Dhuhr")) st = dRec.dhuhr;
                            else if(p.equals("Asr")) st = dRec.asr; else if(p.equals("Maghrib")) st = dRec.maghrib;
                            else if(p.equals("Isha")) st = dRec.isha; else if(p.equals("Witr")) st = dRec.witr;
                            if(!st.equals("yes") && !st.equals("excused")) { isDayCompleted = false; break; }
                        }
                    } else { isDayCompleted = false; }
                    
                    tv.setTextColor(dKey.equals(selectedDate[0]) ? android.graphics.Color.WHITE : (isFuture ? themeColors[4] : (isDayCompleted ? colorAccent : themeColors[2])));
                    GradientDrawable bgD = new GradientDrawable(); bgD.setShape(GradientDrawable.OVAL);
                    if (dKey.equals(selectedDate[0])) { bgD.setColor(colorAccent); tv.setBackground(((MainActivity)activity).getProgressBorder(dKey, dKey.equals(selectedDate[0]))); }
                    else if (isDayCompleted && !isFuture) { bgD.setColor(themeColors[5]); tv.setBackground(((MainActivity)activity).getProgressBorder(dKey, dKey.equals(selectedDate[0]))); }
                    else { bgD.setColor(android.graphics.Color.TRANSPARENT); tv.setBackground(((MainActivity)activity).getProgressBorder(dKey, dKey.equals(selectedDate[0]))); }
                    cell.addView(tv);
                    cell.setOnClickListener(new View.OnClickListener() { 
                        @Override public void onClick(View v) { 
                            if(isFuture) { ui.showPremiumLocked(colorAccent); } else if(isTooOld) { ui.showSmartBanner((android.widget.FrameLayout)activity.findViewById(android.R.id.content), lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); } else { selectedDate[0] = dKey; dialog.dismiss(); if(onDateSelected!=null) onDateSelected.run(); } 
                        } 
                    });
                    currentDay++;
                }
                rowLay.addView(cell);
            }
            gridContainer.addView(rowLay); if (currentDay > totalDays) break;
        }
        card.addView(gridContainer);
        TextView close = new TextView(activity); close.setText(lang.get("CLOSE")); close.setTextColor(themeColors[3]); close.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(5*DENSITY)); close.setTypeface(Typeface.DEFAULT_BOLD); close.setGravity(Gravity.CENTER);
        close.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { dialog.dismiss(); } }); card.addView(close);
    }

    private void showYearPicker(final LinearLayout parentCard, final AlertDialog calDialog) {
        FrameLayout wrap = new FrameLayout(activity); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        LinearLayout container = new LinearLayout(activity); container.setOrientation(LinearLayout.VERTICAL); container.setPadding((int)(25*DENSITY), (int)(25*DENSITY), (int)(25*DENSITY), (int)(25*DENSITY));
        GradientDrawable bg = new GradientDrawable(); bg.setColor(themeColors[1]); bg.setCornerRadius(30f * DENSITY); bg.setStroke((int)(1.5f*DENSITY), themeColors[4]); container.setBackground(bg);
        TextView title = new TextView(activity); title.setText(lang.get("Select Year")); title.setGravity(Gravity.CENTER); title.setTextColor(themeColors[2]); title.setTextSize(18); title.setPadding(0, 0, 0, (int)(20*DENSITY)); title.setTypeface(Typeface.DEFAULT_BOLD); container.addView(title);
        ScrollView scroll = new ScrollView(activity); LinearLayout list = new LinearLayout(activity); list.setOrientation(LinearLayout.VERTICAL);
        Calendar realCurrentCal = Calendar.getInstance(); final int currentRealYear = realCurrentCal.get(Calendar.YEAR); final int currentRealMonth = realCurrentCal.get(Calendar.MONTH);
        
        final AlertDialog[] yearDialog = new AlertDialog[1];
        
        for (int y = currentRealYear; y >= currentRealYear - 100; y--) {
            final int year = y; TextView yTv = new TextView(activity); yTv.setText(lang.bnNum(year)); yTv.setGravity(Gravity.CENTER); yTv.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY)); yTv.setTextSize(18);
            yTv.setTextColor(calendarViewPointer.get(Calendar.YEAR) == year ? colorAccent : themeColors[2]);
            yTv.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { calendarViewPointer.set(Calendar.YEAR, year); if (year == currentRealYear) { calendarViewPointer.set(Calendar.MONTH, currentRealMonth); } renderGregorian(parentCard, calDialog); if(yearDialog[0] != null) yearDialog[0].dismiss(); } });
            list.addView(yTv);
        }
        scroll.addView(list); container.addView(scroll, -1, (int)(350*DENSITY));
        
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(container, flp);
        
        yearDialog[0] = new AlertDialog.Builder(activity).setView(wrap).create(); 
        yearDialog[0].getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        yearDialog[0].getWindow().setGravity(Gravity.CENTER); // ডায়ালগ মাঝখানে রাখার কোড
        applyFont(wrap); yearDialog[0].show();
    }

    public void showHijri() {
        if (Build.VERSION.SDK_INT < 24) return;
        try { hijriViewCal.setTime(sdf.parse(selectedDate[0])); } catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); }
        FrameLayout wrap = new FrameLayout(activity); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        
        final LinearLayout main = new LinearLayout(activity); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(20*DENSITY), (int)(25*DENSITY), (int)(20*DENSITY), (int)(25*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); gd.setStroke((int)(1.5f*DENSITY), themeColors[4]); main.setBackground(gd);
        
        final TextView yearChip = new TextView(activity); 
        yearChip.setTextColor(colorAccent); yearChip.setTextSize(14); yearChip.setTypeface(Typeface.DEFAULT_BOLD); 
        yearChip.setPadding((int)(25*DENSITY), (int)(8*DENSITY), (int)(25*DENSITY), (int)(8*DENSITY));
        GradientDrawable yBg = new GradientDrawable(); yBg.setColor(colorAccent & 0x15FFFFFF); yBg.setCornerRadius(15f * DENSITY); yearChip.setBackground(yBg);
        LinearLayout.LayoutParams yLp = new LinearLayout.LayoutParams(-2, -2); yLp.gravity = Gravity.CENTER_HORIZONTAL; yLp.setMargins(0, 0, 0, (int)(15*DENSITY)); yearChip.setLayoutParams(yLp);
        main.addView(yearChip);

        LinearLayout nav = new LinearLayout(activity); nav.setOrientation(LinearLayout.HORIZONTAL); nav.setGravity(Gravity.CENTER_VERTICAL);
        TextView prev = new TextView(activity); prev.setText("❮"); prev.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY)); prev.setTextColor(themeColors[2]); prev.setTextSize(18); prev.setTypeface(Typeface.DEFAULT_BOLD);
        final TextView monthTitle = new TextView(activity); monthTitle.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f)); monthTitle.setGravity(Gravity.CENTER); monthTitle.setTextColor(themeColors[2]); monthTitle.setTypeface(Typeface.DEFAULT_BOLD); monthTitle.setTextSize(18);
        final TextView next = new TextView(activity); next.setText("❯"); next.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY)); next.setTextColor(themeColors[2]); next.setTextSize(18); next.setTypeface(Typeface.DEFAULT_BOLD);
        nav.addView(prev); nav.addView(monthTitle); nav.addView(next); main.addView(nav);
        
        LinearLayout daysRow = new LinearLayout(activity); String[] wDays = {"S", "M", "T", "W", "T", "F", "S"};
        if (lang.get("Fajr").equals("ফজর")) wDays = new String[]{"র", "সো", "ম", "বু", "বৃ", "শু", "শ"};
        for(String d : wDays) { TextView dt = new TextView(activity); dt.setText(d); dt.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f)); dt.setGravity(Gravity.CENTER); dt.setTextColor(themeColors[3]); dt.setTypeface(Typeface.DEFAULT_BOLD); dt.setTextSize(12); dt.setPadding(0, 0, 0, (int)(10*DENSITY)); daysRow.addView(dt); }
        main.addView(daysRow);
        
        final LinearLayout grid = new LinearLayout(activity); grid.setOrientation(LinearLayout.VERTICAL); main.addView(grid);
        
        LinearLayout footer = new LinearLayout(activity); footer.setOrientation(LinearLayout.HORIZONTAL); footer.setGravity(Gravity.CENTER); footer.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY));
        TextView cancelBtn = new TextView(activity); cancelBtn.setText(lang.get("CLOSE")); cancelBtn.setTextColor(themeColors[3]); cancelBtn.setTextSize(14); cancelBtn.setTypeface(Typeface.DEFAULT_BOLD); cancelBtn.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(5*DENSITY));
        footer.addView(cancelBtn); main.addView(footer);

        final AlertDialog ad = new AlertDialog.Builder(activity).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(Gravity.CENTER); // ডায়ালগ মাঝখানে রাখার কোড
        cancelBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { ad.dismiss(); } });
        
        final Runnable[] renderHolder = new Runnable[1];
        
        yearChip.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                FrameLayout yWrap = new FrameLayout(activity); yWrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
                LinearLayout yMain = new LinearLayout(activity); yMain.setOrientation(LinearLayout.VERTICAL); yMain.setPadding((int)(25*DENSITY), (int)(25*DENSITY), (int)(25*DENSITY), (int)(25*DENSITY));
                GradientDrawable yGd = new GradientDrawable(); yGd.setColor(themeColors[1]); yGd.setCornerRadius(30f * DENSITY); yGd.setStroke((int)(1.5f*DENSITY), themeColors[4]); yMain.setBackground(yGd);
                TextView yTitle = new TextView(activity); yTitle.setText(lang.get("Select Year")); yTitle.setTextColor(themeColors[2]); yTitle.setTextSize(20); yTitle.setTypeface(Typeface.DEFAULT_BOLD); yTitle.setGravity(Gravity.CENTER); yTitle.setPadding(0, 0, 0, (int)(15*DENSITY)); yMain.addView(yTitle);
                
                ScrollView sv = new ScrollView(activity);
                LinearLayout list = new LinearLayout(activity); list.setOrientation(LinearLayout.VERTICAL); list.setPadding((int)(20*DENSITY),0,(int)(20*DENSITY),0);
                
                IslamicCalendar tempIc = new IslamicCalendar(); tempIc.setTime(new Date());
                tempIc.add(IslamicCalendar.DATE, sp.getInt("hijri_offset", 0));
                final int currentRealHYear = tempIc.get(IslamicCalendar.YEAR);
                
                IslamicCalendar viewIc = new IslamicCalendar(); viewIc.setTime(hijriViewCal.getTime()); viewIc.add(IslamicCalendar.DATE, sp.getInt("hijri_offset", 0));
                final int viewHYear = viewIc.get(IslamicCalendar.YEAR);
                
                final AlertDialog yAd = new AlertDialog.Builder(activity).setView(yWrap).create(); 
                yAd.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
                yAd.getWindow().setGravity(Gravity.CENTER); // ডায়ালগ মাঝখানে রাখার কোড
                
                for(int y = currentRealHYear; y >= currentRealHYear - 100; y--) { 
                    final int selectedY = y;
                    TextView yt = new TextView(activity); 
                    yt.setText(lang.bnNum(y) + " " + lang.get("AH")); 
                    yt.setTextSize(18); yt.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY)); yt.setGravity(Gravity.CENTER); yt.setTypeface(y == viewHYear ? Typeface.DEFAULT_BOLD : Typeface.DEFAULT);
                    yt.setTextColor(y == viewHYear ? colorAccent : themeColors[2]);
                    
                    
                    yt.setOnClickListener(new View.OnClickListener() { 
                        @Override public void onClick(View view) { 
                            IslamicCalendar shiftIc = new IslamicCalendar();
                            shiftIc.setTime(hijriViewCal.getTime());
                            shiftIc.add(IslamicCalendar.DATE, sp.getInt("hijri_offset", 0));
                            shiftIc.set(IslamicCalendar.YEAR, selectedY);
                            shiftIc.add(IslamicCalendar.DATE, -sp.getInt("hijri_offset", 0));
                            hijriViewCal.setTime(shiftIc.getTime());
                            yAd.dismiss(); renderHolder[0].run(); 
                        }
                    });
                    LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2); lp.setMargins(0,0,0,(int)(5*DENSITY)); yt.setLayoutParams(lp); list.addView(yt);
                }
                sv.addView(list); yMain.addView(sv, new LinearLayout.LayoutParams(-1, (int)(350*DENSITY)));
                FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = Gravity.CENTER; yWrap.addView(yMain, flp);
                applyFont(yWrap); yAd.show();
            }
        });

        renderHolder[0] = new Runnable() {
            @Override public void run() {
                grid.removeAllViews();
                IslamicCalendar ic = new IslamicCalendar(); ic.setTime(hijriViewCal.getTime());
                final int offset = sp.getInt("hijri_offset", 0); ic.add(IslamicCalendar.DATE, offset);
                String[] hMonths = {"Muharram", "Safar", "Rabi I", "Rabi II", "Jumada I", "Jumada II", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"};
                
                yearChip.setText(lang.bnNum(ic.get(IslamicCalendar.YEAR)) + " " + lang.get("AH"));
                monthTitle.setText(lang.get(hMonths[ic.get(IslamicCalendar.MONTH)]));
                
                Calendar todayCal = Calendar.getInstance(); IslamicCalendar todayIc = new IslamicCalendar(); todayIc.setTime(todayCal.getTime()); todayIc.add(IslamicCalendar.DATE, offset);
                final boolean isFutureMonth = (ic.get(IslamicCalendar.YEAR) > todayIc.get(IslamicCalendar.YEAR)) || (ic.get(IslamicCalendar.YEAR) == todayIc.get(IslamicCalendar.YEAR) && ic.get(IslamicCalendar.MONTH) >= todayIc.get(IslamicCalendar.MONTH));
                next.setAlpha(isFutureMonth ? 0.3f : 1f);
                ic.set(IslamicCalendar.DAY_OF_MONTH, 1); int startDOW = ic.get(IslamicCalendar.DAY_OF_WEEK); int maxDays = ic.getActualMaximum(IslamicCalendar.DAY_OF_MONTH);
                int cellCount = 1; int dayNum = 1;
                for(int r=0; r<6; r++) {
                    LinearLayout row = new LinearLayout(activity); row.setOrientation(LinearLayout.HORIZONTAL);
                    for(int c=0; c<7; c++) {
                        FrameLayout cell = new FrameLayout(activity); cell.setLayoutParams(new LinearLayout.LayoutParams(0, (int)(45*DENSITY), 1f));
                        if (cellCount >= startDOW && dayNum <= maxDays) {
                            final int currentDay = dayNum; TextView dTv = new TextView(activity);
                            dTv.setText(lang.bnNum(currentDay)); dTv.setGravity(Gravity.CENTER); dTv.setTypeface(Typeface.DEFAULT_BOLD);
                            FrameLayout.LayoutParams dLp = new FrameLayout.LayoutParams((int)(35*DENSITY), (int)(35*DENSITY)); dLp.gravity = Gravity.CENTER; dTv.setLayoutParams(dLp);
                            IslamicCalendar cellIc = (IslamicCalendar) ic.clone(); cellIc.set(IslamicCalendar.DAY_OF_MONTH, currentDay);
                            Calendar realGregorian = Calendar.getInstance(); realGregorian.setTime(cellIc.getTime()); realGregorian.add(Calendar.DATE, -offset);
                            final String cellDateKey = sdf.format(realGregorian.getTime()); final boolean isSelected = cellDateKey.equals(selectedDate[0]);
                            final boolean isFutureDate = realGregorian.getTime().after(todayCal.getTime()) && !cellDateKey.equals(sdf.format(todayCal.getTime())); final boolean isTooOld = realGregorian.get(Calendar.YEAR) < todayCal.get(Calendar.YEAR) - 100;
                            
                            boolean isAllDone = true; for(String p : prayers) { if(!sp.getString(cellDateKey+"_"+p, "no").equals("yes") && !sp.getString(cellDateKey+"_"+p, "no").equals("excused")) { isAllDone = false; break; } }
                            dTv.setTextColor(isSelected ? Color.WHITE : (isFutureDate ? themeColors[4] : (isAllDone ? colorAccent : themeColors[2])));
                            
                            GradientDrawable sBg = new GradientDrawable(); sBg.setShape(GradientDrawable.OVAL);
                            if (isSelected) { sBg.setColor(colorAccent); dTv.setBackground(((MainActivity)activity).getProgressBorder(cellDateKey, isSelected)); } 
                            else if (isAllDone && !isFutureDate) { sBg.setColor(themeColors[5]); dTv.setBackground(((MainActivity)activity).getProgressBorder(cellDateKey, isSelected)); }
                            
                            cell.addView(dTv); 
                            cell.setOnClickListener(new View.OnClickListener() { 
                                @Override public void onClick(View v) { 
                                    if (isFutureDate) ui.showPremiumLocked(colorAccent); 
                                    else if(isTooOld) { ui.showSmartBanner((android.widget.FrameLayout)activity.findViewById(android.R.id.content), lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); }
                                    else { selectedDate[0] = cellDateKey; ad.dismiss(); if(onDateSelected!=null) onDateSelected.run(); } 
                                } 
                            }); dayNum++;
                        }
                        row.addView(cell); cellCount++;
                    }
                    grid.addView(row); if (dayNum > maxDays) break;
                }
            }
        };
        
        prev.setOnClickListener(v -> { Calendar chk = (Calendar) hijriViewCal.clone(); chk.add(Calendar.DATE, -29); if(chk.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { hijriViewCal.add(Calendar.DATE, -29); renderHolder[0].run(); } else { ui.showSmartBanner((android.widget.FrameLayout)activity.findViewById(android.R.id.content), lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); } });
        next.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { IslamicCalendar currentIc = new IslamicCalendar(); currentIc.setTime(hijriViewCal.getTime()); currentIc.add(IslamicCalendar.DATE, sp.getInt("hijri_offset", 0)); IslamicCalendar todayIc = new IslamicCalendar(); todayIc.setTime(new Date()); todayIc.add(IslamicCalendar.DATE, sp.getInt("hijri_offset", 0)); if (currentIc.get(IslamicCalendar.YEAR) < todayIc.get(IslamicCalendar.YEAR) || (currentIc.get(IslamicCalendar.YEAR) == todayIc.get(IslamicCalendar.YEAR) && currentIc.get(IslamicCalendar.MONTH) < todayIc.get(IslamicCalendar.MONTH))) { hijriViewCal.add(Calendar.DATE, 30); renderHolder[0].run(); } } });
        
        renderHolder[0].run(); FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams(-1, -2); flp.gravity = Gravity.CENTER; flp.setMargins((int)(20*DENSITY), 0, (int)(20*DENSITY), 0); wrap.addView(main, flp); applyFont(wrap); ad.show();
    }
}