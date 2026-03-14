package com.my.salah.tracker.app;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;

public class LanguageEngine
{
    private String currentLang;
    private HashMap<String, String> bnMap = new HashMap<>();

    public LanguageEngine(String lang)
    {
        this.currentLang = lang;

        bnMap.put("Fajr", "ফজর");
        bnMap.put("Dhuhr", "যোহর");
        bnMap.put("Asr", "আসর");
        bnMap.put("Maghrib", "মাগরিব");
        bnMap.put("Isha", "এশা");
        bnMap.put("Witr", "বিতর");
        bnMap.put("Tahajjud", "তাহাজ্জুদ");
        bnMap.put("Sunnah", "সুন্নাহ");
        bnMap.put("Extras", "অতিরিক্ত");
        bnMap.put("QAZA", "কাজা");
        bnMap.put("Today", "আজকে");
        bnMap.put("This Week", "এই সপ্তাহ");
        bnMap.put("Mark All", "সবগুলো আদায় করেছি");
        bnMap.put("All Done", "সব সম্পন্ন");
        bnMap.put("Good Morning", "শুভ সকাল");
        bnMap.put("Good Afternoon", "শুভ অপরাহ্ন");
        bnMap.put("Good Evening", "শুভ সন্ধ্যা");
        bnMap.put("Good Night", "শুভ রাত্রি");
        bnMap.put("Settings & Options", "সেটিংস এবং অপশন");
        bnMap.put("Add Extra Prayer", "অতিরিক্ত নফল যুক্ত করুন");
        bnMap.put("Prayer Name (e.g. Ishraq)", "নামাজের নাম (যেমন: ইশরাক)");
        bnMap.put("Rakats (e.g. 2)", "রাকাত (যেমন: ২)");
        bnMap.put("Add Prayer", "যুক্ত করুন");
        bnMap.put("Delete Extra Prayer?", "এই নফল নামাজটি ডিলিট করবেন?");
        bnMap.put("This will remove it from your list.", "এটি আপনার লিস্ট থেকে মুছে যাবে।");
        bnMap.put("Rakats", "রাকাত");
        bnMap.put("Wipe All Data", "সব ডাটা মুছে ফেলুন");
        bnMap.put("Are you sure? This will delete all your local data permanently.",
            "আপনি কি নিশ্চিত? এটি আপনার ফোনের সব লোকাল ডাটা চিরতরে মুছে ফেলবে।");
        bnMap.put("Deleting...", "মুছে ফেলা হচ্ছে...");
        bnMap.put("Offline Data", "অফলাইন ডাটা");
        bnMap.put("Data will sync when internet is available.",
            "ইন্টারনেট কানেকশন এলে ডাটা অটোম্যাটিক সিঙ্ক হবে।");
        bnMap.put("Delete", "মুছে ফেলুন");
        bnMap.put("items waiting to sync.", "টি ডেটা সিঙ্কের অপেক্ষায় আছে।");
        bnMap.put("Choose Theme", "থিম পরিবর্তন করুন");
        bnMap.put("Change Language", "ভাষা পরিবর্তন");
        bnMap.put("Backup & Sync", "ব্যাকআপ এবং সিঙ্ক");
        bnMap.put("View Qaza List", "কাজা লিস্ট দেখুন");
        bnMap.put("Advanced Statistics", "বিস্তারিত রিপোর্ট");
        bnMap.put("Done", "সম্পন্ন");
        bnMap.put("CLOSE", "বন্ধ করুন");
        bnMap.put("CANCEL", "বাতিল");
        bnMap.put("OK", "ঠিক আছে");
        bnMap.put("Patience is Virtue", "ভবিষ্যতের নামাজ পড়া সম্ভব নয়");
        bnMap.put("You cannot mark future prayers.", "ভবিষ্যতের নামাজ মার্ক করা যাবে না।");
        bnMap.put("Excused Mode", "পিরিয়ড / ছুটির মোড");
        bnMap.put("Mark Options", "নামাজ মার্ক করুন");
        bnMap.put("Fard Only (6 Prayers)", "শুধুমাত্র ফরজ নামাজ");
        bnMap.put("Include All Sunnahs", "ফরজ ও সুন্নাহ একসাথে");
        bnMap.put("Unmark Options", "নামাজ বাতিল করুন");
        bnMap.put("Remove Fard Only", "শুধুমাত্র ফরজ বাতিল");
        bnMap.put("Remove All (Inc. Sunnah)", "সবগুলো বাতিল করুন");
        bnMap.put("Select Year", "বছর নির্বাচন করুন");
        bnMap.put("Start your journey", "নামাজ শুরু করুন");
        bnMap.put("Great start!", "দারুণ শুরু!");
        bnMap.put("Keep going", "চালিয়ে যান");
        bnMap.put("Good progress!", "অর্ধেক সম্পন্ন!");
        bnMap.put("Almost done!", "প্রায় শেষ!");
        bnMap.put("Mashallah!", "মাশাআল্লাহ!");
        bnMap.put("Purity Achieved!", "আলহামদুলিল্লাহ! সব সম্পন্ন");
        bnMap.put("Secure your data in cloud or local storage",
            "ক্লাউড বা লোকাল স্টোরেজে ডাটা সুরক্ষিত রাখুন");
        bnMap.put("Enter Nickname or Email", "আপনার ইমেইল দিন");
        bnMap.put("Sync Cloud Data", "ক্লাউড সিঙ্ক করুন");
        bnMap.put("Export JSON", "লোকাল ব্যাকআপ");  // ✨ Text shortened
        bnMap.put("Restore JSON", "রিস্টোর করুন");  // ✨ Text shortened
        bnMap.put("Select Backup File", "ব্যাকআপ ফাইল সিলেক্ট করুন");
        bnMap.put("Alhamdulillah! No pending Qaza.", "আলহামদুলিল্লাহ! কোনো কাজা নামাজ নেই।");
        bnMap.put("Weekly Statistics", "সাপ্তাহিক রিপোর্ট");
        bnMap.put("Monthly Statistics", "মাসিক রিপোর্ট");
        bnMap.put("Export Premium PDF", "প্রিমিয়াম PDF ডাউনলোড");
        bnMap.put("Prayers Done", "আদায়কৃত নামাজ");
        bnMap.put("Missed", "কাজা হয়েছে");
        bnMap.put("Mark today's prayers as excused. Streak will not break.",
            "আজকের নামাজগুলো ছুটির মোডে রাখুন। স্ট্রিক ভাঙবে না।");
        bnMap.put("Mark Today as Excused", "আজকের দিনটি ছুটিতে রাখুন");
        bnMap.put("Remove Excused Status", "ছুটির মোড বাতিল করুন");
        bnMap.put(
            "Prayers are currently marked as excused.", "আজকের নামাজগুলো বর্তমানে ছুটির মোডে আছে।");
        bnMap.put("Muharram", "মুহররম");
        bnMap.put("Safar", "সফর");
        bnMap.put("Rabi I", "রবিউল আউয়াল");
        bnMap.put("Rabi II", "রবিউল আখির");
        bnMap.put("Jumada I", "জুমাদাল ঊলা");
        bnMap.put("Jumada II", "জুমাদাল উখরা");
        bnMap.put("Rajab", "রজব");
        bnMap.put("Sha'ban", "শাবান");
        bnMap.put("Ramadan", "রমজান");
        bnMap.put("Shawwal", "শাওয়াল");
        bnMap.put("Dhu al-Qi'dah", "জিলকদ");
        bnMap.put("Dhu al-Hijjah", "জিলহজ");
        bnMap.put("AH", "হিজরি");
        bnMap.put("DAYS STREAK", "দিনের স্ট্রিক");
        bnMap.put("1 YEAR STREAK", "১ বছরের স্ট্রিক");
        bnMap.put("Share Report (Image)", "রিপোর্ট শেয়ার করুন (ছবি)");
        bnMap.put("Current Streak", "বর্তমান স্ট্রিক");
        bnMap.put("My Salah Journey", "আমার নামাজের যাত্রা");
        bnMap.put("Tracked with My Salah Tracker", "My Salah Tracker অ্যাপের মাধ্যমে তৈরি");
        bnMap.put("Share Failed", "শেয়ার ব্যর্থ হয়েছে");
        bnMap.put("Storage permission required.", "স্টোরেজ পারমিশন প্রয়োজন।");
        bnMap.put("Export Successful", "সফলভাবে এক্সপোর্ট হয়েছে");
        bnMap.put("Saved to Downloads folder", "ডাউনলোড ফোল্ডারে সেভ হয়েছে");
        bnMap.put("Export Failed", "এক্সপোর্ট ব্যর্থ হয়েছে");
        bnMap.put("No Backups Found", "কোনো ব্যাকআপ পাওয়া যায়নি");
        bnMap.put("No JSON files in Downloads.", "ডাউনলোড ফোল্ডারে কোনো JSON ফাইল নেই।");
        bnMap.put("Restore Successful", "সফলভাবে রিস্টোর হয়েছে");
        bnMap.put("Data imported", "ডাটা ইমপোর্ট হয়েছে");
        bnMap.put("Restore Failed", "রিস্টোর ব্যর্থ হয়েছে");
        bnMap.put("Corrupted file.", "ফাইলটি নষ্ট বা ত্রুটিযুক্ত।");
        bnMap.put("Syncing Data", "ডাটা সিঙ্ক হচ্ছে");
        bnMap.put("Connecting to cloud...", "ক্লাউডে কানেক্ট হচ্ছে...");
        bnMap.put("Sync Complete", "সিঙ্ক সম্পন্ন হয়েছে");
        bnMap.put("Progress updated.", "প্রোগ্রেস আপডেট হয়েছে।");
        bnMap.put("Network Error", "নেটওয়ার্ক এরর");
        bnMap.put("Check internet connection.", "ইন্টারনেট কানেকশন চেক করুন।");
        bnMap.put("Success", "সফল");
        bnMap.put("Error", "ত্রুটি");
        bnMap.put("Prayers marked.", "নামাজ মার্ক করা হয়েছে।");
        bnMap.put("All marked.", "সবগুলো মার্ক করা হয়েছে।");
        bnMap.put("Qaza Saved", "কাজা সেভ হয়েছে");
        bnMap.put("Entire day marked as pending Qaza.", "পুরো দিনের নামাজ কাজা লিস্টে যুক্ত হয়েছে।");
        bnMap.put("Qaza Removed", "কাজা মুছে ফেলা হয়েছে");
        bnMap.put("Name removed from Qaza list.", "কাজা লিস্ট থেকে মুছে ফেলা হয়েছে।");
        bnMap.put("You've completed all prayers today.\nMay Allah accept it.",
            "আলহামদুলিল্লাহ, আজকের সব নামাজ সম্পন্ন হয়েছে।\nআল্লাহ কবুল করুন।");
        bnMap.put("You've completed all prayers for this day.\nMay Allah accept it.",
            "এই দিনের সব নামাজ সম্পন্ন হয়েছে।\nআল্লাহ কবুল করুন।");
        bnMap.put("Never synced", "কখনো সিঙ্ক করা হয়নি");
        bnMap.put("Last synced", "শেষ সিঙ্ক");
        bnMap.put("Skip", "এড়িয়ে যান");
        bnMap.put("Limit Reached", "লিমিট শেষ");
        bnMap.put("Cannot go back more than 100 years.", "১০০ বছরের বেশি পেছনে যাওয়া সম্ভব নয়।");
        bnMap.put("Already Added", "ইতিমধ্যেই যুক্ত আছে");
        bnMap.put("Already in Qaza list.", "এই দিনটি আগে থেকেই কাজা লিস্টে যুক্ত আছে।");
        bnMap.put("Invalid Email", "ভুল ইমেইল");
        bnMap.put("Please enter a valid email address.", "অনুগ্রহ করে একটি সঠিক ইমেইল অ্যাড্রেস দিন।");
    }

    public String bnNum(Object num)
    {
        if (!currentLang.equals("bn"))
            return String.valueOf(num);
        String s = String.valueOf(num);
        String[] en = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"};
        String[] bn = {"০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯"};
        for (int i = 0; i < 10; i++) s = s.replace(en[i], bn[i]);
        return s;
    }

    public String get(String key)
    {
        if (currentLang.equals("bn") && bnMap.containsKey(key))
            return bnMap.get(key);
        return key;
    }

    // ✨ ম্যাজিক: ই, শে, রা, ঠা যুক্ত করার ফাংশন
    public String getBnSuffix(int d)
    {
        if (!currentLang.equals("bn"))
            return "";
        if (d == 1)
            return "লা";
        if (d == 2 || d == 3)
            return "রা";
        if (d == 4)
            return "ঠা";
        if (d >= 5 && d <= 18)
            return "ই";
        if (d >= 19 && d <= 31)
            return "এ";
        return "শে";
    }

    public String getGregorian(Date d)
    {
        if (!currentLang.equals("bn"))
            return new SimpleDateFormat("EEEE, MMM dd, yyyy", Locale.US).format(d);
        Calendar c = Calendar.getInstance();
        c.setTime(d);
        String[] w = {"রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার"};
        String[] m = {"জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রি", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর",
            "অক্টোবর", "নভেম্বর", "ডিসেম্বর"};
        int day = c.get(Calendar.DAY_OF_MONTH);
        // ✨ এখানে সাফিক্স যুক্ত করে দেওয়া হলো
        return w[c.get(Calendar.DAY_OF_WEEK) - 1] + ", " + bnNum(day) + getBnSuffix(day) + " "
            + m[c.get(Calendar.MONTH)] + ", " + bnNum(c.get(Calendar.YEAR));
    }

    public String getShortGreg(Date d)
    {
        if (!currentLang.equals("bn"))
            return new SimpleDateFormat("MMM dd", Locale.US).format(d);
        Calendar c = Calendar.getInstance();
        c.setTime(d);
        String[] m = {"জানু", "ফেব্রু", "মার্চ", "এপ্রি", "মে", "জুন", "জুল", "আগস্ট", "সেপ্টে", "অক্টো",
            "নভে", "ডিসে"};
        int day = c.get(Calendar.DAY_OF_MONTH);
        // ✨ এখানেও সাফিক্স যুক্ত করে দেওয়া হলো
        return bnNum(day) + getBnSuffix(day) + " " + m[c.get(Calendar.MONTH)];
    }
}