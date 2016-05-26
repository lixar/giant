package com.lixar.athena.model;/*
 *
 * SurveyAnswer
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



public class SurveyAnswer extends Entity{

    @Json(name = "QuestionId")
    private Integer questionId;

    @Json(name = "WhenCreated")
    private OffsetDateTime whenCreated;

    @Json(name = "ResponseSet")
    private List<SurveyAnswerResponseSet> responseSet;

    @Json(name = "Response")
    private String response;

    @Json(name = "ResponseType")
    private Integer responseType;

    public Integer getQuestionId() {
        return questionId;
    }

    public OffsetDateTime getWhenCreated() {
        return whenCreated;
    }

    public List<SurveyAnswerResponseSet> getResponseSet() {
        return responseSet;
    }

    public String getResponse() {
        return response;
    }

    public Integer getResponseType() {
        return responseType;
    }

    public void setQuestionId(Integer questionId) {
        this.questionId = questionId;
    }

    public void setWhenCreated(OffsetDateTime whenCreated) {
        this.whenCreated = whenCreated;
    }

    public void setResponseSet(List<SurveyAnswerResponseSet> responseSet) {
        this.responseSet = responseSet;
    }

    public void setResponse(String response) {
        this.response = response;
    }

    public void setResponseType(Integer responseType) {
        this.responseType = responseType;
    }

}
