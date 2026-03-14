package com.my.salah.tracker.app;

import android.content.Context;
import android.content.SharedPreferences;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class DataMigrationHelper
{
    public static void migrateOldDataToRoom(final Context context)
    {
        final SharedPreferences sp =
            context.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE);

        // যদি আগে থেকেই ট্রান্সফার হয়ে থাকে, তবে আর কিছুই করবে না
        boolean isMigrated = sp.getBoolean("is_migrated_to_room_v1", false);
        if (isMigrated)
            return;

        // ব্যাকগ্রাউন্ড থ্রেডে ডেটা ট্রান্সফার করবে যাতে অ্যাপ হ্যাং না করে
        SalahDatabase.databaseWriteExecutor.execute(new Runnable() {
            @Override public void run()
            {
                SalahDao dao = SalahDatabase.getDatabase(context).salahDao();
                Map<String, ?> allEntries = sp.getAll();
                Set<String> uniqueDates = new HashSet<>();

                // SharedPreferences থেকে সব তারিখ (যেমন: 2026-03-05) খুঁজে বের করা
                for (Map.Entry<String, ?> entry : allEntries.entrySet()) {
                    String key = entry.getKey();
                    if (key.matches("\\d{4}-\\d{2}-\\d{2}.*")) {
                        uniqueDates.add(key.substring(0, 10));
                    }
                }

                // খুঁজে পাওয়া তারিখগুলোর ডেটা Room Database-এ সেভ করা
                for (String date : uniqueDates) {
                    SalahRecord record = new SalahRecord(date);

                    // নামাজের স্ট্যাটাস
                    record.fajr = sp.getString(date + "_Fajr", "no");
                    record.dhuhr = sp.getString(date + "_Dhuhr", "no");
                    record.asr = sp.getString(date + "_Asr", "no");
                    record.maghrib = sp.getString(date + "_Maghrib", "no");
                    record.isha = sp.getString(date + "_Isha", "no");
                    record.witr = sp.getString(date + "_Witr", "no");

                    // কাজা নামাজের স্ট্যাটাস
                    record.fajr_qaza = sp.getBoolean(date + "_Fajr_qaza", false);
                    record.dhuhr_qaza = sp.getBoolean(date + "_Dhuhr_qaza", false);
                    record.asr_qaza = sp.getBoolean(date + "_Asr_qaza", false);
                    record.maghrib_qaza = sp.getBoolean(date + "_Maghrib_qaza", false);
                    record.isha_qaza = sp.getBoolean(date + "_Isha_qaza", false);
                    record.witr_qaza = sp.getBoolean(date + "_Witr_qaza", false);

                    dao.insertRecord(record);
                }

                // ট্রান্সফার সফল হলে মার্ক করে রাখা, যেন দ্বিতীয়বার আর রান না হয়
                sp.edit().putBoolean("is_migrated_to_room_v1", true).apply();
            }
        });
    }
}