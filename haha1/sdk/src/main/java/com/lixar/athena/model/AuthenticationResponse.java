package com.lixar.athena.model;/*
 *
 * AuthenticationResponse
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

public class AuthenticationResponse extends Entity{

    @DatabaseField(canBeNull = false )
    @Json(name = "userName")
    private String userName;

    @DatabaseField(canBeNull = false )
    @Json(name = "token_type")
    private String tokenType;

    @DatabaseField(canBeNull = false , dataType = DataType.SERIALIZABLE)
    @Json(name = ".expires")
    private OffsetDateTime expires;

    @DatabaseField(canBeNull = false )
    @Json(name = "access_token")
    private String accessToken;

    @DatabaseField(canBeNull = false , dataType = DataType.SERIALIZABLE)
    @Json(name = ".issued")
    private OffsetDateTime issued;

    @DatabaseField(canBeNull = false )
    @Json(name = "expires_in")
    private Long expiresIn;

    public String getUserName() {
        return userName;
    }

    public String getTokenType() {
        return tokenType;
    }

    public OffsetDateTime getExpires() {
        return expires;
    }

    public String getAccessToken() {
        return accessToken;
    }

    public OffsetDateTime getIssued() {
        return issued;
    }

    public Long getExpiresIn() {
        return expiresIn;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public void setTokenType(String tokenType) {
        this.tokenType = tokenType;
    }

    public void setExpires(OffsetDateTime expires) {
        this.expires = expires;
    }

    public void setAccessToken(String accessToken) {
        this.accessToken = accessToken;
    }

    public void setIssued(OffsetDateTime issued) {
        this.issued = issued;
    }

    public void setExpiresIn(Long expiresIn) {
        this.expiresIn = expiresIn;
    }

}
