package com.tarian.finalproject;

import android.os.Parcel;
import android.os.Parcelable;

import java.util.UUID;

/**
 * Information for a memorea
 */
public class Item implements Parcelable {
    public String mMessage;
    public double mLatitude;
    public double mLongitude;
    public UUID mId;

    public Item(final UUID id, final String message, final double latitude, final double longitude) {
        this.mId = id;
        this.mMessage = message;
        this.mLatitude = latitude;
        this.mLongitude = longitude;
    }

    protected Item(Parcel in) {
        mMessage = in.readString();
        mLatitude = in.readDouble();
        mLongitude = in.readDouble();
        mId = (UUID) in.readValue(UUID.class.getClassLoader());
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(mMessage);
        dest.writeDouble(mLatitude);
        dest.writeDouble(mLongitude);
        dest.writeValue(mId);
    }

    @SuppressWarnings("unused")
    public static final Parcelable.Creator<Item> CREATOR = new Parcelable.Creator<Item>() {
        @Override
        public Item createFromParcel(Parcel in) {
            return new Item(in);
        }

        @Override
        public Item[] newArray(int size) {
            return new Item[size];
        }
    };
}
