def find_cases(line):
    caseOne = line.find('FindAsync(')
    caseTwo = line.find('ReadAsStringAsync(')
    caseThree = line.find('SendAsync(')
    caseFour = line.find('Status(')
    caseFive = line.find('RunAzureIndexerAsync')
    caseSix = line.find('GetAuthorizeResponse')
    caseSeven = line.find('Register')
    caseEight = line.find('ExecuteAsync')
    caseNine = line.find('DeviceUnblock')
    caseTen = line.find('SendReceiveAsync')
    caseEleven = line.find('GetDocAsync')
    caseTwelve = line.find('SubscribeAsync')
    caseThirteen = line.find('GetBalanceAsync')
    caseFourteen = line.find('GetUserPaymentSourcePayloadAsync')
    caseFifteen = line.find('GetDocsAsync')
    caseSixteen = line.find('Complete')
    caseSeventeen = line.find('ReadAsStringAsync')
    caseEighteen = line.find('BuildLoyaltyCardResponseWithUsernameAsync')
    caseNineteen = line.find('GetCards')
    caseTwenty = line.find('RunAsync')
    caseTwentyOne = line.find('GetCaptureResponse')
    caseTwentyTwo = line.find('CreateStacDoc')
    caseTwentyThree = line.find('LinkAccountAsync')
    caseTwentyFour = line.find('GetTenantSupportCardDocAsync')
    caseTwentyFive = line.find('UploadTextAsync')
    caseTwentySix = line.find('GetSecretValueIfExists')
    caseTwentySeven = line.find('GetStoreAzureModels')
    caseTwentyEight = line.find('ReadAsStreamAsync')
    caseTwentyNine = line.find('offersTask')

    if caseOne != -1:
        return caseOne
    elif caseTwo != -1:
        return caseTwo
    elif caseThree != -1: 
        return caseThree
    elif caseFour != -1:
        return caseFour
    elif caseFive != -1:
        return caseFive
    elif caseSix != -1:
        return caseSix
    elif caseSeven != -1:
        return caseSeven
    elif caseEight != -1:
        exceptionCase = line.find('await')
        if exceptionCase != -1:
            if exceptionCase > caseEight:
                return exceptionCase + 6
        return caseEight
    elif caseNine != -1:
        return caseNine
    elif caseTen != -1:
        return caseTen
    elif caseEleven != -1:
        return caseEleven
    elif caseTwelve != -1:
        return caseTwelve
    elif caseThirteen != -1:
        return caseThirteen
    elif caseFourteen != -1:
        return caseFourteen
    elif caseFifteen != -1:
        return caseFifteen
    elif caseSixteen != -1:
        return caseSixteen
    elif caseSeventeen != -1:
        return caseSeventeen
    elif caseEighteen != -1:
        return caseEighteen
    elif caseNineteen != -1:
        return caseNineteen
    elif caseTwenty != -1:
        return caseTwenty
    elif caseTwentyOne != -1:
        return caseTwentyOne
    elif caseTwentyTwo != -1:
        return caseTwentyTwo
    elif caseTwentyThree != -1:
        return caseTwentyThree
    elif caseTwentyFour != -1:
        return caseTwentyFour
    elif caseTwentyFive != -1:
        return caseTwentyFive
    elif caseTwentySix != -1:
        return caseTwentySix
    elif caseTwentySeven != -1:
        return caseTwentySeven
    elif caseTwentyEight != -1:
        return caseTwentyEight
    elif caseTwentyNine != -1:
        return caseTwentyNine
    else:
        return 999