import os

# 1. Create a Background Worker for Sync
sw = r"""package com.my.salah.tracker.app;
import android.content.Context;
import android.content.SharedPreferences;
import androidx.annotation.NonNull;
import androidx.work.Worker;
import androidx.work.WorkerParameters;

public class SyncWorker extends Worker {
    public SyncWorker(@NonNull Context context, @NonNull WorkerParameters workerParams) { super(context, workerParams); }
    @NonNull @Override public Result doWork() {
        SharedPreferences sp = getApplicationContext().getSharedPreferences("salah_pro_final", Context.MODE_PRIVATE);
        String q = sp.getString("offline_q", ""); String email = sp.getString("user_email", "");
        if(!q.isEmpty() && !email.isEmpty()) {
            String safeEmail = email.replace(".", "_dot_").replace("@", "_at_"); String[] items = q.split(","); boolean success = true;
            for(String item : items) {
                if(item.trim().isEmpty()) continue;
                String[] parts = item.split("\\|");
                if(parts.length == 3) {
                    try {
                        java.net.URL url = new java.net.URL("https://mysalahtracker-49a76-default-rtdb.firebaseio.com/users/" + safeEmail + "/" + parts[0] + "_" + parts[1] + ".json");
                        java.net.HttpURLConnection con = (java.net.HttpURLConnection) url.openConnection();
                        con.setRequestMethod("PUT"); con.setRequestProperty("Content-Type", "application/json"); con.setDoOutput(true);
                        con.getOutputStream().write(("\"" + parts[2] + "\"").getBytes());
                        if(con.getResponseCode() != 200) success = false;
                    } catch(Exception e) { success = false; break; }
                }
            }
            if(success) sp.edit().putString("offline_q", "").putLong("last_sync", System.currentTimeMillis()).apply();
            else return Result.retry();
        } return Result.success();
    }
}"""
open('app/src/main/java/com/my/salah/tracker/app/SyncWorker.java', 'w').write(sw)

# 2. Tell FirebaseManager to trigger this Worker
fb = 'app/src/main/java/com/my/salah/tracker/app/FirebaseManager.java'
c = open(fb).read()
old_catch = 'sp.edit().putString("offline_q", q + dateKey + "|" + prayerName + "|" + status + ",").apply();'
new_catch = """sp.edit().putString("offline_q", q + dateKey + "|" + prayerName + "|" + status + ",").apply();
                    androidx.work.OneTimeWorkRequest syncWork = new androidx.work.OneTimeWorkRequest.Builder(SyncWorker.class).setConstraints(new androidx.work.Constraints.Builder().setRequiredNetworkType(androidx.work.NetworkType.CONNECTED).build()).build();
                    androidx.work.WorkManager.getInstance(activity).enqueueUniqueWork("auto_sync", androidx.work.ExistingWorkPolicy.REPLACE, syncWork);"""
c = c.replace(old_catch, new_catch)
open(fb, 'w').write(c)

print("✅ Auto-Retry Background Sync is Active!")
