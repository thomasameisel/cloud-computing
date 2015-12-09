package com.tarian.finalproject;

import android.Manifest;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.squareup.okhttp.HttpUrl;
import com.squareup.okhttp.MediaType;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import com.squareup.okhttp.Response;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

public class MainActivity extends AppCompatActivity implements AddItemDialog.OnSaveItemDialog {

    final String apiHost = "54.152.164.252";
    final String apiPostUrl = "http://54.152.164.252/messages";

    OkHttpClient client;
    ListAdapter mItemAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final SwipeRefreshLayout swipeRefreshLayout = (SwipeRefreshLayout)
                findViewById(R.id.swipe_refresh_layout);

        swipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                new HttpAsyncTask().execute(apiHost);
                swipeRefreshLayout.setRefreshing(false);
            }
        });

        RecyclerView listView = (RecyclerView)findViewById(R.id.recycler_view);
        listView.setScrollContainer(false);
        final LinearLayoutManager linearLayoutManager = new LinearLayoutManager(this,
                LinearLayoutManager.VERTICAL, false);
        listView.setLayoutManager(linearLayoutManager);

        mItemAdapter = new ListAdapter(this);
        mItemAdapter.setOnItemClickListener(this);
        listView.setAdapter(mItemAdapter);

        client = new OkHttpClient();
        enablePermissions();
    }

    //returns [latitude,longitude]
    double[] getLocation() {
        Location location = getLastKnownLocation();
        double latitude = location.getLatitude();
        double longitude = location.getLongitude();
        return new double[]{latitude,longitude};
    }

    private Location getLastKnownLocation() {
        LocationManager mLocationManager = (LocationManager)getApplicationContext().getSystemService(LOCATION_SERVICE);
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

    // code request code here
    String doGetRequest(String host) throws IOException {
        double[] location = getLocation();
        HttpUrl url = new HttpUrl.Builder()
                .scheme("http")
                .host(host)
                .addPathSegment("messages")
                .addQueryParameter("latitude", Double.toString(location[0]))
                .addQueryParameter("longitude", Double.toString(location[1]))
                .build();
        Request request = new Request.Builder()
                .url(url)
                .build();
        Response response = client.newCall(request).execute();
        return response.body().string();
    }

    private void enablePermissions() {
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.INTERNET)
                != PackageManager.PERMISSION_GRANTED &&
                ContextCompat.checkSelfPermission(this,
                        Manifest.permission.ACCESS_FINE_LOCATION)
                        != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.INTERNET,Manifest.permission.ACCESS_FINE_LOCATION},
                    0);
        } else if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.INTERNET)
                != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.INTERNET},
                    0);
        } else if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    0);
        } else {
            new HttpAsyncTask().execute(apiHost);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String permissions[], int[] grantResults) {
        if ((grantResults.length > 1
                && grantResults[0] == PackageManager.PERMISSION_GRANTED
                && grantResults[1] == PackageManager.PERMISSION_GRANTED) ||
                (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED)) {

            new HttpAsyncTask().execute(apiHost);
        }
    }

    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");

    String doPostRequest(String url, String json) throws IOException {
        RequestBody body = RequestBody.create(JSON, json);
        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();
        Response response = client.newCall(request).execute();
        return response.body().string();
    }

    public void addMessage(View view) {
        final Bundle dialogBundle = AddItemDialog.getCallingArguments("Add Message");
        final AddItemDialog addItemDialog = new AddItemDialog();
        addItemDialog.setArguments(dialogBundle);
        addItemDialog.show(getSupportFragmentManager(), null);
    }

    @Override
    public void onSaveItemDialog(String id, String message) {
        try {
            double[] location = getLocation();
            JSONObject body = createJSONObject(id, message, location[0], location[1]);
            new HttpAsyncTask().execute(apiPostUrl, body.toString());
            Item newItem = new Item(UUID.fromString(id), message, "0.0 meters away");
            mItemAdapter.onItemAdd(newItem,0);
            RecyclerView listView = (RecyclerView)findViewById(R.id.recycler_view);
            listView.smoothScrollToPosition(0);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private JSONObject createJSONObject(String id, String message, double latitude,
                                        double longitude) throws JSONException {
        JSONObject json = new JSONObject();
        json.put("id",id);
        json.put("message",message);
        json.put("latitude",latitude);
        json.put("longitude",longitude);
        return json;
    }

    private class HttpAsyncTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... params) {
            try {
                if(params.length == 1) {
                    return doGetRequest(params[0]);
                } else {
                    return doPostRequest(params[0],params[1]);
                }
            } catch (IOException e) {
                e.printStackTrace();
                return "";
            }
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            try {
                JSONObject fullResult = new JSONObject(result);
                switch(fullResult.getString("type")){
                    case "GET":
                        mItemAdapter.clearData();

                        JSONArray messages = fullResult.getJSONArray("message");
                        double[] userLocation = getLocation();
                        for (int i = 0; i < messages.length(); ++i) {
                            JSONObject messageObject = (JSONObject)messages.get(i);
                            String id = messageObject.getString("id");
                            String message = messageObject.getString("message");

                            //messageLocation is an array [longitude,latitude]
                            JSONArray messageLocation = messageObject.getJSONArray("location");
                            float[] results = new float[1];
                            Location.distanceBetween(messageLocation.getDouble(1),
                                    messageLocation.getDouble(0), userLocation[0], userLocation[1],
                                    results);
                            String distance = Float.toString(results[0])+" meters away";

                            Item addItem = new Item(UUID.fromString(id), message, distance);
                            mItemAdapter.onItemAdd(addItem);
                        }
                        break;
                    case "POST":
                        break;
                    default:
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }
}