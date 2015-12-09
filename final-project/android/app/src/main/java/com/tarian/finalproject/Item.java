package com.tarian.finalproject;

import java.util.UUID;

/**
 * Information for a memorea
 */
public class Item {
    public String mMessage;
    public String mLocation;
    public UUID mId;

    public Item(final UUID id, final String mMessage, final String mLocation) {
        this.mId = id;
        this.mMessage = mMessage;
        this.mLocation = mLocation;
    }
}
