package com.lixar.athena.operation;

import android.content.Context;
import android.text.TextUtils;
import android.util.Log;

import com.lixar.athena.cache.CacheFactory;
import com.lixar.athena.cache.HttpCache;
import com.lixar.athena.model.Entity;
import com.lixar.athena.model.Resource;
import com.lixar.athena.utility.LogUtil;
import com.lixar.athena.utility.MoshiDateTimeAdapter;
import com.squareup.moshi.JsonAdapter;
import com.squareup.moshi.Moshi;

import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import okhttp3.Headers;
import okhttp3.Interceptor;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.ResponseBody;

public class AthenaApiInterceptor implements Interceptor {
    private Context context;
    public AthenaApiInterceptor(Context context) {
        this.context = context;
    }

    private HashMap<String, String> apiTokens = new HashMap<>();

    private static Map<String, String> operationSecurityDefinition;
    static {
        HashMap<String, String> map = new HashMap<>();
        map.put("getUserInfo", "bearer");
        map.put("apikey", null);
        map.put("acceptPrivacyPolicy", "bearer");
        map.put("registerNewUser", null);
        map.put("subscribeToChannel", "bearer");
        map.put("getSurveys", "bearer");
        map.put("logout", "bearer");
        map.put("changePassword", "bearer");
        map.put("getChannels", "bearer");
        map.put("submitSurveyAnswers", "bearer");
        map.put("login", null);
        map.put("resetPassword", "bearer");
        operationSecurityDefinition = Collections.unmodifiableMap(map);
    }

    @Override
    public Response intercept(Chain chain) throws IOException {
        HttpCache restCache = CacheFactory.getRestCache(CacheFactory.CacheStorage.SQLITE, context);

        String authorizationHeaderValue = getApiTokenHeader(chain.request());
        Request original = chain.request();
        Request.Builder requestBuilder = chain.request().newBuilder();
        if(authorizationHeaderValue != null) {
            requestBuilder.addHeader("Authorization", authorizationHeaderValue);
        }

        JsonAdapter<Headers> jsonAdapter = new Moshi.Builder()
                .add(new MoshiDateTimeAdapter())
                .build()
                .adapter(Headers.class);
        Resource cachedResource = restCache.readResource(original);
        if (cachedResource != null) {
            Headers headers = jsonAdapter.fromJson(cachedResource.getRequestHeaders());
            if (!TextUtils.isEmpty(headers.get("ETag"))) {
                requestBuilder.addHeader("If-None-Match", headers.get("ETag"));
            }
        }

        Request request = requestBuilder.build();

        Response response = chain.proceed(request);

       // if the resource exists in db,
        //     use the  resoure etag to set If-None-Match header in the request,
        //     if response code is 304, use the response body in the db
        //     elseif response code is 2**, use the response from server and update resource in db
        //     elseif response code is neither 304 and 2**, use the response body in the db
        // else
        //     set If-None-Match header to be "" in the request
        //     if response code is 2**, use the response from server and update resource in db
        // endif

        String bodyString = "";
        if (!response.isSuccessful()){
            if (response.code() == 403){
                Log.d(LogUtil.getLogTag(this), String.format("http code %d, http response body %s, resource not changed", response.code(), bodyString));
            } else {
                Log.e(LogUtil.getLogTag(this), String.format("http code %d, http response body %s, api is not available", response.code(), bodyString));
            }
            if (cachedResource != null) {
                bodyString = cachedResource.getResponseBody();
                Log.d(LogUtil.getLogTag(this), String.format("using local cache: %s", bodyString));
            }
        }else{
            response.newBuilder().build();

            bodyString = restCache.writeResource(request, response);
        }
        return response.newBuilder()
                .headers(response.headers())
                .body(ResponseBody.create(response.body().contentType(), (bodyString == null || bodyString.isEmpty() ? "null" : bodyString)))
                .build();
    }

    public void setApiToken(String securityDefinitionName, String token) {
        apiTokens.put(securityDefinitionName, token);
    }

    private String getApiTokenHeader(Request request) {
        String operationName = request.header("Operation-Name");
        return apiTokens.get(operationSecurityDefinition.get(operationName));
    }
}