package com.lixar.athena.model;/*
 *
 * Channel
 *
 * This file is GENERATED code.
 *
 * Do not edit code contained in this file.
 * Instead add code as a class extension externally, or edit the template files
 * that produce this file.
 *
 * Do not check this code into source control.
 * Instead, add / update you build script that will regenerate this library.
 *
 * Copyright 2015 (c) Lixar I.T. Inc.
 */

import com.squareup.moshi.Json;

import org.threeten.bp.OffsetDateTime;

import java.util.List;

import com.j256.ormlite.field.DataType;
import com.j256.ormlite.field.DatabaseField;
import com.j256.ormlite.table.DatabaseTable;
import com.j256.ormlite.dao.ForeignCollection;
import com.j256.ormlite.field.ForeignCollectionField;

public class Channel extends Entity{
    public enum Status{
        DENY_ACCESS(0),
        ALLOW_ACCESS(1),
        MODIFIED(2);

        private final int value;

        Status(final int newValue) {
            value = newValue;
        }

        public int getValue() { return value; }
    }
    public enum Privacy{
        PRIVATE(0),
        PUBLIC(1);

        private final int value;

        Privacy(final int newValue) {
            value = newValue;
        }

        public int getValue() { return value; }
    }

    @DatabaseField(canBeNull = false )
    @Json(name = "Status")
    private Integer status;

    @DatabaseField(canBeNull = false )
    @Json(name = "Name")
    private String name;

    @DatabaseField(canBeNull = false )
    @Json(name = "Subscribed")
    private Boolean subscribed;

    @DatabaseField(canBeNull = false )
    @Json(name = "Privacy")
    private Integer privacy;

    @DatabaseField(canBeNull = false )
    @Json(name = "ChannelId")
    private Integer channelId;

    @DatabaseField(canBeNull = false )
    @Json(name = "Description")
    private String description;

    public Integer getStatus() {
        return status;
    }

    public String getName() {
        return name;
    }

    public Boolean getSubscribed() {
        return subscribed;
    }

    public Integer getPrivacy() {
        return privacy;
    }

    public Integer getChannelId() {
        return channelId;
    }

    public String getDescription() {
        return description;
    }

    public void setStatus(Integer status) {
        this.status = status;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setSubscribed(Boolean subscribed) {
        this.subscribed = subscribed;
    }

    public void setPrivacy(Integer privacy) {
        this.privacy = privacy;
    }

    public void setChannelId(Integer channelId) {
        this.channelId = channelId;
    }

    public void setDescription(String description) {
        this.description = description;
    }

}
