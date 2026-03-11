import os

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ওই অজানা ভেরিয়েবলের নামগুলো মুছে শুধু ডেবে থাকা (Sunken) কার্ডের কন্ডিশন রাখা হলো
    mc = mc.replace("neo.getShapeType() == 1 || neo == prevW || neo == nextW", "neo.getShapeType() == 1")

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
        
    print("✅ Unknown Variables Removed! Error Fixed.")
else:
    print("❌ FILE NOT FOUND")
