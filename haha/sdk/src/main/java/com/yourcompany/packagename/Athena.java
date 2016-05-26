package com.lixar.athena;

import android.content.Context;
import android.util.Log;

import com.google.common.util.concurrent.AsyncFunction;
import com.google.common.util.concurrent.Futures;
import com.lixar.athena.cache.CacheFactory;
import com.lixar.athena.cache.ModelCache;
import com.lixar.athena.model.AuthenticationResponse;
import com.lixar.athena.model.Channel;
import com.lixar.athena.model.SubscribeStatusRequest;
import com.lixar.athena.model.UserInfoResponse;
import com.lixar.athena.operation.AccountsService;
import com.lixar.athena.operation.AthenaApiInterceptor;
import com.lixar.athena.operation.ChannelsService;
import com.lixar.athena.operation.SurveysService;
import com.lixar.athena.utility.LogUtil;
import com.lixar.athena.utility.MoshiDateTimeAdapter;
import com.google.common.util.concurrent.ListenableFuture;
import com.google.common.util.concurrent.ListeningExecutorService;
import com.google.common.util.concurrent.MoreExecutors;
import com.squareup.moshi.Moshi;

import org.threeten.bp.OffsetDateTime;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.Executors;

import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.moshi.MoshiConverterFactory;

/**
 * Created by pzhou on 2016-05-16.
 */
final public class Athena {

    private Context context;

    protected ModelCache modelCache;

    public ChannelsService getChannelsService() {
        return channelsService;
    }
    public SurveysService getSurveysService() {
        return surveysService;
    }
    public AccountsService getAccountsService() {
        return accountsService;
    }

    public ListeningExecutorService getExecutor() {
        return executor;
    }

    public static class Builder {
        private String urlString;
        private String apiKey;
        private String clientIdentifier;
        private Context context;
        public Builder(){
            apiKey = "";
            clientIdentifier = "";

        };

        public Builder withContext(Context context){
            this.context = context;
            return this;
        }
        public Builder withUrl(String urlString){
            this.urlString = urlString;
            this.apiKey = "";
            this.clientIdentifier = "";
            return this;
        };

        public Builder withApiKey(String apiKey){
            this.apiKey = "";
            this.clientIdentifier = "";
            return this;
        };

        public Builder withClientIdentifier(String clientIdentifier){
            return this;
        };

        public ListenableFuture<Athena> buildAsync(){
            Athena instance = new Athena(this.urlString, this.apiKey, this.clientIdentifier, this.context);
            return instance.loginAsync();
        }
    }

    private String urlString;
    private String apiKey;
    private String clientIdentifier;

    private ChannelsService channelsService;
    private SurveysService surveysService;
    private AccountsService accountsService;
    private AthenaApiInterceptor athenaApiInterceptor;
    private ListeningExecutorService executor;

    private Athena(String urlString, String apiKey, String clientIdentifier, Context context) {
        this.context = context;
        this.apiKey = apiKey;
        this.clientIdentifier = clientIdentifier;
        this.athenaApiInterceptor = new AthenaApiInterceptor(this.context);
        this.executor = MoreExecutors.listeningDecorator(Executors.newSingleThreadExecutor());

        OkHttpClient client = null;
        if (BuildConfig.DEBUG) {
            HttpLoggingInterceptor loggingInterceptor = new HttpLoggingInterceptor();
            loggingInterceptor.setLevel(HttpLoggingInterceptor.Level.BODY);
            client = new OkHttpClient.Builder()
                    .addInterceptor(athenaApiInterceptor)
                    .addInterceptor(loggingInterceptor)
                    .build();
        }else{
            client = new OkHttpClient.Builder()
                    .addInterceptor(athenaApiInterceptor)
                    .build();
        }

        Moshi moshi = new Moshi.Builder()
                .add(new MoshiDateTimeAdapter())
                .build();

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(urlString)
                .client(client)
                .addConverterFactory(MoshiConverterFactory.create(moshi))
                .build();

        channelsService = retrofit.create(ChannelsService.class);
        surveysService = retrofit.create(SurveysService.class);
        accountsService = retrofit.create(AccountsService.class);

        modelCache = CacheFactory.getModelCache(CacheFactory.CacheStorage.SQLITE, context);
    }

    private ListenableFuture<Athena> loginAsync(){
        ListenableFuture<Athena> loginFuture = executor.submit(new Callable<Athena>() {
            public Athena call() throws Exception {
                Call<AuthenticationResponse> loginCall = accountsService.apikey(Athena.this.apiKey, Athena.this.clientIdentifier);
                try {
                    Response<AuthenticationResponse> response = loginCall.execute();
                    if (response.isSuccessful()){

                        Log.d(LogUtil.getLogTag(this), String.format("Login Succeeded with token: %s", response.body().getAccessToken()));
                        athenaApiInterceptor.setApiToken("bearer", response.body().getAccessToken());
                        return Athena.this;
                    }else{
                        Log.d(LogUtil.getLogTag(this), "Login Failed");
                        Log.d(LogUtil.getLogTag(this), "Code: " + String.valueOf(response.code()) + response.message());
                        Log.d(LogUtil.getLogTag(this), "Headers: " + response.headers().toString());
                        Log.d(LogUtil.getLogTag(this), response.errorBody().string());
                        throw new IOException(String.format("Login Failed with code: %d", response.code()));
                    }

                } catch (IOException e) {
                    throw e;
                }
            }
        });
        return loginFuture;
    };

    public ListenableFuture<UserInfoResponse> getUserInfoAsync(){
        ListenableFuture<UserInfoResponse> callFuture = executor.submit(new Callable<UserInfoResponse>() {
            public UserInfoResponse call() throws Exception {
                Call<UserInfoResponse> restCall = accountsService.getUserInfo();
                try {
                    Response<UserInfoResponse> response = restCall.execute();
                    if (response.isSuccessful()){

                        Log.d(LogUtil.getLogTag(this), String.format("getUserInfoAsync Succeeded with userInfo: %s",response.body().toString()));
                        return response.body();
                    }else{
                        Log.d(LogUtil.getLogTag(this), "getUserInfoAsync Failed!");
                        Log.d(LogUtil.getLogTag(this), "Code: " + String.valueOf(response.code()) + response.message());
                        Log.d(LogUtil.getLogTag(this), "Headers: " + response.headers().toString());
                        throw new IOException(String.format("getUserInfoAsync Failed with code: %d", response.code()));
                    }
                } catch (IOException e) {
                    throw e;
                }
            }
        });
        return callFuture;
    }

    public ListenableFuture<List<Channel>> getChannelsAsync(){
        ListenableFuture<List<Channel>> callFuture = executor.submit(new Callable<List<Channel>>() {
            public List<Channel> call() throws Exception {
                final ArrayList<Integer> exclude = new ArrayList<Integer>();
                final OffsetDateTime whenModified = OffsetDateTime.now();
                Call<List<Channel>> restCall = surveysService.getChannels(exclude, whenModified );
                try {
                    Response<List<Channel>> response = restCall.execute();
                    if (response.isSuccessful()){
                        for (Channel channel : response.body()){
                            channel.setAthena(Athena.this);
                        }
                        modelCache.addUpdateChannels(response.body());
                        Log.d(LogUtil.getLogTag(this), String.format("getChannelsAsync Succeeded with userInfo: %s",response.body().toString()));
                        return response.body();
                    }else{
                        Log.d(LogUtil.getLogTag(this), "getChannelsAsync Failed!");
                        Log.d(LogUtil.getLogTag(this), "Code: " + String.valueOf(response.code()) + response.message());
                        Log.d(LogUtil.getLogTag(this), "Headers: " + response.headers().toString());
                        throw new IOException(String.format("getChannelsAsync Failed with code: %d", response.code()));
                    }
                } catch (IOException e) {
                    throw e;
                }
            }
        });
        return callFuture;
    }

    private ListenableFuture<List<Channel>> getFilteredChannelsAsync(final boolean subscribed){
        ListenableFuture<List<Channel>> getAllChannelsFuture = getChannelsAsync();
        AsyncFunction<List<Channel>, List<Channel>> allChannelsToFilteredChannels = new AsyncFunction<List<Channel>, List<Channel>>() {
            @Override
            public ListenableFuture<List<Channel>> apply(final List<Channel> allChannels) throws Exception {
                return executor.submit(new Callable<List<Channel>>() {
                    @Override
                    public List<Channel> call() throws Exception {
                        List<Channel> filteredChannels = new ArrayList<Channel>();
                        for (Channel channel : allChannels){
                            if (channel.getSubscribed() == subscribed){
                                filteredChannels.add(channel);
                            }
                        }
                        return filteredChannels;
                    };
                });
            }
        };

        ListenableFuture<List<Channel>> filteredChannelsFuture = Futures.transformAsync(getAllChannelsFuture, allChannelsToFilteredChannels);
        return filteredChannelsFuture;
    }


    public ListenableFuture<List<Channel>> getUnsubscribedChannelsAsync(){
        return getFilteredChannelsAsync(false);
    }

    public ListenableFuture<List<Channel>> getSubscribedChannelsAsync(){
        return getFilteredChannelsAsync(true);
    }

    public ListenableFuture<Channel> getChannelAsync(final int channelId){
        ListenableFuture<List<Channel>> getAllChannelsFuture = getChannelsAsync();
        AsyncFunction<List<Channel>, Channel > allChannelsToFoundChannel = new AsyncFunction<List<Channel>, Channel>() {

            @Override
            public ListenableFuture<Channel> apply(final List<Channel> allChannels) throws Exception {
                return executor.submit(new Callable<Channel>() {
                    @Override
                    public Channel call() throws Exception {

                        for (Channel channel : allChannels){
                            if (channel.getChannelId() == channelId){
                                return channel;
                            }
                        }
                        return null;
                    };
                });
            }
        };

        ListenableFuture<Channel> foundChannelFuture = Futures.transformAsync(getAllChannelsFuture, allChannelsToFoundChannel);
        return foundChannelFuture;
    };

    private ListenableFuture<Boolean> setChannelStatusAsync(final Channel channel, final Channel.Status status) {
        ListenableFuture<Boolean> callFuture = this.getExecutor().submit(new Callable<Boolean>() {
            public Boolean call() throws Exception {
                SubscribeStatusRequest request = new SubscribeStatusRequest();
                request.setSubscribed(status.getValue());
                Call<Void> call = Athena.this.getSurveysService().subscribeToChannel(channel.getChannelId(), request);

                Response<Void> response = call.execute();

                if (response.isSuccessful()){
                    return true;
                }else{
                    Log.d(LogUtil.getLogTag(this), "getUserInfoAsync Failed!");
                    Log.d(LogUtil.getLogTag(this), "Code: " + String.valueOf(response.code()) + response.message());
                    Log.d(LogUtil.getLogTag(this), "Headers: " + response.headers().toString());
                    throw new IOException(String.format("subscribe failed with code: %d", response.code()));
                }
            }
        });

        return callFuture;
    }
    public ListenableFuture<Boolean> subscribeToChannelAsync(final Channel channel) {
        ListenableFuture<Boolean> callFuture = setChannelStatusAsync(channel, Channel.Status.ALLOW_ACCESS);

        AsyncFunction<Boolean, Boolean > saveAfter = new AsyncFunction<Boolean, Boolean>() {

            @Override
            public ListenableFuture<Boolean> apply(final Boolean result) throws Exception {
                return executor.submit(new Callable<Boolean>() {
                    @Override
                    public Boolean call() throws Exception {
                        if (result){
                            modelCache.addUpdateChannel(channel);
                        }
                        return result;
                    };
                });
            }
        };
        return  Futures.transformAsync(callFuture, saveAfter);
    }
    public ListenableFuture<Boolean> unsubscribeToChannelAsync(final Channel channel) {
        ListenableFuture<Boolean> callFuture = setChannelStatusAsync(channel, Channel.Status.DENY_ACCESS);

        AsyncFunction<Boolean, Boolean > deleteAfter = new AsyncFunction<Boolean, Boolean>() {

            @Override
            public ListenableFuture<Boolean> apply(final Boolean result) throws Exception {
                return executor.submit(new Callable<Boolean>() {
                    @Override
                    public Boolean call() throws Exception {
                        if (result){
                            modelCache.deleteChannel(channel);
                        }
                        return result;
                    };
                });
            }
        };
        return  Futures.transformAsync(callFuture, deleteAfter);
    }

}