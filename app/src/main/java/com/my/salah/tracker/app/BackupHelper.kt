package com.my.salah.tracker.app

import android.app.Activity
import android.app.ActivityManager
import android.app.AlertDialog
import android.content.Context
import android.content.SharedPreferences
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.Environment
import android.util.Patterns
import android.view.Gravity
import android.widget.Button
import android.widget.EditText
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import org.json.JSONObject
import java.io.File
import java.io.FileWriter
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class BackupHelper(
    private val activity: Activity,
    private val sp: SharedPreferences,
    private val ui: UIComponents,
    private val lang: LanguageEngine,
    private val fbHelper: FirebaseManager,
    private val DENSITY: Float,
    private val themeColors: IntArray,
    private val colorAccent: Int,
    private val root: FrameLayout
) {
    private var tfReg: Typeface = Typeface.DEFAULT
    private var tfBold: Typeface = Typeface.DEFAULT_BOLD

    init {
        try {
            if (sp.getString("app_lang", "en") == "bn") {
                tfReg = Typeface.createFromAsset(activity.assets, "fonts/hind_reg.ttf")
                tfBold = Typeface.createFromAsset(activity.assets, "fonts/hind_bold.ttf")
            } else {
                tfReg = Typeface.createFromAsset(activity.assets, "fonts/poppins_reg.ttf")
                tfBold = Typeface.createFromAsset(activity.assets, "fonts/poppins_bold.ttf")
            }
        } catch (_: Exception) {}
    }

    fun exportData() {
        try {
            val j = JSONObject()
            val m = sp.all
            for ((k, v) in m) {
                j.put(k, v)
            }
            val dir = activity.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS)
            if (dir != null && !dir.exists()) dir.mkdirs()
            val dStr = SimpleDateFormat("dd_MMM_yyyy", Locale.US).format(Date())
            val f = File(dir, "Salah_Backup_${dStr}_${System.currentTimeMillis() % 1000}.json")
            FileWriter(f).use { it.write(j.toString()) }

            ui.showSmartBanner(
                root,
                lang.get("Export Successful"),
                lang.get("Saved to Downloads folder"),
                "img_tick",
                colorAccent,
                null
            )
        } catch (e: Exception) {
            ui.showSmartBanner(
                root,
                lang.get("Export Failed"),
                lang.get("Storage permission required."),
                "img_warning",
                colorAccent,
                null
            )
        }
    }

    fun showRestoreDialog(reload: Runnable?) {
        val dir = activity.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS)
        val files = dir?.listFiles { _, name ->
            name.lowercase(Locale.ROOT).endsWith(".json") && name.contains("Salah")
        }

        if (files.isNullOrEmpty()) {
            ui.showSmartBanner(
                root,
                lang.get("No Backups Found"),
                lang.get("No JSON files in Downloads."),
                "img_warning",
                colorAccent,
                null
            )
            return
        }

        val wrap = FrameLayout(activity).apply {
            layoutParams = FrameLayout.LayoutParams(-1, -1)
        }
        val main = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            val padH = (20 * DENSITY).toInt()
            val padV = (25 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            background = GradientDrawable().apply {
                setColor(themeColors[1])
                cornerRadius = 25f * DENSITY
            }
        }

        val title = TextView(activity).apply {
            text = lang.get("Select Backup File")
            setTextColor(themeColors[2])
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
            setPadding(0, 0, 0, (15 * DENSITY).toInt())
        }
        main.addView(title)

        val sv = ScrollView(activity)
        val list = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
        }

        val ad = AlertDialog.Builder(activity).setView(wrap).create()
        ad.window?.setBackgroundDrawableResource(android.R.color.transparent)
        ad.window?.setGravity(Gravity.CENTER)

        for (f in files) {
            val tv = TextView(activity).apply {
                text = "📄 ${f.name}"
                setTextColor(themeColors[3])
                textSize = 14f
                val pad = (12 * DENSITY).toInt()
                setPadding(pad, pad, pad, pad)
                background = GradientDrawable().apply {
                    setColor(themeColors[4])
                    cornerRadius = 15f * DENSITY
                }
                layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                    setMargins(0, 0, 0, (10 * DENSITY).toInt())
                }
                setOnClickListener {
                    try {
                        val textContent = f.readText()
                        val j = JSONObject(textContent)
                        val ed = sp.edit()
                        val keys = j.keys()
                        while (keys.hasNext()) {
                            val k = keys.next()
                            when (val valObj = j.get(k)) {
                                is Boolean -> ed.putBoolean(k, valObj)
                                is String -> ed.putString(k, valObj)
                                is Int -> ed.putInt(k, valObj)
                                is Long -> ed.putLong(k, valObj)
                            }
                        }
                        val curQ = sp.getString("offline_q", "")
                        ed.putString("offline_q", curQ)
                        ed.putBoolean("is_migrated_to_room_v1", false).apply()
                        DataMigrationHelper.migrateOldDataToRoom(activity)

                        ui.showSmartBanner(
                            root,
                            lang.get("Restore Successful"),
                            lang.get("Data imported"),
                            "img_tick",
                            colorAccent,
                            null
                        )
                        reload?.run()
                        ad.dismiss()
                    } catch (e: Exception) {
                        ui.showSmartBanner(
                            root,
                            lang.get("Restore Failed"),
                            lang.get("Corrupted file."),
                            "img_warning",
                            colorAccent,
                            null
                        )
                    }
                }
            }
            list.addView(tv)
        }
        sv.addView(list)
        main.addView(sv, LinearLayout.LayoutParams(-1, (300 * DENSITY).toInt()))

        // --- DANGER ZONE ---
        val dangerTitle = TextView(activity).apply {
            text = lang.get("Danger Zone")
            setTextColor(Color.parseColor("#FF5252"))
            textSize = 16f
            typeface = tfBold
            setPadding(0, (25 * DENSITY).toInt(), 0, (15 * DENSITY).toInt())
        }
        main.addView(dangerTitle)

        val btnWipeLocal = LinearLayout(activity).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            val pad = (15 * DENSITY).toInt()
            setPadding(pad, pad, pad, pad)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#1AFF4444"))
                cornerRadius = 15f * DENSITY
            }
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(0, 0, 0, (12 * DENSITY).toInt())
            }
        }
        val txtWipeLocal = TextView(activity).apply {
            text = "Delete All Data & Start Fresh"
            setTextColor(Color.parseColor("#FF5252"))
            typeface = tfBold
            textSize = 15f
        }
        btnWipeLocal.addView(txtWipeLocal)
        main.addView(btnWipeLocal)

        btnWipeLocal.setOnClickListener {
            AlertDialog.Builder(activity)
                .setTitle("⚠️ Delete All Data")
                .setMessage("Are you sure? This will wipe your history, settings, and start fresh. This action cannot be undone.")
                .setPositiveButton("Yes, Delete") { _, _ ->
                    Toast.makeText(activity, "Wiping all data...", Toast.LENGTH_SHORT).show()
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
                        val am = activity.getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager
                        am?.clearApplicationUserData()
                    }
                }
                .setNegativeButton("Cancel", null)
                .show()
        }

        val flp = FrameLayout.LayoutParams((300 * DENSITY).toInt(), -2).apply {
            gravity = Gravity.CENTER
        }
        wrap.addView(main, flp)
        wrap.applyFont(tfReg, tfBold)

        if (!activity.isFinishing) {
            ad.show()
        }
    }

    fun showProfileDialog(onReload: Runnable?) {
        val wrap = FrameLayout(activity).apply {
            layoutParams = FrameLayout.LayoutParams(-1, -1)
        }
        val rootDia = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            val padH = (25 * DENSITY).toInt()
            val padV = (30 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            background = GradientDrawable().apply {
                setColor(themeColors[1])
                cornerRadius = 25f * DENSITY
            }
        }

        val iconView = ui.getRoundImage("img_custom_backup", 0, Color.TRANSPARENT, colorAccent).apply {
            layoutParams = LinearLayout.LayoutParams((50 * DENSITY).toInt(), (50 * DENSITY).toInt()).apply {
                gravity = Gravity.CENTER_HORIZONTAL
                setMargins(0, 0, 0, (15 * DENSITY).toInt())
            }
        }
        rootDia.addView(iconView)

        val title = TextView(activity).apply {
            text = lang.get("Backup & Sync")
            gravity = Gravity.CENTER
            setTextColor(themeColors[2])
            textSize = 22f
            typeface = Typeface.DEFAULT_BOLD
        }
        rootDia.addView(title)

        val lastSyncTime = sp.getLong("last_sync", 0)
        val syncDateFmt = SimpleDateFormat("dd MMM, hh:mm a", Locale.US)
        val syncText = if (lastSyncTime == 0L) {
            lang.get("Never synced")
        } else {
            val dateStr = syncDateFmt.format(Date(lastSyncTime))
            "${lang.get("Last synced")}: ${if (lang.get("Fajr") == "ফজর") lang.bnNum(dateStr) else dateStr}"
        }

        val desc = TextView(activity).apply {
            text = "${lang.get("Secure your data in cloud or local storage")}\n($syncText)"
            gravity = Gravity.CENTER
            setTextColor(themeColors[3])
            textSize = 13f
            setPadding(0, 0, 0, (20 * DENSITY).toInt())
        }
        rootDia.addView(desc)

        val emailIn = EditText(activity).apply {
            hint = lang.get("Enter Nickname or Email")
            setText(sp.getString("user_email", ""))
            val padH = (20 * DENSITY).toInt()
            val padV = (15 * DENSITY).toInt()
            setPadding(padH, padV, padH, padV)
            textSize = 15f
            setTextColor(themeColors[2])
            setHintTextColor(themeColors[3])
            isSingleLine = true
            background = GradientDrawable().apply {
                cornerRadius = 15f * DENSITY
                setColor(themeColors[4])
            }
            layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
                setMargins(0, 0, 0, (15 * DENSITY).toInt())
            }
        }
        rootDia.addView(emailIn)

        val actionBtn = Button(activity).apply {
            text = lang.get("Sync Cloud Data")
            isAllCaps = false
            setTextColor(Color.WHITE)
            textSize = 15f
            typeface = Typeface.DEFAULT_BOLD
            background = GradientDrawable().apply {
                setColor(colorAccent)
                cornerRadius = 15f * DENSITY
            }
            layoutParams = LinearLayout.LayoutParams(-1, (50 * DENSITY).toInt()).apply {
                setMargins(0, 0, 0, (20 * DENSITY).toInt())
            }
        }
        rootDia.addView(actionBtn)

        val localRow = LinearLayout(activity).apply {
            orientation = LinearLayout.HORIZONTAL
        }
        val bEx = Button(activity).apply {
            text = lang.get("Export JSON")
            isAllCaps = false
            setTextColor(colorAccent)
            typeface = Typeface.DEFAULT_BOLD
            textSize = 12f
            isSingleLine = true
            background = GradientDrawable().apply {
                setColor(themeColors[5])
                cornerRadius = 12f * DENSITY
            }
            layoutParams = LinearLayout.LayoutParams(0, (45 * DENSITY).toInt(), 1f).apply {
                setMargins(0, 0, (8 * DENSITY).toInt(), 0)
            }
        }
        localRow.addView(bEx)

        val bIm = Button(activity).apply {
            text = lang.get("Restore JSON")
            isAllCaps = false
            setTextColor(colorAccent)
            typeface = Typeface.DEFAULT_BOLD
            textSize = 12f
            isSingleLine = true
            background = GradientDrawable().apply {
                setColor(themeColors[5])
                cornerRadius = 12f * DENSITY
            }
            layoutParams = LinearLayout.LayoutParams(0, (45 * DENSITY).toInt(), 1f).apply {
                setMargins((8 * DENSITY).toInt(), 0, 0, 0)
            }
        }
        localRow.addView(bIm)
        rootDia.addView(localRow)

        val flp = FrameLayout.LayoutParams((320 * DENSITY).toInt(), -2).apply {
            gravity = Gravity.CENTER
        }
        wrap.addView(rootDia, flp)
        wrap.applyFont(tfReg, tfBold)

        val ad = AlertDialog.Builder(activity).setView(wrap).create()
        ad.window?.setBackgroundDrawableResource(android.R.color.transparent)
        ad.window?.setGravity(Gravity.CENTER)

        actionBtn.setOnClickListener {
            val mail = emailIn.text.toString().trim()
            if (mail.isEmpty() || !Patterns.EMAIL_ADDRESS.matcher(mail).matches()) {
                ui.showSmartBanner(
                    root,
                    lang.get("Invalid Email"),
                    lang.get("Please enter a valid email address."),
                    "img_warning",
                    colorAccent,
                    null
                )
                return@setOnClickListener
            }
            sp.edit().putString("user_email", mail).apply()
            ad.dismiss()

            fbHelper.fetchAndLoad(
                {
                    ui.showSmartBanner(
                        root,
                        lang.get("Syncing Data"),
                        lang.get("Connecting to cloud..."),
                        "img_custom_backup",
                        colorAccent,
                        null
                    )
                },
                {
                    ui.showSmartBanner(
                        root,
                        lang.get("Sync Complete"),
                        lang.get("Progress updated."),
                        "img_tick",
                        colorAccent,
                        null
                    )
                    onReload?.run()
                },
                {
                    ui.showSmartBanner(
                        root,
                        lang.get("Network Error"),
                        lang.get("Check internet connection."),
                        "img_warning",
                        colorAccent,
                        null
                    )
                    onReload?.run()
                }
            )
        }

        bEx.setOnClickListener {
            exportData()
            ad.dismiss()
        }

        bIm.setOnClickListener {
            showRestoreDialog(onReload)
            ad.dismiss()
        }

        if (!activity.isFinishing) {
            ad.show()
        }
    }
}
