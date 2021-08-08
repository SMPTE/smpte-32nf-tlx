#!/usr/bin/env python3

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
testSchemaFilename = 'test-schema.json'
# TODO: the test suite includes a "schema" parameter for each collection of tests,
#       but for now, we're not using that.  (Need to set up the resolver code to trace the $ref).

def showUsage():
    print ('USAGE: schemaTest.py [-h][-d] [-s <schemaUnderTestFile> [ <testSuiteFile>]* ]' )
    print (' Validates the schemaUnderTestFile, then tests with zero or more testSuiteFile(s)')
    print (' -d prints debug hints')

def main(argv):
    debug = 0
    firstArg = 0  # with no options, SUT is agrv[0]
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
            firstArg += 1
            
    if len(argv) < firstArg + 1:
        print ('ERR: too few arguments')
        showUsage()
        sys.exit(2)
        
    # load the schema under test (SUT)
    try:
        with open(argv[firstArg]) as schemaUnderTestFile:
            SUT = json.load(schemaUnderTestFile)
            schemaUnderTestFile.close()
            #if debug: print ('DEBUG: 1st arg', argv[firstArg], ' (SUT) seems OK.')
    except Exception as e:
        print('ERR:',argv[firstArg],'is missing or poorly formed JSON')
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
    for i in range ( firstArg + 1, len(argv) ):
        #if debug: print ('DEBUG: loading test suite',argv[i],'for preliminary checks')
        try:
            with open(argv[i]) as currentTestSet:
                try:
                    #if debug: print('DEBUG: verifying test suite file', argv[i],'.')
                    TESTSUITELIST = json.load(currentTestSet)
                except Exception as e:
                    print('WARN: Can\'t parse JSON for test suite', argv[i],'.')
                    print(str(e),'\n skipping...')
                else:
                    try:
                        jsonschema.validate( instance=TESTSUITELIST, schema=TESTSCHEMA)
                    except Exception as e:
                        print('WARN:', argv[i],'isn\'t a well-formed test suite.')
                        print(str(e),'\n skipping...')
                currentTestSet.close()
        except Exception as e:
            print('WARN: Could not read test suite file', argv[i],'.')
            print(str(e),'\n skipping...')

    # now reopen and run each test suite
    for i in range ( firstArg + 1, len(argv) ):
        #if debug: print ('DEBUG: re-loading test suite file',argv[i])
        try:
            with open(argv[i]) as currentTestSet:
                try:
                    #if debug: print('DEBUG: re-verifying test suite', argv[i],'.')
                    TESTSUITELIST = json.load(currentTestSet)
                    currentTestSet.close()
                except Exception as e:
                    print('WARN: Can\'t parse JSON for test suite', argv[i],'.')
                    print(str(e),'\n skipping...')
                    continue
                else:
                    try:
                        jsonschema.validate( instance=TESTSUITELIST, schema=TESTSCHEMA)
                    except Exception as e:
                        print('WARN:', argv[i],'isn\'t a well-formed test suite.')
                        print(str(e),'\n skipping...')
                        continue
        except Exception as e:
            print('WARN: Could not read test suite file', argv[i],'.')
            print(str(e),'\n skipping...')

        print('\nSuite', argv[i], '(', TESTSUITELIST['description'], ')' )
        
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
                print('WARN:', argv[i],'has a faulty schema item in array element',j,'.')
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
                        else:
                            pass
                            #if debug: print('DEBUG:', s,'INVALID and FAILED (correct).')
                    else:
                        #if debug: print('  DEBUG: instance DID validate and validity flag is', isVALID)
                        if isVALID == True:
                            pass
                            #if debug: print('DEBUG:', s,'VALID and PASSED (correct).')
                        else:
                            print('  WARN: this test instance:\n    ', s,'\n  is supposed to be INVALID but PASSED.')
                    finally:
                        continue
    print ('DEBUG: done')
    
    #v = validate(instance= { "TLXptpTimestamp": { "ptpTime": [1,2] } }, schema=SUT)
    #print (v)
    #errors = sorted(v.iter_errors(instance), key=lambda e: e.schema_path)
    #print (errors)

if __name__ == '__main__':
   main(sys.argv[1:])
   print ('main exits silently')
