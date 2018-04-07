#!/usr/bin/env python
#  * @author Devb
#  * @License Apache 2.0
#
import logging
import time
from datetime import date, datetime

from flask import Flask
from flask.helpers import make_response
from flask_restful import Api, Resource
import urllib.request
import random

from consclient import *

app = Flask(__name__)
api = Api(app)

@app.route('/')
@api.representation('application/json')
class UrlaService(Resource):
    def get(self, appid):
        mortgageApp = Urla()
        # property type
        propertyType = PropertyType()
        propertyType.address1 = "24 Blackhole Dr"
        propertyType.address2 = ""
        propertyType.city = "Newton"
        propertyType.state = "NJ"
        propertyType.yearBuilt = 1990
        propertyType.legalDescription = "Colonial, east facing property 16, lot 18"
        propertyType.numberOfUnits = 2
        propertyType.county = ""
        propertyType.zipCode = "07870"
        mortgageApp.property = propertyType

        purposeType = PurposeType()
        # construction
        constructionType = ConstructionType()
        constructionType.amountExistingLiens = 90000.00
        constructionType.costOfImprovements = 22335.68
        constructionType.originalCost = 160000.00
        constructionType.presentValueOfLot = 190000.00
        constructionType.yearLotAcquired = 1976
        # purpose
        purposeType.construction = constructionType
        purposeType.estateHeld = EstateHeld.FEESIMPLE
        purposeType.estateHeldDescription = "Held in simple way"
        purposeType.mannerTitleHeld = None
        purposeType.purposeType = PurposeTypeEnum.PURCHASE
        # refinance
        refinanceType = RefinanceType()
        refinanceType.amountExistingLiens = 32000.0
        refinanceType.improvementCost = 21000.00
        refinanceType.improvements = 12000.00
        refinanceType.improvementType = Improvement_Type.CHANGES_MADE
        refinanceType.originalCost = 21000.00
        refinanceType.purpose = "Curb side improvement"
        refinanceType.yearAcquired = 1998
        purposeType.refinance = refinanceType
        purposeType.sourceOfDownPayment = "Bank financing"
        purposeType.titleHolderName = "Joe Smith"
        purposeType.typeDescription = "Refinance for Improvement"

        # transaction type
        tranType = TransactType()
        tranType.alterationsImprovements = 2500.32
        tranType.closingCosts = 678.63
        tranType.closingCostsSeller = 325.65
        tranType.discount = 0
        tranType.land = 100000
        tranType.loanAmount = 160000

        # other credits create the classes
        otherCreditType = OtherCreditType()

        # other credits
        otherCreditType.amount = 500.0
        otherCreditType.description = "Realtors Fee"

        # transaction type
        tranType.otherCreditType = otherCreditType
        tranType.pmi_MIP = 550.0
        tranType.pmi_MIP_Financed = 550.0
        tranType.prepaidItems = 1200.87
        tranType.purchasePrice = 170000.0
        tranType.refinance = 10000.0
        tranType.subordinateFinancing = 0.0

        # address type
        currentAddress = AddressType()
        currentAddress.addType = AddressEnum.CURRENT_ADDRESS
        currentAddress.propertyType = propertyType
        currentAddress.numberYears = 25
        currentAddress.address_1 = "300 Redmond Avenue"
        currentAddress.address_2 = ""
        currentAddress.city = "Rockaway"
        currentAddress.state = "NJ"
        currentAddress.zipCode = "07866"

        previousAddress = AddressType()
        previousAddress.addType = AddressEnum.PREV_ADDRESS

        # add the address to the addressList

        # borrower type
        # primary borrower
        mainBorrower = BorrowerType()
        mainBorrower.address.append(currentAddress)
        mainBorrower.address.append(previousAddress)

        dateBirth = date(1963, 7, 12)
        mainBorrower.dateOfBirth = dateBirth
        # declarations
        declarations = DeclarationsType()
        declarations.anyJudgments = False
        declarations.borrowedDownPayment = False
        declarations.coMakerNote = False
        declarations.declaredBankrupt = False
        declarations.delinquent = False
        declarations.lawsuit = False
        declarations.obligatedOnAnyLoan = False
        declarations.obligatedToPayAlimony = False
        declarations.ownershipInterest = False
        declarations.permanentResident = False
        declarations.primaryResidence = False
        declarations.propertyForeclosed = False
        declarations.propertyType = PropertyTypeEnum.PRINCIPAL_RESIDENCE
        mainBorrower.declarations = declarations

        # dependents
        dependents = Dependents()
        dependents.name = "Mary Smith"
        dependents.age = 55.6
        mainBorrower.dependents.append(dependents)
        # employment
        employmentType = EmploymentType()
        employer = Employer()
        employer.name = "Blockchain Inc"
        # employment address
        employerAddress = AddressType()
        employer.address.append(employerAddress)
        employmentType.businessPhone = "8001230000"
        employmentType.yearsInProfession = 20

        # date time functions
        dateTo = date.today()
        dateFrom = date(2002, 1, 1)
        employmentType.dateFrom = dateFrom
        employmentType.dateTo = dateTo
        employmentType.employer = employer
        employmentType.isSelfEmployed = False
        employmentType.monthlyIncome = 12000.0
        employmentType.position = "Director"
        employmentType.title = "Director"
        employmentType.typeOfBusiness = "Software Development"
        mainBorrower.employment = employmentType

        # continuing with borrower type
        mainBorrower.firstName = "Joe"
        mainBorrower.lastName = "Smith"
        mainBorrower.middleName = None
        # Marital status
        mainBorrower.borrower = BorrowerEnum.BORROWER
        mainBorrower.maritalStatus = MaritalStatus.MARRIED
        mainBorrower.setphone("9735122222")
        mainBorrower.setssn("890867543")
        mainBorrower.title = "Jr."
        mainBorrower.yearsSchool = 22
        # Income type
        incomeType = IncomeType()
        incomeType.baseEmployment = 200000.0
        incomeType.bonuses = 12000.0
        incomeType.commissions = 4000.0
        incomeType.dividendsInterest = 575.0
        incomeType.netRentalIncome = 10000.0
        incomeType.other1 = 345.0
        incomeType.other2 = 0.0
        # Other income type
        otherIncomeType = OtherIncomeType()
        otherIncomeType.amount = 0.0
        otherIncomeType.description = "None"
        incomeType.otherIncome = otherIncomeType
        incomeType.otherIncomeSources = 0.0
        incomeType.overtime = 600.0
        mainBorrower.income = incomeType

        # government monitoring
        governmentMonitoringType = GovernmentMonitoringType()
        governmentMonitoringType.race = Ethnicity.WHITE
        governmentMonitoringType.sex = Gender.MALE
        mainBorrower.governmentMonitoring = governmentMonitoringType

        # Second borrower or co-borrower
        coBorrower = BorrowerType()
        coBorrower.address.append(currentAddress)
        dateBirth = date(1969, 11, 19)
        coBorrower.dateOfBirth = dateBirth
        coBorrower.declarations = declarations
        coBorrower.dependents.append(dependents)
        coBorrower.employment = EmploymentType()
        # continuing with borrower type
        coBorrower.firstName = "Jane"
        coBorrower.lastName = "Smith"
        coBorrower.middleName = "Diana"
        # Marital status
        coBorrower.Borrower = BorrowerEnum.CO_BORROWER
        coBorrower.maritalStatus = MaritalStatus.MARRIED
        coBorrower.setphone("9735122222")
        coBorrower.setssn("890865123")
        coBorrower.ssn1 = coBorrower.getssn(coBorrower.ssn)
        coBorrower.title = ""
        coBorrower.yearsSchool = 23
        # government monitoring
        gmt2 = GovernmentMonitoringType()
        gmt2.race = Ethnicity.AFRICAN_AMERICAN
        gmt2.sex = Gender.FEMALE
        coBorrower.governmentMonitoring = gmt2

        currentTime = date.today()
        # main mortgage application
        mortgageApp.agencyCaseNumber = "00137689"
        mortgageApp.amortizationTypeDescription = "Mortgage"
        mortgageApp.amount = 200000.56
        mortgageApp.applicationID = "001"
        mortgageApp.dateCreated = currentTime
        mortgageApp.interestRate = 2.55
        mortgageApp.lenderCaseNumber = "012356"
        mortgageApp.numberOfMonths = 240
        mortgageApp.otherIncomeIncluded = True
        mortgageApp.otherLiabilitiesIncluded = True
        # assign purpose
        mortgageApp.purpose = purposeType
        mortgageApp.representativeId = 12001
        mortgageApp.sourceIdentifier = "1324"
        # set the mortageapp to transaction type
        mortgageApp.transactionType = tranType

        mortgageApp.borrower = mainBorrower
        mortgageApp.coborrower = coBorrower

        # all assets and liabilities
        al = AssetsLiabilities()

        # alimony child support
        alim = AlimonyChildSupport()
        alim.monthlyPayment = 0
        alim.monthsLeft = 0
        alim.owedTo = 0
        al.alimonyChildSupport = alim

        # assets
        assets = AssetType()
        assets.amount = 12000
        assets.description = "Life savings"

        # checkings and savings
        checkSavingsArrayList = []
        checkSavings = CheckingSavingsAccount()
        checkSavings.accountNumber = "10001001"
        checkSavings.accountSequence = 1
        checkSavingsAddress = AddressType()
        checkSavingsAddress.address_1 = "101 Broadway"
        checkSavingsAddress.address_2 = ""
        checkSavingsAddress.city = "New York"
        checkSavingsAddress.state = "NY"
        checkSavingsAddress.zipCode = 10001
        checkSavings.bankAddress = checkSavingsAddress
        al.checkingsavings = checkSavings
        checkSavingsArrayList.append(checkSavings)

        # cash deposit
        cashDepositArrayList = []
        cashDepositType = CashDepositType()
        cashDepositType.description = "Deposit 1"
        cashDepositType.amount = 10000
        cashDepositArrayList.append(cashDepositType)
        al.cashDeposit = cashDepositArrayList

        # credit received
        creditReceivedArray = []
        creditReceived = CreditReceivedType()
        creditReceived.accountNumber = "2000-3345-6666-7765"
        creditReceived.alternateName = "Credit Card X"
        creditReceived.creditorName = "Bank of Mars-Moon"
        creditReceivedArray.append(creditReceived)
        al.creditReceived = creditReceivedArray

        # expense
        expenseArrayList = []
        expenseType = ExpenseType()
        expenseType.firstMortgage = 1200.0
        expenseType.hazardInsurance = 700
        expenseType.homeownersAssnDues = 0
        expenseType.mortgageInsurance = 300
        expenseType.other = 0
        expenseType.otherFinancing = 0
        expenseType.realEstateTaxes = 450
        expenseType.rent = 0
        expenseArrayList.append(expenseType)
        al.expense = expenseArrayList

        # other income type
        otherIncomeArrayList = []
        otherIncomeTypeCommon = OtherIncomeType()
        otherIncomeTypeCommon.description = "Other Income 1"
        otherIncomeTypeCommon.amount = 1000
        otherIncomeArrayList.append(otherIncomeTypeCommon)
        al.otherIncome = otherIncomeArrayList

        # job related expenses
        jobRelatedExpList = []
        jobRelatedExpense = JobRelatedExpenseType()
        jobRelatedExpense.description = "Job Expenses 1"
        jobRelatedExpense.monthlyPayment = 100
        jobRelatedExpense.monthsLeft = 12
        jobRelatedExpList.append(jobRelatedExpense)
        al.jobExpenses = jobRelatedExpList

        # Life insurance
        lifeInsuranceList = []
        li = LifeInsurance()
        li.faceAmount = 1000.0
        li.netCashvalue = 200000.0
        lifeInsuranceList.append(li)
        al.lifeInsurance = lifeInsuranceList

        # Stocks and bonds
        stockArrayList = []
        stockBondsAccType = StocksBondsAccountType()
        stockBondsAccType.accountSequence = 1
        stockBondsAccType.amount = 20000.0
        stockBondsAccType.description = "BLK Stocks"
        stockArrayList.append(stockBondsAccType)
        al.stocksBonds = stockArrayList

        mortgageApp.assetsLiabilities = al

        # return jsonpickle.encode(mortgageApp)
        msgjson = mortgageApp.tojjson()
        msg1 = mortgageApp.toJSON()
        print (msg1)

        fabric_cldata = {}
        fabric_prdata = {}
        url = "http://localhost:3000/api/"
        urlclt = url + "Client"
        urlprt = url + "Portfolio"

        fabric_cldata['$class'] = 'com.devb.consolidated.Client'
        clid = mortgageApp.agencyCaseNumber + str(random.randint(1,21)*5)
        fabric_cldata['clientId'] = clid
        fabric_cldata['name'] = mainBorrower.firstName + ' ' + mainBorrower.lastName
        
        self.postFabric(urlclt, fabric_cldata)

        fabric_prdata['$class'] = 'com.devb.consolidated.Portfolio'
        fabric_prdata['portfolioId'] = mortgageApp.lenderCaseNumber + str(random.randint(1,21)*5)
        fabric_prdata['client'] = 'com.devb.consolidated.Client#' + clid
        fabric_prdata['value'] = tranType.loanAmount
        fabric_prdata['jsonAsset'] = msg1

        self.postFabric(urlprt, fabric_prdata)

        return (msgjson)

    def postFabric(self, turl, tjson):
        request = urllib.request.Request(turl)
        # add appropriate header
        request.add_header('Content-Type','application/json; charset=utf-8')
        jsonSentData = json.dumps(tjson)
        jsonSentAsBytes = jsonSentData.encode('utf-8')   # change to bytes
        request.add_header('Content-Length', len(jsonSentAsBytes))
        print(jsonSentAsBytes)
        response = urllib.request.urlopen(request, jsonSentAsBytes)
        return response
        

@app.errorhandler(404)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'Mortgage URL Application: An internal error occurred.', 404


api.add_resource(UrlaService, '/mortgage/webapi/urla/<string:appid>')

if __name__ == '__main__':
    app.run(debug=True)
