## happy path
* greet
  - utter_greet

## say goodbye
* goodbye
  - utter_goodbye

## status path 2
* greet
  - utter_greet
* Payment_Status
  - action_Payment_Status

## affirm path
* affirm OR thank
  - utter_affirm

## deny path
* deny
  - utter_deny

## status path 3
* Payment_Status
  - action_Payment_Status

## payment path 1
* Paid_Amount
  - action_Paid_Amount

## pending path 2
* Pending_Amount
  - action_Pending_Amount

## give source path
* Source
  - action_Source

## Client_Name path 1
* Client_Name
  - action_Client_Name

## Legal_Entity path 1
* Legal_Entity
  - action_Legal_Entity

## Currency path 1
* Currency
  - action_Currency

## Payment_Type path 1
* Payment_Type
  - action_Payment_Type

## Payment_Date path 1
* Payment_Date
  - action_Payment_Date

## Comments path 1
* Comments
  - action_Comments

## creation path 1
* help_payment_creation
  - action_help_payment_creation

## multiaccount path 1
* help_multiple_accounts
  - action_help_multiple_accounts

## pay successful path 1
* help_payment_successful
  - action_help_payment_successful

## get id path 1
* help_get_id
  - action_help_get_id

## cross country path 1
* help_cross_country
  - action_help_cross_country

## dummy path 1
* help_dummy_link
  - utter_help_dummy_link

## add account path 1
* help_add_account 
  - action_help_add_account 

## information path 1
* information
  - utter_information