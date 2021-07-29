# Quick illustration of JSON

Introduction

Put together very quickly – probably has errors.  The “item” definitions are for illustrative purposes only.

## Schema

Schema for TLX

```JSON
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://smpte.com/TLX.schema.json",
  "title": "TLX",
  "type": "object",
  "properties": {
    "timestamp": {
      "$ref": " http://smpte.com/timestamp.schema.json"
    },
    "mediacount": {
      "$ref": " http://smpte.com/mediacount.schema.json"
    }
  }
}
```

The TLX can contain two possible “items”: timestamp and mediacount.  These are defined separately.


## Schema for timestamp

```JSON
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://smpte.com/timestamp.schema.json",
  "title": "timestamp",
  "type": "object",
  "properties": {
    "seconds": {
      "type": "integer",
      "minimum": 0
    },
    "nanoseconds": {
      "type": "integer",
      "minimum": 0,
      "maximum": 999999999
    }
  },
  "required": [ "seconds" ]}
}
```

The timestamp “item” is an object consisting of seconds and nanoseconds.  They are positive integers; nanoseconds is limited to 999999999.  The seconds property is required, nanoseconds is optional.


## Schema for mediacount

```JSON
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "http://smpte.com/mediacount.schema.json",
  "title": "mediacount",
  "type": "integer",
  "minimum": 0
}
```

The mediacount “item” is a positive integer.


## Example instance

As JSON:
```JSON
{
  "timestamp": { "seconds": 1586866984, "nanoseconds": 0 },
  "mediacount": 100
}
```

As UBJSON:

Translation

```UJBJSON
[{]
    [i][9][timestamp][{]
        [i][7][seconds][l][1586866984]
        [i][11][nanoseconds][i][0]
    [}]
    [i][10][mediacount][i][100]
[}]
```

Binary

```
7B 69 09 74 69 6D 65 73 74 61 6D 70 7B 69 07 73
65 63 6F 6E 64 73 6C 5E 95 AB 28 69 0B 6E 61 6E
6F 73 65 63 6F 6E 64 73 69 00 7D 69 0A 6D 65 64
69 61 63 6F 75 6E 74 69 64 7D
```

