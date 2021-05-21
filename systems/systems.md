---
title: ST 2120-1 Systems
---

# Introduction

This is a rewrite of ST 2120 part 1 on TLX systems. The purpose of this document is to introduce terminology and notationxfor describing time labels at a conceptual level. Individual time label items are described in ST 2120-2 Items and time label use cases are described in ST 2120-3 Profiles.

# Time Label Structure

An extensible time label (TLX) comprises a time label header and an unordered list of zero or more time label items. A time label item has a key and a value. The value can be single value, an unordered list of values, or a nested list of unordered key-value pairs.

Each scalar value can include zero or more attributes that provided additional information about the value. 

The time label items are described in ST 2120-2 Items.



***Describe the time label header***



# Data Types



***Move data types here?***



# Media Units

***Define media unit*** 

Example: A media unit is a sample such as a video frame or field or an audio sample.

Each media unit can have at most one time label.

# Media Sequences

A media sequence is an ordered set of zero or more media units with the same media identifier.

Media units are continuous with the sequence.

Note: A media sequence can be a file or a segment of tape.

<!--“Continuous” could be “uninterrupted” instead.-->

Example: A sequence of video frames could contain left and right stereo pairs in two sequences: one sequence for the left frames, the other sequence for the right frames. Although the left and right frames might have many media counts and timestamps in common, the left and right frames can be distinguished by the media identifier in the time label.

The relationship between media samples in two different media sequences is application-specific and out of scope.

Example: The media samples in the left and right stereo sequences may be interleaved in the video track of a media container.

Example: A tape device might record media samples with the media count starting at zero. If the tape is stopped and restarted, the media count may begin again at zero but with a different media identifier and hence a new sequence. Multiple sequences can be concatenated on the tape, each with a unique media identifier.

Within a media container (file, track, or tape for example), if a media unit does not have a media identifier, then the media identifier shall be inferred to be the same as the previous media unit and hence shall be the next media unit in that media sequence.


# Time Labels

Each time label can comprise any combination of the following label items:

* Media identifier
* Media count
* Media count rate
* Media timestamp

The identifier, count, or timestamp for a media unit that does not have a time label can be inferred from the time labels associated with other media units in the same sequence.


## Media Identifier

The media identifier distinguishes media units in different media sequences.

All media units that comprise a media sequence shall have the same media identifier.

Media identifiers shall be unique.

The media identifier could designate the device that captured or processed the media sequence or could be generated when the media is rendered or processed with each new rendering having a new media identifier.

Note: If the media identifier designates a physical device, then that device produces a single media sequence and the media count for each media unit must be unique.  

## Media Count

The media count shall be a non-negative integer. Within a sequence, the media count for a media unit shall be one greater than the media count of the previous media unit. The media count for the first media unit in a sequence is out of scope.

***The media count is the ordinal position within a media sequence.***

Example: A media count can serve the same function as timecode (SMPTE ST 12)  to establish a position in an timecode sequence.

The media count for media units that do not have time labels can be inferred from the media counts in neighboring media units in the same sequence that have time labels.

Media counts can represent either the presentation order or the decoding order of the media units.

The media count for the next time label in a sequence shall be incremented by the number of media units in the sequence since the previous time label that included a media count. This scheme supports several common use cases:

1. If every media unit has a time label and every time label has a media count, then successive media counts will increment by one.

2. If not every media unit has a time label with a media count, then the media count still tallies the number of  media units in the sequence.

   Example: If the first sample in every audio block has a time label with a media count, then the interpolated media counts will increment by one for every audio sample such that the media count minus the starting media count plus one represents the number of samples in the media sequence up to some sample and the media count in any time label corresponds to the first sample in the block.

3. If a sample in a sequence does not have a time label, the media count can be inferred from the media counts in nearby time labels.

4. If blocks of audio samples are deemed to be media units, then the media count increments by one for every block.

   Example: Each block of audio samples corresponds to a video frame at 24 frame per second, the  media count for the audio track increments by one for every frame, and 

See diagram ~/OneDrive/Documents/SMPTE/TLX/20210416 labels for audio blocks.pdf

Note: By analogy with of film edge keycode, the media count provides a unique reference mark for each media unit in an uninterrupted sequence of frames from the unique reference mark to identify a specific frame.

Example: After a media sequence is edited, the media counts within the same media sequence might no longer be continuous. New media counts would have to be generated for that media sequence when the edited video is rendered. The entire rendered video might comprise a single new media sequence with a new media identifier and continuous media counts with the new sequence.

## Media Count Rate

***Define media count rate***


## Media Timestamp

The media timestamp shall be a PTP time stamp.

Media timestamps shall represent the presentation order of the media units.

Note: If the media sequence is captured by a device, then the media timestamps represent the (absolute) capture time which also represents the order (relative time) in which the captured media units are presented.

During the processing of a media sequence, time labels can be copied from the source media sequence or new time labels can be generated.

***What happens when the media is edited?***

***How to interpolate missing timestamps?***





# Annex A. Time Label Schema

The JSON schema for time labels is introduced in this annex.

The JSON schema is extended for individual time label items in Part 2.



# Annex B. Binary Representation of Time Labels

UBJSON can be used as a binary representation of time labels.

Note: Applications can choose a different representation for time labels.



# Bibliography



# Comments

This section holds comments that will be edited into the main body of the document.

Comments are copied from emails in chronological order from oldest to newest.

You recalled our discussion on discontinuous timecode, which we’d said was akin to discontinuous KeyKodes that naturally occur on a work print.  I don’t think we intend to make illegal and analogous use cases using TLXs.  Such use cases relate to viable, though perhaps uncommon nowadays, use cases.  I’m thinking that if our most broadly scoped definitions precludes some use cases, we’ll have overconstrained things.  There could be a more specifically qualified definition that requires continuity (e.g., a construct that uses terms from our tentative definitions, “a sequence having count continuous labels” as being apropos to the use cases you’ve described.  Whether we have a specific term for that construct, or whether that construct is just a constraint imposed for certain profiles, is a worthy discussion.

A particular use case that comes up in discussion where the output of a process or device might have the original TLX labels kept, instead of generating new TLX labels is, I suggest, introducing unnecessary caveats.  It is analogous to recording Source Timecode on a recorded master instead of using Record Timecode.  While this is possible to do, it would generate "discontinuous Timecode".  Like discontinuous Timecode, the TLX labels passed through to the output would be for multiple sequences that are assembled together.

Otherwise, I generally disagree that a PTP Timestamp should be "reconstituted" for the purpose of addressing a media unit that does not otherwise have a TLX label associated with it, at least for where a Media Count would be included.  PTP Timestamps can only represent a sequence where they are generated in a live-capture environment and are always subject to interpolation (being “close” enough) and might not return a “consistent” value, whereas the purpose of the TLX Media Count would be for the foundation of a sequence in TLX labels, by clearly identifying the position within that sequence.

Using the Digital Birth Certificate profile as an example, the “virtual” TLX label would be using the same TLXuniqueSourceID and TLXptpTimestamp values as the actual TLX label, with an updated TLXmediaCount value to address the intended media unit.  In this example, the correct material (or TLX label) would first be identified by using the unique combination of Source UUID and PTP Timestamp, and then the intended position in a sequence of that material would be identified by using the intended Media Count integer value.

Some of the definitions that are being presented for a Media Identifier and Media Timestamp are not what came from the BNS model, at least for what I can tell, especially with regard to defining Media Sequences.  



**Comments after last edit on 2021-04-29**



Studying ST 2120-2 and see that the integer data type is defined as IEEE 754 binary64, but binary64 is double-precision floating-point. See [https://en.wikipedia.org/wiki/IEEE_754](https://nam10.safelinks.protection.outlook.com/?url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FIEEE_754&data=04|01|bschunck%40m.smpte.org|0fa1190d924f4126d03d08d90b50373c|c6051a58269b4f08835feedebf4596b3|0|0|637553261489995928|Unknown|TWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D|1000&sdata=1YvzWoZ3NGDkBtCH550acJh%2FM4RnkD5DWZp%2Fts3Pulc%3D&reserved=0)

 So it would seem we need a better definition for integers. The JSON specification seems to not impose a limit on the sizes of numbers (either integer or floating-point). We can stay at an abstract level and ignore the details, but eventually, when we define a mapping to binary representations, we will need to distinguish between different integer sizes (8, 16, 32, 64 bits) and floating-point numbers (single or double precision).

Part 1 is independent of the other parts and should:

1.1) provide definitions for
                media unit
                sequence
                source
                TLX label
                (identifiers, timestamps, counts, etc. are all related to items that are not discussed until part 2)
                -> I propose you start with the definitions found here:
                Files > Working Documents > older Working Documents > [20200522 Requirement List v12.docx](https://teams.microsoft.com/l/file/790E1504-009C-492B-85DA-972345FEEF83?tenantId=c6051a58-269b-4f08-835f-eedebf4596b3&fileType=docx&objectUrl=https%3A%2F%2Fsmpte.sharepoint.com%2Fsites%2F32nf80-tlx%2FShared%20Documents%2FGeneral%2FWorking%20Documents%2Folder%20Working%20Documents%2F20200529%20Requirement%20List%20v13.docx&baseUrl=https%3A%2F%2Fsmpte.sharepoint.com%2Fsites%2F32nf80-tlx&serviceName=teams&threadId=19:5d34748acf9e43f8a530bcacbdbfcf85@thread.tacv2&groupId=b1606f7d-99ec-4545-9182-a65522d2066f)

The definitions start on the second page.  Most (all?) of them are already in ISO format.  We can amend as needed, but at least that document has definitions we agreed a year ago were fine to leave alone until we knew more.  Maybe now we do know more!

1.2) describe the relationships between
                sources and media units
                media units and sequences
                  how editing of sequence(s) produces a new seuquence
                TLX labels and media units (indicate that embedding or otherwise explicit associations between TLX labels and media 	units is outside the scope of Parts 1-3)

1.3) describe the structure of a TLX
                (an unordered collection of uniquely named items)
                > this implies that multiples of an itemKind
                  will have to inside an itemkind collection,
                                which is itself a kind of item

                (clarify if the TLX can be empty - should it be allowed?)
    
                exemplar JSON schema (bogus item type)

1.4) describe the structure of an item
                (an unordered set of uniquely named attributes

1.5)  Provide an authoritative JSON schema for TLX in the prose - the schema file should (debatably) be associated with Part 2)

1.6) Provide an example schema for an item (e.g., based on a “foo & bar” version of one of John’s item tables).

1.7) Provide an informative example JSON file of a TLX with one or two (different kinds of) items as suggested by the schemas from 5 & 6.

1.8) consider if there’s anything to be said about other carriage formats (MXF, etc.) My guess is that’s a different part (part 4?) which is crafted primarily to supply the strategy and UL details (much as ST 2094-2 is to the rest of the ST 2094 suite - parts 1, 10, 20, 30, and 40).

1.9) [what am I missing?]



I would add to part 1: datatypes. The definitions that are in part 2 now are not sufficient. I will try something more and coordinate with John Fletcher.



binary64

Studying ST 2120-2 and see that the integer data type is defined as IEEE 754 binary64, but binary64 is double-precision floating-point.

 See [https://en.wikipedia.org/wiki/IEEE_754](https://nam10.safelinks.protection.outlook.com/?url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FIEEE_754&data=04|01|bschunck%40m.smpte.org|b8b3895b3e17453fb8c708d9145b6cef|c6051a58269b4f08835feedebf4596b3|0|0|637563205279165480|Unknown|TWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D|1000&sdata=uVBoi2AIkDt%2BmefU5grpO2VglkXIs4x0gOdhxKMFMJw%3D&reserved=0)

 

So it would seem we need a better definition for integers. The JSON specification seems to not impose a limit on the sizes of numbers (either integer or floating-point). We can stay at an abstract level and ignore the details, but eventually, when we define a mapping to binary representations, we will need to distinguish between different integer sizes (8, 16, 32, 64 bits) and floating-point numbers (single or double precision).



Reply from John Fletcher:

The integer data type is not defined as IEEE 754 binary64 but we require that the values can be represented as IEEE 754 binary64. The reason is that many implementations use that representation. (JSON does not distinguish between a number and an integer although JSON schema allows you to require that a number is an integer.)

 

\> when we define a mapping to binary representations, we will need to distinguish between different integer sizes (8, 16, 32, 64 bits) and floating-point numbers (single or double precision)

In the schema, you can specify the allowed range of values and that will determine what size of binary number the value will fit in. UBJSON uses numeric types such as int8 and in mapping JSON to UBJSON you are free to choose an appropriate type, e.g. the smallest one the value will fit in.

 

My reply to John:

Your comment about binary64 clarifies it for me. I read it as saying that the integers must be in binary64, but now I see it means “shall be representable as binary64”.  Agree with your comments about JSON schema and UBJSON. JSON by itself does not distinguish between different integer precisions, but the schema can.



From Peter Symes:

Sorry to be absent from recent meetings – going through a whole pile of changes and an interstate move, so just don’t have the time or attention at the moment. But , really pleased to see what looks like excellent progress.

However, I must say that I think the “w/r” approach to media count is a bad idea.

It ***should*** work OK if conventional media is known to be locked to the timebase of the precision timestamp, but this may not always be the case. 

Probably because I missed the discussions, I don’t understand how this would work in a 1000/1001 environment where “w” would generally represent some non-integer number of frames.

In non-professional environments, it’s quite likely that frame rates would be just nominal. I’m convinced that we do NOT want a value of “seconds” anywhere in a TLX label that diverges from the seconds in the precision time stamp.

Also, consider the time lapse or motion triggered photography scenarios. The original concept (precision time plus MU count) addresses this perfectly …. Keep a count of the images, plus a time for each one. I think w/r may be meaningless in these cases.

Finally – and this may be where my biggest problem lies – being absent from the discussions has left me with no clue as to why w/r would be a good idea!

Perhaps you can put me right?

 

Reply from Bill Redmann:

w/r (by which I think you mean an informal description of the “count” divided by “rate” math for which the equations were provided) produces behaviors similar to those that ST 12 does when rendered as a time-like string. HH:MM:SS:FF isn’t a time in the general case, it’s just another way to display a count, and that is missing (or left to wild west interpretations) if we didn’t say something. So we said something, though as little as we thought we could. It’s behavior with counts and a 1000/1001 rate with is no different than for ST 12 non-drop. Plus, there are so many cases where the timestamp isn’t meaningful to the sequence (e.g., any non-real time process)

For cases where the interpretation of w/r is absurdly nonsensical, e.g., as you point out: time lapse or nature cam, the solution is just don’t include ‘r’. It’s not meaningful. On the other hand, if you do, the math doesn’t explode (it does, however, devolve to one count is one second - as intended).



Reply from Peter:

I still think this is an example of incorporating one application’s needs into a complex and non-intuitive transmission format. I still believe such computations are the responsibility of (and easily performed by) the user application. It is usually good policy to transmit the raw data and not modify to support the possible needs of one user application.



Reply from Bill:

The issue with the value of “rate” is that, if it’s known and used early in the pipeline, but not carried as metadata, it can’t reliably be recreated. Lesson learned from ST 12. Someone’s on-set notes or logs might use the human-handy time-like value, but someone downstream might otherwise guess wrong and recreate the wrong values while attempting to recover media count.

Of course, as with any of this metadata, no application is compelled to *use* it, though some profiles might could require that it be *present*.



Reply from Sieg Heep:

Hoping that your changes and interstate move are going as well as can be. Your discussions and contributions are much appreciated.

I think Bill’s statements are spot on. The intention is to provide a MediaCount with an optional MediaCount.Rate in the TLX label. The formulas presented are for the applications to use.

 To put context around this discussion, there is another formula presented for “t” (time) in the document immediately before this one for “w” (whole seconds) and “r” (whole media units).  

When including my suggested changes, part of section 6.2 would read something like this. (Note the usage of the words “can” and “should”.)

A time or time-like value "t", having the dimension of time, can be produced by dividing **count** by **rate**: 

(t= count / rate)

where a time-like value representing a count of whole seconds "w" and whole media units "r" is being produced, the values for "w" and "r" should be produced by:

(two formulas with **count** and **rate** using the "floor" and "ceiling" functions, and the “modulo” operator)



