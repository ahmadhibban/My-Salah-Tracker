import os

def replace_in_file(path, old, new):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.replace(old, new))
        return True
    return False

# ১. আইকন কাস্টমাইজেশন লজিক (Custom Icon Names)
# আপনি drawable ফোল্ডারে 'img_custom_qaza' এবং 'img_custom_backup' নামে ছবি রাখলে তা অটো সেট হবে।
replace_in_file('app/src/main/java/com/my/salah/tracker/app/MainActivity.java', '"img_qaza"', '"img_custom_qaza"')
replace_in_file('app/src/main/java/com/my/salah/tracker/app/BackupHelper.java', '"img_cloud"', '"img_custom_backup"')

# ২. PDF ওপেন করার লজিক (Open PDF on Banner Click)
pdf_logic_old = "ui.showSmartBanner(root, isBn?\"সফল\":\"Success\", isBn?\"পিডিএফ সেভ হয়েছে\":\"PDF Saved successfully.\", \"img_tick\", colorAccent, null);"
pdf_logic_new = """final File finalFile = file;
            ui.showSmartBanner(root, isBn?"সফল":"Success", isBn?"পিডিএফ সেভ হয়েছে (দেখতে ক্লিক করুন)":"PDF Saved (Click to view)", "img_tick", colorAccent, new Runnable() {
                @Override public void run() {
                    Intent intent = new Intent(Intent.ACTION_VIEW);
                    intent.setDataAndType(Uri.fromFile(finalFile), "application/pdf");
                    intent.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY | Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    try { activity.startActivity(intent); } catch (Exception e) {}
                }
            });"""
replace_in_file('app/src/main/java/com/my/salah/tracker/app/StatsHelper.java', pdf_logic_old, pdf_logic_new)

# ৩. ইংরেজি ক্যালেন্ডারে বাংলা মাস (Bengali Month Name Fix)
old_month_only = 'this.monthOnlyF = new SimpleDateFormat("MMMM", Locale.US);'
new_month_only = 'this.monthOnlyF = new SimpleDateFormat("MMMM", sp.getString("app_lang", "en").equals("bn") ? new Locale("bn") : Locale.US);'
replace_in_file('app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java', old_month_only, new_month_only)

# ৪. ইংরেজি ক্যালেন্ডার হাইলাইট (Rainbow Border Highlight)
old_bg_logic = 'tv.setBackground(isFuture ? bgD : (dKey.equals(selectedDate[0]) ? bgD : ui.getRainbowBorder(dKey, 3)));'
new_bg_logic = """boolean isAllDone = true; SalahRecord dRec = SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(dKey);
                    if(dRec != null) { for(String pName : prayers) { String sStat = dRec.fajr; if(pName.equals("Dhuhr")) sStat=dRec.dhuhr; else if(pName.equals("Asr")) sStat=dRec.asr; else if(pName.equals("Maghrib")) sStat=dRec.maghrib; else if(pName.equals("Isha")) sStat=dRec.isha; else if(pName.equals("Witr")) sStat=dRec.witr; if(!sStat.equals("yes") && !sStat.equals("excused")) { isAllDone = false; break; } } } else { isAllDone = false; }
                    tv.setBackground(isFuture ? bgD : (dKey.equals(selectedDate[0]) ? bgD : (isAllDone ? ui.getRainbowBorder(dKey, 3) : bgD)));"""
replace_in_file('app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java', old_bg_logic, new_bg_logic)

# ৫. ১০০ বছরের সীমা কড়াকড়ি (100 Years Week Nav Security)
old_prev_w = 'selectedCalArr[0].add(Calendar.DATE, -7);'
new_prev_w = 'Calendar checkLimit = (Calendar) selectedCalArr[0].clone(); checkLimit.add(Calendar.DATE, -7); if(checkLimit.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { selectedCalArr[0].add(Calendar.DATE, -7); } else { ui.showSmartBanner(root, "সীমা অতিক্রম", "১০০ বছরের বেশি পেছনে যাওয়া সম্ভব নয়", "img_warning", colorAccent, null); }'
replace_in_file('app/src/main/java/com/my/salah/tracker/app/MainActivity.java', old_prev_w, new_prev_w)

print("🚀 Mega Automation Finished! All issues fixed.")
