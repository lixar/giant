package com.lixar.athena.model;/*
 *
 * UserInfoResponse
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

public class UserInfoResponse extends Entity{

    @DatabaseField(canBeNull = false )
    @Json(name = "LoginProvider")
    private String loginProvider;

    @DatabaseField(canBeNull = false )
    @Json(name = "Points")
    private Integer points;

    @DatabaseField(canBeNull = false )
    @Json(name = "Email")
    private String email;

    @DatabaseField(canBeNull = false )
    @Json(name = "HasRegistered")
    private String hasRegistered;

    public String getLoginProvider() {
        return loginProvider;
    }

    public Integer getPoints() {
        return points;
    }

    public String getEmail() {
        return email;
    }

    public String getHasRegistered() {
        return hasRegistered;
    }

    public void setLoginProvider(String loginProvider) {
        this.loginProvider = loginProvider;
    }

    public void setPoints(Integer points) {
        this.points = points;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setHasRegistered(String hasRegistered) {
        this.hasRegistered = hasRegistered;
    }

}
