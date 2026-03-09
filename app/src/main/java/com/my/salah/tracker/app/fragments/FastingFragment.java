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
import com.my.salah.tracker.app.LanguageEngine;

public class FastingFragment extends Fragment {
    private Object getField(String name) {
        try { Field f = getActivity().getClass().getDeclaredField(name); f.setAccessible(true); return f.get(getActivity()); } catch (Exception e) { return null; }
    }
    @Override public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        Context ctx = getContext();
        int[] themeColors = (int[]) getField("themeColors");
        int colorAccent = themeColors != null ? (Integer) getField("colorAccent") : Color.parseColor("#00BFA5");
        float DENSITY = themeColors != null ? (Float) getField("DENSITY") : 3.0f;
        LanguageEngine lang = (LanguageEngine) getField("lang");
        boolean isBn = false; try { isBn = lang.get("Fajr").equals("ফজর"); } catch(Exception e){}
        Typeface[] fonts = (Typeface[]) getField("appFonts");
        Typeface tfBold = fonts != null ? fonts[1] : Typeface.DEFAULT_BOLD;
        Typeface tfReg = fonts != null ? fonts[0] : Typeface.DEFAULT;

        ScrollView scroll = new ScrollView(ctx);
        scroll.setLayoutParams(new ViewGroup.LayoutParams(-1, -1));
        scroll.setBackgroundColor(themeColors != null ? themeColors[0] : Color.parseColor("#F5F5F5"));

        LinearLayout root = new LinearLayout(ctx);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding((int)(20*DENSITY), (int)(40*DENSITY), (int)(20*DENSITY), (int)(100*DENSITY));
        root.setGravity(Gravity.CENTER_HORIZONTAL);
        scroll.addView(root);

        TextView header = new TextView(ctx);
        header.setText(isBn ? "রোজা (Fasting)" : "Fasting");
        header.setTypeface(tfBold); header.setTextSize(28);
        header.setTextColor(themeColors != null ? themeColors[2] : Color.BLACK);
        header.setGravity(Gravity.CENTER); header.setPadding(0, 0, 0, (int)(30*DENSITY));
        root.addView(header);

        LinearLayout card = new LinearLayout(ctx);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding((int)(25*DENSITY), (int)(40*DENSITY), (int)(25*DENSITY), (int)(40*DENSITY));
        card.setGravity(Gravity.CENTER);
        GradientDrawable bg = new GradientDrawable();
        bg.setColor(themeColors != null ? themeColors[1] : Color.WHITE);
        bg.setCornerRadius(30f * DENSITY);
        if (themeColors != null) bg.setStroke((int)(1.5f * DENSITY), themeColors[4]);
        card.setBackground(bg);
        if (android.os.Build.VERSION.SDK_INT >= 21) card.setElevation(10f);

        TextView iconView = new TextView(ctx);
        iconView.setText("🌙"); iconView.setTextSize(60);
        iconView.setGravity(Gravity.CENTER); iconView.setPadding(0, 0, 0, (int)(15*DENSITY));
        card.addView(iconView);

        TextView title = new TextView(ctx);
        title.setText(isBn ? "খুব শিগগিরই আসছে!" : "Coming Soon!");
        title.setTypeface(tfBold); title.setTextColor(colorAccent);
        title.setTextSize(24); title.setGravity(Gravity.CENTER); title.setPadding(0, 0, 0, (int)(10*DENSITY));
        card.addView(title);

        TextView desc = new TextView(ctx);
        desc.setText(isBn ? "রমজান এবং নফল রোজার ট্র্যাকিং, সাহরি ও ইফতারের সময়সূচিসহ চমৎকার সব ফিচার নিয়ে এই পেজটি পরবর্তী আপডেটে যুক্ত করা হবে ইনশাআল্লাহ্‌।" : "Ramadan & Nafl fasting tracker with Suhoor & Iftar timings will be added in the next update InshaAllah.");
        desc.setTypeface(tfReg); desc.setTextColor(themeColors != null ? themeColors[3] : Color.GRAY);
        desc.setTextSize(16); desc.setGravity(Gravity.CENTER); desc.setLineSpacing(0, 1.2f);
        card.addView(desc);

        root.addView(card);
        return scroll;
    }
}
