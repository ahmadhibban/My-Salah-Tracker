import os
import re

main_activity = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
backup_helper = "app/src/main/java/com/my/salah/tracker/app/BackupHelper.java"

# ১. MainActivity-তে আপনার অরিজিনাল Backup & Sync লিংকটি ফিরিয়ে আনা
if os.path.exists(main_activity):
    with open(main_activity, "r", encoding="utf-8") as f: content = f.read()
    
    bad_link = "showPremiumSyncSettingsDialog();"
    good_link = """backupHelper.showProfileDialog(new Runnable() {
                    @Override public void run() { loadTodayPage(); refreshWidget(); }
                });"""
    if bad_link in content:
        content = content.replace(bad_link, good_link)
        with open(main_activity, "w", encoding="utf-8") as f: f.write(content)
        print("✅ ১. অরিজিনাল 'Backup & Sync' লিংক রিস্টোর করা হয়েছে।")
    else:
        print("⚠️ ১. লিংক আগেই ঠিক করা আছে।")

# ২. BackupHelper-এর অরিজিনাল ডিজাইনে Danger Zone যুক্ত করা
if os.path.exists(backup_helper):
    with open(backup_helper, "r", encoding="utf-8") as f: content = f.read()

    danger_zone = """
        // --- DANGER ZONE START ---
        android.widget.TextView dangerTitle = new android.widget.TextView(context);
        dangerTitle.setText("Danger Zone");
        dangerTitle.setTextColor(android.graphics.Color.parseColor("#FF5252"));
        dangerTitle.setTextSize(18);
        dangerTitle.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        dangerTitle.setPadding(0, (int) (20 * DENSITY), 0, (int) (10 * DENSITY));
        main.addView(dangerTitle);

        android.widget.LinearLayout dangerSection = new android.widget.LinearLayout(context);
        dangerSection.setOrientation(android.widget.LinearLayout.VERTICAL);
        dangerSection.setPadding((int) (15 * DENSITY), (int) (15 * DENSITY), (int) (15 * DENSITY), (int) (15 * DENSITY));
        android.graphics.drawable.GradientDrawable dBg = new android.graphics.drawable.GradientDrawable();
        dBg.setColor(themeColors[4]);
        dBg.setCornerRadius(15f * DENSITY);
        dangerSection.setBackground(dBg);

        android.widget.Button btnWipeLocal = new android.widget.Button(context);
        btnWipeLocal.setText("Delete All Local Data & Start Fresh");
        btnWipeLocal.setTextColor(android.graphics.Color.parseColor("#FF5252"));
        btnWipeLocal.setAllCaps(false);
        android.graphics.drawable.GradientDrawable wBg = new android.graphics.drawable.GradientDrawable();
        wBg.setColor(android.graphics.Color.parseColor("#1AFF4444"));
        wBg.setStroke((int)(1*DENSITY), android.graphics.Color.parseColor("#80FF4444"));
        wBg.setCornerRadius(15f * DENSITY);
        btnWipeLocal.setBackground(wBg);
        android.widget.LinearLayout.LayoutParams wLp = new android.widget.LinearLayout.LayoutParams(-1, (int) (55 * DENSITY));
        wLp.setMargins(0, 0, 0, (int) (10 * DENSITY));
        dangerSection.addView(btnWipeLocal, wLp);

        android.widget.Button btnWipeCloud = new android.widget.Button(context);
        btnWipeCloud.setText("Wipe Cloud Data");
        btnWipeCloud.setTextColor(android.graphics.Color.parseColor("#FF5252"));
        btnWipeCloud.setAllCaps(false);
        btnWipeCloud.setBackground(wBg);
        dangerSection.addView(btnWipeCloud, new android.widget.LinearLayout.LayoutParams(-1, (int) (55 * DENSITY)));

        main.addView(dangerSection);

        btnWipeLocal.setOnClickListener(new android.view.View.OnClickListener() {
            @Override public void onClick(android.view.View v) {
                new android.app.AlertDialog.Builder(context)
                    .setTitle("⚠️ Delete All Data")
                    .setMessage("Are you sure? This will wipe your history, settings, and start fresh. This action cannot be undone.")
                    .setPositiveButton("Yes, Delete", (d, w) -> {
                        android.widget.Toast.makeText(context, "Wiping all data...", android.widget.Toast.LENGTH_SHORT).show();
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
                            ((android.app.ActivityManager) context.getSystemService(android.content.Context.ACTIVITY_SERVICE)).clearApplicationUserData();
                        }
                    })
                    .setNegativeButton("Cancel", null)
                    .show();
            }
        });

        btnWipeCloud.setOnClickListener(new android.view.View.OnClickListener() {
            @Override public void onClick(android.view.View v) {
                 android.widget.Toast.makeText(context, "Cloud Wipe logic will be connected soon!", android.widget.Toast.LENGTH_SHORT).show();
            }
        });
        // --- DANGER ZONE END ---
"""
    if "Danger Zone" not in content:
        # ডায়ালগ বিল্ড হওয়ার ঠিক আগে কোড ইনজেক্ট করা
        match = re.search(r'(FrameLayout\.LayoutParams\s+\w+\s*=\s*new\s+FrameLayout\.LayoutParams[^\n]+;)', content)
        if match:
            content = content[:match.start()] + danger_zone + "\n        " + content[match.start():]
            with open(backup_helper, "w", encoding="utf-8") as f: f.write(content)
            print("✅ ২. আপনার অরিজিনাল ডিজাইনে 'Danger Zone' বাটনগুলো সফলভাবে যুক্ত হয়েছে!")
        else:
            print("❌ BackupHelper.java: ইনজেক্ট করার সঠিক জায়গা পাওয়া যায়নি।")
    else:
        print("⚠️ Danger Zone আগেই যুক্ত আছে।")
else:
    print("❌ BackupHelper.java ফাইলটি পাওয়া যায়নি।")
