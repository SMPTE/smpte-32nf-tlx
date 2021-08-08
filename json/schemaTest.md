# schemaTest.py documentation

```
schemaTest.py [-h][-d] [-s <schemaUnderTestFile> [ <testSuiteFile>]* ]'
```
  
  -h prints the above usage clue.
  
  -d includes some debugging messages (many of which have since been commented away)
  
  -s identifies an argument representing a path to the schema under test (SUT)
  
  the remaining arguments indicate path(s) to test suites.  A collection of files in a folder is a typical usage, e.g., "./tests/smpte-tlx-items/\*" though files can be listed individually, too.
  
  The SUT is evaluated as valid schema file.
  
  Each of the <testSuiteFile> is validated as a test suite using the test-schema.json file (expected to have the relative path of ./schema/test-schema.json).
  
  Upon execution, a report is given of each test run.  Diagnostics are presented when a validation result differs from what is expected.  Diagnostics are those provided by the jsonSchema.exceptions module.
  
  ## Example usage

```
./schemaTest.py -s ./schema/smpte-tlx-items.json ./tests/smpte-tlx-items/*
```

  
  
  ## Modules Required
  sys, getopt, inspect, json, jsonschema, jsonschema.exceptions
  
For the purpose of debugging the program vis-a-vis the test suites, the [test-schema.json](https://github.com/Julian/jsonschema/blob/main/json/test-schema.json) file from Julian Berman's jsonSchema GitHub repository is used.  Per the terms of its use, it is accompanied by this copyright notice:
  
> Copyright (c) 2012 Julian Berman

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.
