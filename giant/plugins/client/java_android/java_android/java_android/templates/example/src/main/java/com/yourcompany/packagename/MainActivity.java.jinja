package com.lixar.athena.example;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import com.jakewharton.threetenabp.AndroidThreeTen;

import com.lixar.athena.*;
import com.lixar.athena.model.*;

import org.threeten.bp.OffsetDateTime;
import com.google.common.util.concurrent.ListenableFuture;
import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private Athena athena;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        AndroidThreeTen.init(this.getApplication());
        setContentView(R.layout.activity_main);



        ListView listView = (ListView) findViewById(R.id.listView);
        String[] items = {
            "GetUserInfo",
            "Apikey",
            "AcceptPrivacyPolicy",
            "RegisterNewUser",
            "SubscribeToChannel",
            "GetSurveys",
            "Logout",
            "ChangePassword",
            "GetChannels",
            "SubmitSurveyAnswers",
            "Login",
            "ResetPassword",
        };
        listView.setAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, items));
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                switch(position) {
                    case 0:
                        MainActivity.this.getUserInfo();
                        break;
                    case 1:
                        MainActivity.this.apikey();
                        break;
                    case 2:
                        MainActivity.this.acceptPrivacyPolicy();
                        break;
                    case 3:
                        MainActivity.this.registerNewUser();
                        break;
                    case 4:
                        MainActivity.this.subscribeToChannel();
                        break;
                    case 5:
                        MainActivity.this.getSurveys();
                        break;
                    case 6:
                        MainActivity.this.logout();
                        break;
                    case 7:
                        MainActivity.this.changePassword();
                        break;
                    case 8:
                        MainActivity.this.getChannels();
                        break;
                    case 9:
                        MainActivity.this.submitSurveyAnswers();
                        break;
                    case 10:
                        MainActivity.this.login();
                        break;
                    case 11:
                        MainActivity.this.resetPassword();
                        break;
                }
            }
        });

        ((TextView) findViewById(R.id.textView)).setMovementMethod(new ScrollingMovementMethod());
        log("Welcome to Giant!");

        ListenableFuture<Athena> future = new Athena.Builder()
                .withContext(this)
                .withApiKey("test")
                .withClientIdentifier("test")
                .withUrl("http://172.28.20.103:10010/")
                .buildAsync();
        Futures.addCallback(future, new FutureCallback<Athena>() {
            @Override
            public void onSuccess(Athena result) {
                MainActivity.this.athena = result;
            }

            @Override
            public void onFailure(Throwable t) {
              log("Failed to construct Athena. Check your network connection and api-key.");
            }
        });
    }

    protected void log(String value) {
        TextView view = (TextView) findViewById(R.id.textView);
        view.append(value + "\n");
        try {
            final int scrollAmount = view.getLayout().getLineTop(view.getLineCount()) - view.getHeight();
            if (scrollAmount > 0) {
                view.scrollTo(0, scrollAmount);
            }
            else {
                view.scrollTo(0, 0);
            }
        }
        catch(NullPointerException e) {
            // swallow it.
        }
    }

    protected void subscribeToChannel() {

    }

    protected void getSurveys() {
        final OffsetDateTime whenModified = OffsetDateTime.now();
        final String acceptLanguage = "ExampleString";


    }

    protected void submitSurveyAnswers() {
        final SurveyAnswersRequest answers = new SurveyAnswersRequest();


    }

    protected void getChannels() {
        final ArrayList<Integer> exclude = new ArrayList<Integer>();
        final OffsetDateTime whenModified = OffsetDateTime.now();


    }

    protected void acceptPrivacyPolicy() {


    }

    protected void logout() {


    }

    protected void resetPassword() {
        final ResetPasswordRequest emailInfo = new ResetPasswordRequest();


    }

    protected void changePassword() {
        final ChangePasswordRequest request = new ChangePasswordRequest();


    }

    protected void getUserInfo() {


    }

    protected void apikey() {
        final String apiKey = "ExampleString";
        final String clientId = "ExampleString";


    }

    protected void login() {
        final String grantType = "ExampleString";
        final String username = "ExampleString";
        final String password = "ExampleString";


    }

    protected void registerNewUser() {
        final RegisterUserRequest registrationInfo = new RegisterUserRequest();


    }
}