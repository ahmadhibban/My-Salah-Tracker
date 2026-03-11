import os

xml_dir = "app/src/main/res/layout"
os.makedirs(xml_dir, exist_ok=True)
xml_file = os.path.join(xml_dir, "activity_main.xml")

# নামাজের লিস্ট জেনারেট করা
prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr"]
cards_xml = ""

for p in prayers:
    cards_xml += f"""
        <soup.neumorphism.NeumorphCardView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginBottom="4dp"
            app:neumorph_shapeType="flat"
            app:neumorph_shadowColorLight="#FFFFFF"
            app:neumorph_shadowColorDark="#cbd5e0"
            app:neumorph_shadowElevation="5dp"
            app:neumorph_cornerFamily="rounded"
            app:neumorph_cornerSize="16dp">
            
            <RelativeLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:padding="20dp">
                
                <TextView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="{p}"
                    android:textSize="20sp"
                    android:textStyle="bold"
                    android:layout_centerVertical="true"
                    android:textColor="#475569"/>
                    
                <soup.neumorphism.NeumorphCardView
                    android:layout_width="48dp"
                    android:layout_height="48dp"
                    android:layout_alignParentRight="true"
                    android:layout_centerVertical="true"
                    app:neumorph_shapeType="pressed"
                    app:neumorph_shadowColorLight="#FFFFFF"
                    app:neumorph_shadowColorDark="#cbd5e0"
                    app:neumorph_shadowElevation="3dp"
                    app:neumorph_cornerFamily="rounded"
                    app:neumorph_cornerSize="24dp">
                    
                    <View
                        android:layout_width="match_parent"
                        android:layout_height="match_parent"
                        android:background="#E2E8F0"/>
                </soup.neumorphism.NeumorphCardView>
                
            </RelativeLayout>
        </soup.neumorphism.NeumorphCardView>
"""

# সম্পূর্ণ XML কোড
xml_code = f"""<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#E2E8F0">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="16dp">

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="My Salah Tracker"
            android:textSize="26sp"
            android:textStyle="bold"
            android:textColor="#334155"
            android:layout_gravity="center"
            android:layout_marginBottom="24dp"
            android:layout_marginTop="16dp"/>

        {cards_xml}

    </LinearLayout>
</ScrollView>
"""

with open(xml_file, "w", encoding="utf-8") as f:
    f.write(xml_code)

# MainActivity তে শুধু ডিজাইনটা দেখানোর জন্য টেম্পোরারি কানেকশন
java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()
    
    # আগের টেম্পোরারি কোড থাকলে মুছে ফেলা
    mc = mc.replace("setContentView(R.layout.activity_main);", "")
    mc = mc.replace("if (true) return; // UI টেস্ট করার জন্য", "")
    
    import re
    mc = re.sub(r'(super\.onCreate\([^)]+\);)', r'\1\n        setContentView(R.layout.activity_main);\n        if (true) return; // UI টেস্ট করার জন্য', mc, count=1)
    
    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)

print("✔ Full Neumorphism UI Generated Successfully! Ready to Build.")
