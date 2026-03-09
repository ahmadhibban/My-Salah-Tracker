package com.my.salah.tracker.app.fragments;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.text.InputType;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import androidx.fragment.app.Fragment;
import java.util.Calendar;
import java.lang.reflect.Field;
import com.my.salah.tracker.app.LanguageEngine;

public class QuranFragment extends Fragment {

    private Object getField(String name) {
        try { Field f = getActivity().getClass().getDeclaredField(name); f.setAccessible(true); return f.get(getActivity()); } catch (Exception e) { return null; }
    }

    private String[] ayats = {
        "فَٱذْكُرُونِىٓ أَذْكُرْكُمْ وَٱشْكُرُوا۟ لِى وَلَا تَكْفُرُونِ|অতএব তোমরা আমাকে স্মরণ কর, আমিও তোমাদেরকে স্মরণ করব। আর তোমরা আমার প্রতি কৃতজ্ঞ হও এবং অকৃতজ্ঞ হয়ো না। (সূরা আল-বাকারা: ১৫২)|Therefore remember Me, I will remember you, and be thankful to Me. (Al-Baqarah: 152)",
        "إِنَّ ٱللَّهَ مَعَ ٱلصَّـٰبِرِينَ|নিশ্চয়ই আল্লাহ ধৈর্যশীলদের সাথে আছেন। (সূরা আল-বাকারা: ১৫৩)|Indeed, Allah is with the patient. (Al-Baqarah: 153)",
        "وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ|এবং তোমরা যেখানেই থাক না কেন, তিনি তোমাদের সাথেই আছেন। (সূরা আল-হাদীদ: ৪)|And He is with you wherever you are. (Al-Hadid: 4)",
        "لَا تَحْزَنْ إِنَّ ٱللَّهَ مَعَنَا|চিন্তা করো না, নিশ্চয়ই আল্লাহ আমাদের সাথে আছেন। (সূরা আত-তাওবাহ: ৪০)|Do not grieve; indeed Allah is with us. (At-Tawbah: 40)",
        "فَإِنَّ مَعَ ٱلْعُسْرِ يُسْرًا|নিশ্চয়ই কষ্টের সাথেই রয়েছে স্বস্তি। (সূরা আশ-শারহ: ৫)|For indeed, with hardship [will be] ease. (Ash-Sharh: 5)",
        "وَٱللَّهُ يَهْدِى مَن يَشَآءُ إِلَىٰ صِرَٰطٍ مُّسْتَقِيمٍ|আর আল্লাহ যাকে ইচ্ছা সরল পথের দিশা দেন। (সূরা আল-বাকারা: ২১৩)|And Allah guides whom He wills to a straight path. (Al-Baqarah: 213)",
        "وَخُلِقَ ٱلْإِنسَـٰنُ ضَعِيفًا|আর মানুষকে সৃষ্টি করা হয়েছে দুর্বল করে। (সূরা আন-নিসা: ২৮)|And mankind was created weak. (An-Nisa: 28)",
        "ٱهْدِنَا ٱلصِّرَٰطَ ٱلْمُسْتَقِيمَ|আমাদেরকে সরল পথ প্রদর্শন করুন। (সূরা আল-ফাতিহা: ৬)|Guide us to the straight path. (Al-Fatihah: 6)"
    };

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        Context ctx = getContext();
        int[] themeColors = (int[]) getField("themeColors");
        int colorAccent = themeColors != null ? (Integer) getField("colorAccent") : Color.parseColor("#00BFA5");
        float DENSITY = themeColors != null ? (Float) getField("DENSITY") : 3.0f;
        LanguageEngine lang = (LanguageEngine) getField("lang");
        boolean isBnTemp = false; try { isBnTemp = lang.get("Fajr").equals("ফজর"); } catch(Exception e){}
        final boolean isBn = isBnTemp;
        Typeface[] fonts = (Typeface[]) getField("appFonts");
        Typeface tfBold = fonts != null ? fonts[1] : Typeface.DEFAULT_BOLD;
        Typeface tfReg = fonts != null ? fonts[0] : Typeface.DEFAULT;
        Typeface arabicFont = null; try { arabicFont = Typeface.createFromAsset(ctx.getAssets(), "fonts/al_majeed_quranic_font_shiped.ttf"); } catch (Exception e) {}

        ScrollView scroll = new ScrollView(ctx);
        scroll.setLayoutParams(new ViewGroup.LayoutParams(-1, -1));
        scroll.setBackgroundColor(themeColors != null ? themeColors[0] : Color.parseColor("#F5F5F5"));

        LinearLayout root = new LinearLayout(ctx);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding((int)(20*DENSITY), (int)(30*DENSITY), (int)(20*DENSITY), (int)(100*DENSITY));
        scroll.addView(root);

        TextView header = new TextView(ctx);
        header.setText(isBn ? "আল কুরআন" : "Al Quran");
        header.setTypeface(tfBold); header.setTextSize(28);
        header.setTextColor(themeColors != null ? themeColors[2] : Color.BLACK);
        header.setGravity(Gravity.CENTER); header.setPadding(0, 0, 0, (int)(20*DENSITY));
        root.addView(header);

        LinearLayout ayatCard = new LinearLayout(ctx);
        ayatCard.setOrientation(LinearLayout.VERTICAL);
        ayatCard.setPadding((int)(20*DENSITY), (int)(25*DENSITY), (int)(20*DENSITY), (int)(25*DENSITY));
        GradientDrawable bg = new GradientDrawable();
        bg.setColor(themeColors != null ? themeColors[1] : Color.WHITE);
        bg.setCornerRadius(25f * DENSITY);
        if (themeColors != null) bg.setStroke((int)(1.5f * DENSITY), themeColors[4]);
        ayatCard.setBackground(bg);
        if (android.os.Build.VERSION.SDK_INT >= 21) ayatCard.setElevation(8f);

        TextView ayatTitle = new TextView(ctx);
        ayatTitle.setText(isBn ? "আজকের আয়াত" : "Ayat of the Day");
        ayatTitle.setTypeface(tfBold); ayatTitle.setTextColor(themeColors != null ? themeColors[3] : Color.GRAY);
        ayatTitle.setTextSize(14); ayatTitle.setGravity(Gravity.CENTER); ayatTitle.setPadding(0, 0, 0, (int)(15*DENSITY));
        ayatCard.addView(ayatTitle);

        int dayOfYear = Calendar.getInstance().get(Calendar.DAY_OF_YEAR);
        String[] todayAyat = ayats[dayOfYear % ayats.length].split("\\|");

        TextView arabicText = new TextView(ctx);
        arabicText.setText(todayAyat[0]);
        if (arabicFont != null) arabicText.setTypeface(arabicFont);
        arabicText.setTextColor(themeColors != null ? themeColors[2] : Color.BLACK);
        arabicText.setTextSize(32); arabicText.setGravity(Gravity.CENTER); arabicText.setLineSpacing(0, 1.3f);
        ayatCard.addView(arabicText);

        TextView transText = new TextView(ctx);
        transText.setText(isBn ? todayAyat[1] : todayAyat[2]);
        transText.setTypeface(tfReg); transText.setTextColor(themeColors != null ? themeColors[3] : Color.DKGRAY);
        transText.setTextSize(16); transText.setGravity(Gravity.CENTER); transText.setPadding(0, (int)(20*DENSITY), 0, (int)(5*DENSITY));
        ayatCard.addView(transText);
        root.addView(ayatCard);

        LinearLayout trackCard = new LinearLayout(ctx);
        trackCard.setOrientation(LinearLayout.VERTICAL);
        trackCard.setPadding((int)(20*DENSITY), (int)(25*DENSITY), (int)(20*DENSITY), (int)(25*DENSITY));
        trackCard.setBackground(bg);
        if (android.os.Build.VERSION.SDK_INT >= 21) trackCard.setElevation(8f);
        LinearLayout.LayoutParams tLp = new LinearLayout.LayoutParams(-1, -2);
        tLp.setMargins(0, (int)(25*DENSITY), 0, 0);
        trackCard.setLayoutParams(tLp);

        TextView trackTitle = new TextView(ctx);
        trackTitle.setText(isBn ? "তিলাওয়াত ট্র্যাকার" : "Recitation Tracker");
        trackTitle.setTypeface(tfBold); trackTitle.setTextColor(themeColors != null ? themeColors[2] : Color.BLACK);
        trackTitle.setTextSize(18); trackTitle.setGravity(Gravity.CENTER); trackTitle.setPadding(0, 0, 0, (int)(15*DENSITY));
        trackCard.addView(trackTitle);

        final SharedPreferences prefs = ctx.getSharedPreferences("QuranPrefs", Context.MODE_PRIVATE);
        LinearLayout inputRow = new LinearLayout(ctx);
        inputRow.setOrientation(LinearLayout.HORIZONTAL);
        inputRow.setWeightSum(2f);

        EditText paraInput = new EditText(ctx);
        paraInput.setHint(isBn ? "পারা (১-৩০)" : "Para (1-30)");
        paraInput.setTypeface(tfReg); paraInput.setInputType(InputType.TYPE_CLASS_NUMBER);
        paraInput.setGravity(Gravity.CENTER); paraInput.setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY));
        paraInput.setTextSize(16); paraInput.setTextColor(themeColors != null ? themeColors[2] : Color.BLACK);
        paraInput.setHintTextColor(themeColors != null ? themeColors[3] : Color.GRAY);
        GradientDrawable iBg = new GradientDrawable(); iBg.setColor(themeColors != null ? themeColors[4] : Color.LTGRAY); iBg.setCornerRadius(15f*DENSITY);
        paraInput.setBackground(iBg); paraInput.setText(prefs.getString("saved_para", ""));
        LinearLayout.LayoutParams pLp = new LinearLayout.LayoutParams(0, -2, 1f); pLp.setMargins(0, 0, (int)(8*DENSITY), 0);
        paraInput.setLayoutParams(pLp); inputRow.addView(paraInput);

        EditText pageInput = new EditText(ctx);
        pageInput.setHint(isBn ? "পৃষ্ঠা নম্বর" : "Page No.");
        pageInput.setTypeface(tfReg); pageInput.setInputType(InputType.TYPE_CLASS_NUMBER);
        pageInput.setGravity(Gravity.CENTER); pageInput.setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY));
        pageInput.setTextSize(16); pageInput.setTextColor(themeColors != null ? themeColors[2] : Color.BLACK);
        pageInput.setHintTextColor(themeColors != null ? themeColors[3] : Color.GRAY);
        pageInput.setBackground(iBg); pageInput.setText(prefs.getString("saved_page", ""));
        LinearLayout.LayoutParams pgLp = new LinearLayout.LayoutParams(0, -2, 1f); pgLp.setMargins((int)(8*DENSITY), 0, 0, 0);
        pageInput.setLayoutParams(pgLp); inputRow.addView(pageInput);
        trackCard.addView(inputRow);

        Button saveBtn = new Button(ctx);
        saveBtn.setText(isBn ? "সংরক্ষণ করুন" : "Save Progress");
        saveBtn.setTypeface(tfBold); saveBtn.setTextColor(Color.WHITE); saveBtn.setAllCaps(false); saveBtn.setTextSize(16);
        GradientDrawable bBg = new GradientDrawable(); bBg.setColor(colorAccent); bBg.setCornerRadius(15f*DENSITY);
        saveBtn.setBackground(bBg);
        LinearLayout.LayoutParams btnLp = new LinearLayout.LayoutParams(-1, (int)(50*DENSITY)); btnLp.setMargins(0, (int)(20*DENSITY), 0, 0);
        saveBtn.setLayoutParams(btnLp);
        saveBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                prefs.edit().putString("saved_para", paraInput.getText().toString()).putString("saved_page", pageInput.getText().toString()).apply();
                Toast.makeText(getContext(), isBn ? "মাশাআল্লাহ! সেভ হয়েছে।" : "Mashallah! Saved.", Toast.LENGTH_SHORT).show();
            }
        });
        trackCard.addView(saveBtn);
        root.addView(trackCard);
        return scroll;
    }
}
