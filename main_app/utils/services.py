import requests


class RandomNumberService:
    '''
    Service handles fetching and preprocessing of api call to random number generator.

    Returns a list of 4 numbers from 1-7 as strings (['1', '1', '4,', '7']) in a variable winning_combinations
    '''

    def __init__(self):
        self.url = 'https://www.random.org/integers/'  # api endpoint
        self.params = {
            'num': 4,
            'min': 0,
            'max': 7,
            'col': 1,
            'base': 10,
            'format': 'plain',
            'rnd': 'new'
        }

    def fetch_random_numbers(self):
        try:
            response = requests.get(self.url, params=self.params)
            if response.status_code == 200:  # if get request is successful successful
                # Log the response text and preprocess with split() to remove whitespace and \n to create a winning combination
                winning_combination = response.text.split()
                # Additional processing can go here if needed. for now an array of nums as strings is fine.
                return winning_combination
            # if the HTTP
            else:
                # Handle non-successful HTTP status code
                print("Failed to fetch random numbers:", response.status_code)
                return None
        except requests.RequestException as e:
            print("Error occurred during API request:", e)
            return None
