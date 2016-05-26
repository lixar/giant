package com.lixar.athena;

import android.util.Log;

import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;
import com.lixar.athena.model.Channel;
import com.lixar.athena.utility.LogUtil;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.util.List;
import java.util.concurrent.CountDownLatch;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertNotNull;

/**
 * Created by pzhou on 2016-05-16.
 */
public class AthenaTest extends TestCase {

    @Before
    public void setUp() throws Exception{
        super.setUp();
        endSignal = new CountDownLatch(1);
    }
    @After
    public void tearDown() throws Exception {
        super.tearDown();
    }
    @Test
    public void testGetChannelAsync() throws Exception{
        final Channel[] channels = new Channel[]{null};

        ListenableFuture<Channel> future = athena.getChannelAsync(1);
        Futures.addCallback(future, new FutureCallback<Channel>() {
            @Override
            public void onSuccess(Channel result) {
                channels[0] = result;
                endSignal.countDown();
            }

            @Override
            public void onFailure(Throwable t) {
                Log.e(LogUtil.getLogTag(AthenaTest.this), "", t);

                endSignal.countDown();
            }
        });

        endSignal.await();
        assertNotNull(channels[0]);
        assertEquals(channels[0].getChannelId().intValue(), 1);

    }
    @Test
    public void testGetUnsubscribedChannelsAsync() throws Exception{
        final List<Channel>[] channels = new List[]{null};
        ListenableFuture<List<Channel>> future = athena.getUnsubscribedChannelsAsync();
        Futures.addCallback(future, new FutureCallback<List<Channel>>() {
            @Override
            public void onSuccess(List<Channel> result) {
                channels[0] = result;
                endSignal.countDown();
            }

            @Override
            public void onFailure(Throwable t) {
                Log.e(LogUtil.getLogTag(AthenaTest.this), "", t);

                endSignal.countDown();
            }
        });

        endSignal.await();
        assertEquals(channels[0].size(), 1);
        assertEquals(athena.modelCache.getChannels().size(), 1);
    }

    @Test
    public void testGetSubscribedChannelsAsync() throws Exception{
        final List<Channel>[] channels = new List[]{null};
        ListenableFuture<List<Channel>> future = athena.getSubscribedChannelsAsync();
        Futures.addCallback(future, new FutureCallback<List<Channel>>() {
            @Override
            public void onSuccess(List<Channel> result) {
                channels[0] = result;
                endSignal.countDown();
            }

            @Override
            public void onFailure(Throwable t) {
                Log.e(LogUtil.getLogTag(AthenaTest.this), "", t);

                endSignal.countDown();
            }
        });

        endSignal.await();
        assertEquals(channels[0].size(), 1);
        assertEquals(athena.modelCache.getChannels().size(), 1);
    }

    @Test
    public void testGetChannelsAsync() throws Exception{
        final List<Channel>[] channels = new List[]{null};
        ListenableFuture<List<Channel>> future = athena.getChannelsAsync();
        Futures.addCallback(future, new FutureCallback<List<Channel>>() {
            @Override
            public void onSuccess(List<Channel> result) {
                channels[0] = result;
                endSignal.countDown();
            }

            @Override
            public void onFailure(Throwable t) {
                Log.e(LogUtil.getLogTag(AthenaTest.this), "", t);

                endSignal.countDown();
            }
        });

        endSignal.await();
        assertEquals(channels[0].size(), 2);
        assertEquals(athena.modelCache.getChannels().size(), 1);
    }

    @Test
    public void testSubscribeAsync() throws Exception{
        final Channel[] channels = new Channel[]{null};
        final Boolean[] subscribeResults = new Boolean[]{false};
        ListenableFuture<Channel> future = athena.getChannelAsync(1);
        Futures.addCallback(future, new FutureCallback<Channel>() {
            @Override
            public void onSuccess(Channel result) {
                channels[0] = result;
                endSignal.countDown();
            }

            @Override
            public void onFailure(Throwable t) {
                Log.e(LogUtil.getLogTag(AthenaTest.this), "", t);

                endSignal.countDown();
            }
        });

        endSignal.await();
        assertNotNull(channels[0]);


        endSignal = new CountDownLatch(1);
        ListenableFuture<Boolean> futureSubscribe = athena.subscribeToChannelAsync(channels[0]);
        Futures.addCallback(futureSubscribe, new FutureCallback<Boolean>() {
            @Override
            public void onSuccess(Boolean result) {
                subscribeResults[0] = result;
                endSignal.countDown();
            }

            @Override
            public void onFailure(Throwable t) {
                Log.e(LogUtil.getLogTag(AthenaTest.this), "", t);

                endSignal.countDown();
            }
        });

        endSignal.await();
        assertEquals(subscribeResults[0], true);
        assertEquals(athena.modelCache.getChannels().size(), 2);
    }

    @Test
    public void testUnsubscribeAsync() throws Exception{
        final Channel[] channels = new Channel[]{null};
        final Boolean[] subscribeResults = new Boolean[]{false};
        ListenableFuture<Channel> future = athena.getChannelAsync(2);
        Futures.addCallback(future, new FutureCallback<Channel>() {
            @Override
            public void onSuccess(Channel result) {
                channels[0] = result;
                endSignal.countDown();
            }

            @Override
            public void onFailure(Throwable t) {
                Log.e(LogUtil.getLogTag(AthenaTest.this), "", t);

                endSignal.countDown();
            }
        });

        endSignal.await();
        assertNotNull(channels[0]);


        endSignal = new CountDownLatch(1);
        ListenableFuture<Boolean> futureSubscribe = athena.unsubscribeToChannelAsync(channels[0]);
        Futures.addCallback(futureSubscribe, new FutureCallback<Boolean>() {
            @Override
            public void onSuccess(Boolean result) {
                subscribeResults[0] = result;
                endSignal.countDown();
            }

            @Override
            public void onFailure(Throwable t) {
                Log.e(LogUtil.getLogTag(AthenaTest.this), "", t);

                endSignal.countDown();
            }
        });

        endSignal.await();
        assertEquals(subscribeResults[0], true);
        assertEquals(athena.modelCache.getChannels().size(), 0);
    }
}