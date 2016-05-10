//
//  NSDate+ISO8601.m
//  Project
//
//  Created by Sandy Chapman on 5/9/16.
//
//

#import "NSDate+ISO8601.h"

@implementation NSDate (ISO8601)

- (NSString*)iso8601
{
  NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
  NSLocale *enUSPOSIXLocale = [NSLocale localeWithLocaleIdentifier:@"en_US_POSIX"];
  [dateFormatter setLocale:enUSPOSIXLocale];
  [dateFormatter setDateFormat:@"yyyy-MM-dd'T'HH:mm:ssZZZZZ"];
  
  NSDate *now = [NSDate date];
  NSString *iso8601String = [dateFormatter stringFromDate:now];
  return iso8601String;
}

@end
