package com.lixar.athena.operation;

import retrofit2.Call;
import retrofit2.http.*;
import org.threeten.bp.OffsetDateTime;
import java.util.List;
import com.lixar.athena.model.*;

public interface SurveysService {

    @Headers("Operation-Name: getSurveys")
    @GET("/api/v1/surveys")
    Call<List<Survey>> getSurveys(@Query("whenModified") OffsetDateTime whenModified, @Header("Accept-Language") String acceptLanguage);

    @Headers("Operation-Name: submitSurveyAnswers")
    @POST("/api/v1/answers")
    Call<Void> submitSurveyAnswers(@Body SurveyAnswersRequest answers);

    @Headers("Operation-Name: getChannels")
    @GET("/api/v1/channels")
    Call<List<Channel>> getChannels(@Query("exclude") List<Integer> exclude, @Query("whenModified") OffsetDateTime whenModified);

    @Headers("Operation-Name: subscribeToChannel")
    @PUT("/api/v1/channels/{channelId}")
    Call<Void> subscribeToChannel(@Path("channelId") Integer channelId, @Body SubscribeStatusRequest subscribeState);

}
