package com.my.salah.tracker.app;

public class AppConstants
{
    // নামাজের নামগুলো
    public static final String[] PRAYERS = {"Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr"};

    // নতুন ১০টি সুন্নত/নফলের ডিসপ্লে নাম
    public static final String[] EXTRA_PRAYERS_BN = {"ফজরের সুন্নত\n(পূর্বে)", "ইশরাক", "চাশত",
        "যোহরের সুন্নত\n(পূর্বে)", "যোহরের সুন্নত\n(পরে)", "আসরের সুন্নত\n(পূর্বে)", "মাগরিবের সুন্নত\n(পরে)",
        "আওয়াবীন", "এশার সুন্নত\n(পরে)", "তাহাজ্জুদ"};

    public static final String[] EXTRA_PRAYERS_EN = {"Sunnah\n(Before Fajr)", "Ishraq", "Chasht",
        "Sunnah\n(Before Dhuhr)", "Sunnah\n(After Dhuhr)", "Sunnah\n(Before Asr)",
        "Sunnah\n(After Maghrib)", "Awabeen", "Sunnah\n(After Isha)", "Tahajjud"};

    // পুরনো ডেটাবেস Key (যাতে আগের ডেটা না হারায়)
    public static final String[] EXTRA_DB_KEYS = {"Fajr_2 Rakat Sunnah (Before)",
        "Fajr_4 Rakat Ishraq", "Fajr_4 Rakat Chasht", "Dhuhr_4 Rakat Sunnah (Before)",
        "Dhuhr_2 Rakat Sunnah (After)", "Asr_4 Rakat Sunnah (Before)",
        "Maghrib_2 Rakat Sunnah (After)", "Maghrib_6 Rakat Awabeen", "Isha_2 Rakat Sunnah (After)",
        "Isha_4 Rakat Tahajjud"};

    // ডিফল্ট রাকাত সংখ্যা
    public static final int[] EXTRA_DEF_RAKAT = {2, 4, 4, 4, 2, 4, 2, 6, 2, 4};

    // সুন্নাহর লিস্ট
    public static final String[][] SUNNAHS = {
        {"2 Rakat Sunnah (Before)", "4 Rakat Ishraq", "4 Rakat Chasht"},
        {"4 Rakat Sunnah (Before)", "2 Rakat Sunnah (After)"}, {"4 Rakat Sunnah (Before)"},
        {"2 Rakat Sunnah (After)", "6 Rakat Awabeen"}, {"2 Rakat Sunnah (After)"},
        {"4 Rakat Tahajjud"}};
}
