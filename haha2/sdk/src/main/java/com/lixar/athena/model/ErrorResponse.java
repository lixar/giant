package com.lixar.athena.model;/*
 *
 * ErrorResponse
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



public class ErrorResponse extends Entity{

    @Json(name = "error_description")
    private String errorDescription;

    @Json(name = "error")
    private String error;

    public String getErrorDescription() {
        return errorDescription;
    }

    public String getError() {
        return error;
    }

    public void setErrorDescription(String errorDescription) {
        this.errorDescription = errorDescription;
    }

    public void setError(String error) {
        this.error = error;
    }

}
