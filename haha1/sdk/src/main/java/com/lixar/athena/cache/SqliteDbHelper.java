package com.lixar.athena.cache;


import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

import com.j256.ormlite.android.apptools.OpenHelperManager;
import com.j256.ormlite.android.apptools.OrmLiteSqliteOpenHelper;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.table.TableUtils;
import com.lixar.athena.model.Channel;
import com.lixar.athena.model.Resource;
import com.lixar.athena.model.Survey;
import com.lixar.athena.utility.LogUtil;

import java.sql.SQLException;

/**
 * Created by pzhou on 2016-05-19.
 */
final public class SqliteDbHelper extends OrmLiteSqliteOpenHelper {
    private static SqliteDbHelper instance = null;



    public static void releaseInstance(){
        if (instance != null) {
            OpenHelperManager.releaseHelper();
            instance = null;
        }
    }
    public static SqliteDbHelper getInstance(Context context) {
        if (instance == null){
            instance = new SqliteDbHelper(context);
        }
        return instance;
    }
    public static final String DATABASE_NAME = "com.lixar.athena.db";
    // any time you make changes to your database objects, you may have to increase the database version
    public static final int DATABASE_VERSION = 1;

    // the DAO object we use to access  tables
    private Dao<Resource, String> resourceDao = null;
    private Dao<Channel, Integer> channelDao = null;
    private Dao<Survey, Integer> surveyDao = null;

    private Context context;

    private SqliteDbHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
        this.context = context;
    }

    /**
     * This is called when the database is first created. Usually you should call createTable statements here to create
     * the tables that will store your data.
     */
    @Override
    public void onCreate(SQLiteDatabase db, ConnectionSource connectionSource) {
        try {
            Log.i(LogUtil.getLogTag(this), "onCreate");

            TableUtils.createTable(connectionSource, Resource.class);
            TableUtils.createTable(connectionSource, Channel.class);
            TableUtils.createTable(connectionSource, Survey.class);

        } catch (SQLException e) {
            Log.e(LogUtil.getLogTag(this),  "Can't create database");
            throw new RuntimeException(e);
        }

    }

    /**
     * This is called when your application is upgraded and it has a higher version number. This allows you to adjust
     * the various data to match the new version number.
     */
    @Override
    public void onUpgrade(SQLiteDatabase db, ConnectionSource connectionSource, int oldVersion, int newVersion) {
        try {
            Log.i(LogUtil.getLogTag(this), "onUpgrade");
            //DbUpgradeHelper.upgradeFromTo(db, context, "db_upgrade_scripts.txt", oldVersion, newVersion);

        } catch (Exception e) {
            Log.e(LogUtil.getLogTag(this), "Can't drop databases", e);
            throw new RuntimeException(e);
        }
    }


    public Dao<Resource, String> getResourceDao() {
        if (resourceDao == null) {
            try {
                resourceDao = getDao(Resource.class);
            }catch (SQLException e) {
                Log.e(LogUtil.getLogTag(this),  "Getting Resource Dao failed", e);
                throw new RuntimeException(e);
            }

        }
        return resourceDao;
    }

    public Dao<Channel, Integer> getChannelDao() {
        if (channelDao == null) {
            try {
                channelDao = getDao(Channel.class);
            }catch (SQLException e) {
                Log.e(LogUtil.getLogTag(this),  "Getting Resource Dao failed", e);
                throw new RuntimeException(e);
            }

        }
        return channelDao;
    }

    public Dao<Survey, Integer> getSurveyDao() {
        if (surveyDao == null) {
            try {
                surveyDao = getDao(Survey.class);
            }catch (SQLException e) {
                Log.e(LogUtil.getLogTag(this),  "Getting Resource Dao failed", e);
                throw new RuntimeException(e);
            }

        }
        return surveyDao;
    }



    /**
     * Close the database connections and clear any cached DAOs.
     */
    @Override
    public void close() {
        super.close();
        resourceDao = null;
        surveyDao = null;
        channelDao =  null;
    }


}