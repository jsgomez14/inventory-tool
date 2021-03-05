package com.example.basicapp;
import org.bson.Document;
import org.bson.types.ObjectId;

public class StockSummary extends Document{
    ObjectId _id;
    int id;
    String name;

    public StockSummary(ObjectId _id, int id, String name) {
        this._id = _id;
        this.id = id;
        this.name = name;
    }
}
