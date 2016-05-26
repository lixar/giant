package com.lixar.athena.model;/*
 *
 * ModelErrorResponse
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



public class ModelErrorResponse extends Entity{

    @Json(name = "ModelState")
    private ModelErrorResponseState modelState;

    @Json(name = "Message")
    private String message;

    public ModelErrorResponseState getModelState() {
        return modelState;
    }

    public String getMessage() {
        return message;
    }

    public void setModelState(ModelErrorResponseState modelState) {
        this.modelState = modelState;
    }

    public void setMessage(String message) {
        this.message = message;
    }

}
