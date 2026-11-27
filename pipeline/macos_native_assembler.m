#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
#import <AppKit/AppKit.h>
#import <CoreVideo/CoreVideo.h>

// Creates CVPixelBuffer from CGImageRef scaled and centered to target width/height
CVPixelBufferRef CreatePixelBufferFromImage(CGImageRef image, int targetWidth, int targetHeight) {
    NSDictionary *options = @{
        (id)kCVPixelBufferCGImageCompatibilityKey: @YES,
        (id)kCVPixelBufferCGBitmapContextCompatibilityKey: @YES
    };
    CVPixelBufferRef pixelBuffer = NULL;
    CVReturn status = CVPixelBufferCreate(kCFAllocatorDefault,
                                          targetWidth,
                                          targetHeight,
                                          kCVPixelFormatType_32ARGB,
                                          (__bridge CFDictionaryRef)options,
                                          &pixelBuffer);
    if (status != kCVReturnSuccess || pixelBuffer == NULL) {
        return NULL;
    }

    CVPixelBufferLockBaseAddress(pixelBuffer, 0);
    void *pixelData = CVPixelBufferGetBaseAddress(pixelBuffer);
    CGColorSpaceRef rgbColorSpace = CGColorSpaceCreateDeviceRGB();
    CGContextRef context = CGBitmapContextCreate(pixelData,
                                                 targetWidth,
                                                 targetHeight,
                                                 8,
                                                 CVPixelBufferGetBytesPerRow(pixelBuffer),
                                                 rgbColorSpace,
                                                 kCGImageAlphaNoneSkipFirst);

    // Fill background with black
    CGContextSetRGBFillColor(context, 0.0, 0.0, 0.0, 1.0);
    CGContextFillRect(context, CGRectMake(0, 0, targetWidth, targetHeight));

    // Calculate aspect fill / fit
    CGFloat imgW = CGImageGetWidth(image);
    CGFloat imgH = CGImageGetHeight(image);
    CGFloat scale = MAX((CGFloat)targetWidth / imgW, (CGFloat)targetHeight / imgH);
    CGFloat drawW = imgW * scale;
    CGFloat drawH = imgH * scale;
    CGFloat drawX = ((CGFloat)targetWidth - drawW) / 2.0;
    CGFloat drawY = ((CGFloat)targetHeight - drawH) / 2.0;

    CGContextDrawImage(context, CGRectMake(drawX, drawY, drawW, drawH), image);

    CGColorSpaceRelease(rgbColorSpace);
    CGContextRelease(context);
    CVPixelBufferUnlockBaseAddress(pixelBuffer, 0);

    return pixelBuffer;
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSUserDefaults *args = [NSUserDefaults standardUserDefaults];
        NSString *shotsFile = [args stringForKey:@"shots"];
        NSString *audioFile = [args stringForKey:@"audio"];
        NSString *outputFile = [args stringForKey:@"output"];
        int width = [args integerForKey:@"width"] ? (int)[args integerForKey:@"width"] : 1920;
        int height = [args integerForKey:@"height"] ? (int)[args integerForKey:@"height"] : 1080;
        int fps = [args integerForKey:@"fps"] ? (int)[args integerForKey:@"fps"] : 24;

        if (!shotsFile || !outputFile) {
            fprintf(stderr, "Usage: macos_native_assembler -shots <shots.json> -output <output.mp4> [-audio <audio.wav>] [-width 1920] [-height 1080] [-fps 24]\n");
            return 1;
        }

        NSError *err = nil;
        NSData *jsonData = [NSData dataWithContentsOfFile:shotsFile];
        if (!jsonData) {
            fprintf(stderr, "Cannot read shots file: %s\n", [shotsFile UTF8String]);
            return 1;
        }
        NSArray *shots = [NSJSONSerialization JSONObjectWithData:jsonData options:0 error:&err];
        if (!shots) {
            fprintf(stderr, "Invalid JSON in shots file: %s\n", [[err localizedDescription] UTF8String]);
            return 1;
        }

        NSURL *outputURL = [NSURL fileURLWithPath:outputFile];
        [[NSFileManager defaultManager] removeItemAtURL:outputURL error:nil];

        AVAssetWriter *writer = [AVAssetWriter assetWriterWithURL:outputURL fileType:AVFileTypeMPEG4 error:&err];
        if (!writer) {
            fprintf(stderr, "Cannot create AVAssetWriter: %s\n", [[err localizedDescription] UTF8String]);
            return 1;
        }

        NSDictionary *videoSettings = @{
            AVVideoCodecKey: AVVideoCodecTypeH264,
            AVVideoWidthKey: @(width),
            AVVideoHeightKey: @(height),
            AVVideoCompressionPropertiesKey: @{
                AVVideoAverageBitRateKey: @(width > 1200 ? 5000000 : 3000000),
                AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel
            }
        };

        AVAssetWriterInput *videoInput = [AVAssetWriterInput assetWriterInputWithMediaType:AVMediaTypeVideo outputSettings:videoSettings];
        videoInput.expectsMediaDataInRealTime = NO;

        NSDictionary *sourceBufferAttributes = @{
            (id)kCVPixelBufferPixelFormatTypeKey: @(kCVPixelFormatType_32ARGB),
            (id)kCVPixelBufferWidthKey: @(width),
            (id)kCVPixelBufferHeightKey: @(height)
        };
        AVAssetWriterInputPixelBufferAdaptor *adaptor = [AVAssetWriterInputPixelBufferAdaptor assetWriterInputPixelBufferAdaptorWithAssetWriterInput:videoInput sourcePixelBufferAttributes:sourceBufferAttributes];

        if (![writer canAddInput:videoInput]) {
            fprintf(stderr, "Cannot add video input to writer\n");
            return 1;
        }
        [writer addInput:videoInput];

        // Audio reader & writer if audio file provided
        AVAssetReader *audioReader = nil;
        AVAssetReaderTrackOutput *audioReaderOutput = nil;
        AVAssetWriterInput *audioInput = nil;

        if (audioFile && [[NSFileManager defaultManager] fileExistsAtPath:audioFile]) {
            NSURL *audioURL = [NSURL fileURLWithPath:audioFile];
            AVURLAsset *audioAsset = [AVURLAsset URLAssetWithURL:audioURL options:nil];
            NSArray *audioTracks = [audioAsset tracksWithMediaType:AVMediaTypeAudio];
            if (audioTracks.count > 0) {
                audioReader = [AVAssetReader assetReaderWithAsset:audioAsset error:&err];
                audioReaderOutput = [AVAssetReaderTrackOutput assetReaderTrackOutputWithTrack:audioTracks[0] outputSettings:nil];
                if ([audioReader canAddOutput:audioReaderOutput]) {
                    [audioReader addOutput:audioReaderOutput];

                    AudioChannelLayout acl;
                    bzero(&acl, sizeof(acl));
                    acl.mChannelLayoutTag = kAudioChannelLayoutTag_Stereo;

                    NSDictionary *audioSettings = @{
                        AVFormatIDKey: @(kAudioFormatMPEG4AAC),
                        AVNumberOfChannelsKey: @2,
                        AVSampleRateKey: @44100.0,
                        AVEncoderBitRateKey: @192000,
                        AVChannelLayoutKey: [NSData dataWithBytes:&acl length:sizeof(AudioChannelLayout)]
                    };

                    audioInput = [AVAssetWriterInput assetWriterInputWithMediaType:AVMediaTypeAudio outputSettings:audioSettings];
                    audioInput.expectsMediaDataInRealTime = NO;
                    if ([writer canAddInput:audioInput]) {
                        [writer addInput:audioInput];
                    } else {
                        audioInput = nil;
                    }
                }
            }
        }

        if (![writer startWriting]) {
            fprintf(stderr, "AVAssetWriter startWriting failed: %s\n", [[writer.error localizedDescription] UTF8String]);
            return 1;
        }
        [writer startSessionAtSourceTime:kCMTimeZero];
        if (audioReader) {
            [audioReader startReading];
        }

        // Write video frames
        int64_t currentFrame = 0;
        printf("[*] Encoding %lu shots into %dx%d H.264 MP4 @ %d fps...\n", (unsigned long)shots.count, width, height, fps);

        for (NSDictionary *shot in shots) {
            NSString *imgPath = shot[@"image"];
            double duration = [shot[@"duration"] doubleValue];
            int shotFrames = (int)round(duration * fps);

            NSImage *nsImg = [[NSImage alloc] initWithContentsOfFile:imgPath];
            CGImageRef cgImg = NULL;
            if (nsImg) {
                NSRect rect = NSMakeRect(0, 0, nsImg.size.width, nsImg.size.height);
                cgImg = [nsImg CGImageForProposedRect:&rect context:nil hints:nil];
            }

            CVPixelBufferRef pxBuffer = NULL;
            if (cgImg) {
                pxBuffer = CreatePixelBufferFromImage(cgImg, width, height);
            }

            for (int f = 0; f < shotFrames; f++) {
                while (!videoInput.isReadyForMoreMediaData) {
                    [NSThread sleepForTimeInterval:0.005];
                }
                CMTime frameTime = CMTimeMake(currentFrame, fps);
                if (pxBuffer) {
                    [adaptor appendPixelBuffer:pxBuffer withPresentationTime:frameTime];
                }
                currentFrame++;
            }
            if (pxBuffer) {
                CVPixelBufferRelease(pxBuffer);
            }
        }

        [videoInput markAsFinished];

        // Write audio buffers
        if (audioReader && audioInput) {
            printf("[*] Muxing synchronized AAC audio track...\n");
            while ([audioReader status] == AVAssetReaderStatusReading) {
                CMSampleBufferRef sampleBuffer = [audioReaderOutput copyNextSampleBuffer];
                if (sampleBuffer) {
                    while (!audioInput.isReadyForMoreMediaData) {
                        [NSThread sleepForTimeInterval:0.005];
                    }
                    [audioInput appendSampleBuffer:sampleBuffer];
                    CFRelease(sampleBuffer);
                } else {
                    break;
                }
            }
            [audioInput markAsFinished];
        }

        dispatch_semaphore_t sema = dispatch_semaphore_create(0);
        [writer finishWritingWithCompletionHandler:^{
            dispatch_semaphore_signal(sema);
        }];
        dispatch_semaphore_wait(sema, DISPATCH_TIME_FOREVER);

        if (writer.status == AVAssetWriterStatusCompleted) {
            printf("[✓] Master MP4 exported successfully: %s\n", [outputFile UTF8String]);
            return 0;
        } else {
            fprintf(stderr, "Export failed: %s\n", [[writer.error localizedDescription] UTF8String]);
            return 1;
        }
    }
}
