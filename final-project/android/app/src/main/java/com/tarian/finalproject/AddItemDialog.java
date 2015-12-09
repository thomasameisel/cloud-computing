package com.tarian.finalproject;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.DialogFragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;

import java.util.UUID;

public class AddItemDialog extends DialogFragment {

    public interface OnSaveItemDialog {

        void onSaveItemDialog(String id, String message);
    }

    public static Bundle getCallingArguments(String dialogTitle) {
        final Bundle callingBundle = new Bundle();
        callingBundle.putString(DIALOG_TITLE, dialogTitle);
        return callingBundle;
    }

    private static final String DIALOG_TITLE = "dialogTitle";

    private EditText mMessage;
    private OnSaveItemDialog mSaveListener;

    @Override
    public void onAttach(final Activity activity) {
        super.onAttach(activity);
        try {
            mSaveListener = (OnSaveItemDialog)activity;
        } catch (ClassCastException e) {
            throw new ClassCastException(activity.toString() + " must implement OnSaveItemDialog");
        }
    }

    @NonNull
    @Override
    public Dialog onCreateDialog(final Bundle savedInstanceState) {
        final AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        // Get the layout inflater
        final LayoutInflater inflater = getActivity().getLayoutInflater();
        final View addView = inflater.inflate(R.layout.fragment_add_item, null);
        mMessage = (EditText)addView.findViewById(R.id.edit_text_message);

        builder.setView(addView)
                .setPositiveButton("Save", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        mSaveListener.onSaveItemDialog(UUID.randomUUID().toString(),
                                mMessage.getText().toString());
                    }
                })
                .setNegativeButton("Cancel", null)
                .setTitle(getArguments().getString(DIALOG_TITLE));
        final Dialog dialog = builder.create();
        dialog.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);
        dialog.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_HIDDEN);
        return dialog;
    }
}
