package com.my.salah.tracker.app

import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class LanguageEngine(val currentLang: String) {

    private val bnMap: Map<String, String> = mapOf(
        "Fajr" to "ফজর",
        "Dhuhr" to "যোহর",
        "Asr" to "আসর",
        "Maghrib" to "মাগরিব",
        "Isha" to "এশা",
        "Witr" to "বিতর",
        "Tahajjud" to "তাহাজ্জুদ",
        "Sunnah" to "সুন্নাহ",
        "Extras" to "অতিরিক্ত",
        "QAZA" to "কাজা",
        "Today" to "আজকে",
        "This Week" to "এই সপ্তাহ",
        "Mark All" to "সবগুলো আদায় করেছি",
        "All Done" to "সব সম্পন্ন",
        "Good Morning" to "শুভ সকাল",
        "Good Afternoon" to "শুভ অপরাহ্ন",
        "Good Evening" to "শুভ সন্ধ্যা",
        "Good Night" to "শুভ রাত্রি",
        "Settings & Options" to "সেটিংস এবং অপশন",
        "Add Extra Prayer" to "অতিরিক্ত নফল যুক্ত করুন",
        "Prayer Name (e.g. Ishraq)" to "নামাজের নাম (যেমন: ইশরাক)",
        "Rakats (e.g. 2)" to "রাকাত (যেমন: ২)",
        "Add Prayer" to "যুক্ত করুন",
        "Delete Extra Prayer?" to "এই নফল নামাজটি ডিলিট করবেন?",
        "This will remove it from your list." to "এটি আপনার লিস্ট থেকে মুছে যাবে।",
        "Rakats" to "রাকাত",
        "Wipe All Data" to "সব ডাটা মুছে ফেলুন",
        "Are you sure? This will delete all your local data permanently." to "আপনি কি নিশ্চিত? এটি আপনার ফোনের সব লোকাল ডাটা চিরতরে মুছে ফেলবে।",
        "Deleting..." to "মুছে ফেলা হচ্ছে...",
        "Offline Data" to "অফলাইন ডাটা",
        "Data will sync when internet is available." to "ইন্টারনেট কানেকশন এলে ডাটা অটোম্যাটিক সিঙ্ক হবে।",
        "Delete" to "মুছে ফেলুন",
        "items waiting to sync." to "টি ডেটা সিঙ্কের অপেক্ষায় আছে।",
        "Choose Theme" to "থিম পরিবর্তন করুন",
        "Change Language" to "ভাষা পরিবর্তন",
        "Backup & Sync" to "ব্যাকআপ এবং সিঙ্ক",
        "View Qaza List" to "কাজা লিস্ট দেখুন",
        "Advanced Statistics" to "বিস্তারিত রিপোর্ট",
        "Done" to "সম্পন্ন",
        "CLOSE" to "বন্ধ করুন",
        "CANCEL" to "বাতিল",
        "OK" to "ঠিক আছে",
        "Patience is Virtue" to "ভবিষ্যতের নামাজ পড়া সম্ভব নয়",
        "You cannot mark future prayers." to "ভবিষ্যতের নামাজ মার্ক করা যাবে না।",
        "Excused Mode" to "পিরিয়ড / ছুটির মোড",
        "Mark Options" to "নামাজ মার্ক করুন",
        "Fard Only (6 Prayers)" to "শুধুমাত্র ফরজ নামাজ",
        "Include All Sunnahs" to "ফরজ ও সুন্নাহ একসাথে",
        "Unmark Options" to "নামাজ বাতিল করুন",
        "Remove Fard Only" to "শুধুমাত্র ফরজ বাতিল",
        "Remove All (Inc. Sunnah)" to "সবগুলো বাতিল করুন",
        "Select Year" to "বছর নির্বাচন করুন",
        "Start your journey" to "নামাজ শুরু করুন",
        "Great start!" to "দারুণ শুরু!",
        "Keep going" to "চালিয়ে যান",
        "Good progress!" to "অর্ধেক সম্পন্ন!",
        "Almost done!" to "প্রায় শেষ!",
        "Mashallah!" to "মাশাআল্লাহ!",
        "Purity Achieved!" to "আলহামদুলিল্লাহ! সব সম্পন্ন",
        "Secure your data in cloud or local storage" to "ক্লাউড বা লোকাল স্টোরেজে ডাটা সুরক্ষিত রাখুন",
        "Enter Nickname or Email" to "আপনার ইমেইল দিন",
        "Sync Cloud Data" to "ক্লাউড সিঙ্ক করুন",
        "Export JSON" to "লোকাল ব্যাকআপ",
        "Restore JSON" to "রিস্টোর করুন",
        "Select Backup File" to "ব্যাকআপ ফাইল সিলেক্ট করুন",
        "Alhamdulillah! No pending Qaza." to "আলহামদুলিল্লাহ! কোনো কাজা নামাজ নেই।",
        "Weekly Statistics" to "সাপ্তাহিক রিপোর্ট",
        "Monthly Statistics" to "মাসিক রিপোর্ট",
        "Export Premium PDF" to "প্রিমিয়াম PDF ডাউনলোড",
        "Prayers Done" to "আদায়কৃত নামাজ",
        "Missed" to "কাজা হয়েছে",
        "Mark today's prayers as excused. Streak will not break." to "আজকের নামাজগুলো ছুটির মোডে রাখুন। স্ট্রিক ভাঙবে না।",
        "Mark Today as Excused" to "আজকের দিনটি ছুটিতে রাখুন",
        "Remove Excused Status" to "ছুটির মোড বাতিল করুন",
        "Prayers are currently marked as excused." to "আজকের নামাজগুলো বর্তমানে ছুটির মোডে আছে।",
        "Muharram" to "মুহররম",
        "Safar" to "সফর",
        "Rabi I" to "রবিউল আউয়াল",
        "Rabi II" to "রবিউল আখির",
        "Jumada I" to "জুমাদাল ঊলা",
        "Jumada II" to "জুমাদাল উখরা",
        "Rajab" to "রজব",
        "Sha'ban" to "শাবান",
        "Ramadan" to "রমজান",
        "Shawwal" to "শাওয়াল",
        "Dhu al-Qi'dah" to "জিলকদ",
        "Dhu al-Hijjah" to "জিলহজ",
        "AH" to "হিজরি",
        "DAYS STREAK" to "দিনের স্ট্রিক",
        "1 YEAR STREAK" to "১ বছরের স্ট্রিক",
        "Share Report (Image)" to "রিপোর্ট শেয়ার করুন (ছবি)",
        "Current Streak" to "বর্তমান স্ট্রিক",
        "My Salah Journey" to "আমার নামাজের যাত্রা",
        "Tracked with My Salah Tracker" to "My Salah Tracker অ্যাপের মাধ্যমে তৈরি",
        "Share Failed" to "শেয়ার ব্যর্থ হয়েছে",
        "Storage permission required." to "স্টোরেজ পারমিশন প্রয়োজন।",
        "Export Successful" to "সফলভাবে এক্সপোর্ট হয়েছে",
        "Saved to Downloads folder" to "ডাউনলোড ফোল্ডারে সেভ হয়েছে",
        "Export Failed" to "এক্সপোর্ট ব্যর্থ হয়েছে",
        "No Backups Found" to "কোনো ব্যাকআপ পাওয়া যায়নি",
        "No JSON files in Downloads." to "ডাউনলোড ফোল্ডারে কোনো JSON ফাইল নেই।",
        "Restore Successful" to "সফলভাবে রিস্টোর হয়েছে",
        "Data imported" to "ডাটা ইমপোর্ট হয়েছে",
        "Restore Failed" to "রিস্টোর ব্যর্থ হয়েছে",
        "Corrupted file." to "ফাইলটি নষ্ট বা ত্রুটিযুক্ত।",
        "Syncing Data" to "ডাটা সিঙ্ক হচ্ছে",
        "Connecting to cloud..." to "ক্লাউডে কানেক্ট হচ্ছে...",
        "Sync Complete" to "সিঙ্ক সম্পন্ন হয়েছে",
        "Progress updated." to "প্রোগ্রেস আপডেট হয়েছে।",
        "Network Error" to "নেটওয়ার্ক এরর",
        "Check internet connection." to "ইন্টারনেট কানেকশন চেক করুন।",
        "Success" to "সফল",
        "Error" to "ত্রুটি",
        "Prayers marked." to "নামাজ মার্ক করা হয়েছে।",
        "All marked." to "সবগুলো মার্ক করা হয়েছে।",
        "Qaza Saved" to "কাজা সেভ হয়েছে",
        "Entire day marked as pending Qaza." to "পুরো দিনের নামাজ কাজা লিস্টে যুক্ত হয়েছে।",
        "Qaza Removed" to "কাজা মুছে ফেলা হয়েছে",
        "Name removed from Qaza list." to "কাজা লিস্ট থেকে মুছে ফেলা হয়েছে।",
        "You've completed all prayers today.\nMay Allah accept it." to "আলহামদুলিল্লাহ, আজকের সব নামাজ সম্পন্ন হয়েছে।\nআল্লাহ কবুল করুন।",
        "You've completed all prayers for this day.\nMay Allah accept it." to "এই দিনের সব নামাজ সম্পন্ন হয়েছে।\nআল্লাহ কবুল করুন।",
        "Never synced" to "কখনো সিঙ্ক করা হয়নি",
        "Last synced" to "শেষ সিঙ্ক",
        "Skip" to "এড়িয়ে যান",
        "Limit Reached" to "লিমিট শেষ",
        "Cannot go back more than 100 years." to "১০০ বছরের বেশি পেছনে যাওয়া সম্ভব নয়।",
        "Already Added" to "ইতিমধ্যেই যুক্ত আছে",
        "Already in Qaza list." to "এই দিনটি আগে থেকেই কাজা লিস্টে যুক্ত আছে।",
        "Invalid Email" to "ভুল ইমেইল",
        "Please enter a valid email address." to "অনুগ্রহ করে একটি সঠিক ইমেইল অ্যাড্রেস দিন।"
    )

    fun bnNum(num: Any?): String {
        val s = num?.toString() ?: ""
        return if (currentLang == "bn") s.toBnDigits() else s
    }

    fun get(key: String): String {
        return if (currentLang == "bn") bnMap[key] ?: key else key
    }

    fun getBnSuffix(d: Int): String {
        if (currentLang != "bn") return ""
        return when (d) {
            1 -> "লা"
            2, 3 -> "রা"
            4 -> "ঠা"
            in 5..18 -> "ই"
            in 19..31 -> "এ"
            else -> "শে"
        }
    }

    fun getGregorian(d: Date): String {
        if (currentLang != "bn") {
            return SimpleDateFormat("EEEE, MMM dd, yyyy", Locale.US).format(d)
        }
        val c = Calendar.getInstance().apply { time = d }
        val w = arrayOf("রবিবার", "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", "শুক্রবার", "শনিবার")
        val m = arrayOf(
            "জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন",
            "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"
        )
        val day = c.get(Calendar.DAY_OF_MONTH)
        val dayOfWeek = c.get(Calendar.DAY_OF_WEEK) - 1
        val monthIdx = c.get(Calendar.MONTH)
        val year = c.get(Calendar.YEAR)

        return "${w[dayOfWeek]}, ${bnNum(day)}${getBnSuffix(day)} ${m[monthIdx]}, ${bnNum(year)}"
    }

    fun getShortGreg(d: Date): String {
        if (currentLang != "bn") {
            return SimpleDateFormat("MMM dd", Locale.US).format(d)
        }
        val c = Calendar.getInstance().apply { time = d }
        val m = arrayOf("জানু", "ফেব্রু", "মার্চ", "এপ্রি", "মে", "জুন", "জুল", "আগস্ট", "সেপ্টে", "অক্টো", "নভে", "ডিসে")
        val day = c.get(Calendar.DAY_OF_MONTH)
        val monthIdx = c.get(Calendar.MONTH)

        return "${bnNum(day)}${getBnSuffix(day)} ${m[monthIdx]}"
    }
}
