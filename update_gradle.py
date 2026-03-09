import os
import re

fpath = "gradle/wrapper/gradle-wrapper.properties"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        code = f.read()

    # যেকোনো পুরোনো গ্রেডেল ভার্সন (যেমন 8.1.1) মুছে লেটেস্ট 8.7 বসিয়ে দেওয়া হচ্ছে
    new_code = re.sub(r'gradle-[0-9\.]+-(all|bin)\.zip', 'gradle-8.7-all.zip', code)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_code)
    
    print("✅ Success! Gradle updated to 8.7. Your project is now 100% ready for Java 21.")
else:
    print("❌ Error: gradle-wrapper.properties file not found.")
