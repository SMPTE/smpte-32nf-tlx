# Quick illustration of TLX

## Introduction

TLX, the 'Extensible Time Label', provides metadata about a single media unit that is simple, versatile, and extensible.

A TLX label (see ST 2120-1*) is comprised of one or more "items" (see 2120-2*).  Each item has one or more "attributes".  The metadata is represented in those attributes.

In general, no item is required.  However, TLX profiles (see 2120-3*) can be defined to impose additional constraints on the formulation of a TLX label, requiring or forbidding certain items, attributes.  A profile can specify further constraints, e.g., how a certain metadata is produced.

    * these documents are members of the ST 2120 suite of standards, which as of AUG, 2021 are being drafted.

## Example: the Digital Birth Certificate (DBC)

One profile, the DBC, requires a conforming TLX label to include three specific items:

```JSON
{
    "TLXmediaCount": { "count": 300, "rate": [ 50, 1 ] },
    "TLXptpTimestamp": { "ptpTime": [1234567890, 123456789 ], "localOffset": -25237 },
    "TLXuniqueSourceID": { "sourceID": "51793043-be99-4c40-9d9f-b1e865e516c5" }
}
```

The example above is presented in the text-based UTF-8 encoded protocol "JSON".  JSON is a great choice when trying to understand what's in a message – it's quite easy to read.  Of course, for a complete understanding of the elements, one should consult the SMPTE ST 2120 suite of documents, still in draft.  However, a JSON representation is not at all compact.  The underlying metadata data can be much more efficiently represented by other encodings, such as the SMPTE KLV data encoding protocol described in SMTPE ST 336, which should suggest that a TLX label could be encoded in multiple, different ways.

## TLX Schemas: smpte-tlx-items & smpte-tlx-profiles

An instance of a TLX label, such as the one above, can be verified to be a valid TLX instance by the JSON Schema smpte-tlx-items.json.  The TLX label itself is merely an object: a non-empty, unordered collection of items, none of which are required.  TLX items are themselves objects, an non-empty unordered collection of attributes, some of which might be required.  The smpte-tlx-items schema includes the overall TLX schema, a subschema for each of the TLX items and its attributes, and some derived types that also appear as subschemas to assist in consistency when describing the attributes.

An instance of a TLX label can be further examined for compliance with a TLX profile (such as the DBC), by verification against the appropriate subschema withn the smpte-tlx-profiles.json schema.  Each profile subschema tests for those (testable) constraints that are additional relative to those already needed for a TLX label to be valid.

For more information about the JSON Schema language, see https://json-schema.org/

## SubSchema for the TLXptpTimestamp item

Here is an exemplary portion of the smpte-tlx-items schema, to give you an idea of how to read it.  This portion describes what is allowed for the TLXptpTimestamp, the middle line of the example TLX label above.

```JSON
    ....
    "TLXptpTimestamp": {
        "$id": "#TLXptpTimestamp",
        "title": "TLXptpTimestamp",
        "type": "object",
        "description": "Creation time of this TLX label.",
        "examples": [
            { "ptpTime": [ 1234567890, 123456789 ], "currentLocalOffset": -25237, "isLeapSecond": false },
            { "ptpTime": [ 12345678901, 999999999 ], "currentLocalOffset": -25237},
            { "ptpTime": [ 12345678901, 999999999 ], "currentLocalOffset": -25237, "foo": "bar" } ],
        "properties": {
            "ptpTime": { "type": "array",
                "items": [
                    { "description": "seconds", "type": "integer", "minimum": 0, "exclusiveMaximum": 281474976710656 },
                    { "description": "nanoseconds", "type": "integer", "minimum": 0, "exclusiveMaximum": 1000000000 } ],
                "minItems": 2, "additionalItems": false },
            "localOffset": { "type": "integer", "minimum": -2147483648, "exclusiveMaximum": 2147483648 },
            "isLeapSecond": { "type": "boolean", "default": false }
        },
        "required": [ "ptpTime" ],
        "additionalProperties": true
    }...
```

The TLXptpTimestamp “item” is an object that requires the attribute "ptpTime", which is an array containing two integers representing seconds and nanoseconds.  Both integers are constrained to be positive; but each has a different limit, which comes from the PTP timestamp representation specified in IEEE 1588, e.g., nanoseconds is limited to 999,999,999 and thus rolling over at one second.  Both are explicitly required and additional elements are explicitly precluded.  The TLXptpTimestamp item permits additional attributes to be added, which is one way the TLX structure provides future extensibility.

## UBJSON encoding

Another example encoding available for JSON is UBJSON.  Although UBJSON provides a binary encoding, it does not compress strings, such as the names of name-value pairs and values of type string (including hexadecimal strings).  Thus, which it offers another example for ways to encode a TLX label, it is only about 30% more efficient than JSON itself.

As a UBJSON tokenized translation from JSON :

```UJBJSON
[{]
    [i][13][TLXmediaCount][{]
        [i][5][count][I][300]
        [i][4][rate][[]
            [i][50]
            [i][1]
        []]
    [}]
    [i][15][TLXptpTimestamp][{]
        [i][7][ptpTime][[]
            [l][1234567890]
            [l][123456789]
        []]
        [i][11][localOffset][I][-25237]
    [}]
    [i][17][TLXuniqueSourceID][{]
        [i][8][sourceID][S][i][36][51793043-be99-4c40-9d9f-b1e865e516c5]
    [}]
[}]
```

Binary

```
7B 69 0D 54 4C 58 6D 65 64 69 61 43 6F 75 6E 74
7B 69 05 63 6F 75 6E 74 49 01 2C 69 04 72 61 74
65 5B 69 32 69 01 5D 7D 69 0F 54 4C 58 70 74 70
54 69 6D 65 73 74 61 6D 70 7B 69 07 70 74 70 54
69 6D 65 5B 6C 49 96 02 D2 6C 07 5B CD 15 5D 69
0B 6C 6F 63 61 6C 4F 66 66 73 65 74 49 9D 6B 7D
69 11 54 4C 58 75 6E 69 71 75 65 53 6F 75 72 63
65 49 44 7B 69 08 73 6F 75 72 63 65 49 44 53 69
24 35 31 37 39 33 30 34 33 2D 62 65 39 39 2D 34
63 34 30 2D 39 64 39 66 2D 62 31 65 38 36 35 65
35 31 36 63 35 7D 7D
```

