package com.tarian.finalproject;

import android.app.Activity;
import android.content.Context;
import android.location.Location;
import android.location.LocationManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.TimeZone;
import java.util.UUID;

/**
 * Adapter for the RecyclerView
 */
public class ListAdapter extends RecyclerView.Adapter<ListAdapter.ViewHolder> {

    private static final String GMT = "GMT";

    private Context mContext;

    private ArrayList<Item> mList;
    private AdapterView.OnItemClickListener mOnItemClickListener;

    public ListAdapter(Context context) {
        this.mContext = context;
        this.mList = new ArrayList<>();
    }

    public void setOnItemClickListener(final Activity activity) {
        if (activity instanceof AdapterView.OnItemClickListener) {
            mOnItemClickListener = (AdapterView.OnItemClickListener) activity;
        }
    }

    @Override
    public ViewHolder onCreateViewHolder(final ViewGroup parent, final int viewType) {
        final View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_card, parent, false);
        return new ViewHolder(itemView, this);
    }

    @Override
    public void onBindViewHolder(final ViewHolder holder, final int position) {
        Location currentLocation = getLastKnownLocation();
        final Item memorea = mList.get(position);
        holder.setMessage(memorea.mMessage);
        holder.setLocation(memorea.mLatitude, memorea.mLongitude, currentLocation.getLatitude(),
                currentLocation.getLongitude());
    }

    /**
     * Returns the number of items
     */
    @Override
    public int getItemCount() {
        return mList.size();
    }

    public void clearData() {
        int size = mList.size();
        mList.clear();
        notifyItemRangeRemoved(0, size);
    }

    public ArrayList<Item> getList() {
        return mList;
    }

    public void addAll(final Collection<Item> itemList) {
        for (Item item : itemList) {
            onItemAdd(item);
        }
    }

    /**
     * Adds a memorea to the bottom of the list
     */
    public void onItemAdd(final Item item) {
        onItemAdd(item, getItemCount());
    }

    /**
     * Adds a memorea to the list in the position specified
     */
    public void onItemAdd(final Item item, final int position) {
        mList.add(position, item);
        notifyItemInserted(position);
    }

    /**
     * Returns the memorea with the mId field matching the parameter<br>
     * If none exist, returns null
     */
    public Item getItemByUUID(final UUID uuid) {
        return getItemByUUID(mList, uuid);
    }

    /**
     * Returns the memorea at the specified position
     */
    public Item getItem(final int position) {
        return mList.get(position);
    }

    /**
     * Calls notifyItemChanged(position) for every position in the memorea list
     */
    public void notifyAllItemsChanged() {
        for (int i = 0; i < mList.size(); ++i) {
            notifyItemChanged(i);
        }
    }

    private Item getItemByUUID(final List<Item> list, final UUID uuid) {
        for (Item item : list) {
            if (uuid.equals(item.mId)) {
                return item;
            }
        }

        return null;
    }

    private void onItemHolderClick(final ViewHolder viewHolder) {
        if (mOnItemClickListener != null) {
            mOnItemClickListener.onItemClick(null, viewHolder.itemView,
                    viewHolder.getAdapterPosition(), viewHolder.getItemId());
        }
    }

    private Location getLastKnownLocation() {
        LocationManager mLocationManager = (LocationManager)mContext.getSystemService(mContext.LOCATION_SERVICE);
        List<String> providers = mLocationManager.getProviders(true);
        Location bestLocation = null;
        for (String provider : providers) {
            Location l = mLocationManager.getLastKnownLocation(provider);
            if (l == null) {
                continue;
            }
            if (bestLocation == null || l.getAccuracy() < bestLocation.getAccuracy()) {
                // Found best last known location: %s", l);
                bestLocation = l;
            }
        }
        return bestLocation;
    }

    /**
     * Binds the memorea to its view
     */
    public static class ViewHolder extends RecyclerView.ViewHolder {
        private TextView message, location;
        private ListAdapter listAdapter;

        /**
         * Constructor for ViewHolder
         * @param memoreaView View corresponds to the memorea
         * @param listAdapter RecyclerView Adapter for the memorea list
         */
        public ViewHolder(final View memoreaView, final ListAdapter listAdapter) {
            super(memoreaView);

            message = (TextView) memoreaView.findViewById(R.id.text_view_message);
            location = (TextView) memoreaView.findViewById(R.id.text_view_location);

            this.listAdapter = listAdapter;
        }

        /**
         * Sets the mTitle in the view of the memorea
         */
        public void setMessage(String title) {
            this.message.setText(title);
        }

        public void setLocation(double messageLatitude, double messageLongitude,
                                double currentLatitude, double currentLongitude) {
            float[] results = new float[1];
            Location.distanceBetween(messageLatitude, messageLongitude, currentLatitude,
                    currentLongitude, results);
            String distance = Float.toString(results[0])+" meters away";
            this.location.setText(distance);
        }
    }
}
