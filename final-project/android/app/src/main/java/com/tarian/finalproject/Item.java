package com.tarian.finalproject;

import java.util.UUID;

/**
 * Information for a memorea
 */
public class Item {
    public String mMessage;
    public String mLocation;
    public UUID mId;

    public Item(final String mMessage, final String mLocation) {
        this.mMessage = mMessage;
        this.mLocation = mLocation;
    }

    /**
     * Generates a new mId for the memorea
     */
    public void generateNewId() {
        mId = UUID.randomUUID();
    }
}
