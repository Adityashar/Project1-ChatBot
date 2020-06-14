## happy path
* greet
  - utter_greet

## say goodbye
* goodbye
  - utter_goodbye

## status path 2
* greet
  - utter_greet
* payment_status
  - action_payment
  - utter_payment
> check_path_2

## affirm path
> check_path_3
> check_path_2
* affirm OR thank
  - utter_affirm

## deny path
> check_path_3
> check_path_2
* deny
  - utter_deny

## status path 3
* payment_status
  - action_payment

## payment path 1
* paid_amount
  - action_amount_paid

## payment path 2
* greet
  - utter_greet
* paid_amount
  - action_amount_paid
> check_path_3

## pending path 1
* greet
  - utter_greet
* pending_amount
  - action_amount_pending
* paid_amount
  - utter_paidamount
* payment_status
  - utter_payment
* affirm OR thank
  - utter_affirm

## pending path 2
* pending_amount
  - action_amount_pending