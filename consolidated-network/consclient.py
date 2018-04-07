#!/usr/bin/env python
#  * @author Devb
#  * @License Apache 2.0
#
import json
from datetime import date
from json import JSONEncoder

from flask.helpers import make_response
from flask_restful import Api, Resource
import base64

def enum(**enums):
    return type('Enum', (), enums)

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

# Enums
EstateHeld = enum(FEESIMPLE='FEESIMPLE',
                  LEASEHOLD='LEASEHOLD')
BorrowerEnum = enum(BORROWER='BORROWER',
                    CO_BORROWER='CO_BORROWER')
AddressEnum = enum(
    CURRENT_ADDRESS='CURRENT_ADDRESS',
    PREV_ADDRESS='PREV_ADDRESS',
    WORK_ADDRESS='WORK_ADDRESS',
    COMMERCIAL_ADDRESS='COMMERCIAL_ADDRESS')
Ethnicity = enum(WHITE='WHITE',              AFRICAN_AMERICAN='AFRICAN_AMERICAN',
                 ASIAN='ASIAN',
                 HISPANIC='HISPANIC',
                 LATINO='LATINO',
                 MIDDLE_EAST='MIDDLE_EAST')
Gender = enum(
    MALE='MALE', FEMALE='FEMALE',
    UNKNOWN='UNKNOWN')
MaritalStatus = enum(
    MARRIED='MARRIED',
    SINGLE='SINGLE', DIVORCED='DIVORCED',
    WIDOWED='WIDOWED')
Improvement_Type = enum(
    CHANGES_MADE='CHANGES_MADE',
    CHANGES_TOBEMADE='CHANGES_TOBEMADE',
    NONE='NONE')
PropertyTypeEnum = enum(
    INVESTMENT_PROPERTY='INVESTMENT_PROPERTY',
    PRINCIPAL_RESIDENCE='PRINCIPAL_RESIDENCE',
    SECOND_HOME='SECOND_HOME',
    NOT_SPECIFIED='NOT_SPECIFIED')
PurposeTypeEnum = enum(
    CONSTRUCTION='CONSTRUCTION',
    CONSTRUCTION_PERMANENT='CONSTRUCTION_PERMANENT',
    PURCHASE='PURCHASE',
    REFINANCE='REFINANCE',
    OTHER='OTHER')
# End Enums

secret_key = '1234567890123456' 

# DEF CLASS
class AlimonyChildSupport(object):
    monthlyPayment = float()
    monthsLeft = float()
    owedTo = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class AddressType(object):
    address_1 = None
    address_2 = None
    city = None
    numberYears = int()
    state = None
    zipCode = int()
    propertyType = None
    numberYears = int()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class AssetType(object):
    amount = float()
    description = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class AssetsLiabilities(object):
    alimonyChildSupport = AlimonyChildSupport()
    asset = AssetType()
    automobile = None
    businessOwned = float()
    cashDeposit = None
    checkingSavings = None
    creditPrevious = None
    jobRelatedExpense = None
    liability = None
    lifeInsurance = None
    realEstate = None
    realEstateOwned = float()
    retirementFund = float()
    stocksBonds = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class AutomobileType(object):
    amount = float()
    autoSequence = int()
    description = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class BorrowerType(object):
    address = []  # list of addresstype
    borrower = None
    dateOfBirth = date
    declarations = None
    dependents = []
    employment = None
    firstName = None
    governmentMonitoring = None
    income = None
    lastName = None
    maritalStatus = None
    middleName = None
    title = None
    yearsSchool = int()
    phone = None
    ssn = None

    def __init__(self):
        """ method __init__ """

    def setssn(self, value):
        self.ssn = encode(secret_key, str(value))

    def getssn(self, value):    
        return decode(secret_key, self.ssn)

    def setphone(self, newphone):
        self.phone = encode(secret_key, str(newphone))

    def getphone(self, value):    
        return decode(secret_key, self.phone)
# UNDEF CLASS

# DEF CLASS
class CashDepositType(object):
    amount = float()
    description = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class CheckingSavingsAccount(object):
    accountNumber = None
    accountSequence = int()
    bankAddress = AddressType()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class ConstructionType(object):
    amountExistingLiens = float()
    costOfImprovements = float()
    originalCost = float()
    presentValueOfLot = float()
    yearLotAcquired = int()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class CreditReceivedType(object):
    accountNumber = None
    alternateName = None
    creditorName = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class DeclarationsType(object):
    anyJudgments = bool()
    borrowedDownPayment = bool()
    coMakerNote = bool()
    declaredBankrupt = bool()
    delinquent = bool()
    lawsuit = bool()
    obligatedOnAnyLoan = bool()
    obligatedToPayAlimony = bool()
    ownershipInterest = bool()
    permanentResident = bool()
    primaryResidence = bool()
    propertyForeclosed = bool()
    propertyType = None
    titleHeld = None
    uS_Citizen = bool()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class Dependents(object):
    age = float()
    name = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class EmploymentType(object):
    businessPhone = None
    dateFrom = None
    dateTo = None
    employer = None
    isSelfEmployed = bool()
    monthlyIncome = float()
    position = None
    title = None
    typeOfBusiness = None
    yearsInProfession = float()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class Employer(object):
    address = []
    name = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class ExpenseType(object):
    firstMortgage = float()
    hazardInsurance = float()
    homeownersAssnDues = float()
    mortgageInsurance = float()
    other = float()
    otherFinancing = float()
    realEstateTaxes = float()
    rent = float()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class GovernmentMonitoringType(object):
    race = Ethnicity
    sex = Gender

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class IncomeType(object):
    baseEmployment = float()
    bonuses = float()
    commissions = float()
    dividendsInterest = float()
    netRentalIncome = float()
    other1 = float()
    other2 = float()
    otherIncome = None
    otherIncomeSources = float()
    overtime = float()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class JobRelatedExpenseType(object):
    description = None
    monthlyPayment = float()
    monthsLeft = int()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class LiabilityType(object):
    accountNumber = None
    address = None
    isToBePaidOff = bool()
    liabilitySequence = int()
    monthlyPayment = float()
    monthsLeft = int()
    name = None
    unpaidBalance = float()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class LifeInsurance(object):
    faceAmount = float()
    netCashvalue = float()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class OtherCreditType(object):
    amount = float()
    description = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class OtherIncomeType(object):
    amount = float()
    description = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class PropertyType(object):
    address1 = None
    address2 = None
    city = None
    county = None
    legalDescription = None
    numberOfUnits = int()
    state = None
    yearBuilt = int()
    zipCode = int()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class PurposeType(object):
    construction = None
    estateHeld = None
    estateHeldDescription = None
    mannerTitleHeld = None
    purposeType = None
    refinance = None
    sourceOfDownPayment = None
    titleHolderName = None
    typeDescription = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class RealEstatePropertyType(object):
    address = None
    grossRental = float()
    insuranceMisc = float()
    marketValue = float()
    mortgageLiens = float()
    mortgagePayments = float()
    netRental = float()
    propertySequence = int()
    status = None
    type_ = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class RefinanceType(object):
    amountExistingLiens = float()
    improvementCost = float()
    improvements = float()
    improvementType = None
    originalCost = float()
    purpose = None
    yearAcquired = int()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class StocksBondsAccountType(object):
    accountSequence = int()
    amount = float()
    description = None

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# DEF CLASS
class TransactType(object):
    alterationsImprovements = float()
    closingCosts = float()
    closingCostsSeller = float()
    discount = float()
    land = float()
    loanAmount = float()
    otherCreditType = OtherCreditType()
    pmi_MIP = float()
    pmi_MIP_Financed = float()
    prepaidItems = float()
    purchasePrice = float()
    refinance = float()
    subordinateFinancing = float()

    def __init__(self):
        """ method __init__ """
# UNDEF CLASS

# MAIN CLASS
# DEF CLASS
class Urla(object):
    agencyCaseNumber = None
    amortizationTypeDescription = None
    amount = float()
    applicationID = None
    dateCreated = None
    interestRate = float()
    lenderCaseNumber = None
    numberOfMonths = int()
    otherIncomeIncluded = bool()
    otherLiabilitiesIncluded = bool()
    residentialproperty = None
    purpose = PurposeType()
    representativeId = int()
    sourceIdentifier = None
    transactionType = None
    typeDescription = None
    borrower = BorrowerType()
    coborrower = BorrowerType()
    assetLiabilities = None
    employment = None

    def __init__(self):
        ''' method __init__ '''

    def toJSON(self):
        instDict = json.dumps(self.__dict__, sort_keys=False, default=mortgage_json_handler)
        return instDict

    def tojjson(self):
        resp = make_response(json.dumps(self.__dict__, sort_keys=False, default=mortgage_json_handler))
        # if there is a need
        # resp.headers.extend({})
        return resp

    def output_json(self, code, headers=None):
        resp = make_response(json.dumps(self), code)
        resp.headers.extend(headers or {})
        return resp
# UNDEF CLASS

def mortgage_json_handler(x):
    if isinstance(x, date):
        return x.isoformat()
    if isinstance(x, AddressType):
        return x.__dict__
    if isinstance(x, AlimonyChildSupport):
        return x.__dict__
    if isinstance(x, AssetsLiabilities):
        return x.__dict__
    if isinstance(x, AssetType):
        return x.__dict__
    if isinstance(x, BorrowerType):
        return x.__dict__
    if isinstance(x, CashDepositType):
        return x.__dict__
    if isinstance(x, CheckingSavingsAccount):
        return x.__dict__
    if isinstance(x, ConstructionType):
        return x.__dict__
    if isinstance(x, CreditReceivedType):
        return x.__dict__
    if isinstance(x, DeclarationsType):
        return x.__dict__
    if isinstance(x, Dependents):
        return x.__dict__
    if isinstance(x, EmploymentType):
        return x.__dict__
    if isinstance(x, Employer):
        return x.__dict__
    if isinstance(x, ExpenseType):
        return x.__dict__
    if isinstance(x, GovernmentMonitoringType):
        return x.__dict__
    if isinstance(x, IncomeType):
        return x.__dict__
    if isinstance(x, JobRelatedExpenseType):
        return x.__dict__
    if isinstance(x, LifeInsurance):
        return x.__dict__
    if isinstance(x, OtherCreditType):
        return x.__dict__
    if isinstance(x, OtherIncomeType):
        return x.__dict__
    if isinstance(x, PropertyType):
        return x.__dict__
    if isinstance(x, PurposeType):
        return x.__dict__
    if isinstance(x, RefinanceType):
        return x.__dict__
    if isinstance(x, StocksBondsAccountType):
        return x.__dict__
    if isinstance(x, TransactType):
        return x.__dict__
    raise TypeError(str(x) + " Unknown type")
# the end
