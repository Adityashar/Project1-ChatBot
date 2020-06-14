## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there

## intent:goodbye
- bye
- goodbye
- see you around
- see you later

## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really

## intent:thank
- tysm
- thanks
- thank you so much
- appreciate your efforts

## intent:payment_status
- what is the status of the agreement [103256](account_id)
- what is the status of the agreement with id [102729](account_id)
- what is the status of the transaction with [103197](account_id) account id
- Brief me about the deal with account id [104112](account_id)
- Brief me about the transaction deal with agreement id [103640](account_id) 
- Brief me about the payment agreement deal with [103600](account_id) id
- Tell me the status of the transaction [101872](account_id)
- Give the details of the account [101369](account_id)
- Give the details about agreement [102906](account_id) accound id
- Tell me something about the deal with [105086](account_id) id
- How are things going on with the agreement [103180](account_id) id
- For [103490](account_id) agreement give me the details pls
- For the id [103490](account_id) tell me the status 
- Tell me the status for the transaction from [CitiBank Pune](legal_entity) with id [103560](account_id)
- Tell me the details for the transaction from [citibank pune]{"entity": "legal_entity", "value":"CitiBank Pune"} with id [103561](account_id)
- Tell me the details for the payment from [citibank Hongkong]{"entity": "legal_entity", "value":"CitiBank HongKong"} with [103161](account_id) id
- Tell me the status for the transaction from [CitiBank Pune](legal_entity) for agreement [103570](account_id)
- Brief me about the payment status from [CitiBank Bangalore]{"entity": "legal_entity", "value":"CitiBank Bengaluru"} for account [103360](account_id)
- Brief us for the agreement of [CitiBank Pune](legal_entity) for transaction id [103660](account_id)
- Give me details about the status of the payment from [CitiBank NYC]{"entity": "legal_entity", "value":"CitiBank NewYork"} for agreement [103510](account_id) id
- Give me something about the current status of the transaction from [CitiBank NewYorkCity]{"entity": "legal_entity", "value":"CitiBank NewYork"} for payment id [103520](account_id) 
- For the id [103923](account_id) provide me the details of the current status of payment from [CitiBank London](legal_entity) 
- for the transaction [18331](account_id) give me status of agreement deal from [CitiBank Bengaluru](legal_entity)
- for the agreement id [18391](account_id) give me report of transaction from [CitiBank Bengaluru](legal_entity)
- Give me the status report for the transaction from [CitiBank Pune](legal_entity) for agreement [103520](account_id)


## intent:paid_amount
- what is the amount paid in the agreement [103256](account_id)
- what is the amount paid in the agreement with id [102729](account_id)
- what is the amount paid during the transaction with [103197](account_id) account id
- Brief me about the money paid in deal with account id [104112](account_id)
- Brief me about the transaction done in deal with agreement id [103640](account_id) 
- Brief me about the payment made in the agreement deal with [103600](account_id) id
- Tell me how much money was delivered in the transaction [101872](account_id)
- Give the details of the money transferred with account id [101369](account_id)
- Give the amount paid for agreement [102906](account_id) accound id
- Tell me something about money payment done in the deal with [105086](account_id) id
- How much amount transaction took place with the agreement [103180](account_id) id
- How much amount transferred in the agreement [103180](account_id) id
- For [103490](account_id) agreement give me the paid amount details
- For the id [103440](account_id) tell me the payment made


## intent:pending_amount
- what is the amount pending in the agreement [103256](account_id)
- what is the amount pending in the agreement with id [102729](account_id)
- what is the amount pending during the transaction with [103197](account_id) account id
- Brief me about the money to be paid in deal with account id [104112](account_id)
- Brief me about the transaction to be done in deal with agreement id [103640](account_id) 
- Brief me about the payment pending in the agreement deal with [103600](account_id) id
- Tell me how much money needs to be delivered in the transaction [101872](account_id)
- Tell me how much money needs to be paid in the transaction [101272](account_id)
- Tell me how much money is pending in the transaction [101172](account_id)
- Give the details of the money that needs to be transferred with account id [101369](account_id)
- Give the amount pending for agreement [102906](account_id) accound id
- Tell me something about money payment to be done in the deal with [105086](account_id) id
- Tell me something about money payment pending in the deal with [105086](account_id) id
- How much amount transaction is left to take place with the agreement [103180](account_id) id
- How much amount needs to be transferred in the agreement [103180](account_id) id
- For [103490](account_id) agreement give me the pending amount details
- For the id [103440](account_id) tell me the pending amount

## lookup:client_name
   data/Client_name.txt

## lookup:legal_entity
   data/legal_entity.txt

## lookup:currency
   data/currency.txt

## synonym:CitiBank Pune
- citibank Pune
- citi bank pune
- citibankpune
- Citibank Pune

