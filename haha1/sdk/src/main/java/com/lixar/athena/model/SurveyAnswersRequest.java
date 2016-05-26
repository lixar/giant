package com.lixar.athena.model;/*
 *
 * SurveyAnswersRequest
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



public class SurveyAnswersRequest extends Entity{

    @Json(name = "SurveySessionId")
    private Integer surveySessionId;

    @Json(name = "ChannelId")
    private Integer channelId;

    @Json(name = "Answers")
    private List<SurveyAnswer> answers;

    public Integer getSurveySessionId() {
        return surveySessionId;
    }

    public Integer getChannelId() {
        return channelId;
    }

    public List<SurveyAnswer> getAnswers() {
        return answers;
    }

    public void setSurveySessionId(Integer surveySessionId) {
        this.surveySessionId = surveySessionId;
    }

    public void setChannelId(Integer channelId) {
        this.channelId = channelId;
    }

    public void setAnswers(List<SurveyAnswer> answers) {
        this.answers = answers;
    }

}
