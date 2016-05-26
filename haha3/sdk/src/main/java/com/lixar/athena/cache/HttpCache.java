package com.lixar.athena.cache;

import com.lixar.athena.model.Resource;

import okhttp3.Headers;
import okhttp3.Request;
import okhttp3.Response;

/**
 * Created by pzhou on 2016-05-20.
 */
public interface HttpCache {
    Resource readResource(Request request);
    String writeResource(Request request, Response response);
}