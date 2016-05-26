package com.lixar.athena.model;/*
 *
 * SurveyQuestion
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

public class SurveyQuestion extends Entity{

    @DatabaseField(canBeNull = false )
    @Json(name = "Topic")
    private String topic;

    @DatabaseField(canBeNull = false )
    @Json(name = "QuestionId")
    private Integer questionId;

    @DatabaseField(canBeNull = false )
    @Json(name = "Position")
    private Integer position;

    @DatabaseField(canBeNull = false , dataType = DataType.SERIALIZABLE)
    @Json(name = "Metadata")
    private SurveyQuestionMetadata metadata;

    @DatabaseField(canBeNull = false ,foreign = true)
    private Survey survey;

    public String getTopic() {
        return topic;
    }

    public Integer getQuestionId() {
        return questionId;
    }

    public Integer getPosition() {
        return position;
    }

    public SurveyQuestionMetadata getMetadata() {
        return metadata;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }

    public void setQuestionId(Integer questionId) {
        this.questionId = questionId;
    }

    public void setPosition(Integer position) {
        this.position = position;
    }

    public void setMetadata(SurveyQuestionMetadata metadata) {
        this.metadata = metadata;
    }

}
