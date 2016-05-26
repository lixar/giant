package com.lixar.athena.utility;

import com.squareup.moshi.FromJson;
import com.squareup.moshi.ToJson;

import org.threeten.bp.OffsetDateTime;

public class MoshiDateTimeAdapter {

    @ToJson
    String toJson(OffsetDateTime dateTime) {
        return dateTime.toString();
    }

    @FromJson
    OffsetDateTime fromJson(String dateTime) {
        return OffsetDateTime.parse(dateTime);
    }
}