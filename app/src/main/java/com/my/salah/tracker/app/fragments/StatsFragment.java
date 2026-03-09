package com.my.salah.tracker.app.fragments;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import androidx.fragment.app.Fragment;
import java.lang.reflect.Field;
import java.text.SimpleDateFormat;
import com.my.salah.tracker.app.StatsHelper;
import com.my.salah.tracker.app.LanguageEngine;
import com.my.salah.tracker.app.UIComponents;

public class StatsFragment extends Fragment {

    // MainActivity থেকে অরিজিনাল ডাটা এবং লজিক আনার জন্য Reflection মেথড
    private Object getField(String name) {
        try {
            Field f = getActivity().getClass().getDeclaredField(name);
            f.setAccessible(true);
            return f.get(getActivity());
        } catch (Exception e) { return null; }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        Context ctx = getContext();
        
        // অরিজিনাল লজিক কানেকশন
        final StatsHelper statsHelper = (StatsHelper) getField("statsHelper");
        LanguageEngine lang = (LanguageEngine) getField("lang");
        UIComponents ui = (UIComponents) getField("ui");
        int[] themeColors = (int[]) getField("themeColors");
        int colorAccent = themeColors != null ? (Integer) getField("colorAccent") : Color.parseColor("#00BFA5");
        float DENSITY = themeColors != null ? (Float) getField("DENSITY") : 3.0f;
        final SimpleDateFormat sdf = (SimpleDateFormat) getField("sdf");
        final String[] selectedDate = (String[]) getField("selectedDate");

        boolean isBn = false;
        try { isBn = lang.get("Fajr").equals("ফজর"); } catch(Exception e){}

        Typeface tfBold = Typeface.DEFAULT_BOLD;
        try {
            if (isBn) tfBold = Typeface.createFromAsset(ctx.getAssets(), "fonts/hind_bold.ttf");
            else tfBold = Typeface.createFromAsset(ctx.getAssets(), "fonts/poppins_bold.ttf");
        } catch (Exception e) {}

        ScrollView scroll = new ScrollView(ctx);
        scroll.setLayoutParams(new ViewGroup.LayoutParams(-1, -1));
        scroll.setBackgroundColor(themeColors != null ? themeColors[0] : Color.parseColor("#F8FAFC"));

        LinearLayout root = new LinearLayout(ctx);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding((int)(20*DENSITY), (int)(40*DENSITY), (int)(20*DENSITY), (int)(150*DENSITY));
        scroll.addView(root);

        // হেডার ডিজাইন
        TextView header = new TextView(ctx);
        header.setText(isBn ? "বিস্তারিত রিপোর্ট" : "Advanced Statistics");
        header.setTypeface(tfBold);
        header.setTextSize(28);
        header.setTextColor(themeColors != null ? themeColors[2] : Color.BLACK);
        header.setGravity(Gravity.CENTER);
        header.setPadding(0, 0, 0, (int)(40*DENSITY));
        root.addView(header);

        // অরিজিনাল ডাটাবেস সিঙ্ক করা
        try {
            if (statsHelper != null && sdf != null && selectedDate != null) {
                statsHelper.syncDate(sdf.parse(selectedDate[0]));
            }
        } catch (Exception e) {}

        // বাটনের তালিকা
        String[] titles = {
            isBn ? "সাপ্তাহিক পরিসংখ্যান" : "Weekly Statistics",
            isBn ? "মাসিক পরিসংখ্যান" : "Monthly Statistics",
            isBn ? "রিপোর্ট শেয়ার (ছবি)" : "Share Report (Image)",
            isBn ? "প্রিমিয়াম এক্সেল (XLS) এক্সপোর্ট" : "Export Premium XLS",
            isBn ? "প্রিমিয়াম পিডিএফ এক্সপোর্ট" : "Export Premium PDF"
        };
        
        String[] emojis = {"📊", "📈", "🖼️", "📗", "📕"};

        // বাটনের অ্যাকশন (অরিজিনাল StatsHelper মেথড কল করা)
        final Runnable[] actions = {
            new Runnable() { public void run() { if(statsHelper!=null) statsHelper.showStats(true); } },
            new Runnable() { public void run() { if(statsHelper!=null) statsHelper.showStats(false); } },
            new Runnable() { public void run() { 
                try { java.lang.reflect.Method m = statsHelper.getClass().getDeclaredMethod("showShareTypeDialog"); m.setAccessible(true); m.invoke(statsHelper); } catch(Exception e){}
            } },
            new Runnable() { public void run() { if(statsHelper!=null) statsHelper.exportXls(); } },
            new Runnable() { public void run() { if(statsHelper!=null) statsHelper.exportPdf(); } }
        };

        // ৫টি প্রিমিয়াম বাটন তৈরি করা
        for (int i = 0; i < titles.length; i++) {
            final int idx = i;
            LinearLayout btn = new LinearLayout(ctx);
            btn.setOrientation(LinearLayout.HORIZONTAL);
            btn.setGravity(Gravity.CENTER_VERTICAL);
            btn.setPadding((int)(20*DENSITY), (int)(22*DENSITY), (int)(20*DENSITY), (int)(22*DENSITY));
            
            GradientDrawable bg = new GradientDrawable();
            bg.setColor(themeColors != null ? themeColors[1] : Color.WHITE);
            bg.setCornerRadius(20f * DENSITY);
            if (themeColors != null) bg.setStroke((int)(1.5f * DENSITY), themeColors[4]);
            btn.setBackground(bg);
            
            if (android.os.Build.VERSION.SDK_INT >= 21) {
                btn.setElevation(8f);
            }
            
            LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2);
            lp.setMargins((int)(10*DENSITY), 0, (int)(10*DENSITY), (int)(20*DENSITY));
            btn.setLayoutParams(lp);

            if (ui != null) {
                View icon = ui.getPremiumIcon(emojis[i], colorAccent, colorAccent, 38);
                LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY));
                icLp.setMargins(0, 0, (int)(18*DENSITY), 0);
                icon.setLayoutParams(icLp);
                btn.addView(icon);
            }

            TextView tv = new TextView(ctx);
            tv.setText(titles[i]);
            tv.setTextColor(themeColors != null ? themeColors[2] : Color.BLACK);
            tv.setTextSize(16);
            tv.setTypeface(tfBold);
            btn.addView(tv);

            btn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                    actions[idx].run();
                }
            });

            if (ui != null) ui.addClickFeedback(btn);
            
            root.addView(btn);
        }

        return scroll;
    }
}
