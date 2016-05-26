package com.lixar.athena.cache;


import android.content.Context;
import android.util.Log;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.stmt.DeleteBuilder;
import com.lixar.athena.model.Channel;
import com.lixar.athena.model.Entity;
import com.lixar.athena.model.Resource;
import com.lixar.athena.model.Survey;
import com.lixar.athena.utility.LogUtil;
import com.lixar.athena.utility.MoshiDateTimeAdapter;
import com.squareup.moshi.JsonAdapter;
import com.squareup.moshi.Moshi;

import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import okhttp3.Headers;
import okhttp3.Request;
import okhttp3.Response;

/**
 * Created by pzhou on 2016-05-20.
 */
public class SqliteDbCache implements ModelCache, HttpCache {
    private SqliteDbHelper sqliteDbHelper = null;
    private Context context = null;

    public SqliteDbCache(Context context) {
        this.context = context;
        this.sqliteDbHelper = SqliteDbHelper.getInstance(this.context);
    }

    @Override
    public List<Channel> getChannels() {
        List<Channel> channelsRead = new ArrayList<>();
        SqliteDbHelper dbHelperInstance = SqliteDbHelper.getInstance(context);
        try {
            channelsRead = dbHelperInstance.getChannelDao().queryForAll();
        } catch (SQLException e) {
            Log.e(LogUtil.getLogTag(this), "", e);
        }
        return channelsRead;
    }

    @Override
    public void addUpdateChannels(List<Channel> channels) {
        SqliteDbHelper dbHelperInstance = SqliteDbHelper.getInstance(context);
        for (Channel channel : channels) {
            dbHelperInstance.getWritableDatabase().beginTransaction();
            try {
                if (channel.getStatus() == Channel.Status.DENY_ACCESS.getValue()){
                    DeleteBuilder<Channel, Integer> deleteBuilder = dbHelperInstance.getChannelDao().deleteBuilder();
                    deleteBuilder.where().eq("ChannelId", channel.getChannelId());
                    deleteBuilder.delete();
                }else {
                    dbHelperInstance.getChannelDao().createOrUpdate(channel);
                }
                dbHelperInstance.getWritableDatabase().setTransactionSuccessful();
            } catch (SQLException e) {
                Log.e(LogUtil.getLogTag(this), String.format("createOrUpdate channel failed, channel: %s", channel.toString()), e);
            } finally {
                dbHelperInstance.getWritableDatabase().endTransaction();
            }
        }
    }

    @Override
    public void addUpdateChannel(Channel channel) {
        SqliteDbHelper dbHelperInstance = SqliteDbHelper.getInstance(context);
        try {
            dbHelperInstance.getChannelDao().createOrUpdate(channel);
        } catch (SQLException e) {
            Log.e(LogUtil.getLogTag(this), String.format("channel: %s", channel), e);
        }
    }

    @Override
    public void deleteChannel(Channel channel) {
        SqliteDbHelper dbHelperInstance = SqliteDbHelper.getInstance(context);
        try {
            dbHelperInstance.getChannelDao().delete(channel);
        } catch (SQLException e) {
            Log.e(LogUtil.getLogTag(this), String.format("channel: %s", channel), e);
        }
    }

    @Override
    public void addUpdateSurveys(List<Survey> surveys) {
        SqliteDbHelper dbHelperInstance = SqliteDbHelper.getInstance(context);
        for (Survey survey : surveys) {
            dbHelperInstance.getWritableDatabase().beginTransaction();
            try {
                dbHelperInstance.getSurveyDao().createOrUpdate(survey);
                dbHelperInstance.getWritableDatabase().setTransactionSuccessful();
            } catch (SQLException e) {
                Log.e(LogUtil.getLogTag(this), String.format("createOrUpdate survey failed, survey:%s", survey.toString()), e);
            } finally {
                dbHelperInstance.getWritableDatabase().endTransaction();
            }
        }
    }

    @Override
    public Resource readResource(Request request) {
        Dao<Resource, String> resourceDao = SqliteDbHelper.getInstance(context).getResourceDao();
        Resource cachedResource = null;
        JsonAdapter<Headers> jsonAdapter = new Moshi.Builder()
                .add(new MoshiDateTimeAdapter())
                .build()
                .adapter(Headers.class);

        try {
            if (resourceDao.idExists(request.url().encodedPath())) {
                cachedResource = resourceDao.queryForId(request.url().encodedPath());
                return cachedResource;
            }
        } catch (SQLException e) {
            Log.e(LogUtil.getLogTag(this), "reading cached resource failed", e);
        }
        return null;
    }

    @Override
    public String writeResource(Request request, Response response) {
        Dao<Resource, String> resourceDao = SqliteDbHelper.getInstance(context).getResourceDao();
        JsonAdapter<Headers> jsonAdapter = new Moshi.Builder()
                .add(new MoshiDateTimeAdapter())
                .build()
                .adapter(Headers.class);

        String bodyString = "";
        try {
            bodyString = response.body().string();
            Resource resourceToCache = Resource.create(request.url().encodedPath(),
                    jsonAdapter.toJson(request.headers()),
                    request.body() == null ? "" : request.body().toString(),
                    jsonAdapter.toJson(response.headers()),
                    bodyString,
                    request.method(),
                    response.code(), Entity.class.getName());


            resourceDao.createOrUpdate(resourceToCache);

            Log.d(LogUtil.getLogTag(this), String.format("caching resource succeeded: %s", resourceToCache));
        } catch (SQLException e) {
            Log.e(LogUtil.getLogTag(this), " caching resource failed", e);
        } catch (IOException e) {
            Log.e(LogUtil.getLogTag(this), "caching resource failed", e);
        }
        return bodyString;
    }
}