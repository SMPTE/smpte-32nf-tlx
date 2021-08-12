#!/usr/bin/env python3
# chmod 777 schemaTest.py
# hoping the execution permissions propagate to GitHub (then these two lines can go away)

import sys, getopt, inspect, json, jsonschema, jsonschema.exceptions
#from jsonschema import validate

jsonSchema = 'json-schema-draft-7'
#print out what format checkers are available for use by jsonschema
#print('INFO: known formats:\n',str(jsonschema.FormatChecker.checkers))

# this is the JSON schema being tested
#
# schemaUnderTestFile (file object)
# SUT    (dictionary from JSON)


# this is the JSON schema that validates a good test suite
testSchemaFilename = './schema/test-schema.json'
# TODO: the test suite includes a "schema" parameter for each collection of tests,
#       but for now, we're not using that.  (Need to set up the resolver code to trace the $ref).

def showUsage():
    print ('USAGE: schemaTest.py [-h][-d] [-s <schemaUnderTestFile> [ <testSuiteFile>]+ ]' )
    print (' Validates the schemaUnderTestFile, then tests with zero or more testSuiteFile(s)')
    print (' -d prints debug hints')

def main(argv):
    debug = 0

    # counters for report at end
    suitesRun = 0
    suitesBroken = 0
    testsPassed = 0
    testsFailed = 0

    schemaUnderTestFilename = ''

    # validate the arguments passed
    try:
        opts, args = getopt.getopt(argv,'hds:')
    except getopt.GetoptError as e:
        print ('ERR:',str(e))
        showUsage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            showUsage()
            sys.exit()
        if opt == '-d':
            debug = 1
        if opt == '-s':
            schemaUnderTestFilename = arg
    ListOfTestFiles = args
    if (len(ListOfTestFiles) == 0) or schemaUnderTestFilename == '':        
        print ('ERR: too few arguments')
        showUsage()
        sys.exit(2)
        
    # load the schema under test (SUT)
    try:
        with open(schemaUnderTestFilename) as schemaUnderTestFile:
            SUT = json.load(schemaUnderTestFile)
            schemaUnderTestFile.close()
            #if debug: print ('DEBUG: the -s arg' + schemaUnderTestFilename + ' (SUT) seems OK.')
    except Exception as e:
        print('ERR:',schemaUnderTestFilename,'is missing or poorly formed JSON')
        print(str(e))
        sys.exit(2)

    # load the test set schema (TESTSCHEMA)
    try:
        with open(testSchemaFilename) as testSchemaFile:
            TESTSCHEMA = json.load(testSchemaFile)
            testSchemaFile.close()
            #if debug: print ('DEBUG: internal ref', testSchemaFilename, '(TESTSCHEMA) seems OK.')
    except Exception as e:
        print('ERR: Expected',testSchemaFilename,'to be in this accessible')
        print(str(e))
        sys.exit(2)

    # validate that all the test set files are readable and valid
    for i in range ( 0, len(ListOfTestFiles) ):
        #if debug: print ('DEBUG: re-loading test suite file',ListOfTestFiles[i])
        try:
            with open(ListOfTestFiles[i]) as currentTestSet:
                try:
                    #if debug: print('DEBUG: re-verifying test suite', ListOfTestFiles[i],'.')
                    TESTSUITELIST = json.load(currentTestSet)
                    currentTestSet.close()
                except Exception as e:
                    print('WARN: Can\'t parse JSON for test suite', ListOfTestFiles[i],'.')
                    print(str(e),'\n skipping...')
                    suitesBroken += 1
                    continue
                else:
                    try:
                        jsonschema.validate( instance=TESTSUITELIST, schema=TESTSCHEMA)
                    except Exception as e:
                        print('WARN:', ListOfTestFiles[i],'isn\'t a well-formed test suite.')
                        print(str(e),'\n skipping...')
                        suitesBroken += 1
                        continue
        except Exception as e:
            print('WARN: Could not read test suite file', ListOfTestFiles[i],'.')
            print(str(e),'\n skipping...')
            suitesBroken += 1
            continue

        print('\nSuite', ListOfTestFiles[i], '(' + str(TESTSUITELIST[0]['description']) + ')' )
        suitesRun += 1
        # TODO constant index of [0] is not appropriate for description when multiple test sets are in a single file
        
        # TESTS could have multiple schemas, but one is expected
        for j in range ( 0, len(TESTSUITELIST) ):
            TESTSUITE = TESTSUITELIST[j]
            try:
                pass
                #validate that the schema provided in the test suite is itself OK
                # NOT USING SCHEMA WITHIN TEST SUITE FILE
                #if debug: print('DEBUG:', '[line ' + str(inspect.getframeinfo(inspect.currentframe()).lineno) + ']' , str(TESTSUITE),'.')
                #if debug: print('DEBUG:', str(TESTSUITE['schema']),'.')
                #jsonschema.validate(instance=TEST['schema'], schema=schema.json)
            except Exception as e:
                print('WARN:', ListOfTestFiles[i],'has a faulty schema item in array element',j,'.')
                print(str(e),'\n skipping...')
                continue
            else:
                pass
            finally:
                #validate each of the tests vs the schema
                testcount = len(TESTSUITE['tests'])
                for k in range (0, testcount ):
                    instance = TESTSUITE['tests'][k]
                    print('\n  Test [',k+1,'] >', str(instance['description']))

                   #perform inst test
                    INST = instance['data']
                    isVALID = instance['valid']
                    s = json.dumps(INST)

                    #check vs SUT
                    try:
                        jsonschema.validate(instance = INST, schema = SUT)
                    except Exception as e:
                        #if debug: print('  DEBUG: instance did NOT validate and validity flag is', isVALID)
                        if isVALID == True:
                            print('  WARN: instance is supposed to be VALID but FAILED.')
                            print('\n  DIAGNOSTIC: \n-------------------------------------\n',str(e),'\n-------------------------------------\n')
                            testsFailed += 1
                        else:
                            testsPassed += 1
                            #if debug: print('DEBUG:', s,'INVALID and FAILED (correct).')
                    else:
                        #if debug: print('  DEBUG: instance DID validate and validity flag is', isVALID)
                        if isVALID == True:
                            testsPassed += 1
                            #if debug: print('DEBUG:', s,'VALID and PASSED (correct).')
                        else:
                            testsFailed += 1
                            print('  WARN: this test instance:\n    ', s,'\n  is supposed to be INVALID but PASSED.')
                    finally:
                        continue

    print ('\n\nResults:\nOf', suitesRun + suitesBroken, 'test suites,', suitesBroken, 'were broken, leaving', suitesRun, 'to run.')
    print ('From those,', testsPassed + testsFailed, 'tests were run with', testsPassed, 'PASSED and', testsFailed, 'FAILED.')
    print ('\n\nDone.')

if __name__ == '__main__':
   main(sys.argv[1:])
   #print ('main exits silently')
