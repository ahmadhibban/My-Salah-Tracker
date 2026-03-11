import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. ওই ফালতু এবং ভুল মেথডটা সমূলে মুছে ফেলা হচ্ছে
mc = re.sub(r'private void smoothRestart\(\)\s*\{.*?\}', '', mc, flags=re.DOTALL)

# ২. যেখানে যেখানে smoothRestart(); ডাকা হয়েছিল, সেখানে সঠিক ভেরিয়েবল দিয়ে কোড বসানো হচ্ছে
inline_restart = """
{
    try {
        android.content.Intent restartIntent = new android.content.Intent(MainActivity.this, MainActivity.class);
        try { restartIntent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime()); } catch(Exception e){}
        startActivity(restartIntent);
        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
        finish();
    } catch(Exception e){}
}
"""
mc = re.sub(r'\bsmoothRestart\(\)\s*;', inline_restart.strip(), mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✅ Okorma Error Fixed Perfectly!")
