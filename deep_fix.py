import os

main_activity = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(main_activity):
    with open(main_activity, "r", encoding="utf-8") as f:
        content = f.read()

    bad_call = "showWipeDataDialog();"
    
    # ফাংশন কল করার বদলে সরাসরি কোড দিয়ে দেওয়া হলো
    perfect_logic = """new android.app.AlertDialog.Builder(MainActivity.this)
                .setTitle("⚠️ Delete All Data")
                .setMessage("Are you sure? This will wipe your history, settings, and start fresh.")
                .setPositiveButton("Yes, Delete", (d, w) -> {
                    android.widget.Toast.makeText(MainActivity.this, "Wiping data...", android.widget.Toast.LENGTH_SHORT).show();
                    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
                        ((android.app.ActivityManager) getSystemService(android.content.Context.ACTIVITY_SERVICE)).clearApplicationUserData();
                    }
                })
                .setNegativeButton("Cancel", null)
                .show();"""

    if bad_call in content:
        new_content = content.replace(bad_call, perfect_logic)
        with open(main_activity, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ Deep Fix Applied! লজিক সরাসরি বাটনের ভেতরে বসে গেছে।")
    else:
        print("⚠️ আগের ভুল কলটি খুঁজে পাওয়া যায়নি।")
else:
    print("❌ MainActivity পাওয়া যায়নি।")
