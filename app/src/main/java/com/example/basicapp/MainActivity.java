package com.example.basicapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Credentials;
import android.os.Bundle;
import android.view.View;

import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import org.bson.Document;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        MongoClientURI uri = new MongoClientURI("");

        MongoClient mongoClient = new MongoClient(uri);
        MongoDatabase database = mongoClient.getDatabase("inventory");

        MongoCollection<Document> collection = database.getCollection("stock_summary");

        Document queryFilter  = new Document("type", "perennial");
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