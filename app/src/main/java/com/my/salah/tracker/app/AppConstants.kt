package com.my.salah.tracker.app

object AppConstants {
    // নামাজের নামগুলো
    @JvmField
    val PRAYERS = arrayOf("Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr")

    // নতুন ১০টি সুন্নত/নফলের ডিসপ্লে নাম
    @JvmField
    val EXTRA_PRAYERS_BN = arrayOf(
        "ফজরের সুন্নত\n(পূর্বে)", "ইশরাক", "চাশত",
        "যোহরের সুন্নত\n(পূর্বে)", "যোহরের সুন্নত\n(পরে)", "আসরের সুন্নত\n(পূর্বে)",
        "মাগরিবের সুন্নত\n(পরে)", "আওয়াবীন", "এশার সুন্নত\n(পরে)", "তাহাজ্জুদ"
    )

    @JvmField
    val EXTRA_PRAYERS_EN = arrayOf(
        "Sunnah\n(Before Fajr)", "Ishraq", "Chasht",
        "Sunnah\n(Before Dhuhr)", "Sunnah\n(After Dhuhr)", "Sunnah\n(Before Asr)",
        "Sunnah\n(After Maghrib)", "Awabeen", "Sunnah\n(After Isha)", "Tahajjud"
    )

    // পুরনো ডেটাবেস Key (যাতে আগের ডেটা না হারায়)
    @JvmField
    val EXTRA_DB_KEYS = arrayOf(
        "Fajr_2 Rakat Sunnah (Before)",
        "Fajr_4 Rakat Ishraq", "Fajr_4 Rakat Chasht", "Dhuhr_4 Rakat Sunnah (Before)",
        "Dhuhr_2 Rakat Sunnah (After)", "Asr_4 Rakat Sunnah (Before)",
        "Maghrib_2 Rakat Sunnah (After)", "Maghrib_6 Rakat Awabeen", "Isha_2 Rakat Sunnah (After)",
        "Isha_4 Rakat Tahajjud"
    )

    // ডিফল্ট রাকাত সংখ্যা
    @JvmField
    val EXTRA_DEF_RAKAT = intArrayOf(2, 4, 4, 4, 2, 4, 2, 6, 2, 4)

    // সুন্নাহর লিস্ট
    @JvmField
    val SUNNAHS = arrayOf(
        arrayOf("2 Rakat Sunnah (Before)", "4 Rakat Ishraq", "4 Rakat Chasht"),
        arrayOf("4 Rakat Sunnah (Before)", "2 Rakat Sunnah (After)"),
        arrayOf("4 Rakat Sunnah (Before)"),
        arrayOf("2 Rakat Sunnah (After)", "6 Rakat Awabeen"),
        arrayOf("2 Rakat Sunnah (After)"),
        arrayOf("4 Rakat Tahajjud")
    )
}
