---
title: ST 2120-1 Systems
---

# Introduction

This is a rewrite of ST 2120 part 1 on TLX systems. The purpose of this document is to introduce terminology and notationxfor describing time labels at a conceptual level. Individual time label items are described in ST 2120-2 Items and time label use cases are described in ST 2120-3 Profiles.

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



You recalled our discussion on discontinuous timecode, which we’d said was akin to discontinuous KeyKodes that naturally occur on a work print.  I don’t think we intend to make illegal and analogous use cases using TLXs.  Such use cases relate to viable, though perhaps uncommon nowadays, use cases.  I’m thinking that if our most broadly scoped definitions precludes some use cases, we’ll have overconstrained things.  There could be a more specifically qualified definition that requires continuity (e.g., a construct that uses terms from our tentative definitions, “a sequence having count continuous labels” as being apropos to the use cases you’ve described.  Whether we have a specific term for that construct, or whether that construct is just a constraint imposed for certain profiles, is a worthy discussion.

A particular use case that comes up in discussion where the output of a process or device might have the original TLX labels kept, instead of generating new TLX labels is, I suggest, introducing unnecessary caveats.  It is analogous to recording Source Timecode on a recorded master instead of using Record Timecode.  While this is possible to do, it would generate "discontinuous Timecode".  Like discontinuous Timecode, the TLX labels passed through to the output would be for multiple sequences that are assembled together.

Otherwise, I generally disagree that a PTP Timestamp should be "reconstituted" for the purpose of addressing a media unit that does not otherwise have a TLX label associated with it, at least for where a Media Count would be included.  PTP Timestamps can only represent a sequence where they are generated in a live-capture environment and are always subject to interpolation (being “close” enough) and might not return a “consistent” value, whereas the purpose of the TLX Media Count would be for the foundation of a sequence in TLX labels, by clearly identifying the position within that sequence.

Using the Digital Birth Certificate profile as an example, the “virtual” TLX label would be using the same TLXuniqueSourceID and TLXptpTimestamp values as the actual TLX label, with an updated TLXmediaCount value to address the intended media unit.  In this example, the correct material (or TLX label) would first be identified by using the unique combination of Source UUID and PTP Timestamp, and then the intended position in a sequence of that material would be identified by using the intended Media Count integer value.

Some of the definitions that are being presented for a Media Identifier and Media Timestamp are not what came from the BNS model, at least for what I can tell, especially with regard to defining Media Sequences.  


