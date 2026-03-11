import os, re

xml_file = "app/src/main/res/layout/activity_main.xml"
java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

# ১. activity_main.xml ফাইলটি Neumorphism কোড দিয়ে আপডেট করা
xml_code = """<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#E2E8F0">

    <soup.neumorphism.NeumorphCardView
        android:layout_width="300dp"
        android:layout_height="200dp"
        android:layout_centerInParent="true"
        app:neumorph_shapeType="flat"
        app:neumorph_shadowColorLight="#FFFFFF"
        app:neumorph_shadowColorDark="#cbd5e0"
        app:neumorph_shadowElevation="8dp"
        app:neumorph_cornerFamily="rounded"
        app:neumorph_cornerSize="24dp">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_centerInParent="true"
            android:text="Bismillah! Soft 3D"
            android:textSize="24sp"
            android:textStyle="bold"
            android:textColor="#64748B"/>
            
    </soup.neumorphism.NeumorphCardView>
</RelativeLayout>
"""

with open(xml_file, "w", encoding="utf-8") as f:
    f.write(xml_code)

# ২. MainActivity.java তে অত্যন্ত নিরাপদে XML কানেক্ট করা
if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()
    
    # super.onCreate খুঁজে বের করে তার ঠিক নিচে setContentView বসানো
    if "setContentView(R.layout.activity_main);" not in mc:
        mc = re.sub(r'(super\.onCreate\([^)]+\);)', r'\1\n        setContentView(R.layout.activity_main);\n        return; // UI টেস্ট করার জন্য পুরনো জাভা কোডগুলো আপাতত অফ রাখা হলো', mc, count=1)
        with open(java_file, "w", encoding="utf-8") as f:
            f.write(mc)
            
print("✔ Magic Test Code Applied Successfully! Ready to Build.")
