import os

main_activity = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(main_activity):
    with open(main_activity, "r", encoding="utf-8") as f:
        content = f.read()

    # ১. Backup & Sync বাটনকে নতুন প্রিমিয়াম পেইজের সাথে লিংক করা
    old_backup = """mr.addImg("Backup & Sync", "img_cloud", new Runnable() {
            @Override public void run()
            {
                backupHelper.showProfileDialog(new Runnable() {
                    @Override public void run()
                    {
                        loadTodayPage();
                        refreshWidget();
                    }
                });
            }
        });"""
    
    new_backup = """mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "ব্যাকআপ এবং সিঙ্ক" : "Backup & Sync", "img_cloud", new Runnable() {
            @Override public void run()
            {
                showPremiumSyncSettingsDialog();
            }
        });"""

    # ২. কাজা নামাজের বাটনটি দৃশ্যমান (Uncomment) করা
    old_qaza = """// mr.addImg("View Qaza List", "img_custom_qaza", new Runnable() { @Override
        // public void run() { showQazaListDialog(); }});"""
    
    new_qaza = """mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "কাজা নামাজের তালিকা" : "View Qaza List", "img_custom_qaza", new Runnable() {
            @Override public void run() { showQazaListDialog(); }
        });"""

    # রিপ্লেস করা
    if old_backup in content or old_qaza in content:
        content = content.replace(old_backup, new_backup)
        content = content.replace(old_qaza, new_qaza)
        
        with open(main_activity, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Success! বাটনগুলোর লিংক ঠিক করা হয়েছে এবং কাজা নামাজের লিস্ট চালু করা হয়েছে।")
    else:
        print("⚠️ কোডগুলো ফাইলে পাওয়া যায়নি। হয়তো আগেই পরিবর্তন করা হয়েছে।")
else:
    print("❌ MainActivity পাওয়া যায়নি।")
