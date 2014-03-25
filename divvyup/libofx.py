#!/usr/bin/env python

import sys
from ctypes import *


c_time = c_long # Represents the 'time_t' type from C

#
# From libofx.h
#
# Defines
#

OFX_ELEMENT_NAME_LENGTH        = 100
OFX_SVRTID2_LENGTH             = 36 + 1
OFX_CHECK_NUMBER_LENGTH        = 12 + 1
OFX_REFERENCE_NUMBER_LENGTH    = 32 + 1
OFX_FITID_LENGTH               = 255 + 1
OFX_TOKEN2_LENGTH              = 36 + 1
OFX_MEMO_LENGTH                = 255 + 1
OFX_FIID_LENGTH                = 32 + 1
OFX_MEMO2_LENGTH               = 390 + 1
OFX_BALANCE_NAME_LENGTH        = 32 + 1
OFX_BALANCE_DESCRIPTION_LENGTH = 80 + 1
OFX_CURRENCY_LENGTH            = 3 + 1
OFX_BANKID_LENGTH              = 9 + 1
OFX_BRANCHID_LENGTH            = 22 + 1
OFX_ACCTID_LENGTH              = 22 + 1
OFX_ACCTKEY_LENGTH             = 22 + 1
OFX_BROKERID_LENGTH            = 22 + 1
OFX_ACCOUNT_ID_LENGTH          = OFX_BANKID_LENGTH + \
                                 OFX_BRANCHID_LENGTH + \
                                 OFX_ACCTID_LENGTH + 1
OFX_ACCOUNT_NAME_LENGTH        = 255
OFX_MARKETING_INFO_LENGTH      = 360 + 1
OFX_TRANSACTION_NAME_LENGTH    = 32 + 1
OFX_UNIQUE_ID_LENGTH           = 32 + 1
OFX_UNIQUE_ID_TYPE_LENGTH      = 10 + 1
OFX_SECNAME_LENGTH             = 32 + 1
OFX_TICKER_LENGTH              = 32 + 1
OFX_ORG_LENGTH                 = 32 + 1
OFX_FID_LENGTH                 = 32 + 1
OFX_USERID_LENGTH              = 32 + 1
OFX_USERPASS_LENGTH            = 32 + 1
OFX_URL_LENGTH                 = 500 + 1
OFX_APPID_LENGTH               = 32
OFX_APPVER_LENGTH              = 32
OFX_HEADERVERSION_LENGTH       = 32

OFX_AMOUNT_LENGTH     = 32 + 1
OFX_PAYACCT_LENGTH    = 32 + 1
OFX_STATE_LENGTH      = 5 + 1
OFX_POSTALCODE_LENGTH = 11 + 1
OFX_NAME_LENGTH       = 32 + 1



#
# From libofx.h
#
# Enumerations
#

class LibofxFileFormat(c_int):
    AUTODETECT = 0
    OFX        = 1
    OFC        = 2
    QIF        = 3
    UNKNOWN    = 4
    LAST       = 5


class Severity(c_int):
    INFO  = 0
    WARN  = 1
    ERROR = 2


class AccountType(c_int):
    OFX_CHECKING   = 0
    OFX_SAVINGS    = 1
    OFX_MONEYMRKT  = 2
    OFX_CREDITLINE = 3
    OFX_CMA        = 4
    OFX_CREDITCARD = 5
    OFX_INVESTMENT = 6


class TransactionType(c_int):
    OFX_CREDIT      = 0
    OFX_DEBIT       = 1
    OFX_INT         = 2
    OFX_DIV         = 3
    OFX_FEE         = 4
    OFX_SRVCHG      = 5
    OFX_DEP         = 6
    OFX_ATM         = 7
    OFX_POS         = 8
    OFX_XFER        = 9
    OFX_CHECK       = 10
    OFX_PAYMENT     = 11
    OFX_CASH        = 12
    OFX_DIRECTDEP   = 13
    OFX_DIRECTDEBIT = 14
    OFX_REPEATPMT   = 15
    OFX_OTHER       = 16


class InvTransactionType(c_int):
    OFX_BUYDEBT        = 1
    OFX_BUYMF          = 1
    OFX_BUYOPT         = 2
    OFX_BUYOTHER       = 3
    OFX_BUYSTOCK       = 4
    OFX_CLOSUREOPT     = 5
    OFX_INCOME         = 6
    OFX_INVEXPENSE     = 7
    OFX_JRNLFUND       = 8
    OFX_JRNLSEC        = 9
    OFX_MARGININTEREST = 10
    OFX_REINVEST       = 11
    OFX_RETOFCAP       = 12
    OFX_SELLDEBT       = 13
    OFX_SELLMF         = 14
    OFX_SELLOPT        = 15
    OFX_SELLOTHER      = 16
    OFX_SELLSTOCK      = 17
    OFX_SPLIT          = 18
    OFX_TRANSFER       = 19


class FiIdCorrectionAction(c_int):
    DELETE  = 0
    REPLACE = 1


#
# From libofx.h
#
# Structures
#


class LibofxFileFormatInfo(Structure):
    _fields_ = [('format', LibofxFileFormat),
                ('format_name', c_char_p),
                ('description', c_char_p)]

    def __init__(self, format, format_name, description):
        self.format = format
        self.format_name = format_name
        self.description = description


class OfxStatusData(Structure):
    _fields_ = [('ofx_element_name', c_char * OFX_ELEMENT_NAME_LENGTH),
                ('ofx_element_name_valid', c_int),
                ('code', c_int),
                ('name', c_char_p),
                ('description', c_char_p),
                ('code_valid', c_int),
                ('severity_valid', Severity),
                ('server_message', c_char_p),
                ('server_message_valid', c_char_p)]


class OfxAccountData(Structure):
    _fields_ = [('account_id', c_char * OFX_ACCOUNT_ID_LENGTH),
                ('account_name', c_char * OFX_ACCOUNT_NAME_LENGTH),
                ('account_id_valid', c_int),
                ('account_type', AccountType),
                ('account_type_valid', c_int),
                ('currency', c_char * OFX_CURRENCY_LENGTH),
                ('currency_valid', c_int),
                ('account_number', c_char * OFX_ACCTID_LENGTH),
                ('account_number_valid', c_int),
                ('bank_id', c_char * OFX_BANKID_LENGTH),
                ('bank_id_valid', c_int),
                ('broker_id', c_char * OFX_BROKERID_LENGTH),
                ('broker_id_valid', c_int),
                ('branch_id', c_char * OFX_BRANCHID_LENGTH),
                ('branch_id_valid', c_int)]


class OfxSecurityData(Structure):
    _fields_ = [('unique_id', c_char * OFX_UNIQUE_ID_LENGTH),
                ('unique_id_valid', c_int),
                ('unique_id_type', c_char * OFX_UNIQUE_ID_TYPE_LENGTH),
                ('unique_id_type_valid', c_int),
                ('secname', c_char * OFX_SECNAME_LENGTH),
                ('secname_valid', c_int),
                ('ticker', c_char * OFX_TICKER_LENGTH),
                ('ticker_valid', c_int),
                ('unitprice', c_double),
                ('unitprice_valid', c_int),
                ('date_unitprice', c_time),
                ('date_unitprice_valid', c_int),
                ('currency', c_char * OFX_CURRENCY_LENGTH),
                ('currency_valid', c_int),
                ('memo', c_char * OFX_MEMO2_LENGTH),
                ('memo_valid', c_int),
                ('fiid', c_char * OFX_FIID_LENGTH),
                ('fiid_valid', c_int)]


class OfxTransactionData(Structure):
    _fields_ = [('account_id', c_char * OFX_ACCOUNT_ID_LENGTH),
                ('account_ptr', POINTER(OfxAccountData)),
                ('account_id_valid', c_int),
                ('transactiontype', TransactionType),
                ('transactiontype_valid', c_int),
                ('invtransactiontype', InvTransactionType),
                ('invtransactiontype_valid', c_int),
                ('units', c_double),
                ('units_valid', c_int),
                ('unitprice', c_double),
                ('unitprice_valid', c_int),
                ('amount', c_double),
                ('amount_valid', c_int),
                ('fi_id', c_char * 256),
                ('fi_id_valid', c_int),
                ('unique_id', c_char * OFX_UNIQUE_ID_LENGTH),
                ('unique_id_valid', c_int),
                ('unique_id_type', c_char * OFX_UNIQUE_ID_TYPE_LENGTH),
                ('unique_id_type_valid', c_int),
                ('security_data_ptr', POINTER(OfxSecurityData)),
                ('security_data_valid', c_int),
                ('date_posted', c_time),
                ('date_posted_valid', c_int),
                ('date_initiated', c_time),
                ('date_initiated_valid', c_int),
                ('date_funds_available', c_time),
                ('date_funds_available_valid', c_int),
                ('fi_id_corrected', c_char * 256),
                ('fi_id_corrected_valid', c_int),
                ('fi_id_correction_action', FiIdCorrectionAction),
                ('fi_id_correction_action_valid', c_int),
                ('server_transaction_id', c_char * OFX_SVRTID2_LENGTH),
                ('server_transaction_id_valid', c_int),
                ('check_number', c_char * OFX_CHECK_NUMBER_LENGTH),
                ('check_number_valid', c_int),
                ('reference_number', c_char * OFX_REFERENCE_NUMBER_LENGTH),
                ('reference_number_valid', c_int),
                ('standard_industrial_code', c_long),
                ('standard_industrial_code_valid', c_int),
                ('payee_id', c_char * OFX_SVRTID2_LENGTH),
                ('payee_id_valid', c_int),
                ('name', c_char * OFX_TRANSACTION_NAME_LENGTH),
                ('name_valid', c_int),
                ('memo', c_char * OFX_MEMO2_LENGTH),
                ('memo_valid', c_int),
                ('commision', c_double),
                ('commision_valid', c_int),
                ('fees', c_double),
                ('fees_valid', c_int),
                ('oldunits', c_double),
                ('oldunits_valid', c_int),
                ('newunits', c_double),
                ('newunits_valid', c_int)]


class OfxStatementData(Structure):
    _fields_ = [('currency', c_char * OFX_CURRENCY_LENGTH),
                ('currency_valid', c_int),
                ('account_id', c_char * OFX_ACCOUNT_ID_LENGTH),
                ('account_ptr', POINTER(OfxAccountData)),
                ('account_id_valid', c_int),
                ('ledger_balance', c_double),
                ('ledger_balance_valid', c_int),
                ('ledger_balance_date', c_time),
                ('ledger_balance_date_valid', c_int),
                ('available_balance', c_double),
                ('available_balance_valid', c_int),
                ('available_balance_date', c_time),
                ('available_balance_date_valid', c_int),
                ('date_start', c_time),
                ('date_start_valid', c_int),
                ('date_end', c_time),
                ('date_end_valid', c_int),
                ('marketing_info', c_char * OFX_MARKETING_INFO_LENGTH),
                ('marketing_info_valid', c_int)]


class OfxCurrency(Structure):
    _fields_ = [('currency', c_char * OFX_CURRENCY_LENGTH),
                ('exchange_rate', c_double),
                ('must_convert', c_int)]


class OfxFiServiceInfo(Structure):
    _fields_ = [('fid', c_char * OFX_FID_LENGTH),
                ('org', c_char * OFX_ORG_LENGTH),
                ('url', c_char * OFX_URL_LENGTH),
                ('accountlist', c_int),
                ('statements', c_int),
                ('billpay', c_int),
                ('investments', c_int)]


class OfxFiLogin(Structure):
    _fields_ = [('fid', c_char * OFX_FID_LENGTH),
                ('org', c_char * OFX_ORG_LENGTH),
                ('userid', c_char * OFX_USERID_LENGTH),
                ('userpass', c_char * OFX_USERPASS_LENGTH),
                ('header_version', c_char * OFX_HEADERVERSION_LENGTH),
                ('appid', c_char * OFX_APPID_LENGTH),
                ('appver', c_char * OFX_APPVER_LENGTH)]
 

class OfxPayment(Structure):
    _fields_ = [('amount', c_char * OFX_AMOUNT_LENGTH),
                ('account', c_char * OFX_PAYACCT_LENGTH),
                ('datedue', c_char * 9),
                ('memo', c_char * OFX_MEMO_LENGTH)]


class OfxPayee(Structure):
    _fields_ = [('name', c_char * OFX_NAME_LENGTH),
                ('address1', c_char * OFX_NAME_LENGTH),
                ('city', c_char * OFX_NAME_LENGTH),
                ('state', c_char * OFX_STATE_LENGTH),
                ('postalcode', c_char * OFX_POSTALCODE_LENGTH),
                ('phone', c_char * OFX_NAME_LENGTH)]


LibofxImportFormatList = (LibofxFileFormatInfo * 5)( \
        LibofxFileFormatInfo(LibofxFileFormat.AUTODETECT, b'AUTODETECT', \
                b'AUTODETECT (File format will be automatically detected later)'), \
        LibofxFileFormatInfo(LibofxFileFormat.OFX, b'OFX', \
                b'OFX (Open Financial eXchange (OFX or QFX))'), \
        LibofxFileFormatInfo(LibofxFileFormat.OFC, b'OFC', \
                b'OFC (Microsoft Open Financial Connectivity)'), \
        LibofxFileFormatInfo(LibofxFileFormat.QIF, b'QIF', \
                b'QIF (Intuit Quicken Interchange Format) NOT IMPLEMENTED'), \
        LibofxFileFormatInfo(LibofxFileFormat.LAST, b'LAST', \
                b'Not a file format, meant as a loop breaking condition'))

LibofxContextPtr = c_void_p
LibofxProcStatementCallback = CFUNCTYPE(c_int, OfxStatementData, c_void_p)
LibofxProcTransactionCallback = CFUNCTYPE(c_int, OfxTransactionData, c_void_p)

#print('Loading the library')
libofx = cdll.LoadLibrary('libofx.so.4')

libofx.libofx_get_new_context.argtypes = None
libofx.libofx_get_new_context.restype = LibofxContextPtr

libofx.ofx_set_transaction_cb.argtypes = (LibofxContextPtr, LibofxProcTransactionCallback, c_void_p)
libofx.ofx_set_transaction_cb.restype = None

libofx.libofx_get_file_format_from_str.argtypes = (LibofxFileFormatInfo * 5, c_char_p)
libofx.libofx_get_file_format_from_str.restype = c_int

libofx.libofx_proc_file.argtypes = (LibofxContextPtr, c_char_p, LibofxFileFormat)
libofx.libofx_proc_file.restype = c_int

def transaction_cb(data, transaction_data):
    if data.name_valid and data.amount_valid:
        print('{amount:>10} \'{name}\''.format(amount=data.amount, name=data.name.decode()))
    else:
        print('Invalid transaction')
    return 0

if len(sys.argv) == 1:
    print('Please enter an OFX / QFX filename')
    sys.exit(1)

print('Loading context')
ofx_context = libofx.libofx_get_new_context()

print('Adding callbacks')
libofx.ofx_set_transaction_cb(ofx_context, LibofxProcTransactionCallback(transaction_cb), 0)

print('Getting file format')
file_format = libofx.libofx_get_file_format_from_str(LibofxImportFormatList, b'AUTODETECT')

print('Processing file')
status = libofx.libofx_proc_file(ofx_context, sys.argv[1].encode(), file_format)

print('Closing context')
status = libofx.libofx_free_context(ofx_context)
