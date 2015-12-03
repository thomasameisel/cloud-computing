package com.tarian.finalproject;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;


public class MainActivity extends AppCompatActivity implements AddItemDialog.OnSaveItemDialog {

    ListAdapter mItemAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        RecyclerView listView = (RecyclerView)findViewById(R.id.recycler_view);
        listView.setScrollContainer(false);
        final LinearLayoutManager linearLayoutManager = new LinearLayoutManager(this,
                LinearLayoutManager.VERTICAL, false);
        listView.setLayoutManager(linearLayoutManager);

        mItemAdapter = new ListAdapter(this);
        mItemAdapter.setOnItemClickListener(this);
        listView.setAdapter(mItemAdapter);

        mItemAdapter.onItemAdd(new Item("This is a message", "3 miles away"));
        mItemAdapter.onItemAdd(new Item("This is a message", "10 miles away"));
        mItemAdapter.onItemAdd(new Item("This is a message\n\n\nLonglonglonglonglonglong", "34 miles away"));
        mItemAdapter.onItemAdd(new Item("This is a message", "57 miles away"));
    }

    public void addMessage(View view) {
        final Bundle dialogBundle = AddItemDialog.getCallingArguments("Add Message");

        final AddItemDialog addItemDialog = new AddItemDialog();
        addItemDialog.setArguments(dialogBundle);
        addItemDialog.show(getSupportFragmentManager(), null);
    }

    @Override
    public void onSaveItemDialog(String id, String message, String location) {
        mItemAdapter.onItemAdd(new Item(message, location), 0);
        RecyclerView listView = (RecyclerView)findViewById(R.id.recycler_view);
        listView.smoothScrollToPosition(0);
    }
}
