package com.lixar.athena.model;/*
 *
 * SurveyQuestionMetadata
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



public class SurveyQuestionMetadata extends Entity{

    @Json(name = "Size")
    private Integer size;

    @Json(name = "Values")
    private List<String> values;

    @Json(name = "Placeholders")
    private List<String> placeholders;

    @Json(name = "Labels")
    private List<String> labels;

    @Json(name = "Type")
    private Integer type;

    @Json(name = "MaxValue")
    private Integer maxValue;

    @Json(name = "MinValue")
    private Integer minValue;

    public Integer getSize() {
        return size;
    }

    public List<String> getValues() {
        return values;
    }

    public List<String> getPlaceholders() {
        return placeholders;
    }

    public List<String> getLabels() {
        return labels;
    }

    public Integer getType() {
        return type;
    }

    public Integer getMaxValue() {
        return maxValue;
    }

    public Integer getMinValue() {
        return minValue;
    }

    public void setSize(Integer size) {
        this.size = size;
    }

    public void setValues(List<String> values) {
        this.values = values;
    }

    public void setPlaceholders(List<String> placeholders) {
        this.placeholders = placeholders;
    }

    public void setLabels(List<String> labels) {
        this.labels = labels;
    }

    public void setType(Integer type) {
        this.type = type;
    }

    public void setMaxValue(Integer maxValue) {
        this.maxValue = maxValue;
    }

    public void setMinValue(Integer minValue) {
        this.minValue = minValue;
    }

}
