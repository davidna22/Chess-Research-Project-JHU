-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------
README:
Extracting the Data:
-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------

Step 1: API Call

There are two steps to running the GET step. The first is the API call. You DO NOT need to run the API
call in order to do step two. The API call step can take up to 24 hours to complete (limited by the
speed throttle of Lichess database). At the end of the API call all essential dataframes are saved
as a CSV file and those CSV files are used in the next step.

PLEASE NOTE THE REQUIREMENTS FOR THE API CALL AT THE BOTTOM OF STEP 1.

To run step 1, all you need to do is restart and run all in the following file:
Data Extraction (API).ipynb

Linked Class File:

Extractor.py

This file contains the class I created to help parse the API data. There are 6 important methods
- Initializor: 
	Creates the requests session

- Request(self, method, path, **kwargs): 
	Initializes a request to be made to the API

- Get(self, **kwargs): 
	helper function to make a GET request. 
	Params should be provided here

- parse(response, convert=False): 
	returns the JSON response as a JSON to read. 
	(Convert option was omitted)

- parse_team(user_data): 
	Takes as argument the return from parse (NDJson file)
	Returns a dataframe of all the users on the parsed team with their profile data

- parse_games(game_data):
	Takes as a list of games from the API
	args must be a dictionary (for optimal speed)
	Returns a dataframe of all the games pulled

- parse_countries(data_list):
	Takes a list of games (returned from parse_games)
	Generates an API call to get the country and number of games the player has played
	Returns a dataframe of the game_data updated with the new values

- parse_winstreak(data_list):
	Takes a list of games (returned from parse_games)
	Gets the current winstreak of the player up to the time of the game
	Due to how long it took to run this call, it is omitted from the data


REQUIREMENTS:
**import ndjson**
NDJSON must be a package installed via pip - Lichess data only available in PGN or NDJSON

-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------

Step 2: CSVs to DB

Extract.ipynb

Simply reads the CSV files for each of the data tables from the API call.
Creates tables in the database: chessdb.db
You can run the code in Extract.ipynb to perform this step.

Tables in DB:
countries : Maps country to Two letter code
users : List of all scraped users
users_selected : List of all the users I select to scrape games from
all_games_raw : List of all available games on file
all_games_country : List of all games with the country filled
all_games_country_selected : List of all games selected with country
all_games_countries_winstreak : List of all games with country and winstreak (incomplete)

-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------


