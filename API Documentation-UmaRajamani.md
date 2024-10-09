# ACCOUNT AUTHENTICATION SERVICE API USER GUIDE
## 1 Introduction
This document outlines the invoking of APIs for Account Authentication by customers of ABC Bank. Details include Early Warning (EW) API endpoints, sample request-response formats, field specifications and error codes. In addition to identifying the intended category of users of this document, this section provides a list of acronyms and abbreviations along with their expansions and explanation, which will help users, understand the key technical terms used across the document.
###	1.1 Purpose and Intended Audience
The purpose of this documentation is to assist developers (of clients of ABC Bank) to invoke APIs with the required Inputs and interpret the Responses from the Account Authentication Service of ABC Bank.  It describes the processes/routines involved in the interaction.  
###	1.2 Abbreviations, Acronyms, Terms and Definitions
The following table lists the acronyms, abbreviations, terms and definitions used in this document.
|Acronym     | Definition|
|------------|:----------|
|AOA         | Account Owner Authentication |
|API         | Application Program Interface | 
|DDA         | Demand Deposit Account | 
|EW          | Early Warning Connector that connects to the Early Warning service    |
|JSON RPC 2.0| Java Script Object Notation Remote Procedure Call Version 2.0 |
|XML         | eXtensible Markup Language used for data transfer |
|RDC        | Real Time Deposit Check | 


|Key Terms    | Definition|
|------------ |:----------|
|User                  |*	Refers to the employee(s) of ABC Bank clients who consume the services.              *	Specifically refers to ABC Bank clients that consume EW (AOA) Services.|
|JSON Format          | Message encoded in JSON Format. The standard file format uses human readable text for the purpose of transmitting data. The Request Format includes ID, Method and Parameters (API, Payload).Response Format includes ID and Result (Parameters)|
|Payload              | The actual data in a specified format, that is transmitted along with protocol overhead when interacting with applications | 
|Processing Response | Refers to response data with System Error Codes, Inquiry Field Validation Codes and Result Codes|
|Account Level Response| JRefers to response data with Account Score Responses, and reason codes |
|Request Parameters    | The Fields in the Payload used for the purpose of eliciting a response from the AOA service. |
|Response Parameters    |The Fields received as a Response from the AOA Service to the Request transmitted in the Payload.| 
## 2	Service Overview
Account Authentication Service is intended to offer real time verification of account ownership, by matching account owner data such as Account Name, SSN, DOB, Account Number, and Routing Number.  Calling parties (ABC BANK Clients) access Account Authentication Service by invoking APIs. On receipt of the account authentication information provided by the Service, the calling party uses the verified information to either carry out risk assessment or take suitable action as may be deemed fit. 
### 2.1	How the Service Works
The User (ABC BANK Client) subscribes for Account Authentication Service through ABC BANK. The User pays a fee for use of the services, at rates specified in the contract entered with ABC BANK.

Whenever the User requires Account Authentication to be carried out, the User sends a Request in JSON Format seeking information on any one of the three Service Categories – Account Status only, Account Owner only and Both Account Status & Account Owner (explained in Section 2.2 below).

The verified information from the Account Authentication Service is transmitted back to the User, with the Response containing two types of Response Data – Processing Response and Account Level Response. 
*	Processing Response– is the Response data that carries the System Error Codes, the Inquiry Field Validation Error Codes and Result Codes.
*	Account Level Response – is the Response data that carries the Account Score Responses and Reason Codes.
The Response Data offers the User (ABC BANK Clients) with information that can either be used for assessing risk or for appropriate action as deemed fit.
### 2.2 Service Categories
Participating financial institutions can receive responses in one of the following three categories.

* Account status only – This returns information pertaining only to the Status of the queried Account.

*	Account owner only – This returns information pertaining only to the Status of the Account Owner of the queried Account.

*	Account status combined with account owner– This returns information pertaining to the Status of the Account as well as the Account Owner of the queried Account.

## 3	Access Protocols& Process Flow

Users connect either via the NATS Messaging System or via TCP/IP. If the connection is sought to be established via NATS, the assigned and unique URL would be, for e.g. nats://xx:xxxxxx1111@xx.xxx.xx.xx:xxxx. If the connection is sought to be established via TCP/IP, the assigned URL would be https://xxxxxxx. Users rely on the Request-Response Method for seeking information.  Responses are transmitted back to the user via the NATS Messaging System or TCP/IP in real time. 
1. The User receives an email from ABC Bank with a folder attachment containing sample codes and API Key. The folder also contains details of 2 NATS Server URLs, which are unique to the User, in addition to TCP/IP details.

    * Sample structures of the URLs for access via NATS Messaging System : 

        nats://xx:xxxxxx1111@70.163.40.38:4222
        nats://xx:xxxxxx1111@70.163.40.38:4223 

    *	URL for access via TCP/IP  : 

        https://ew.xxxxxx.com/ew/rest/inquire
        https://connectors.xxxxxxx.com:8443/ew/rest/inquire

2.	The User (ABC Bank Client) can create own Private Key or can request for one from ABC Bank (at present, the one shared byABC Bank is the only one that is used).  This is also shared in the email.  
3. The User utilizes the combination of API Key and username and converts it into Basic Auth for Credentials.
4.	The User generates a Digital Signature by signing the private key along with the requesting payload.  
5.	The User sends a request in JSON RPC Format with **Subject/Topic** either through NATS or TCP/IP to Account Authentication Service.
6.	The Account Authentication Service processes the request and responds in JSON RPC Format over NATS or TCP/IP.
7.	ABC Bank Clients (Users) whose Profiles are “Active” in the EW Connector, seek information from the Account Authentication Service by transmitting a request in JSON Format. 
8.	The Account Authentication Service verifies the information and transmits the Response back to the Client. 
9.	This authentication of ownership is transmitted in one of three types of verification responses – **Yes** *(Correct)*, **No** *(Incorrect)* or **Conditional** *(Partially Correct)*.
10.	The response contains one of the following:
    *	Account owner match codes. 
    *	Hard-hit warnings on participant accounts
    *	Informational responses on participant accounts

The three methods mentioned above are exposed by EW as a SOAP interface. A REST wrapper has been built around the SOAP requests and responses and all specifications are in the JSON format.

![Process Flow](./ProcessFlow.jpg "Process Flow"){ width=60%,height:30px }

## 4	Message Layout and Parameters

4.1	Format Description of JSON RPC 2.0

**Request Strucuture**
      
--> {"jsonrpc":"2.0", "method":"XXXX", "params": {XXXXXXX}, "id":X}
|Keys        | Description|
|------------|:----------|
|ID          | Refers to Identification Number sent by the customer |
|Method      | Refers to Identification Number sent by the customer| 
|Params      | Refers to the Request Parameters sent in by the Customer | 
>> Note: Params comprises API and Payload. The API carries the Authentication Parameters, and the Payload carries the Requested Parameters by the Customer.

**Response Structure**

<--{"jsonrpc":"2.0","result":XX,"id":X}
|Keys        | Description|
|------------|:----------|
|ID          | Refers to Identification Number sent by the customer |
|Result      | Refers to the Response Parameters sent by Early Warning in response to Customer's request| 

### 4.2	Authentication
The EW connector generates a unique API key, which is issued to the user (ABC Bank Client). The combination of API key and user credentials are used to authenticate the user request. Additionally, IP white listing is carried out in the application and firewall. Sample authentication parameters mentioned below are a part of the API payload sent in the request JSON. 

|Parameter Name   |Possible Values | Field Length|Type| Requirement |
|-----------------|:---------------|:------------|:---|:------------|
|Credential       | Basic Y2hyaXN0b3B0ZXIubXVycmF5QGRlcG9zaXQtc29sdXRpb25zLmNgbTo5MjUwNThiZGQ5MDU0ZDcxOTJmNDhhNTE4ZjQzZrk4NQ== |N/A|String|Mandatory|
|Signature        | MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg0nSRl9qZvY5mFY6W|1-17 |String|Mandatory|  

# 5	Request and Response parameters
## 5.1	Account Inquiry
Early Warning evaluates the Account information. Account Inquiry includes Account level information - Account, Account number, routing number, and fee Attributes / Channel Indicator.
### 5.1.1	Request Parameters
|Parameter Name   |Possible Values | Field Length|Type| Requirement |
|------------------|:--------------|:------------|:---|:------------|
|Type	|ACCOUNT|	N/A	|String|	Mandatory
|accountNumber	|	|1-17| 	Non-negative integer	|Mandatory|
|routingNumber|	|	9 |	Non-negative integer	|Mandatory||
|feeAttrib|	AA, BB, CC, DD, EE, FF, GG, HH, II |	2 |	String|	Mandatory|

### 5.1.2	Sample Request (JSON)
```
{
  "id": 21,
  "method": "ew.inquire",
  "params": {
    "api": {
      "credential": "Basic Y2hyaXN0b3B0ZXIubXVycmF5QGRlcG9zaXQtc29sdXRpb25zLmNgbTo5MjUwNThiZGQ5MDU0ZDcxOTJmNDhhNTE4ZjQzZrk4NQ==",
      "signature": " MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AuEHBG0lawIBAQQgonSRl9qZvY5mFY6W "
    },
    "payload": {
    "type": "ACCOUNT",
    "accountNumber": "61231234340",
    "routingNumber": "122199983",
    "feeAttrib": "BB" }
  }
}
```
Account status response includes Owner status match code, Match Result containing FirstName, Last Name, Business Name, Social Security Number, Date of Birth, City, Address; Primary Account Status code, Secondary Account Status code, Additional Account Status code, Error codes and Status.

**High Risk Warning codes are:**

* Closed, pending closed, or post no debit statuses codes 002, 003, 010, 012, 013, 014, 102, 103, 110, 112, 113, 114
* Stop-payment status codes004-007, 104-107
* Highest-risk Enhanced Overdrawn status codes 020-022, Overdrawn status codes 030, 031, 130

** Informational Response codes are: **
*	Returning item status are 015-016 unless this is the only information returned on the account
*	The account is a not a demand deposit account (DDA). Non-DDA status codes are 080, 081, 082, 084, or 098
*	The account is present- 099, 199
*	No known information about the account - 096
### 5.1.3	Response Parameters
|Parameter Name   |Possible Values |
|-----------------|:--------------|
|ownerStatus        |	E.g. C000, where C is the match code and 000 is the participant status code. Please refer Appendix A for possible match codes and participant status codes.|
|matchResult (object)|	This object is returned with all null values because none of information below is passed in the account only inquiry|
|firstName|	Null|
|lastName|	Null|
|businessName|	Null|
|Ssn|	Null|
 dob    |Null|
| city	 |Null| 
| address|Null|
|priAccountStatus|	Please refer [APPENDIX A HTTP Errors] (./# APPENDIX A HTTP Errors) for possible primary account status codes and their interpretation.|
|secAccountStatus|	Please refer [Appendix A] (#appendix-a) for possible secondary account status codes and their interpretation.|
|addAccountStatus|	Please refer [Appendix A] (#appendix-a) for possible additional account status codes and their interpretation.|
|errorCode|	Please refer Appendix A[Appendix A] (#appendix-a) for possible error codes and their interpretation.||
|Status	|OK, indicating that the request and the response were sent and received successfully, respectively.|

### 5.1.4	Sample response (JSON)
```
{
  "id": "21",
  "result":{
    "ownerStatus": "C900",
    "matchResult": {
        "firstName": null,
        "lastName": null,
        "businessName": null,
        "ssn": null,
        "dob": null,
        "city": null,
        "address": null
    },
    "priAccountStatus": "S130",
    "secAccountStatus": "000",
    "addAccountStatus": "000",
    "errorCode": "0",
    "status": "OK"
}
}

```
## 5.2	Owner Inquiry
Account owner authentication and evaluation is done by Early Warning. Account Owner Inquiry includes first name, last name, business name, Address 1, Address 2, City, State, Zip, Home Phone, Work Phone, Social Security number, Date of Birth, Account number, routing number, Free Attrib and type of the Inquiry.
### 5.2.1	Request Parameters
|Parameter Name   |Possible Values | Field Length|Type| Requirement |
|------------------|:--------------|:------------|:---|:------------|
|firstName	|	1-40 |	String|	Mandatory *|
|lastName	|	1-40 |	String|	Mandatory *|
|businessName|		1-87 |	String	|Mandatory *|
|address1	|	1-40	|String	|Optional|
|address2|		1-40|	String|	Optional|
|City	|	1-25|	String|	Optional|
|State	|	2	|String	|Optional|
|Zip	|	5-10|	String|	Optional|
|homePhone	|	10	|Non-negative integer|	Optional|
|workPhone	|	10|	Non-negative integer|	Optional|
|SSN	|	9	|Non-negative integer|	Optional|
|Dob|		8	|Non-negative integer (yyyymmdd)|	Optional
|accountNumber	|	1-17 	|Non-negative integer|	Mandatory|
|routingNumber|		9 |	Non-negative integer|	Mandatory|
|feeAttrib|	AA, BB, CC, DD, EE, FF, GG, HH, II |	2 	|String	|Mandatory|
|Type|	OWNER|	N/A	|String	|Mandatory|

* Inquiry must contain one of the following – If one is populated, the other can be left blank
	* firstName AND lastName
OR
    * businessName
### 5.2.2	Sample Request (JSON)
```
{
  "id": 21,
  "method": "ew.inquire",
  "params": {
    "api": {
      "credential": "Basic Y2hyaXN0b3B0ZXIubXVycmF5QGRlcG9zaXQtc29sdXRpb25zLmNgbTo5MjUwNThiZGQ5MDU0ZDcxOTJmNDhhNTE4ZjQzZrk4NQ==",
      "signature": " MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AuEHBG0lawIBAQQgonSRl9qZvY5mFY6W "
          },
    "payload":
   {
  "firstName": "Jane",
  "businessName": null,
  "lastName": "Viola",
  "address1": "W 5th Street",
  "address2": "",
  "city": "Manhattan",
  "state": “NY”,
  "zip": “10020”,
  "homePhone": "9712452012",
  "workPhone": "9712452012",
  "ssn": "911018872",
  "dob": "19680407",
  "feeAttrib": "HH",
  "accountNumber": "61231234340",
  "routingNumber": "122199983",
  "type": "OWNER"
}
}   
} 
```
Account Owner Enquiry Response includes Matching Owner status, Match result containing first name, last name, business name, Address, City, error code and status.

In the response of the Owner Inquiry, the Owner Status is a four-character code with the first character being a letter, followed by 3 numbers. The letter indicates the match code and the number indicates the condition code. The match code depends on the overall match for name, address, SSN, DOB and other details provided for verification. The remaining three characters of the owner status response is a code known as the participant status code. The code indicates the high-level account status and indicates whether the inquiry resulted in a hard or soft hit.
### 5.2.3	Response Parameters
Parameter Name   |Possible Values |
|-----------------|:--------------|
|ownerStatus|	Please refer Appendix A for possible codes|
|matchResult (object)|	For this inquiry, match values must be returned for some or all of the fields in this object, depending on what information were passed.|
|firstName|	Y/N/null|
|lastName|	Y/N/null|
|businessName	|Y/N/null|
|Ssn	|Y/N/null|
| dob|	Y/N/null|
| city	Y/N/null|
|  address|	Y/N/null|
|errorCode	|Please refer Appendix C for possible error codes|
|Status	|OK, indicating that the request and the response were sent and received successfully, respectively.|

Early Warning evaluates Both Account and Owner information; the Inquiry includes first name, last name, business name, Address 1, Address 2, City, State, Zip, Home Phone, Work Phone, Social Security number, Date of Birth, Account number, routing number, Fee Attribute and type of Inquiry (Both Account and Owner). 
### 5.2.4	Sample response (JSON)
```
{
  "id": "21",
  "result":
{
    "ownerStatus": "C000",
    "matchResult": {
        "firstName": "Y",
        "lastName": "Y",
        "businessName": null,
        "ssn": "N",
        "dob": "N",
        "city": "N",
        "address": "N"
    },
    "errorCode": "0",
    "status": "OK"
}
}

```
## 5.3	Both Account / Owner Inquiry
Early Warning evaluates Both Account and Owner information; the Inquiry includes first name, last name, business name, Address 1, Address 2, City, State, Zip, Home Phone, Work Phone, Social Security number, Date of Birth, Account number, routing number, Fee Attribute and type of Inquiry (Both Account and Owner). 
### 5.3.1	Request Parameters
|Parameter Name   |Possible Values | Field Length|Type| Requirement |
|------------------|:--------------|:------------|:---|:------------|
|firstName|		1-40 |	String|	Mandatory *|
|lastName|		1-40 |	String|	Mandatory *|
|businessName	|	1-87 |	String	|Mandatory *|
|address1	|	1-40	|String	|Optional|
|address2|		1-40	|String|	Optional|
|City	|	1-25	|String|	Optional|
|State	|	2	|String|	Optional|
|Zip	|	5-10|	String|	Optional|
|homePhone|		10|	Non-negative integer|	Optional|
|workPhone|		10|	Non-negative integer|	Optional|
|Ssn	|	9|	Non-negative integer|	Optional|
|Dob	|	8|	Non-negative integer (yyyymmdd)	|Optional
|accountNumber	|	1-17 |	Non-negative integer	|Mandatory|
|routingNumber	|	9 	|Non-negative integer	|Mandatory|
f|eeAttrib	AA, BB, CC, DD, EE, FF, GG, HH, II|	2 	|String	|Mandatory|
|Type|	BOTH	|N/A	|String|	Mandatory|


### 5.3.2	Sample Request (JSON)
```
{
  "id": 21,
  "method": "ew.inquire",
  "params": {
    "api": {
      "credential": "Basic Y2hyaXN0b3B0ZXIubXVycmF5QGRlcG9zaXQtc29sdXRpb25zLmNgbTo5MjUwNThiZGQ5MDU0ZDcxOTJmNDhhNTE4ZjQzZrk4NQ==",
      "signature": "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AuEHBG0lawIBAQQgonSRl9qZvY5mFY6W"
         },
    "payload":{
  "firstName": "Jane ",
  "businessName": null,
  "lastName": "Viola",
  "address1": "W 5th street",
  "address2": "",
  "city": "Manhattan",
  "state": "NY",
  "zip": "10020",
  "homePhone": "9712452012",
  "workPhone": "9712452012",
  "ssn": "911018872",
  "dob": "19680407",
  "feeAttrib": "HH",
  "accountNumber": "61231234340",
  "routingNumber": "101100045",
  "type": "BOTH"
         }
   }
}

```

### 5.3.3	Response parameters
|Parameter Name   |Possible Values |
|-----------------|:--------------|
|ownerStatus|	Please refer Appendix A for possible condition codes|
|matchResult (object)|	For this inquiry, match values must be returned for some or all of the fields in this object, depending on what information were passed.|
|firstName|	Y/N/null|
|lastName|	Y/N/null|
|businessName|	Y/N/null|
|SSN|	Y/N/null|
 |dob|	Y/N/null|
 | city	|Y/N/null|
 | address|	Y/N/null|
|errorCode|	Please refer Appendix A for possible error codes|
|Status	|OK, indicating that request/response were sent and received successfully. |

### 5.3.4	Sample Response (JSON)

```
{
  "id": "21",
  "result":
{
    "ownerStatus": "C300",
    "matchResult": {
        "firstName": null,
        "lastName": null,
        "businessName": null,
        "ssn": null,
        "dob": null,
        "city": null,
        "address": null
    },
    "priAccountStatus": "S096",
    "secAccountStatus": "000",
    "addAccountStatus": "000",
    "errorCode": "0",
    "status": "OK"
}
}


````
# 6	Understanding the service parameters

** Table showing Parameter Name and respective description**
|Parameter Name   |Description    |
|-----------------|:--------------|
|type	|Refers to the validation of ‘Type of Inquiry’ – Valid values are ACCOUNT, OWNER, or BOTH |
|accountNumber	|Refers to the account number –containing only digits; a minimum of 4 digits to a maximum of 17 digits|
|routingNumber	|Bank routing number is a nine-digit numeric ID that is assigned to Banks. This unique code indicates the location of the US Bank, and is printed on the bottom of checks. | 
|feeAttrib|	Refers to the Fee Attributes. Valid values are AA, BB, CC, DD, EE, FF, GG, HH, II, NT, NA, NR, and NW. Refer Appendix B for list of values and their interpretations.|
|ownerStatus|	Refers to the Owner status code – a four-character code with the first character being a letter, followed by 3 numbers; e.g. C000, where C is the match code and 000 is the condition code. The match code depends on the overall match for name, address, SSN, DOB and other details provided for verification. | 
|matchResult (object)|	This object is returned with all null values because none of information below is passed in the account only inquiry.Refers to the match result object { "firstName": "Null",  "lastName": "Null","ssn": "Null","dob": "Null",    "city": "Null", "address": "Null" }|
|firstName	|Refers to the First name of the Account Holder|
|lastName	|Refers to the Last name of the Account Holder|
|businessName|	Refers to the name of the Organization| 
|SSN|	Refers to the Unique 9-digit Social Security Number that of the Account Holder that is the national identification number used for taxation and related purposes|
|DOB|	Refers to the Date of birth of Account Holder|
|City|	Refers to the Name of the city where the Account Holder resides|
|Address|	Refers to the Account Holder’s address | 
|priAccountStatus|	Refers to the primary account status code.| 
|secAccountStatus|	Refers to the secondary account status code. |
|addAccountStatus|	Refers to the Additional account status code.| 
|errorCode|	Refers to the error code
status	Refers to the status indicating that the request and the response were sent and received successfully, respectively.|
|address1|	Refers to Line1 of the Account Holder’s address  |
|address2|	Refers to Line2 of the Account Holder’s address  |
state|	Refers to the Name of the state where the Account Holder resides |
|zip|	Refers to the Postal code of the Account Holder’s address|


# 7	Support
The Technical Support Team provides dedicated technical support for all technical issues of intended Users. The team specifically addresses issues related to Access Protocols, Request-Response Formats, Error Codes, and Connectivity.

**For Technical Support:** support@abcbank.com

# APPENDIX A HTTP Errors
|Match Codes |Participant Codes  |
|------------|:------------------|
|ownerstatus:
          type: integer
          format: int32
          example: C900
          description: Eg. C000, where C is the match code and 000 is the participant status code. Refers to the Owner status code – a four-character code with the first character being a letter, followed by 3 numbers; e.g. C000, where C is the match code and 000 is the condition code. The match code depends on the overall match for name, address, SSN, DOB and other details provided for verification. The match codes received can be one of the following
            Y = The inquiry field closely or exactly matches the database.
            C = The inquiry field conditionally (partially) matches the     database. 
            N = The inquiry field does not match the database.
            U = No identifying data is available in the database for the account provided.
            The remaining three characters of the owner status response is a code known as the participant status code. The code indicates the high level account status and indicates whether the inquiry resulted in a hard or soft hit. The following participant status codes may be returned by Early Warning
            Soft  000  Not Located  Account requested for verification does not exist on the Contributor's master account file. This condition may indicate an account number misread or a potentially fraudulent item.
            Hard  002  Closed For Cause  A transaction account which has been closed by Contributor FSO as a result of unacceptable use by the customer. This judgment is made by the FSO in accordance with its transaction account policies.
            Hard  003  Closed for  Account has been removed from the Contributor's master Cause/Purged  account file. Account will be retained by Early Warning until reissued by the Contributor
            Hard  004  Stop Payment  A check inquiry (transit item) where all four MICR fields (ABA,4 Field Individual  account number, serial number, and dollar amount) match an individual/Match  unique stop-payment record in the National Shared Database  resource.
            Hard 005 Stop Payment A check inquiry (transit item) where all four MICR fields (ABA, 4 Field Range account number, serial number and dollar amount) match a range of stop- Match  payment records in the Database.
            Hard  006  Stop Payment ¾  A check inquiry (transit item) where three MICR fields (ABA,Individual  account number, and serial number) match an individual/ unique stop- payment record in the Database.
            Hard  007  Stop Payment ¾  A check inquiry (transit item) where three MICR fields (ABA,  Range  account number, and serial number) match a range stop-payment record in the Database.
            Hard  010  Post No Debits  Account will not accept any debit activity.
            Hard  013  Closed/Purged  Account has been closed and removed from Contributor's master account file. Account will be retained by Early Warning until the first occurrence of Three years from the date account originally closed Account is reissued by Contributor.
            Hard  014  Pending Closed  Account was closed in the last processing cycle. This status will automatically change to a Status 012 in the next processing cycle unless modified by the contributing FSO.
            Hard  0151  Return Item  High probability of return.
            Soft  0161  Account  Moderate probability of return.
            Hard  020      Available balance less than zero, with,
                 X = Consecutive days in OD status.
                 021  Enhanced OD  
                 Y = Time account has been on the books.
                 022  
            Soft  028  Divested Account  Account has been purchased or assumed by another FSO and
             – Purged  has been removed from Contributor’s master account file. The account will be retained by Early Warning for six months.
            Soft  030  Overdrawn  Available balance less than zero. Activity may post upon review.
            Soft  031  Overdrawn New  Available balance less than zero, and account opened within Account  prior 60 days. Activity may post upon review.
            Soft  032  Uncollected Funds  Collected balance less than zero. Activity may post upon review.
            Soft  033  UCF/New Account  Collected balance less than zero and account opened within prior 60 days. Activity may post upon review. 
            Soft  034  Dormant/Inactive  Account dormant or inactive. Activity may post upon review.
            Soft  035  Deceased  Account holder deceased. Activity may post upon review.
            Soft  036  Lost/Stolen  Account holder reported check(s) lost or stolen. Activity mayCheck(s)  post upon review.
            Soft  037  Attached  Account subject to levy, garnishment, government reclamation,lien, court order or other restriction of limited amount. Activity  may post upon review.
            Soft  038  Divested Account  An account purchased or assumed by another FSO.
            Informational  040  New Account  Account opened between 8-60 days. (8-60)
            Informational  041  New Account  Account opened between 0-7 days.  (0-7)
            Informational  042  New Account (61-  Account opened between 61-120 days. 120)
            Informational  043  New Account (121-  Account opened between 121-180 days. 180)
            Informational  055  Official Item  Cash-equivalent item such as official check, cashier's check, or teller check.
            Informational  080  Credit Card Check  Item drawn on non-DDA that is posted to a credit card account and/or drawn against a credit card FSO.
            Informational  081  Participant Line of  Item drawn on non-DDA and is posted to a credit line account.  Credit Check  The drawee FSO is a Contributor to the Database.
            Informational  082  Participant Home  Item drawn on non-DDA and is posted to a home equity  Equity Check  account. The drawee FSO is a Contributor to the Database.
            Informational  084  Participant Broker  Item drawn on non-DDA and is posted to a brokerage account Check and/or drawn against a broker-only FSO. The drawee FSO is a Contributor to the Database.Informational  096  No Known  No positive or negative information is known about the item.  Information
            Informational  098  Non-DDA  Item drawn on a non-DDA and not included in statuses 080, 081, 082, and 084.
            Informational  099  Present  Account is present in Contributor's master account file and  contains no other status code. Typically, these are accounts  with positive balances.
            Hard  102  Savings Closed for  A savings account which has been closed by the Contributor Cause  FSO as a result of unacceptable use by the customer. This judgment is made by the FSO in accordance with its transaction account policies.
            Hard  103  Savings Closed for  Closed for Cause savings account has been removed from the Cause/ Purged  Contributor's master account file. Account will be retained by Early Warning until reissued by the Contributor.
            Hard  104  Savings Stop  A savings inquiry where all four MICR fields (ABA, account number, Payment 4 Field  serial number and dollar amount) match an individual/ unique stop-  Individual Match  payment record in the Database.
            Hard  105  Savings Stop  A savings inquiry where all four MICR fields (ABA, account number,Payment 4 Field  serial number and dollar amount) match a range of stop-payment Range Match  records in the Database.
            Hard  106  Savings Stop  A savings inquiry where all three MICR fields (ABA, account number,Payment ¾  and serial number) match an individual/unique stop-payment record in Individual  the Database.
            Hard  107  Savings Stop  A savings inquiry where three MICR fields (ABA, account number, and Payment ¾ Range  serial number) match a range stop-payment record in the Database.
            Hard  110  Savings Post No  Savings account will not accept any debit activity.Debits 
            Hard  112  Savings Closed  Savings account closed.
            Hard  113  Savings  Savings account has been closed and removed from Closed/Purged  Contributor’s master account file. Account will be retained by Early Warning until the first occurrence of, Three years from the date account originally closed       Account is reissued by Contributor.
            Hard  114  Savings Pending  Savings account is closed. Account was closed in the last Closed  processing cycle. This status will automatically change to a Status 112 in the next processing cycle unless modified by the contributing FSO.
            Soft  128  Savings Divested  A savings account purchased or assumed by another FSO and Account/Purged  removed from the Contributor's master account file. The Account will be retained by Early Warning for six months.
            Soft  130  Savings  Savings account available balance less than zero. Activity may Overdrawn  post upon review.
            Soft  132  Savings  Savings account collected balance less than zero. Activity mayUncollected Funds  post upon review.
            Soft  133  Savings UCF/New  Savings account collected balance less than zero and account  Account  opened within prior 60 days. Activity may post upon review.
            Soft  134  Savings  Savings account dormant or inactive. Activity may post upon  Dormant/Inactive  review.
            Soft  135  Savings Deceased  Savings account holder deceased. -Activity may post upon  review.
            Soft  137  Savings Attached  Savings account subject to levy, garnishment, government reclamation, lien, court order or other restriction of limited amount. Activity may post upon review.
            Soft  138  Savings Divested  Savings account purchased or assumed by another FSO.Account
            Informational  140  Savings New  Savings account opened between 8-60 days.  Account (8-60)
            Informational  141  Savings New  Savings account opened between 0-7 days.  Account (0-7)  
            Informational  142  Savings New  Savings account opened between 61-120 days.Account (61-120)
            Informational  143  Savings New  Savings account opened between 121-180 days.Account (121-180)  
            Informational  199  Savings Present  Savings account is present in the Contributor’s master account file and contains no other status codes. These are typically  accounts with positive balances.
        matchresult:
          type: object
          description: This object is returned with all null values because none of information below is passed in the account only inquiry. This object is returned with all null values because none of information below is passed in the account only inquiry.
            Refers to the match result object 
          properties:
            firstname:
              type: string
              description: First name of the Account Holder
              example: Null {}
            lastname:
              type: string
              description: Last name of the Account Holder
              example: Null {}
            businessname:
              type: string
              description: name of the Organization
              example: Null {}
            ssn:
              type: string
              description: Unique 9-digit Social Security Number that of the Account Holder that is the national identification number used for taxation and related purposes
              example: Null {}
            dob:
              type: string
              description: Date of birth of Account Holder
              example: Null {}
            city:
              type: string
              description: Name of the city where the Account Holder resides
              example: Null {}
            address:
              type: string
              description:  Account Holder’s address 
              example: Null {}
        priAccountStatus:
          type: string
          description: Primary account status code 
          example: S130
        secAccountStatus:
          type: string
          description: Secondary account status code
          example: "000"
        addAccountStatus:
          type: string
          description: Additional account status code
          example: "000"
        errorCode:
          type: string
          description: Error Code
          example: "0"
        status:
          type: string
          description: Request Status indicating that the request and the response were sent and received successfully, respectively.
          example: OK
        

# APPENDIX B – Fee Attributes
|Value  |Defiition |
|-------------|:--------------|
|AA|	RDC All|
|BB	|RDC Consumer Home|
|CC|	RDC Consumer Mobile|
|DD	|RDC Small Business|
|EE	|Branch/Teller|
|FF	|ATM|
|GG	|Lockbox/Mail/Corporate|
|HH|	ACH - Deposit|


# APPENDIX C – HTTP Errors
|Error Code   |Description    |Explanation  |
|-------------|:--------------|:------------|
|403 |	Forbidden|	Access Denied – API key is not enabled or the token header is missing or no token has been sent in the header or the format of the header is incorrect (such as unwanted white spaces)|
|500 |	Internal Server Error|	Invalid Credentials - Username or API token is missing or user is trying to access the API from a non-white listed IP address |
|415|	Unsupported Media Type	|Content-Type header is missing, empty or has incorrect value.|
|400|	Bad Request	|Bad syntax on one or more parameters.|
