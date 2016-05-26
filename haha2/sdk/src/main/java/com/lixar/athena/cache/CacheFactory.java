package com.lixar.athena.cache;


import android.content.Context;

/**
 * Created by pzhou on 2016-05-20.
 */
public class CacheFactory {
    public enum CacheStorage{
        SQLITE,
        REALM
    }
    public static HttpCache getRestCache(CacheStorage cacheStorage, Context context){

        if(cacheStorage == CacheStorage.SQLITE){
            return new SqliteDbCache(context);
        }

        return null;
    }

    public static ModelCache getModelCache(CacheStorage cacheStorage, Context context){

        if(cacheStorage == CacheStorage.SQLITE){
            return new SqliteDbCache(context);
        }

        return null;
    }
}