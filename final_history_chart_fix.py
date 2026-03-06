import os

print("🚀 Starting Final History & Chart Fix...")

# 1. Update MainActivity.java to sync date
main_path = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
if os.path.exists(main_path):
    with open(main_path, 'r', encoding='utf-8') as f:
        m_data = f.read()
    
    if 'statsHelper.syncDate' not in m_data:
        m_data = m_data.replace('statsHelper.showStatsOptionsDialog();', 'try{statsHelper.syncDate(sdf.parse(selectedDate[0]));}catch(Exception e){} statsHelper.showStatsOptionsDialog();')
        m_data = m_data.replace('statsHelper.showStats(true);', 'try{statsHelper.syncDate(sdf.parse(selectedDate[0]));}catch(Exception e){} statsHelper.showStats(true);')
        
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(m_data)
        print("✅ MainActivity: History Sync Enabled.")
    else:
        print("⚠️ MainActivity already synced.")

# 2. Update StatsHelper.java
stats_path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
if os.path.exists(stats_path):
    with open(stats_path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Insert syncDate method
    if 'public void syncDate(' not in c:
        c = c.replace('public void exportPdf() {', 'public void syncDate(java.util.Date d) { if(d != null) statsCalPointer.setTime(d); }\n\n    public void exportPdf() {')
    
    # Remove unwanted reset to 'today' inside showStats
    c = c.replace('statsCalPointer.setTime(new Date());', '// statsCalPointer.setTime(new Date()); Removed to keep history')

    # Fix PDF height overlap
    c = c.replace('int pdfHeight = 1600;', 'int pdfHeight = 1950;')

    # Replace shareImageReport completely
    start_idx = c.find('public void shareImageReport(boolean isWeekly) {')
    end_idx = c.find('private void drawReportCard(Canvas canvas,')
    
    if start_idx != -1 and end_idx != -1:
        new_share = r"""public void shareImageReport(boolean isWeekly) {
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
    }"""
        c = c[:start_idx] + new_share + "\n\n    " + c[end_idx:]
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("✅ StatsHelper.java: Charts added, footer fixed, history synced.")
    else:
        print("⚠️ Could not find shareImageReport bounds.")
