package com.my.salah.tracker.app;

import androidx.annotation.NonNull;
import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "salah_records")
public class SalahRecord {

    @PrimaryKey
    @NonNull
    public String date; // তারিখ হবে আমাদের প্রাইমারি-কি (যেমন: 2026-03-05)

    // ৫ ওয়াক্ত এবং বিতর এর স্ট্যাটাস ("yes", "no", "excused")
    public String fajr = "no";
    public String dhuhr = "no";
    public String asr = "no";
    public String maghrib = "no";
    public String isha = "no";
    public String witr = "no";

    // কাজা নামাজের হিসাব (true মানে কাজা অপেক্ষমাণ আছে, false মানে পড়া হয়েছে বা মাপ)
    public boolean fajr_qaza = false;
    public boolean dhuhr_qaza = false;
    public boolean asr_qaza = false;
    public boolean maghrib_qaza = false;
    public boolean isha_qaza = false;
    public boolean witr_qaza = false;

    // কনস্ট্রাক্টর
    public SalahRecord(@NonNull String date) {
        this.date = date;
    }
}