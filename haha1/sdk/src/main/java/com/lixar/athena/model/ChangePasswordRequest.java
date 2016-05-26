package com.lixar.athena.model;/*
 *
 * ChangePasswordRequest
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



public class ChangePasswordRequest extends Entity{

    @Json(name = "NewPassword")
    private String newPassword;

    @Json(name = "OldPassword")
    private String oldPassword;

    @Json(name = "ConfirmPassword")
    private String confirmPassword;

    public String getNewPassword() {
        return newPassword;
    }

    public String getOldPassword() {
        return oldPassword;
    }

    public String getConfirmPassword() {
        return confirmPassword;
    }

    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }

    public void setOldPassword(String oldPassword) {
        this.oldPassword = oldPassword;
    }

    public void setConfirmPassword(String confirmPassword) {
        this.confirmPassword = confirmPassword;
    }

}
