package com.lixar.athena.operation;

import retrofit2.Call;
import retrofit2.http.*;
import org.threeten.bp.OffsetDateTime;
import java.util.List;
import com.lixar.athena.model.*;

public interface AccountsService {

    @Headers("Operation-Name: acceptPrivacyPolicy")
    @PUT("/api/v1/account/acceptPolicy")
    Call<Void> acceptPrivacyPolicy();

    @Headers("Operation-Name: logout")
    @POST("/api/v1/account/logout")
    Call<Void> logout();

    @Headers("Operation-Name: resetPassword")
    @PUT("/api/v1/account/reset")
    Call<Void> resetPassword(@Body ResetPasswordRequest emailInfo);

    @Headers("Operation-Name: changePassword")
    @POST("/api/v1/account/changePassword")
    Call<Void> changePassword(@Body ChangePasswordRequest request);

    @Headers("Operation-Name: getUserInfo")
    @GET("/api/v1/account/userinfo")
    Call<UserInfoResponse> getUserInfo();

    @Headers("Operation-Name: apikey")
    @FormUrlEncoded
    @POST("/apikey")
    Call<AuthenticationResponse> apikey(@Field("apiKey") String apiKey, @Field("clientId") String clientId);

    @Headers("Operation-Name: login")
    @FormUrlEncoded
    @POST("/token")
    Call<AuthenticationResponse> login(@Field("grant_type") String grant_type, @Field("username") String username, @Field("password") String password);

    @Headers("Operation-Name: registerNewUser")
    @POST("/api/v1/account/register")
    Call<Void> registerNewUser(@Body RegisterUserRequest RegistrationInfo);

}
