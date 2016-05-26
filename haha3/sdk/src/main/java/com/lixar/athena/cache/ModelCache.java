package com.lixar.athena.cache;


import com.lixar.athena.model.Channel;
import com.lixar.athena.model.Survey;

import java.util.List;

/**
 * Created by pzhou on 2016-05-20.
 */
public interface ModelCache {
    List<Channel> getChannels();
    void addUpdateChannels(List<Channel> channels);
    void addUpdateChannel(Channel channel);
    void deleteChannel(Channel channel);
    void addUpdateSurveys(List<Survey> surveys);
}