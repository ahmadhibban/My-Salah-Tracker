import os
import re

print("🚀 Starting Master Fix v4...")

# ১. LanguageEngine.java - তে নতুন অনুবাদ যুক্ত করা
lang_path = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
if os.path.exists(lang_path):
    with open(lang_path, 'r', encoding='utf-8') as f:
        c = f.read()
    if '"Limit Reached"' not in c:
        new_translations = """bnMap.put("You've completed all prayers for this day.\\nMay Allah accept it.", "এই দিনের সব নামাজ সম্পন্ন হয়েছে।\\nআল্লাহ কবুল করুন।");
        bnMap.put("Limit Reached", "সীমা অতিক্রম");
        bnMap.put("Cannot go back more than 100 years.", "১০০ বছরের বেশি পেছনে যাওয়া সম্ভব নয়।");
        bnMap.put("Total Days", "মোট দিন");
        bnMap.put("Pending Qaza", "অপেক্ষমান কাজা");
        bnMap.put("Current Streak", "বর্তমান স্ট্রিক");"""
        c = c.replace('bnMap.put("You\'ve completed all prayers for this day.\\nMay Allah accept it.", "এই দিনের সব নামাজ সম্পন্ন হয়েছে।\\nআল্লাহ কবুল করুন।");', new_translations)
        with open(lang_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("✅ Language translations added.")

# ২. MainActivity.java - তে ভাষার বাগ ফিক্স করা
main_path = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
if os.path.exists(main_path):
    with open(main_path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('"সীমা অতিক্রম"', 'lang.get("Limit Reached")')
    c = c.replace('"১০০ বছরের বেশি পেছনে যাওয়া সম্ভব নয়"', 'lang.get("Cannot go back more than 100 years.")')
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Language mixing bug fixed in MainActivity.")

# ৩. CalendarHelper.java - তে ইংরেজি ক্যালেন্ডার হাইলাইট এবং ভাষার বাগ ফিক্স
cal_path = 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java'
if os.path.exists(cal_path):
    with open(cal_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # 100 Year check update
    old_nav_limit = 'calendarViewPointer.add(Calendar.MONTH, -1); renderGregorian(card, dialog); \n           \n             }'
    new_nav_limit = 'calendarViewPointer.add(Calendar.MONTH, -1); renderGregorian(card, dialog); \n                } else { \n                    android.widget.FrameLayout root = activity.findViewById(android.R.id.content);\n                    if(root != null) ui.showSmartBanner(root, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null);\n                }'
    if old_nav_limit in c: c = c.replace(old_nav_limit, new_nav_limit)

    # Gregorian Highlight exact match Hijri style
    c = re.sub(
        r'FrameLayout\.LayoutParams boxLp = new FrameLayout\.LayoutParams\(boxSize, boxSize\); boxLp\.gravity = Gravity\.CENTER; tv\.setLayoutParams\(boxLp\);.*?cell\.addView\(tv\);',
        r'''FrameLayout.LayoutParams boxLp = new FrameLayout.LayoutParams(boxSize, boxSize); boxLp.gravity = Gravity.CENTER; tv.setLayoutParams(boxLp);
                    boolean isAllDone = true;
                    for(String p : prayers) { if(!sp.getString(dKey+"_"+p, "no").equals("yes") && !sp.getString(dKey+"_"+p, "no").equals("excused")) { isAllDone = false; break; } }
                    tv.setTextColor(dKey.equals(selectedDate[0]) ? android.graphics.Color.WHITE : (isFuture ? android.graphics.Color.LTGRAY : (isAllDone ? colorAccent : themeColors[2])));
                    GradientDrawable bgD = new GradientDrawable(); bgD.setShape(GradientDrawable.OVAL);
                    if (dKey.equals(selectedDate[0])) { bgD.setColor(colorAccent); tv.setBackground(bgD); }
                    else if (isAllDone && !isFuture) { bgD.setColor(themeColors[5]); tv.setBackground(bgD); }
                    else { bgD.setColor(android.graphics.Color.TRANSPARENT); tv.setBackground(bgD); }
                    cell.addView(tv);''',
        c, flags=re.DOTALL
    )
    with open(cal_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ English Calendar Highlight & Limits applied perfectly.")

# ৪. StatsHelper.java - তে PDF এর মতো Summary সহ Ultra Premium XLS
stats_path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
if os.path.exists(stats_path):
    with open(stats_path, 'r', encoding='utf-8') as f:
        c = f.read()

    ultra_xls = """public void exportXls() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            java.io.File dir = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists()) dir.mkdirs();
            java.io.File file = new java.io.File(dir, "Salah_Report_" + System.currentTimeMillis() + ".xls");
            java.io.PrintWriter pw = new java.io.PrintWriter(new java.io.OutputStreamWriter(new java.io.FileOutputStream(file), "UTF-8"));
            
            // Statistics Calculation
            int tDays = 0, tDone = 0, tMissed = 0, tExcused = 0, tQaza = 0;
            Calendar sumCal = (Calendar) statsCalPointer.clone(); sumCal.set(Calendar.DAY_OF_MONTH, 1);
            int mDays = sumCal.getActualMaximum(Calendar.DAY_OF_MONTH);
            Calendar nowSum = Calendar.getInstance();
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
            
            for(int j=1; j<=mDays; j++) {
                sumCal.set(Calendar.DAY_OF_MONTH, j);
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

            // HTML Structure
            pw.println("<html xmlns:o=\\"urn:schemas-microsoft-com:office:office\\" xmlns:x=\\"urn:schemas-microsoft-com:office:excel\\" xmlns=\\"http://www.w3.org/TR/REC-html40\\">");
            pw.println("<head><meta charset=\\"UTF-8\\"><style>");
            pw.println("table { border-collapse: collapse; font-family: 'Segoe UI', Arial, sans-serif; width: 100%; margin-bottom: 30px; }");
            pw.println("th { color: white; padding: 15px; font-size: 16px; border: 1px solid #ddd; text-align: center; }");
            pw.println("td { padding: 12px; border: 1px solid #ddd; text-align: center; font-size: 15px; vertical-align: middle; font-weight: bold; }");
            pw.println(".yes { color: #2E7D32; background-color: #E8F5E9; } .no { color: #C62828; background-color: #FFEBEE; } .excused { color: #AD1457; background-color: #FCE4EC; }");
            pw.println(".title { font-size: 28px; font-weight: bold; color: #ffffff; background-color: #1C1C1E; text-align: center; padding: 25px; }");
            pw.println(".sum-th { font-size: 14px; padding: 10px; border-radius: 10px 10px 0 0; border: none; }");
            pw.println(".sum-td { font-size: 24px; padding: 15px; background: #F8F9FA; color: #333; border: 1px solid #eee; }");
            pw.println("</style></head><body>");
            
            String monthName = new SimpleDateFormat("MMMM yyyy", Locale.US).format(statsCalPointer.getTime());
            if(isBn) monthName = lang.get(new SimpleDateFormat("MMMM", Locale.US).format(statsCalPointer.getTime())) + " " + lang.bnNum(statsCalPointer.get(Calendar.YEAR));
            
            // Header
            pw.println("<table><tr><td colspan=\\"8\\" class=\\"title\\">" + (isBn?"মাসিক নামাজের রিপোর্ট":"Monthly Salah Report") + " - " + monthName + "</td></tr></table>");
            
            // Premium Summary Block
            pw.println("<table><tr>");
            pw.println("<th class=\\"sum-th\\" style=\\"background:#00BFA5;\\">" + lang.get("Total Days") + "</th>");
            pw.println("<th class=\\"sum-th\\" style=\\"background:#3B82F6;\\">" + lang.get("Prayers Done") + "</th>");
            pw.println("<th class=\\"sum-th\\" style=\\"background:#FF5252;\\">" + lang.get("Missed") + "</th>");
            pw.println("<th class=\\"sum-th\\" style=\\"background:#FF9500;\\">" + lang.get("Pending Qaza") + "</th>");
            pw.println("<th class=\\"sum-th\\" style=\\"background:#FF4081;\\">" + lang.get("Excused Mode") + "</th>");
            pw.println("<th class=\\"sum-th\\" style=\\"background:#9B59B6;\\">" + lang.get("Current Streak") + "</th>");
            pw.println("</tr><tr>");
            pw.println("<td class=\\"sum-td\\">" + lang.bnNum(tDays) + "</td>");
            pw.println("<td class=\\"sum-td\\" style=\\"color:#3B82F6;\\">" + lang.bnNum(tDone) + "</td>");
            pw.println("<td class=\\"sum-td\\" style=\\"color:#FF5252;\\">" + lang.bnNum(tMissed) + "</td>");
            pw.println("<td class=\\"sum-td\\" style=\\"color:#FF9500;\\">" + lang.bnNum(tQaza) + "</td>");
            pw.println("<td class=\\"sum-td\\" style=\\"color:#FF4081;\\">" + lang.bnNum(tExcused) + "</td>");
            pw.println("<td class=\\"sum-td\\" style=\\"color:#9B59B6;\\">" + lang.bnNum(streak) + "</td>");
            pw.println("</tr></table>");

            // Daily Grid
            pw.println("<table><tr><th style=\\"background:#333;\\">" + (isBn?"তারিখ":"Date") + "</th><th style=\\"background:#333;\\">" + (isBn?"ফজর":"Fajr") + "</th><th style=\\"background:#333;\\">" + (isBn?"যোহর":"Dhuhr") + "</th><th style=\\"background:#333;\\">" + (isBn?"আসর":"Asr") + "</th><th style=\\"background:#333;\\">" + (isBn?"মাগরিব":"Maghrib") + "</th><th style=\\"background:#333;\\">" + (isBn?"এশা":"Isha") + "</th><th style=\\"background:#333;\\">" + (isBn?"বিতর":"Witr") + "</th><th style=\\"background:#333;\\">" + (isBn?"সারসংক্ষেপ":"Status") + "</th></tr>");
            
            Calendar cal = (Calendar) statsCalPointer.clone(); cal.set(Calendar.DAY_OF_MONTH, 1);
            for(int i=1; i<=mDays; i++) {
                cal.set(Calendar.DAY_OF_MONTH, i);
                String dKey = sdf.format(cal.getTime());
                SalahRecord r = getRoomRecord(dKey);
                
                String dateDisplay = isBn ? lang.bnNum(i) + " " + lang.get(new SimpleDateFormat("MMM", Locale.US).format(cal.getTime())) : dKey;
                pw.println("<tr><td style=\\"color:#333; background-color:#F8F9FA;\\">" + dateDisplay + "</td>");
                
                boolean allDone = true;
                for(String p : prayers) {
                    String s = getFardStat(r, p);
                    String cCls = s.equals("yes") ? "yes" : (s.equals("excused") ? "excused" : "no");
                    String cTxt = s.equals("yes") ? (isBn ? "✅ সম্পন্ন" : "✅ Done") : (s.equals("excused") ? (isBn ? "🌸 ছুটি" : "🌸 Excused") : (isBn ? "❌ কাজা" : "❌ Missed"));
                    pw.println("<td class=\\"" + cCls + "\\">" + cTxt + "</td>");
                    if(!s.equals("yes") && !s.equals("excused")) allDone = false;
                }
                String sCls = allDone ? "yes" : "no";
                String sTxt = allDone ? (isBn ? "🌟 আলহামদুলিল্লাহ" : "🌟 Perfect") : (isBn ? "⚠️ অসম্পূর্ণ" : "⚠️ Incomplete");
                pw.println("<td class=\\"" + sCls + "\\">" + sTxt + "</td></tr>");
            }
            pw.println("</table></body></html>");
            pw.close();
            
            final java.io.File finalFile = file;
            ui.showSmartBanner((android.widget.FrameLayout) activity.findViewById(android.R.id.content), isBn?"সফল":"Success", isBn?"XLS ফাইল সেভ হয়েছে (ওপেন করতে ক্লিক)":"XLS Saved (Click to open)", "img_tick", colorAccent, new Runnable() {
                @Override public void run() {
                    Intent intent = new Intent(Intent.ACTION_VIEW);
                    android.net.Uri uri = androidx.core.content.FileProvider.getUriForFile(activity, activity.getPackageName() + ".provider", finalFile);
                    intent.setDataAndType(uri, "application/vnd.ms-excel");
                    intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    activity.startActivity(Intent.createChooser(intent, "Open with..."));
                }
            });
        } catch(Exception e) {}
    }

    public void showStatsOptionsDialog() {"""
    
    c = re.sub(r'public void exportXls\(\)\s*\{.*?public void showStatsOptionsDialog\(\)\s*\{', ultra_xls, c, flags=re.DOTALL)
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Ultra Premium XLS Engine Added (With PDF Summary Info).")

print("🎉 ALL DONE! Please Rebuild the App.")
