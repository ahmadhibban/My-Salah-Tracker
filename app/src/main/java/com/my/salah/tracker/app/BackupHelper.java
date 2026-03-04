package com.my.salah.tracker.app;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Environment;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Iterator;
import java.util.Locale;
import java.util.Map;

public class BackupHelper {
    private Activity activity;
    private SharedPreferences sp;
    private UIComponents ui;
    private LanguageEngine lang;
    private FirebaseManager fbHelper;
    private float DENSITY;
    private int[] themeColors;
    private int colorAccent;
    private FrameLayout root;

    public BackupHelper(Activity activity, SharedPreferences sp, UIComponents ui, LanguageEngine lang, FirebaseManager fbHelper, float DENSITY, int[] themeColors, int colorAccent, FrameLayout root) {
        this.activity = activity;
        this.sp = sp;
        this.ui = ui;
        this.lang = lang;
        this.fbHelper = fbHelper;
        this.DENSITY = DENSITY;
        this.themeColors = themeColors;
        this.colorAccent = colorAccent;
        this.root = root;
    }

    public void exportData() {
        try {
            JSONObject j = new JSONObject();
            Map<String, ?> m = sp.getAll();
            for (String k : m.keySet()) j.put(k, m.get(k));
            File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists()) dir.mkdirs();
            File f = new File(dir, "Salah_Backup_" + System.currentTimeMillis() + ".json");
            FileWriter w = new FileWriter(f);
            w.write(j.toString());
            w.close();
            ui.showSmartBanner(root, lang.get("Export Successful"), lang.get("Saved to Downloads folder"), "img_tick", colorAccent, null);
        } catch (Exception e) {
            ui.showSmartBanner(root, lang.get("Export Failed"), lang.get("Storage permission required."), "img_warning", colorAccent, null);
        }
    }

    public void showRestoreDialog(final Runnable reload) {
        File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
        final File[] files = dir.listFiles(new FilenameFilter() {
            @Override public boolean accept(File d, String name) { return name.toLowerCase().endsWith(".json") && name.contains("Salah"); }
        });
        if (files == null || files.length == 0) {
            ui.showSmartBanner(root, lang.get("No Backups Found"), lang.get("No JSON files in Downloads."), "img_warning", colorAccent, null);
            return;
        }
        
        FrameLayout wrap = new FrameLayout(activity); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        LinearLayout main = new LinearLayout(activity); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(20*DENSITY), (int)(25*DENSITY), (int)(20*DENSITY), (int)(25*DENSITY));
        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        TextView title = new TextView(activity); title.setText(lang.get("Select Backup File")); title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(15*DENSITY)); main.addView(title);
        
        ScrollView sv = new ScrollView(activity); LinearLayout list = new LinearLayout(activity); list.setOrientation(LinearLayout.VERTICAL);
        
        final AlertDialog ad = new AlertDialog.Builder(activity).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(Gravity.CENTER);
        
        for (final File f : files) {
            TextView tv = new TextView(activity); tv.setText("📄 " + f.getName()); tv.setTextColor(themeColors[3]); tv.setTextSize(14); tv.setPadding((int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY));
            GradientDrawable bg = new GradientDrawable(); bg.setColor(themeColors[4]); bg.setCornerRadius(15f*DENSITY); tv.setBackground(bg);
            LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2); lp.setMargins(0, 0, 0, (int)(10*DENSITY)); tv.setLayoutParams(lp);
            tv.setOnClickListener(new View.OnClickListener() {
                @Override public void onClick(View v) {
                    try {
                        BufferedReader r = new BufferedReader(new FileReader(f)); StringBuilder sb = new StringBuilder(); String l;
                        while ((l = r.readLine()) != null) sb.append(l); r.close();
                        JSONObject j = new JSONObject(sb.toString()); SharedPreferences.Editor ed = sp.edit();
                        Iterator<String> keys = j.keys();
                        while (keys.hasNext()) {
                            String k = keys.next(); Object val = j.get(k);
                            if (val instanceof Boolean) ed.putBoolean(k, (Boolean) val);
                            else if (val instanceof String) ed.putString(k, (String) val);
                            else if (val instanceof Integer) ed.putInt(k, (Integer) val);
                            else if (val instanceof Long) ed.putLong(k, (Long) val);
                        }
                        ed.apply(); ui.showSmartBanner(root, lang.get("Restore Successful"), lang.get("Data imported"), "img_tick", colorAccent, null);
                        if (reload != null) reload.run(); ad.dismiss();
                    } catch (Exception e) { ui.showSmartBanner(root, lang.get("Restore Failed"), lang.get("Corrupted file."), "img_warning", colorAccent, null); }
                }
            });
            list.addView(tv);
        }
        sv.addView(list); main.addView(sv, new LinearLayout.LayoutParams(-1, (int)(300*DENSITY)));
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp);
        ad.show();
    }

    public void showProfileDialog(final Runnable onReload) {
        FrameLayout wrap = new FrameLayout(activity); wrap.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        final LinearLayout rootDia = new LinearLayout(activity); rootDia.setOrientation(LinearLayout.VERTICAL); rootDia.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        GradientDrawable bg = new GradientDrawable(); bg.setColor(themeColors[1]); bg.setCornerRadius(25f * DENSITY); rootDia.setBackground(bg);
        
        View iconView = ui.getRoundImage("img_cloud", 0, Color.TRANSPARENT, colorAccent); 
        LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(50*DENSITY), (int)(50*DENSITY));
        icLp.gravity = Gravity.CENTER_HORIZONTAL; icLp.setMargins(0, 0, 0, (int)(15*DENSITY));
        iconView.setLayoutParams(icLp); rootDia.addView(iconView); 
        
        TextView title = new TextView(activity); title.setText(lang.get("Backup & Sync")); title.setGravity(Gravity.CENTER); title.setTextColor(themeColors[2]); title.setTextSize(22); title.setTypeface(Typeface.DEFAULT_BOLD); rootDia.addView(title);
        
        long lastSyncTime = sp.getLong("last_sync", 0);
        String syncText = lastSyncTime == 0 ? "Never synced" : "Last synced: " + new SimpleDateFormat("dd MMM, hh:mm a", Locale.US).format(new Date(lastSyncTime));
        if(lang.get("Fajr").equals("ফজর")) { syncText = lastSyncTime == 0 ? "কখনো সিঙ্ক করা হয়নি" : "শেষ সিঙ্ক: " + lang.bnNum(new SimpleDateFormat("dd MMM, hh:mm a", Locale.US).format(new Date(lastSyncTime))); }
        
        TextView desc = new TextView(activity); desc.setText(lang.get("Secure your data in cloud or local storage") + "\n(" + syncText + ")"); desc.setGravity(Gravity.CENTER); desc.setTextColor(themeColors[3]); desc.setTextSize(13); desc.setPadding(0, 0, 0, (int)(20*DENSITY)); rootDia.addView(desc);
        
        final EditText emailIn = new EditText(activity); emailIn.setHint(lang.get("Enter Nickname or Email")); emailIn.setText(sp.getString("user_email", "")); emailIn.setPadding((int)(20*DENSITY), (int)(15*DENSITY), (int)(20*DENSITY), (int)(15*DENSITY)); emailIn.setTextSize(15); emailIn.setTextColor(themeColors[2]); emailIn.setHintTextColor(themeColors[3]); emailIn.setSingleLine(true);
        GradientDrawable gIn = new GradientDrawable(); gIn.setCornerRadius(15f * DENSITY); gIn.setColor(themeColors[4]); emailIn.setBackground(gIn);
        LinearLayout.LayoutParams lpIn = new LinearLayout.LayoutParams(-1, -2); lpIn.setMargins(0, 0, 0, (int)(15*DENSITY)); emailIn.setLayoutParams(lpIn); rootDia.addView(emailIn);
        
        Button actionBtn = new Button(activity); actionBtn.setText(lang.get("Sync Cloud Data")); actionBtn.setAllCaps(false); actionBtn.setTextColor(Color.WHITE); actionBtn.setTextSize(15); actionBtn.setTypeface(Typeface.DEFAULT_BOLD);
        GradientDrawable btnBg = new GradientDrawable(); btnBg.setColor(colorAccent); btnBg.setCornerRadius(15f * DENSITY); actionBtn.setBackground(btnBg);
        LinearLayout.LayoutParams btnLp = new LinearLayout.LayoutParams(-1, (int)(50*DENSITY)); btnLp.setMargins(0,0,0,(int)(20*DENSITY)); rootDia.addView(actionBtn, btnLp); 
        
        LinearLayout localRow = new LinearLayout(activity); localRow.setOrientation(LinearLayout.HORIZONTAL);
        Button bEx = new Button(activity); bEx.setText(lang.get("Export JSON")); bEx.setAllCaps(false); bEx.setTextColor(colorAccent); bEx.setTextSize(13); bEx.setTypeface(Typeface.DEFAULT_BOLD);
        GradientDrawable gEx = new GradientDrawable(); gEx.setColor(themeColors[5]); gEx.setCornerRadius(12f*DENSITY); bEx.setBackground(gEx);
        LinearLayout.LayoutParams lpEx = new LinearLayout.LayoutParams(0, (int)(45*DENSITY), 1f); lpEx.setMargins(0,0,(int)(8*DENSITY),0); localRow.addView(bEx, lpEx);
        
        Button bIm = new Button(activity); bIm.setText(lang.get("Restore JSON")); bIm.setAllCaps(false); bIm.setTextColor(colorAccent); bIm.setTextSize(13); bIm.setTypeface(Typeface.DEFAULT_BOLD);
        GradientDrawable gIm = new GradientDrawable(); gIm.setColor(themeColors[5]); gIm.setCornerRadius(12f*DENSITY); bIm.setBackground(gIm);
        LinearLayout.LayoutParams lpIm = new LinearLayout.LayoutParams(0, (int)(45*DENSITY), 1f); lpIm.setMargins((int)(8*DENSITY),0,0,0); localRow.addView(bIm, lpIm); rootDia.addView(localRow);
        
        FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(rootDia, flp);
        
        final AlertDialog ad = new AlertDialog.Builder(activity).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(Gravity.CENTER);
        
        actionBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { 
            String mail = emailIn.getText().toString().trim(); 
            if (!mail.isEmpty()) { 
                sp.edit().putString("user_email", mail).apply(); ad.dismiss(); 
                fbHelper.fetchAndLoad(
                    new Runnable() { @Override public void run() { ui.showSmartBanner(root, lang.get("Syncing Data"), lang.get("Connecting to cloud..."), "img_cloud", colorAccent, null); }}, 
                    new Runnable() { @Override public void run() { ui.showSmartBanner(root, lang.get("Sync Complete"), lang.get("Progress updated."), "img_tick", colorAccent, null); if(onReload!=null) onReload.run(); }}, 
                    new Runnable() { @Override public void run() { ui.showSmartBanner(root, lang.get("Network Error"), lang.get("Check internet connection."), "img_warning", colorAccent, null); if(onReload!=null) onReload.run(); }} 
                ); 
            } 
        } });
        bEx.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { exportData(); ad.dismiss(); }}); 
        bIm.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showRestoreDialog(onReload); ad.dismiss(); }});
        ad.show();
    }
}