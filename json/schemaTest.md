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
  
  ## Modules Required
  sys, getopt, inspect, json, jsonschema, jsonschema.exceptions
  
