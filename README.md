#Tenant- Support Chatbot

##Project Overview
A chatbot designed to help tenants manage their premises by allowing them to create and track tickets

##Setup Instructions
###Prerequisites
-Python 3.12.2
-python-telegram-bot 21.4
-telegram 0.0.1

###Project Structure
-chatbot.py : Main entry point of the chatbot
-api/
    -auth.py - Handles API request to generate authentication token
    -find_user.py - Handles API request to fetch user details 
    -premise.py - Hanldes API request to fetch the premise details of the user
    -service_request.py - Handles API request to generate ticket
    -ticket_status.py - Handles API request to fetch ticket status 
    -media_request.py - Hnadles API request to upload media 
-handlers/
    - existing_ticket.py - Manages the interaction with existing tickets, allowing users to view the status of previously created tickets.
    - new_ticket.py - Manages the creation of new tickets

