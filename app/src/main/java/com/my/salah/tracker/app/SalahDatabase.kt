package com.my.salah.tracker.app

import android.content.ContentValues
import android.content.Context
import android.database.Cursor
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

/**
 * Entity representing a single day's prayer completion and Qaza records.
 */
data class SalahRecord(
    var date: String,
    var fajr: String = "no",
    var dhuhr: String = "no",
    var asr: String = "no",
    var maghrib: String = "no",
    var isha: String = "no",
    var witr: String = "no",
    var fajr_qaza: Boolean = false,
    var dhuhr_qaza: Boolean = false,
    var asr_qaza: Boolean = false,
    var maghrib_qaza: Boolean = false,
    var isha_qaza: Boolean = false,
    var witr_qaza: Boolean = false
) {
    fun getFardStat(p: String): String = when (p) {
        "Fajr" -> fajr
        "Dhuhr" -> dhuhr
        "Asr" -> asr
        "Maghrib" -> maghrib
        "Isha" -> isha
        "Witr" -> witr
        else -> "no"
    }

    fun setFardStat(p: String, s: String) {
        when (p) {
            "Fajr" -> fajr = s
            "Dhuhr" -> dhuhr = s
            "Asr" -> asr = s
            "Maghrib" -> maghrib = s
            "Isha" -> isha = s
            "Witr" -> witr = s
        }
    }

    fun getQazaStat(p: String): Boolean = when (p) {
        "Fajr" -> fajr_qaza
        "Dhuhr" -> dhuhr_qaza
        "Asr" -> asr_qaza
        "Maghrib" -> maghrib_qaza
        "Isha" -> isha_qaza
        "Witr" -> witr_qaza
        else -> false
    }

    fun setQazaStat(p: String, q: Boolean) {
        when (p) {
            "Fajr" -> fajr_qaza = q
            "Dhuhr" -> dhuhr_qaza = q
            "Asr" -> asr_qaza = q
            "Maghrib" -> maghrib_qaza = q
            "Isha" -> isha_qaza = q
            "Witr" -> witr_qaza = q
        }
    }

    fun isDone(p: String): Boolean {
        val s = getFardStat(p)
        return s == "yes" || s == "excused"
    }

    fun countDone(): Int = AppConstants.PRAYERS.count { isDone(it) }
}

/**
 * Data Access Object interface for SalahRecord queries.
 */
interface SalahDao {
    fun getRecordByDate(date: String): SalahRecord?
    fun getAllRecords(): List<SalahRecord>
    fun insertRecord(record: SalahRecord)
    fun updateRecord(record: SalahRecord)
    fun deleteRecord(record: SalahRecord)
}

/**
 * High-performance, lightweight native SQLite database implementation.
 * Completely eliminates KAPT, Room annotation processing, and ARM64 sqlite-jdbc crashes.
 */
class SalahDatabase private constructor(context: Context) : SQLiteOpenHelper(context.applicationContext, DB_NAME, null, DB_VERSION) {

    private val dao = object : SalahDao {
        override fun getRecordByDate(date: String): SalahRecord? {
            val db = readableDatabase
            return try {
                db.rawQuery("SELECT * FROM $TABLE_NAME WHERE date = ? LIMIT 1", arrayOf(date))?.use { cursor ->
                    if (cursor.moveToFirst()) cursorToRecord(cursor) else null
                }
            } catch (e: Exception) {
                null
            }
        }

        override fun getAllRecords(): List<SalahRecord> {
            val list = mutableListOf<SalahRecord>()
            val db = readableDatabase
            try {
                db.rawQuery("SELECT * FROM $TABLE_NAME", null)?.use { cursor ->
                    if (cursor.moveToFirst()) {
                        do {
                            list.add(cursorToRecord(cursor))
                        } while (cursor.moveToNext())
                    }
                }
            } catch (e: Exception) {
            }
            return list
        }

        override fun insertRecord(record: SalahRecord) {
            try {
                val db = writableDatabase
                val cv = recordToContentValues(record)
                db.insertWithOnConflict(TABLE_NAME, null, cv, SQLiteDatabase.CONFLICT_REPLACE)
            } catch (e: Exception) {
            }
        }

        override fun updateRecord(record: SalahRecord) {
            try {
                val db = writableDatabase
                val cv = recordToContentValues(record)
                db.update(TABLE_NAME, cv, "date = ?", arrayOf(record.date))
            } catch (e: Exception) {
            }
        }

        override fun deleteRecord(record: SalahRecord) {
            try {
                val db = writableDatabase
                db.delete(TABLE_NAME, "date = ?", arrayOf(record.date))
            } catch (e: Exception) {
            }
        }
    }

    fun salahDao(): SalahDao = dao

    fun clearAllTables() {
        try {
            writableDatabase.delete(TABLE_NAME, null, null)
        } catch (e: Exception) {
        }
    }

    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(
            """
            CREATE TABLE IF NOT EXISTS $TABLE_NAME (
                date TEXT PRIMARY KEY NOT NULL,
                fajr TEXT NOT NULL,
                dhuhr TEXT NOT NULL,
                asr TEXT NOT NULL,
                maghrib TEXT NOT NULL,
                isha TEXT NOT NULL,
                witr TEXT NOT NULL,
                fajr_qaza INTEGER NOT NULL,
                dhuhr_qaza INTEGER NOT NULL,
                asr_qaza INTEGER NOT NULL,
                maghrib_qaza INTEGER NOT NULL,
                isha_qaza INTEGER NOT NULL,
                witr_qaza INTEGER NOT NULL
            )
            """.trimIndent()
        )
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
    }

    private fun cursorToRecord(c: Cursor): SalahRecord {
        return SalahRecord(
            date = c.getString(c.getColumnIndexOrThrow("date")),
            fajr = c.getString(c.getColumnIndexOrThrow("fajr")),
            dhuhr = c.getString(c.getColumnIndexOrThrow("dhuhr")),
            asr = c.getString(c.getColumnIndexOrThrow("asr")),
            maghrib = c.getString(c.getColumnIndexOrThrow("maghrib")),
            isha = c.getString(c.getColumnIndexOrThrow("isha")),
            witr = c.getString(c.getColumnIndexOrThrow("witr")),
            fajr_qaza = c.getInt(c.getColumnIndexOrThrow("fajr_qaza")) == 1,
            dhuhr_qaza = c.getInt(c.getColumnIndexOrThrow("dhuhr_qaza")) == 1,
            asr_qaza = c.getInt(c.getColumnIndexOrThrow("asr_qaza")) == 1,
            maghrib_qaza = c.getInt(c.getColumnIndexOrThrow("maghrib_qaza")) == 1,
            isha_qaza = c.getInt(c.getColumnIndexOrThrow("isha_qaza")) == 1,
            witr_qaza = c.getInt(c.getColumnIndexOrThrow("witr_qaza")) == 1
        )
    }

    private fun recordToContentValues(r: SalahRecord): ContentValues {
        return ContentValues().apply {
            put("date", r.date)
            put("fajr", r.fajr)
            put("dhuhr", r.dhuhr)
            put("asr", r.asr)
            put("maghrib", r.maghrib)
            put("isha", r.isha)
            put("witr", r.witr)
            put("fajr_qaza", if (r.fajr_qaza) 1 else 0)
            put("dhuhr_qaza", if (r.dhuhr_qaza) 1 else 0)
            put("asr_qaza", if (r.asr_qaza) 1 else 0)
            put("maghrib_qaza", if (r.maghrib_qaza) 1 else 0)
            put("isha_qaza", if (r.isha_qaza) 1 else 0)
            put("witr_qaza", if (r.witr_qaza) 1 else 0)
        }
    }

    companion object {
        private const val DB_NAME = "salah_tracker_db"
        private const val DB_VERSION = 1
        private const val TABLE_NAME = "salah_records"

        @Volatile
        private var INSTANCE: SalahDatabase? = null

        @JvmField
        val databaseWriteExecutor: ExecutorService = Executors.newFixedThreadPool(4)

        @JvmStatic
        fun getDatabase(context: Context): SalahDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = SalahDatabase(context)
                INSTANCE = instance
                instance
            }
        }

        @JvmStatic
        fun getInstance(context: Context): SalahDatabase = getDatabase(context)
    }
}

/**
 * Helper to migrate legacy SharedPreferences data to SQLite database on first launch.
 */
object DataMigrationHelper {
    @JvmStatic
    fun migrateOldDataToRoom(context: Context) {
        val sp = context.getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE)
        if (sp.getBoolean("is_migrated_to_room_v1", false)) return

        SalahDatabase.databaseWriteExecutor.execute {
            val dao = SalahDatabase.getDatabase(context).salahDao()
            val allEntries = sp.all
            val uniqueDates = HashSet<String>()

            for (key in allEntries.keys) {
                if (key.matches(Regex("\\d{4}-\\d{2}-\\d{2}.*"))) {
                    uniqueDates.add(key.substring(0, 10))
                }
            }

            for (date in uniqueDates) {
                val record = SalahRecord(
                    date = date,
                    fajr = sp.getString("${date}_Fajr", "no") ?: "no",
                    dhuhr = sp.getString("${date}_Dhuhr", "no") ?: "no",
                    asr = sp.getString("${date}_Asr", "no") ?: "no",
                    maghrib = sp.getString("${date}_Maghrib", "no") ?: "no",
                    isha = sp.getString("${date}_Isha", "no") ?: "no",
                    witr = sp.getString("${date}_Witr", "no") ?: "no",
                    fajr_qaza = sp.getBoolean("${date}_Fajr_qaza", false),
                    dhuhr_qaza = sp.getBoolean("${date}_Dhuhr_qaza", false),
                    asr_qaza = sp.getBoolean("${date}_Asr_qaza", false),
                    maghrib_qaza = sp.getBoolean("${date}_Maghrib_qaza", false),
                    isha_qaza = sp.getBoolean("${date}_Isha_qaza", false),
                    witr_qaza = sp.getBoolean("${date}_Witr_qaza", false)
                )
                dao.insertRecord(record)
            }
            sp.edit().putBoolean("is_migrated_to_room_v1", true).apply()
        }
    }
}
