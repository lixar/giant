package com.lixar.athena.utility;

/**
 * Created by pzhou on 2016-05-20.
 */
public class LogUtil {
    static public String getLogTag(Object obj)
    {

        String stringToParse = obj.getClass().toString();
        int lastDotIndex = stringToParse.lastIndexOf(".");

        String className = stringToParse.substring(lastDotIndex + 1);

        stringToParse = stringToParse.substring(0, lastDotIndex );

        //find the product name
        String productName = stringToParse.substring(stringToParse.indexOf(".") + 1);
        productName = productName.substring(productName.indexOf(".") + 1);

        StackTraceElement[] stacktrace = Thread.currentThread().getStackTrace();
        boolean foundMe = false;
        String callingMethodName = "";
        for(int i=0; i <stacktrace.length; i++) {
            StackTraceElement e = stacktrace[i];

            if (foundMe) {
                callingMethodName = e.getMethodName();
                break;
            } else {
                if (e.getMethodName().equals("getLogTag")) {
                    foundMe = true;
                }
            }

        }
        return productName + "." + className + "." + callingMethodName + "[" + Thread.currentThread().getName() + "]";

    }
}