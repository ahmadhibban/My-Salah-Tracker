import os

main_activity = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(main_activity):
    with open(main_activity, "r", encoding="utf-8") as f:
        content = f.read()

    wipe_method = """
    private void showWipeDataDialog() {
        new android.app.AlertDialog.Builder(this)
            .setTitle("⚠️ Delete All Data")
            .setMessage("Are you sure you want to delete all data? This will wipe your history, settings, and start fresh. This action cannot be undone.")
            .setPositiveButton("Yes, Delete", (dialog, which) -> {
                android.widget.Toast.makeText(this, "Wiping all data...", android.widget.Toast.LENGTH_SHORT).show();
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
                    ((android.app.ActivityManager) getSystemService(android.content.Context.ACTIVITY_SERVICE)).clearApplicationUserData();
                }
            })
            .setNegativeButton("Cancel", null)
            .show();
    }
"""

    # এবার শুধু নাম নয়, void সহ খুঁজবে যাতে বাটন ক্লিকের সাথে কনফিউজড না হয়
    if "void showWipeDataDialog" not in content:
        last_brace_index = content.rfind('}')
        if last_brace_index != -1:
            new_content = content[:last_brace_index] + wipe_method + '\n}' + content[last_brace_index+1:]
            with open(main_activity, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("✅ Error Fixed! এবার সত্যিই ফাংশনটি যুক্ত হয়েছে!")
        else:
            print("❌ ফাইলের শেষে কোনো ব্র্যাকেট পাওয়া যায়নি!")
    else:
        print("⚠️ ফাংশনটি সত্যিই আগে থেকেই আছে।")
else:
    print("❌ MainActivity পাওয়া যায়নি।")
