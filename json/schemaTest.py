#!/usr/bin/env python3

import sys, os.path, glob, traceback, getopt, inspect, json, jsonschema #, jsonschema.exceptions

#jsonSchema = 'json-schema-draft-7'

# print list of format checkers available for use by jsonschema
#print('INFO: known formats:\n',str(jsonschema.FormatChecker.checkers))

# change from prior version
# added resolver to schema validation so that '$ref': to other schemas are correctly used when validating
#    this required a refactor of the -s <schemaPath> argument and how it's used.
#    now it loads schemaStore such that the $id field is properly the identifier

# each test set file (tupically the files under the ./tests directory) is validated as being a test set
# each test set comprises one or more test suites, directed to a particular theme.
# each test suite has it's own schema definition against which it's tests (TLX instances) are validated.
# some tests are intended to fail and are marked "valid": false, other are valid.

testSchemaFilename = 'test-schema.json'  # this is the schema file for validating test sets
testSchemaID = '' # set this when this schema is loaded into the store

def showUsage():
    print ('USAGE: schemaTest.py [-h][-d][-v] [-s <schemaPath> [ <testSuiteFile>]+ ]' )
    print (' Validates using schemas in <schemaPath>, as directed by various instances in each of one or more <testSuiteFile>s')
    print (' -d prints debug hints, -v raises verbosity')
    print ('\n <schemaPath> defaults to ./schema')

def main(argv):
    debug = 0
    verbose = 0
    quiet = 0

    # counters for report at end
    schemasLoaded = 0
    schemasBroken = 0
    suitesRun = 0
    suitesBroken = 0
    testsPassed = 0
    testsFailed = 0
    warnings = 0

    # this is where the schemas should be found (with a default)
    schemaPath = './schema'

    # validate the arguments passed
    try:
        opts, args = getopt.getopt(argv,'vhdqs:')
    except getopt.GetoptError as e:
        print ('ERR:',e)
        showUsage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            showUsage()
            sys.exit()
        if opt == '-d':
            debug = 1
        if opt == '-s':
            schemaPath = arg
        if opt == '-v':
            verbose = 1
        if opt == '-q':
            verbose = 0
            quiet += 1

    # remaining arguments should be a list of test files
    if debug: print('DEBUG: \noptlist as detected:', opts, '\nremaining arguments:', args)
    listOfTestFiles = []
    for f in args:
        listOfTestFiles += glob.glob(f)
    if (len(listOfTestFiles) == 0):
        print ('ERR: missing <testSuiteFile>.  One or more is needed.')
        showUsage()
        sys.exit(2)
        
    # check that that the schemaPath is at least a directory
    if os.path.isdir(schemaPath):
        schemaPath = os.path.realpath(schemaPath) + '/'
    else:
        print('ERR: expected a schema path, use -s <schemaPath> option')
        sys.exit(2)

    if quiet < 1: print('SCHEMATEST: will run the tests listed in', args, 'against the schemas found in', schemaPath + "." )


    if verbose: print('LOADING SCHEMAS...')

    # load all schemas, by $id, into schemaStore dictionary
    schemaStore = {}
    for filename in os.listdir(schemaPath):
        if (not os.path.isdir(filename)) and filename.endswith(".json"):
            # read each json file, expecting a schema
            try:
                with open(os.path.join(schemaPath, filename) ) as candidateSchemaFile:
                    candidateSchema = json.load(candidateSchemaFile)
                    candidateSchemaFile.close()
            except Exception as e:
                print('\nWARN: Could not read valid JSON from', filename, '\n  skipping...')
                if quiet < 2: print('  ', e)
                schemasBroken += 1
                warnings += 1
                continue
            else:
                try:
                    # check if candidate schema has an id, suitable for indexing in the schema store
                    id = candidateSchema['$id']
                except Exception as e:
                    print('\nWARN: schema candidate', filename, 'does not have an "$id" element, so won\'t be referenced as a schema.\n  skipping...')
                    schemasBroken += 1
                    warnings += 1
                    continue
                else:
                    # confirm that the schema is valid
                    try:
                        jsonschema.validate( instance= candidateSchema, schema=json.loads('{}'))
                    except Exception as e:
                        print('\nWARN: schema candidate', filename, 'does not validate as a schema.\n', e, '\n  skipping...')
                        schemasBroken += 1
                        warnings += 1
                        continue
                    else:
                        # add to the store by id
                        schemasLoaded += 1
                        schemaStore[id] = candidateSchema
                        if filename == testSchemaFilename: testSchemaID = id  # record this for when validating test files
        else:
            if os.path.isdir(filename):
                print("\nWARN: Directory", filename, 'in schema directory was not a file of type .json.\n  skipping...')
                schemasBroken += 1
                warnings += 1
            else:
                if filename[0] != '.': #ignore hidden files that fail, it's expected
                    print('\nWARN: File', filename, 'in schema directory was not of type .json.\n  skipping...')
                    warnings += 1
            continue
    if verbose: print('LOADED', len(schemaStore), 'SCHEMAS')
        

    if debug:
        print ('  DEBUG: Schema store contents:')
        for schemaURI in schemaStore.keys():
            print( '    schema $id:', schemaURI,'\n      value length:', len(str(schemaStore[schemaURI])) )


    if verbose: print('READY WITH', len(listOfTestFiles), "TEST FILES...")
    if debug: print ('DEBUG: list of test files -', listOfTestFiles )
    # validate that each of the test set files are readable and valid
    for testFilename in listOfTestFiles:
        if verbose: print("TESTING WITH", testFilename)
        try:
            with open(testFilename) as currentTestFile:
                try:
                    currentTestSuite = json.load(currentTestFile)
                    currentTestFile.close()
                except Exception as e:
                    print('\nWARN: Can\'t parse JSON for test suite', testFilename, '.\n  skipping...')
                    if quiet < 2: print('  ', e)
                    suitesBroken += 1
                    warnings += 1
                    continue
                else:
                    try:
                        schemaForTestSets = schemaStore[testSchemaID]
                        jsonschema.validate( instance= currentTestSuite, schema= schemaForTestSets)
                    except jsonschema.exceptions.SchemaError as e:
                        print('\nERR: schema for validating testSets,', testSchemaFilename, ' is faulty.')
                        print('  ', e)
                        sys.exit(2)
                    except jsonschema.exceptions.ValidationError as e:
                        print('\nWARN: currentTestSuite from "' + testFilename + '" is NOT well-formed.\n  skipping...')
                        if quiet < 2: print('  ', e)
                        suitesBroken += 1
                        warnings += 1
                        continue
                    else:
                        if debug: print('DEBUG: Test suite in, from ', testFilename,', is well-formed.')
        except Exception as e:
            print('\nWARN: currentTestSuite, from', testFilename,' couldn\'t be read.\n  skipping...')
            if quiet < 2: print('  ', e)
            suitesBroken += 1
            warnings += 1
            continue


        # the test suite was valid,
        if quiet < 2: print('\nSuite', testFilename, '(' + str(currentTestSuite['description']) + ')' )
        suitesRun += 1
        
        schemaUnderTest = currentTestSuite['schema']
        
        
        #validate each of the tests vs the schema
        testNumber = 0 # restart for each suite, testsPassed + testsFailed = total of tests already run
        for instance in currentTestSuite['tests']:
            testNumber += 1
            if quiet < 1: print('\n  Test [' + str(suitesRun + suitesBroken) + '.' + str(testNumber) + '] [[' + str(testsPassed + testsFailed + 1) + ']] >', str(instance['description']))

            #perform validation test on the current TLX instance
            currentTestInstance = instance['TLX']
            isVALID = instance['valid']

            #check vs schemaUnderTest
            if debug: print ( '    prepping to validate','\n    currentTestInstance:', currentTestInstance, '\n    schemaUnderTest:', schemaUnderTest)

            # add schemaUnderTest to store
            schemaStore[ schemaUnderTest['$id'] ] = currentTestInstance
            
            try:
                schemaNeeded = currentTestSet['schema']['$ref']
                # strip any fragment
                schemaNeeded = schemaNeeded.split('#')[0]
            except:
                # don't care if no $schema required (I think)
                pass
            else:
                try:
                    schemaOnHand = schemaStore[ schemaNeeded ]
                except:
                  print('WARN: Test file', testFilename, 'requires $schema', schemaNeeded, 'which is not present in the store.'  )
                  suitesBroken += 1
                  warnings += 1
                  break
                
            # rebuild the resolver for each schemaUnderTest (usually only once per test file)
            resolver= jsonschema.RefResolver( None, referrer= schemaUnderTest, store= schemaStore )
            #resolver= jsonschema.RefResolver( base_uri= None, referrer= None, store= schemaStore)

            try:
                jsonschema.validate(instance= currentTestInstance, schema= schemaUnderTest, resolver = resolver)
            except jsonschema.exceptions.SchemaError as e:
                # this shouldn't happen here - it should be caught above
                print('  WARN: schema in', testFilename, 'is faulty')
                warnings += 1
                if quiet < 2: print('\n  DIAGNOSTIC: \n-------------------------------------\n   ', e, '\n', traceback.print_exc(), '\n-------------------------------------\n')
            except jsonschema.exceptions.ValidationError as e:
                if isVALID == True:
                    # FAILED, but supposedly VALID
                    print('  WARN: instance is supposed to be VALID but FAILED.')
                    if quiet < 2: print('\n  DIAGNOSTIC: \n-------------------------------------\n   ', e, '\n', traceback.print_exc(), '\n-------------------------------------\n')
                    testsFailed += 1
                    warnings += 1
                else:
                    # FAILD and supposedly INVALID
                    testsPassed += 1
                    if debug: print('DEBUG:', currentTestInstance,'INVALID and FAILED (correct).')
            else:
                if debug: print('  DEBUG: instance DID validate and validity flag is', isVALID)
                if isVALID == True:
                    # PASSED and supposedly VALID
                    testsPassed += 1
                else:
                    # PASSED but supposedly INVALID
                    testsFailed += 1
                    print('  WARN: this test instance:\n    ', currentTestInstance,'\n  is supposed to be INVALID but PASSED.')
                    warnings += 1
            finally:
                # remove schemaUnderTest from store
                del schemaStore[schemaUnderTest['$id']]

                #break
            continue

    print ('\n\nResults:')
    if warnings > 0: print("Total WARNINGS:", warnings)
    print ('Of', schemasLoaded + schemasBroken, 'files at <schemaPath>,',
        schemasBroken, ('was' if schemasBroken == 1 else 'were') + ' skipped,', schemasLoaded, 'were used.')
    print ('Of', suitesRun + suitesBroken, 'test suites,',
        suitesBroken, ('was' if suitesBroken == 1 else 'were') + ' broken, leaving', suitesRun, 'to run.')
    print ('From those,\n  ', testsPassed + testsFailed, 'tests were run with', testsPassed, 'PASSED and', testsFailed, 'FAILED.')
    print ('\n\nDone.')

if __name__ == '__main__':
   main(sys.argv[1:])
    