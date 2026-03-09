package com.my.salah.tracker.app.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.view.Gravity;
import androidx.fragment.app.Fragment;

public class SalahFragment extends Fragment {
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // আপাতত এটি একটি সিম্পল টেক্সট দেখাবে
        TextView tv = new TextView(getContext());
        tv.setText("Salah Page");
        tv.setGravity(Gravity.CENTER);
        tv.setTextSize(24f);
        return tv;
    }
}
