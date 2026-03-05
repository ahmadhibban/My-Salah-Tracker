package com.my.salah.tracker.app;

import android.app.Activity;
import android.content.SharedPreferences;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import org.json.JSONObject;

public class FirebaseManager {
    private final String DB_URL = "https://mysalahtracker-49a76-default-rtdb.firebaseio.com/users/";
    private SharedPreferences sp;
    private Activity activity;

    public FirebaseManager(Activity activity, SharedPreferences sp) {
        this.activity = activity;
        this.sp = sp;
    }

    public void save(final String dateKey, final String prayerName, final String status) {
        final String email = sp.getString("user_email", ""); 
        if (email.isEmpty()) return;
        final String safeEmail = email.replace(".", "_dot_").replace("@", "_at_");
        
        new Thread(new Runnable() {
            @Override public void run() {
                try {
                    URL url = new URL(DB_URL + safeEmail + "/" + dateKey + "_" + prayerName + ".json");
                    HttpURLConnection con = (HttpURLConnection) url.openConnection();
                    con.setRequestMethod("PUT"); 
                    con.setRequestProperty("Content-Type", "application/json"); 
                    con.setDoOutput(true);
                    con.getOutputStream().write(("\"" + status + "\"").getBytes()); 
                    con.getResponseCode();
                    sp.edit().putLong("last_sync", System.currentTimeMillis()).apply();
                } catch(Exception e) {
                    String q = sp.getString("offline_q", ""); 
                    sp.edit().putString("offline_q", q + dateKey + "|" + prayerName + "|" + status + ",").apply();
                }
            }
        }).start();
    }

    public void processOfflineQueue(final Runnable onStart, final Runnable onSuccess, final Runnable onFail) {
        String q = sp.getString("offline_q", "");
        if(!q.isEmpty() && !sp.getString("user_email", "").isEmpty()) {
            if(onStart != null) activity.runOnUiThread(onStart);
            final String safeEmail = sp.getString("user_email", "").replace(".", "_dot_").replace("@", "_at_");
            final String[] items = q.split(",");
            new Thread(new Runnable() {
                @Override public void run() {
                    boolean success = true;
                    for(String item : items) {
                        if(item.trim().isEmpty()) continue;
                        String[] parts = item.split("\\|");
                        if(parts.length == 3) {
                            try {
                                URL url = new URL(DB_URL + safeEmail + "/" + parts[0] + "_" + parts[1] + ".json");
                                HttpURLConnection con = (HttpURLConnection) url.openConnection();
                                con.setRequestMethod("PUT"); 
                                con.setRequestProperty("Content-Type", "application/json"); 
                                con.setDoOutput(true);
                                con.getOutputStream().write(("\"" + parts[2] + "\"").getBytes()); 
                                if(con.getResponseCode() != 200) success = false;
                            } catch(Exception e) { success = false; break; }
                        }
                    }
                    if(success) { 
                        sp.edit().putString("offline_q", "").putLong("last_sync", System.currentTimeMillis()).apply(); 
                        if(onSuccess != null) activity.runOnUiThread(onSuccess); 
                    } else { 
                        if(onFail != null) activity.runOnUiThread(onFail); 
                    }
                }
            }).start();
        }
    }

    public void fetchAndLoad(final Runnable onStart, final Runnable onSuccess, final Runnable onFail) {
        final String email = sp.getString("user_email", ""); 
        if (email.isEmpty()) return;
        final String safeEmail = email.replace(".", "_dot_").replace("@", "_at_");
        if(onStart != null) activity.runOnUiThread(onStart);
        
        new Thread(new Runnable() {
            @Override public void run() {
                try {
                    URL url = new URL(DB_URL + safeEmail + ".json");
                    HttpURLConnection con = (HttpURLConnection) url.openConnection();
                    con.setRequestMethod("GET");
                    InputStream in = con.getInputStream(); 
                    BufferedReader reader = new BufferedReader(new InputStreamReader(in));
                    StringBuilder result = new StringBuilder(); 
                    String line; 
                    while((line = reader.readLine()) != null) result.append(line); 
                    reader.close();
                    
                    final String jsonResult = result.toString();
                    
                    // ✨ HYBRID SYNC: SharedPreferences + Room Database ✨
                    if (jsonResult != null && !jsonResult.equals("null") && jsonResult.startsWith("{")) {
                        try {
                            JSONObject obj = new JSONObject(jsonResult); 
                            SharedPreferences.Editor editor = sp.edit();
                            Iterator<String> keys = obj.keys(); 
                            
                            SalahDao dao = SalahDatabase.getDatabase(activity).salahDao();
                            HashMap<String, SalahRecord> roomRecords = new HashMap<>();

                            while(keys.hasNext()) { 
                                String k = keys.next(); 
                                String val = obj.getString(k); 
                                editor.putString(k, val); // ব্যাকআপ হিসেবে SharedPreferences এ সেভ
                                
                                // Room Database এর জন্য ডেটা প্রসেস করা
                                if (k.length() >= 10 && k.matches("\\d{4}-\\d{2}-\\d{2}.*")) {
                                    String date = k.substring(0, 10);
                                    String type = k.substring(11);
                                    
                                    SalahRecord record = roomRecords.get(date);
                                    if (record == null) {
                                        record = dao.getRecordByDate(date);
                                        if (record == null) record = new SalahRecord(date);
                                        roomRecords.put(date, record);
                                    }
                                    
                                    // কোন ওয়াক্তের ডেটা সেটা মিলিয়ে Room-এ সেট করা
                                    if (type.equals("Fajr")) record.fajr = val;
                                    else if (type.equals("Dhuhr")) record.dhuhr = val;
                                    else if (type.equals("Asr")) record.asr = val;
                                    else if (type.equals("Maghrib")) record.maghrib = val;
                                    else if (type.equals("Isha")) record.isha = val;
                                    else if (type.equals("Witr")) record.witr = val;
                                }
                            }
                            
                            // সব ডেটা একসাথে Room DB তে ইনসার্ট করে দেওয়া (Super Fast)
                            for (SalahRecord r : roomRecords.values()) {
                                dao.insertRecord(r);
                            }

                            editor.putLong("last_sync", System.currentTimeMillis()); 
                            editor.apply(); 
                            
                            activity.runOnUiThread(new Runnable() {
                                @Override public void run() { if(onSuccess != null) onSuccess.run(); }
                            });
                        } catch(Exception e) { 
                            activity.runOnUiThread(new Runnable() { @Override public void run() { if(onFail!=null) onFail.run(); }}); 
                        }
                    } else { 
                        activity.runOnUiThread(new Runnable() { @Override public void run() { if(onFail!=null) onFail.run(); }}); 
                    }
                } catch(final Exception e) { 
                    activity.runOnUiThread(new Runnable() { 
                        @Override public void run() { if(onFail != null) onFail.run(); }
                    }); 
                }
            }
        }).start();
    }
}