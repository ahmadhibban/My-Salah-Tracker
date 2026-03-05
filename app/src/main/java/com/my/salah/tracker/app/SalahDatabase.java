package com.my.salah.tracker.app;

import android.content.Context;
import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

// এখানে আমরা বলে দিচ্ছি যে আমাদের ডেটাবেসে SalahRecord নামের একটি টেবিল থাকবে
@Database(entities = {SalahRecord.class}, version = 1, exportSchema = false)
public abstract class SalahDatabase extends RoomDatabase {

    public abstract SalahDao salahDao();

    // Singleton প্যাটার্ন: যাতে পুরো অ্যাপে ডেটাবেসের একটাই ইঞ্জিন চালু থাকে
    private static volatile SalahDatabase INSTANCE;
    
    // ব্যাকগ্রাউন্ডে দ্রুত কাজ করার জন্য থ্রেড পুল (অ্যাপ যেন হ্যাং না করে)
    private static final int NUMBER_OF_THREADS = 4;
    public static final ExecutorService databaseWriteExecutor = Executors.newFixedThreadPool(NUMBER_OF_THREADS);

    public static SalahDatabase getDatabase(final Context context) {
        if (INSTANCE == null) {
            synchronized (SalahDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(context.getApplicationContext(),
                            SalahDatabase.class, "salah_tracker_db")
                            .allowMainThreadQueries() // উইজেট ও দ্রুত লোডিংয়ের জন্য
                            .fallbackToDestructiveMigration() // আপডেট করলে ক্র্যাশ ঠেকানোর জন্য
                            .build();
                }
            }
        }
        return INSTANCE;
    }
}