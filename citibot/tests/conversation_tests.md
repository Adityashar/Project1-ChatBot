## happy path
* greet:hi
  - utter_greet

## say goodbye
* goodbye: Byee
  - utter_goodbye

## status path 2
* greet: hi
  - utter_greet
* payment_status: tell me details for id [103560](account_id)
  - action_payment
  - utter_payment

## affirm path
* affirm: yes
  - utter_affirm

## deny path
* deny: dont like this
  - utter_deny

