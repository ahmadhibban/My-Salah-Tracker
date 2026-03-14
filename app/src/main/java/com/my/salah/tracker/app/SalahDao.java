package com.my.salah.tracker.app;

import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.OnConflictStrategy;
import androidx.room.Query;
import androidx.room.Update;
import java.util.List;

@Dao
public interface SalahDao {
    // নতুন দিনের ডেটা সেভ করবে বা আগে থেকে থাকলে রিপ্লেস করবে
    @Insert(onConflict = OnConflictStrategy.REPLACE) void insertRecord(SalahRecord record);

    // ডেটা আপডেট করবে (যখন ইউজার টিক চিহ্ন দেবে)
    @Update void updateRecord(SalahRecord record);

    // নির্দিষ্ট একটি তারিখের ডেটা খুঁজে বের করবে
    @Query("SELECT * FROM salah_records WHERE date = :targetDate LIMIT 1")
    SalahRecord getRecordByDate(String targetDate);

    // পুরো মাসের ডেটা একসাথে আনবে (পরিসংখ্যানের জন্য)
    @Query("SELECT * FROM salah_records WHERE date LIKE :monthPrefix || '%'")
    List<SalahRecord> getRecordsByMonth(String monthPrefix);  // Format: "2026-03"

    // মোট কতগুলো কাজা বাকি আছে সেটা গুনবে
    @Query(
        "SELECT SUM(fajr_qaza + dhuhr_qaza + asr_qaza + maghrib_qaza + isha_qaza + witr_qaza) FROM salah_records")
    int
    getTotalPendingQaza();
}