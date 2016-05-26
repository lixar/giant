package com.lixar.athena.model;/*
 *
 * SubscribeStatusRequest
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



public class SubscribeStatusRequest extends Entity{
    public enum Subscribed{
        UNSUBSCRIBE(0),
        SUBSCRIBE(1);

        private final int value;

        Subscribed(final int newValue) {
            value = newValue;
        }

        public int getValue() { return value; }
    }

    @Json(name = "Subscribed")
    private Integer subscribed;

    public Integer getSubscribed() {
        return subscribed;
    }

    public void setSubscribed(Integer subscribed) {
        this.subscribed = subscribed;
    }

}
