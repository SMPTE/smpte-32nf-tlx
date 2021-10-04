# schemaTest.py documentation

```
schemaTest.py [-h][-d] [-q]* [-v] [-s <schemaPath> [ <testSuiteFile>]* ]'
```
  
  -h prints the above usage clue.
  
  -s provides a path all schemas to be used.  Metaschemas need not be included.  Defaults to './schema'
  
  -d activates some debugging messages (many of which, and eventually all could be commented away)
  
  -v verbose prints extra messages about progress successful steps
  
  -q quiet omits identification of individual test instances.  Use again to silence identification of test suites & longer warning diagnostics
  

  
  the remaining argument(s) indicate path(s) to the test suite(s).  A collection of files in a folder is a typical usage, e.g., "./tests/smpte-tlx-items/\*" though files can be listed individually, too.
  
  Each non-hidden file in the \<schemapath\> directory is loaded (if possible) as a schema file and produces a warning otherwise
  
  Each \<testSuiteFile\> is validated as a test suite using the test-schema.json file, which is expected to have been found in \<schemaPath\>.
  
  Upon execution, a report is given for each test run.  Diagnostics are presented when a validation result differs from what is expected.  Diagnostics are those provided by the jsonSchema.exceptions module.
  
  ## Example usage

```
./schemaTest.py ./tests/smpte-tlx-items/*
```
which uses the default schemaPath of './schema'

```
./schemaTest.py -s /mySchemaLibrary ./tests/smpte-tlx-profiles/*
```

  ## Modules Required
  sys, os.path, glob, traceback, getopt, inspect, json, jsonschema
  
  ## Schemas Required
  
  test-schema.json - defines the structure of a valid test suite, must be present in \<schemaPath\>
  This schema file includes a description of both the overall test suite structure and the structure for individual test instances, and this schema can validate the same.
  
  ## Test "Test Suites"
  
  The tests/smpte-tlx-items-deliberateBadTests/ folder includes a number of test suites which are deliberately faulty for use in validating that schemaTest.py correctly recognizes, rejects, and diagnoses faulty test suite files.
  
  ## Expected Use

This application was developed to provide automated testing of the following schemas:  
* smpte-tlx-items.json - an informative schema consistent with SMPTE ST 2120-2 - TLX Items
* smpte-tlx-profiles.json - an informative schema consistent with SMPTE ST 2120-3 - TLX Profiles

Test suites corresponding to these schemas can be found in tests/smpte-tlx-items/ and tests/smpte-tlx-profiles/ respectively.
