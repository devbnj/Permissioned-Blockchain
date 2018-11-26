import urllib.request
import json

cltjson = {"$class": "com.devb.consolidated.Client", "clientId": "9998", "name": "trial"}
prtjson = {"$class": "com.devb.consolidated.Portfolio", 
   "portfolioId": "9998", 
   "jsonAsset": '{"agencyCaseNumber": "00137689", "amortizationTypeDescription": "Mortgage", "amount": 200000.56, "applicationID": "001", "assetsLiabilities": {"cashDeposit": [{"amount": 10000, "description": "Deposit 1"}], "checkingsavings": {"accountNumber": "10001001", "accountSequence": 1, "bankAddress": {"address_1": "101 Broadway", "address_2": "", "city": "New York", "state": "NY", "zipCode": 10001}}, "creditReceived": [{"accountNumber": "2000-3345-6666-7765", "alternateName": "Credit Card X", "creditorName": "Bank of Mars-Moon"}], "expense": [{"firstMortgage": 1200.0, "hazardInsurance": 700, "homeownersAssnDues": 0, "mortgageInsurance": 300, "other": 0, "otherFinancing": 0, "realEstateTaxes": 450, "rent": 0}], "jobExpenses": [{"description": "Job Expenses 1", "monthlyPayment": 100, "monthsLeft": 12}], "lifeInsurance": [{"faceAmount": 1000.0, "netCashvalue": 200000.0}], "otherIncome": [{"amount": 1000, "description": "Other Income 1"}], "stocksBonds": [{"accountSequence": 1, "amount": 20000.0, "description": "BLK Stocks"}]}, "borrower": {"borrower": "BORROWER", "dateOfBirth": "1963-07-12", "declarations": {"anyJudgments": false, "borrowedDownPayment": false, "coMakerNote": false, "declaredBankrupt": false, "delinquent": false, "lawsuit": false, "obligatedOnAnyLoan": false, "obligatedToPayAlimony": false, "ownershipInterest": false, "permanentResident": false, "primaryResidence": false, "propertyForeclosed": false, "propertyType": "PRINCIPAL_RESIDENCE"}, "employment": {"businessPhone": "8001230000", "dateFrom": "2002-01-01", "dateTo": "2018-04-06", "employer": {"name": "Blockchain Inc"}, "isSelfEmployed": false, "monthlyIncome": 12000.0, "position": "Director", "title": "Director", "typeOfBusiness": "Software Development", "yearsInProfession": 20}, "firstName": "Joe", "governmentMonitoring": {"race": "WHITE", "sex": "MALE"}, "income": {"baseEmployment": 200000.0, "bonuses": 12000.0, "commissions": 4000.0, "dividendsInterest": 575.0, "netRentalIncome": 10000.0, "other1": 345.0, "other2": 0.0, "otherIncome": {"amount": 0.0, "description": "None"}, "otherIncomeSources": 0.0, "overtime": 600.0}, "lastName": "Smith", "maritalStatus": "MARRIED", "middleName": null, "phone": "amlmaWZoaWprYg==", "ssn": "aWtjbGttbGxs", "title": "Jr.", "yearsSchool": 22}, "coborrower": {"Borrower": "CO_BORROWER", "dateOfBirth": "1969-11-19", "declarations": {}, "employment": {}, "firstName": "Jane", "lastName": "Smith", "maritalStatus": "MARRIED", "middleName": "Diana", "phone": "amlmaWZoaWprYg==", "ssn": "aWtjbGtraGps", "ssn1": "890865123", "title": "", "yearsSchool": 23}, "dateCreated": "2018-04-06", "interestRate": 2.55, "lenderCaseNumber": "012356", "numberOfMonths": 240, "otherIncomeIncluded": true, "otherLiabilitiesIncluded": true, "property": {"address1": "24 Blackhole Dr", "address2": null, "city": "Newton", "county": null, "legalDescription": "Colonial, east facing property 16, lot 18", "numberOfUnits": 2, "state": "NJ", "yearBuilt": 1990, "zipCode": "07870"}, "purpose": {"construction": {"amountExistingLiens": 90000.0, "costOfImprovements": 22335.68, "originalCost": 160000.0, "presentValueOfLot": 190000.0, "yearLotAcquired": 1976}, "estateHeld": "FEESIMPLE", "estateHeldDescription": "Held in simple way", "mannerTitleHeld": null, "purposeType": "PURCHASE", "refinance": {"amountExistingLiens": 32000.0, "improvementCost": 21000.0, "improvementType": "CHANGES_MADE", "improvements": 12000.0, "originalCost": 21000.0, "purpose": "Curb side improvement", "yearAcquired": 1998}, "sourceOfDownPayment": "Bank financing", "titleHolderName": "Joe Smith", "typeDescription": "Refinance for Improvement"}, "representativeId": 12001, "sourceIdentifier": "1324", "transactionType": {"alterationsImprovements": 2500.32, "closingCosts": 678.63, "closingCostsSeller": 325.65, "discount": 0, "land": 100000, "loanAmount": 160000, "otherCreditType": {"amount": 500.0, "description": "Realtors Fee"}, "pmi_MIP": 550.0, "pmi_MIP_Financed": 550.0, "prepaidItems": 1200.87, "purchasePrice": 170000.0, "refinance": 10000.0, "subordinateFinancing": 0.0}}',  
   "client": "com.devb.consolidated.Client#9998",  
   "value": 9999 }


urlclt = "http://localhost:3000/api/Client"
urlprt = "http://localhost:3000/api/Portfolio"

# create the request
request = urllib.request.Request(urlprt)

# add appropriate header

request.add_header('Content-Type','application/json; charset=utf-8')
jsonSentData = json.dumps(prtjson)
jsonSentAsBytes = jsonSentData.encode('utf-8')   # change to bytes
request.add_header('Content-Length', len(jsonSentAsBytes))
print(jsonSentAsBytes)
response = urllib.request.urlopen(request, jsonSentAsBytes)
