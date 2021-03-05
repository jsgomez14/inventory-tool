package com.example.basicapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void createEntry(View view) {
        Intent intent = new Intent(MainActivity.this, CreateEntry.class);
        startActivity(intent);
    }

    public void createOut(View view) {
        Intent intent = new Intent(MainActivity.this, CreateOut.class);
        startActivity(intent);
    }

    public void viewEntries(View view) {
        Intent intent = new Intent(MainActivity.this, ViewEntriesActivity.class);
        startActivity(intent);
    }

    public void viewOuts(View view) {
        Intent intent = new Intent(MainActivity.this, ViewOutsActivity.class);
        startActivity(intent);
    }
}