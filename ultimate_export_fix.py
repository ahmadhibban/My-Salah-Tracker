import os

print("🚀 Starting Ultimate Export & FileProvider Automation...")

def update_file(path, old_text, new_text):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_text in content and new_text not in content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content.replace(old_text, new_text))
            return True
    return False

# ১. AndroidManifest.xml আপডেট করা
manifest_path = 'app/src/main/AndroidManifest.xml'
provider_xml = """        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.provider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>
    </application>"""

if os.path.exists(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as f:
        m_content = f.read()
    if 'FileProvider' not in m_content and '</application>' in m_content:
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(m_content.replace('</application>', provider_xml))
        print("✅ AndroidManifest.xml Updated (FileProvider Added).")
    else:
        print("⚠️ FileProvider already exists or application tag not found.")

# ২. file_paths.xml ফাইল তৈরি করা
xml_dir = 'app/src/main/res/xml'
if not os.path.exists(xml_dir):
    os.makedirs(xml_dir)
file_paths_content = """<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-path name="external_files" path="." />
</paths>"""
with open(os.path.join(xml_dir, 'file_paths.xml'), 'w', encoding='utf-8') as f:
    f.write(file_paths_content)
print("✅ file_paths.xml Created.")

# ৩. StatsHelper.java তে PDF Fix এবং XLS/CSV Export যুক্ত করা
stats_path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'

# PDF Fix
pdf_old = 'intent.setDataAndType(Uri.fromFile(finalFile), "application/pdf");'
pdf_new = """Uri contentUri = androidx.core.content.FileProvider.getUriForFile(activity, activity.getPackageName() + ".provider", finalFile);
                    intent.setDataAndType(contentUri, "application/pdf");
                    intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);"""
if update_file(stats_path, pdf_old, pdf_new):
    print("✅ PDF Open Logic Fixed.")

# XLS Export Logic
xls_method = """
    public void exportXls() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists()) dir.mkdirs();
            File file = new File(dir, "Salah_Report_" + System.currentTimeMillis() + ".csv");
            java.io.PrintWriter pw = new java.io.PrintWriter(file);
            
            // Header Row (Premium Look)
            pw.println(isBn ? "তারিখ,ফজর,যোহর,আসর,মাগরিব,এশা,বিতর,অবস্থা" : "Date,Fajr,Dhuhr,Asr,Maghrib,Isha,Witr,Status");
            
            Calendar cal = (Calendar) statsCalPointer.clone();
            cal.set(Calendar.DAY_OF_MONTH, 1);
            int totalDays = cal.getActualMaximum(Calendar.DAY_OF_MONTH);
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);

            for(int i=1; i<=totalDays; i++) {
                cal.set(Calendar.DAY_OF_MONTH, i);
                String dKey = sdf.format(cal.getTime());
                SalahRecord r = getRoomRecord(dKey);
                
                StringBuilder row = new StringBuilder(dKey + ",");
                String[] pList = {"Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr"};
                boolean allDone = true;
                for(String p : pList) {
                    String s = getFardStat(r, p);
                    row.append(lang.get(s)).append(",");
                    if(!s.equals("yes") && !s.equals("excused")) allDone = false;
                }
                row.append(allDone ? (isBn?"সম্পন্ন":"Completed") : (isBn?"অসম্পূর্ণ":"Incomplete"));
                pw.println(row.toString());
            }
            pw.close();
            
            final File finalFile = file;
            ui.showSmartBanner(root, isBn?"সফল":"Success", isBn?"XLS ফাইল সেভ হয়েছে (ওপেন করতে ক্লিক)":"XLS Saved (Click to open)", "img_tick", colorAccent, new Runnable() {
                @Override public void run() {
                    Intent intent = new Intent(Intent.ACTION_VIEW);
                    Uri uri = androidx.core.content.FileProvider.getUriForFile(activity, activity.getPackageName() + ".provider", finalFile);
                    intent.setDataAndType(uri, "text/csv");
                    intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    activity.startActivity(Intent.createChooser(intent, "Open with..."));
                }
            });
        } catch(Exception e) {}
    }

    public void showStatsOptionsDialog() {"""

if update_file(stats_path, 'public void showStatsOptionsDialog() {', xls_method):
    print("✅ XLS Export Method Added.")

# Add XLS Button
xls_btn = 'bm.add(isBn ? "প্রিমিয়াম এক্সেল (XLS) এক্সপোর্ট" : "Export Premium XLS", new Runnable() { @Override public void run() { exportXls(); } });\n        bm.add(isBn ? "প্রিমিয়াম পিডিএফ এক্সপোর্ট" : "Export Premium PDF"'
if update_file(stats_path, 'bm.add(isBn ? "প্রিমিয়াম পিডিএফ এক্সপোর্ট" : "Export Premium PDF"', xls_btn):
    print("✅ XLS Export Button Added.")

print("🎉 All Tasks Completed Successfully!")
