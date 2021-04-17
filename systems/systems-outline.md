---
title: ST 2120-1 Systems
---

# Introduction
This is a rewrite of ST 2120 part 1 on TLX systems. The purpose of this document is to introduce terminology and notation for describing time labels. Individual time label items are described in ST 2120-2 Items and time label use cases are described in ST 2120-3 Profiles.



# Media Units





# Time Labels

Each time label can comprise any combination of the following label items:

* Media identifier
* Media count
* Media timestamp

Each media unit can have at most one time label.

The identifier, count, and timestamp for a media unit that does not have a time label must be inferred from the time labels associated with other media units in the same sequence.



## Media Identifier

All media units that comprise a media sequence shall have the same media identifier.

Note: The media identifier could be a UUID.

## Media Count

The media count shall be a non-negative integer. Within a sequence, the media count for a media unit shall be one greater than the media count of the previous media unit, earlier in the sequence. The media count for the first media unit in a sequence is out of scope.

Media counts can represent either the presentation order or the decoding order of the media units.

## Media Timestamp

The media timestamp shall be a PTP time stamp.

Within a sequence, the media timestamps for media units shall be larger than the media timestamp of the previous media unit, earlier in the sequence.

Media timestamps can represent either the presentation order or the decoding order of the media units.



# Media Sequences

A media sequence comprises zero or more media units with time labels that have the same identifier.

Note: A media sequence can be a file or a segment of tape.

Example: A media unit is a sample such as a video frame or field or an audio sample.

Example: A sequence of video frames could contain left and right stereo pairs in two sequences: one sequence for the left frames, the other sequence for the right frames. Although the left and right frames might have many timestamps in common, the left and right frames can be distinguished by the identifier (UUID) in the time label.

The relationship between media samples in two different media sequences is application-specific and out of scope.

Example: The media samples in the left and right stereo sequences may be interleaved in the sequence.

Example: A tape device might record media samples with media count starting at zero. If the tape is stopped and restarted, the media count may begin again at zero but with a different media identifier and hence a new sequence. Multiple sequences can be concatenated on the tape comprising multiple sequences, each with a unique media identifier.




# Annex A. Time Label Schema

The JSON schema for time labels is introduced in this annex.

The JSON schema is extended for individual time label items in Part 2.



# Annex B. Binary Representation of Time Labels

UBJSON can be used as a binary representation of time labels.

Note: Applications can choose a different representation for time labels.



# Bibliography

