import os
import re

main_activity = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

print("⚙️ জাভা লজিক যুক্ত করা হচ্ছে...")

if os.path.exists(main_activity):
    with open(main_activity, "r", encoding="utf-8") as f:
        content = f.read()

    # নতুন ডায়ালগ ফাংশন
    dialog_method = """
    private void showPremiumSyncSettingsDialog() {
        android.app.Dialog dialog = new android.app.Dialog(this);
        dialog.setContentView(R.layout.dialog_premium_settings);
        dialog.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT));
        dialog.getWindow().setLayout(android.view.ViewGroup.LayoutParams.MATCH_PARENT, android.view.ViewGroup.LayoutParams.WRAP_CONTENT);

        android.widget.TextView tvEmail = dialog.findViewById(R.id.tv_current_email);
        android.widget.Switch switchSync = dialog.findViewById(R.id.switch_auto_sync);
        
        android.widget.Button btnChangeEmail = dialog.findViewById(R.id.btn_change_email);
        android.widget.Button btnExportJson = dialog.findViewById(R.id.btn_export_json);
        android.widget.Button btnImportJson = dialog.findViewById(R.id.btn_import_json);
        android.widget.Button btnWipeCloud = dialog.findViewById(R.id.btn_wipe_cloud);
        android.widget.Button btnWipeAll = dialog.findViewById(R.id.btn_wipe_all);

        // ডেমো ডাটা (পরে আপনার আসল লজিক বসবে)
        String currentEmail = prefs.getString("user_email", "Not connected");
        tvEmail.setText("Current Email: " + currentEmail);
        switchSync.setChecked(prefs.getBoolean("auto_sync", true));

        // ডিলিট বাটনের আসল লজিক যুক্ত করা হলো
        btnWipeAll.setOnClickListener(v -> {
            dialog.dismiss();
            showWipeDataDialog(); 
        });

        // অন্যান্য বাটনগুলোর জন্য (আপাতত টোস্ট মেসেজ)
        btnChangeEmail.setOnClickListener(v -> {
            android.widget.Toast.makeText(this, "Login / Change Email clicked", android.widget.Toast.LENGTH_SHORT).show();
        });
        btnExportJson.setOnClickListener(v -> {
            android.widget.Toast.makeText(this, "JSON Export clicked", android.widget.Toast.LENGTH_SHORT).show();
        });
        btnImportJson.setOnClickListener(v -> {
            android.widget.Toast.makeText(this, "JSON Import clicked", android.widget.Toast.LENGTH_SHORT).show();
        });
        btnWipeCloud.setOnClickListener(v -> {
            android.widget.Toast.makeText(this, "Wipe Cloud clicked", android.widget.Toast.LENGTH_SHORT).show();
        });

        dialog.show();
    }
"""

    if "showPremiumSyncSettingsDialog" not in content:
        # ফাইলের একদম শেষের ব্র্যাকেটের আগে কোড বসানো
        content = re.sub(r'}\s*$', dialog_method + '\n}', content)
        
        with open(main_activity, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ MainActivity-তে লজিক সফলভাবে যুক্ত হয়েছে!")
    else:
        print("⚠️ লজিকটি আগে থেকেই যুক্ত আছে।")
else:
    print("❌ MainActivity.java ফাইলটি পাওয়া যায়নি।")
