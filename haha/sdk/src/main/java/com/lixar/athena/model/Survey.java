package com.lixar.athena.model;/*
 *
 * Survey
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

public class Survey extends Entity{

    @DatabaseField(canBeNull = false )
    @Json(name = "Privacy")
    private Integer privacy;

    @DatabaseField(canBeNull = false )
    @Json(name = "ChannelId")
    private Integer channelId;

    @DatabaseField(canBeNull = false , dataType = DataType.SERIALIZABLE)
    @Json(name = "ExpiryDate")
    private OffsetDateTime expiryDate;

    @DatabaseField(canBeNull = false )
    @Json(name = "Topic")
    private String topic;

    @DatabaseField(canBeNull = false )
    @Json(name = "SurveyId")
    private Integer surveyId;

    @DatabaseField(canBeNull = false )
    @Json(name = "SurveySessionId")
    private Integer surveySessionId;

    @DatabaseField(canBeNull = false )
    @Json(name = "Points")
    private Integer points;

    @ForeignCollectionField(eager = false)
    @Json(name = "Questions")
    private ForeignCollection<SurveyQuestion> questions;

    public Integer getPrivacy() {
        return privacy;
    }

    public Integer getChannelId() {
        return channelId;
    }

    public OffsetDateTime getExpiryDate() {
        return expiryDate;
    }

    public String getTopic() {
        return topic;
    }

    public Integer getSurveyId() {
        return surveyId;
    }

    public Integer getSurveySessionId() {
        return surveySessionId;
    }

    public Integer getPoints() {
        return points;
    }

    public ForeignCollection<SurveyQuestion> getQuestions() {
        return questions;
    }

    public void setPrivacy(Integer privacy) {
        this.privacy = privacy;
    }

    public void setChannelId(Integer channelId) {
        this.channelId = channelId;
    }

    public void setExpiryDate(OffsetDateTime expiryDate) {
        this.expiryDate = expiryDate;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }

    public void setSurveyId(Integer surveyId) {
        this.surveyId = surveyId;
    }

    public void setSurveySessionId(Integer surveySessionId) {
        this.surveySessionId = surveySessionId;
    }

    public void setPoints(Integer points) {
        this.points = points;
    }

    public void setQuestions(ForeignCollection<SurveyQuestion>  questions) {
        this.questions = questions;
    }

}
