import requests
import dotenv
import os
from dotenv import load_dotenv



# FUNCTIONS

def prompt(message): #simple Y/N prompt that returns bool
    while True:
        user_input = input(message + " (Y/N): ").strip().lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")




# MAIN SCRIPT

#load environment variables from the .env file
load_dotenv()

#get API key
api_key = os.environ.get("API_KEY")

#get search term
search_query = input("Enter a search term (e.g., event title, performer, or venue): ")

#set up parameters and define API endpoint URL for finding event
params = { 
    "client_id": api_key,
    "q": search_query
}
url = "https://api.seatgeek.com/2/events"

#send the request to get a venue ID
response = requests.get(url, params=params)

#check if the request was successful ? prompt : error
if response.status_code == 200:
    #parse the JSON response and extract relevent info to prompt user
    data = response.json()
    events = data["events"]


    for event in events: #for each event
        #get info
        event_id = event["id"]
        title = event["title"]
        venue = event["venue"]["name"]
        date = event["datetime_local"]

        #print an event for user to either interrogate or pass
        print(f"Event ID: {event_id}, Title: {title}, Venue: {venue}, Date: {date}") 
        result = prompt("Do you to interrogate this venue?")
        if result:
            print(f"Interrogating event ID: {event_id}")

            #define the API endpoint URL for finding event info
            url = f"https://api.seatgeek.com/2/events/{event_id}"

            #send the API request
            response = requests.get(url, params=params)

            #check if the request was successful ? prompt : error
            if response.status_code == 200:
                #parse the JSON response and extract relevent info to prompt user
                data = response.json()
                listings = data["stats"]["listing_count"]
                average_price = data["stats"]["average_price"]
                lowest_price = data["stats"]["lowest_price"]
                highest_price = data["stats"]["highest_price"]

                print(f"Total Listings: {listings}")
                print(f"Average Price: ${average_price}")
                print(f"Lowest Price: ${lowest_price}")
                print(f"Highest Price: ${highest_price}")
            else:
                print(f"Error: {response.status_code} - {response.text}")
            exit(0)


        else:
            print("Searching for other events that match the search query...")
            continue


    print(f"Error: there are no more events matching these parameters")
    exit(1)

    
else:
    print(f"Error: {response.status_code} - {response.text}")


