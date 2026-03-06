import os
import re

print("🚀 Starting Modernization...")

# ১. LanguageEngine.java থেকে (PDF) লেখা রিমুভ করা
lang_path = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
if os.path.exists(lang_path):
    with open(lang_path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('bnMap.put("Advanced Statistics", "বিস্তারিত রিপোর্ট (PDF)");', 'bnMap.put("Advanced Statistics", "বিস্তারিত রিপোর্ট");')
    with open(lang_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Language text updated. (PDF removed)")

# ২. StatsHelper.java তে মডার্ন XLS লজিক বসানো
stats_path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
if os.path.exists(stats_path):
    with open(stats_path, 'r', encoding='utf-8') as f:
        c = f.read()
        
    modern_xls = """public void exportXls() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            java.io.File dir = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists()) dir.mkdirs();
            // .xls ফরম্যাট ব্যবহার করা হচ্ছে
            java.io.File file = new java.io.File(dir, "Salah_Report_" + System.currentTimeMillis() + ".xls");
            java.io.PrintWriter pw = new java.io.PrintWriter(new java.io.OutputStreamWriter(new java.io.FileOutputStream(file), "UTF-8"));
            
            // আধুনিক HTML Table ডিজাইন (এক্সেল এটিকে রঙিন শিট হিসেবে রিড করবে)
            pw.println("<html xmlns:o=\\"urn:schemas-microsoft-com:office:office\\" xmlns:x=\\"urn:schemas-microsoft-com:office:excel\\" xmlns=\\"http://www.w3.org/TR/REC-html40\\">");
            pw.println("<head><meta charset=\\"UTF-8\\"><style>");
            pw.println("table { border-collapse: collapse; font-family: 'Segoe UI', Arial, sans-serif; width: 100%; }");
            pw.println("th { background-color: #00BFA5; color: white; padding: 15px; font-size: 16px; border: 1px solid #ddd; text-align: center; }");
            pw.println("td { padding: 12px; border: 1px solid #ddd; text-align: center; font-size: 15px; vertical-align: middle; font-weight: bold; }");
            pw.println(".yes { color: #2E7D32; background-color: #E8F5E9; }");
            pw.println(".no { color: #C62828; background-color: #FFEBEE; }");
            pw.println(".excused { color: #AD1457; background-color: #FCE4EC; }");
            pw.println(".title { font-size: 26px; font-weight: bold; color: #ffffff; background-color: #1C1C1E; text-align: center; padding: 20px; }");
            pw.println("</style></head><body>");
            
            pw.println("<table>");
            String reportTitle = isBn ? "মাসিক নামাজের রিপোর্ট" : "Monthly Salah Report";
            String monthName = new SimpleDateFormat("MMMM yyyy", Locale.US).format(statsCalPointer.getTime());
            if(isBn) { monthName = lang.get(new SimpleDateFormat("MMMM", Locale.US).format(statsCalPointer.getTime())) + " " + lang.bnNum(statsCalPointer.get(Calendar.YEAR)); }
            
            pw.println("<tr><td colspan=\\"8\\" class=\\"title\\">" + reportTitle + " - " + monthName + "</td></tr>");
            pw.println("<tr><th>" + (isBn ? "তারিখ" : "Date") + "</th><th>" + (isBn ? "ফজর" : "Fajr") + "</th><th>" + (isBn ? "যোহর" : "Dhuhr") + "</th><th>" + (isBn ? "আসর" : "Asr") + "</th><th>" + (isBn ? "মাগরিব" : "Maghrib") + "</th><th>" + (isBn ? "এশা" : "Isha") + "</th><th>" + (isBn ? "বিতর" : "Witr") + "</th><th>" + (isBn ? "সারসংক্ষেপ" : "Status") + "</th></tr>");
            
            Calendar cal = (Calendar) statsCalPointer.clone();
            cal.set(Calendar.DAY_OF_MONTH, 1);
            int totalDays = cal.getActualMaximum(Calendar.DAY_OF_MONTH);
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);

            for(int i=1; i<=totalDays; i++) {
                cal.set(Calendar.DAY_OF_MONTH, i);
                String dKey = sdf.format(cal.getTime());
                SalahRecord r = getRoomRecord(dKey);
                
                String dateDisplay = isBn ? lang.bnNum(i) + " " + lang.get(new SimpleDateFormat("MMM", Locale.US).format(cal.getTime())) : dKey;
                pw.println("<tr><td style=\\"color:#333; background-color:#F8F9FA;\\">" + dateDisplay + "</td>");
                
                String[] pList = {"Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr"};
                boolean allDone = true;
                for(String p : pList) {
                    String s = getFardStat(r, p);
                    String cellClass = s.equals("yes") ? "yes" : (s.equals("excused") ? "excused" : "no");
                    String cellText = s.equals("yes") ? (isBn ? "✅ সম্পন্ন" : "✅ Done") : (s.equals("excused") ? (isBn ? "🌸 ছুটি" : "🌸 Excused") : (isBn ? "❌ কাজা" : "❌ Missed"));
                    pw.println("<td class=\\"" + cellClass + "\\">" + cellText + "</td>");
                    if(!s.equals("yes") && !s.equals("excused")) allDone = false;
                }
                String statusClass = allDone ? "yes" : "no";
                String statusText = allDone ? (isBn ? "🌟 আলহামদুলিল্লাহ" : "🌟 Perfect") : (isBn ? "⚠️ অসম্পূর্ণ" : "⚠️ Incomplete");
                pw.println("<td class=\\"" + statusClass + "\\">" + statusText + "</td></tr>");
            }
            
            pw.println("</table></body></html>");
            pw.close();
            
            final java.io.File finalFile = file;
            ui.showSmartBanner((android.widget.FrameLayout) activity.findViewById(android.R.id.content), isBn?"সফল":"Success", isBn?"XLS ফাইল সেভ হয়েছে (ওপেন করতে ক্লিক)":"XLS Saved (Click to open)", "img_tick", colorAccent, new Runnable() {
                @Override public void run() {
                    Intent intent = new Intent(Intent.ACTION_VIEW);
                    Uri uri = androidx.core.content.FileProvider.getUriForFile(activity, activity.getPackageName() + ".provider", finalFile);
                    intent.setDataAndType(uri, "application/vnd.ms-excel");
                    intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    activity.startActivity(Intent.createChooser(intent, "Open with..."));
                }
            });
        } catch(Exception e) {}
    }

    public void showStatsOptionsDialog() {"""
    
    # রেগুলার এক্সপ্রেশন দিয়ে আগের exportXls মেথডটি রিপ্লেস করা
    c = re.sub(r'public void exportXls\(\)\s*\{.*?public void showStatsOptionsDialog\(\)\s*\{', modern_xls, c, flags=re.DOTALL)
    
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Modern Premium XLS Engine Installed!")
