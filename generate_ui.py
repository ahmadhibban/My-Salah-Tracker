import os

layout_dir = "app/src/main/res/layout"
drawable_dir = "app/src/main/res/drawable"

os.makedirs(layout_dir, exist_ok=True)
os.makedirs(drawable_dir, exist_ok=True)

print("🎨 প্রিমিয়াম UI জেনারেট করা হচ্ছে...")

# ১. Danger Button এর ব্যাকগ্রাউন্ড তৈরি (লালচে)
danger_btn_xml = """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <corners android:radius="16dp" />
    <solid android:color="#1AFF4444" />
    <stroke android:width="1dp" android:color="#80FF4444" />
</shape>"""
with open(f"{drawable_dir}/bg_btn_danger.xml", "w") as f: f.write(danger_btn_xml)

# ২. Normal Button এর ব্যাকগ্রাউন্ড তৈরি (আপনার গ্লাস থিমের সাথে ম্যাচ করে)
normal_btn_xml = """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <corners android:radius="16dp" />
    <solid android:color="#20888888" />
    <stroke android:width="1dp" android:color="#40888888" />
</shape>"""
with open(f"{drawable_dir}/bg_btn_normal.xml", "w") as f: f.write(normal_btn_xml)

# ৩. মূল সেটিংস লেআউট তৈরি
settings_layout_xml = """<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp"
    android:scrollbars="none"
    android:background="@android:color/transparent">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Settings &amp; Backup"
            android:textSize="24sp"
            android:textStyle="bold"
            android:layout_gravity="center"
            android:layout_marginBottom="24dp" />

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:background="@drawable/bg_glass_dark"
            android:padding="20dp"
            android:layout_marginBottom="16dp">

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Cloud Account"
                android:textStyle="bold"
                android:textSize="18sp"
                android:layout_marginBottom="12dp" />

            <TextView
                android:id="@+id/tv_current_email"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="Not connected"
                android:textSize="14sp"
                android:layout_marginBottom="16dp" />

            <Switch
                android:id="@+id/switch_auto_sync"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="Auto Sync"
                android:layout_marginBottom="16dp" />

            <Button
                android:id="@+id/btn_change_email"
                android:layout_width="match_parent"
                android:layout_height="50dp"
                android:text="Change Email / Login"
                android:background="@drawable/bg_btn_normal"
                android:textAllCaps="false" />
        </LinearLayout>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:background="@drawable/bg_glass_dark"
            android:padding="20dp"
            android:layout_marginBottom="16dp">

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Local Backup (JSON)"
                android:textStyle="bold"
                android:textSize="18sp"
                android:layout_marginBottom="16dp" />

            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:weightSum="2">

                <Button
                    android:id="@+id/btn_export_json"
                    android:layout_width="0dp"
                    android:layout_height="50dp"
                    android:layout_weight="1"
                    android:text="Export"
                    android:background="@drawable/bg_btn_normal"
                    android:layout_marginEnd="8dp"
                    android:textAllCaps="false" />

                <Button
                    android:id="@+id/btn_import_json"
                    android:layout_width="0dp"
                    android:layout_height="50dp"
                    android:layout_weight="1"
                    android:text="Import"
                    android:background="@drawable/bg_btn_normal"
                    android:layout_marginStart="8dp"
                    android:textAllCaps="false" />
            </LinearLayout>
        </LinearLayout>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:background="@drawable/bg_glass_dark"
            android:padding="20dp"
            android:layout_marginBottom="24dp">

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Danger Zone"
                android:textColor="#FF4444"
                android:textStyle="bold"
                android:textSize="18sp"
                android:layout_marginBottom="16dp" />

            <Button
                android:id="@+id/btn_wipe_cloud"
                android:layout_width="match_parent"
                android:layout_height="50dp"
                android:text="Wipe Cloud Data"
                android:textColor="#FF4444"
                android:background="@drawable/bg_btn_danger"
                android:layout_marginBottom="12dp"
                android:textAllCaps="false" />

            <Button
                android:id="@+id/btn_wipe_all"
                android:layout_width="match_parent"
                android:layout_height="50dp"
                android:text="Delete All Data &amp; Start Fresh"
                android:textColor="#FF4444"
                android:background="@drawable/bg_btn_danger"
                android:textAllCaps="false" />
        </LinearLayout>

    </LinearLayout>
</ScrollView>"""

with open(f"{layout_dir}/dialog_premium_settings.xml", "w") as f: f.write(settings_layout_xml)

print("✅ প্রিমিয়াম লেআউট এবং স্টাইল সফলভাবে তৈরি হয়েছে!")
