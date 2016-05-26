package com.lixar.athena;

import android.content.Context;
import android.support.v7.appcompat.BuildConfig;
import android.util.Log;

import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;
import com.lixar.athena.cache.SqliteDbHelper;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.mockito.MockitoAnnotations;
import org.robolectric.RobolectricGradleTestRunner;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.annotation.Config;
import org.robolectric.shadows.ShadowLog;

import java.util.concurrent.CountDownLatch;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertNotNull;

/**
 * Base class for Robolectric rest tests.
 * Inherit from this class to create a test.
 */
@RunWith(RobolectricGradleTestRunner.class)
@Config(
        packageName = "com.lixar.athena",
        constants = BuildConfig.class, sdk=21
)
public abstract class TestCase {
    private final static String TAG = "RestTest";
    protected Context fakeContext;
    protected CountDownLatch endSignal;

    Athena athena;

    @After
    public void tearDown() throws Exception {

        SqliteDbHelper.releaseInstance();
    }

    @Before
    public void setUp() throws Exception{
        MockitoAnnotations.initMocks(this);
        ShadowLog.stream = System.out;
        fakeContext = RuntimeEnvironment.application.getApplicationContext();
        final CountDownLatch loginEndSignal = new CountDownLatch(1);

        ListenableFuture<Athena> future = new Athena.Builder()
                .withContext(fakeContext)
                .withApiKey("test")
                .withClientIdentifier("test")
                .withUrl("http://localhost:10010/")
                .buildAsync();

        Futures.addCallback(future, new FutureCallback<Athena>() {
            @Override
            public void onSuccess(Athena result) {
                athena = result;

                loginEndSignal.countDown();
            }

            @Override
            public void onFailure(Throwable t) {
                Log.e(TAG, "", t);
                athena = null;
                loginEndSignal.countDown();

            }
        });

        loginEndSignal.await();
        assertNotNull(athena);

    }


}