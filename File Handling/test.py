intents:
  - lol_work
  - greet
  - goodbye
  - affirm
  - deny
  - bot_challenge
  - payment_status
  - pending_payment

entities:
  - legal_entity
  - client_name
  - currency
  - payment_date
  - amount
  - account_id

actions:
  - lol_work
  - action_payment
  - action_pending

responses:
  utter_greet:
  - text: "Hey! How are you?"

  utter_did_that_help:
  - text: "Did that help you?"

  utter_goodbye:
  - text: "Bye"

  utter_iamabot:
  - text: "I am a bot, powered by Rasa."

  utter_payment:
  - text: "I have received the payment"

  utter_default:
  - text: "Please try again !!"

session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true
