# import library to allow outbound HttpRequests
import requests


def fetch_random_numbers():
    url = 'https://www.random.org/integers/'  # api endpoint
    params = {
        'num': 4,
        'min': 0,
        'max': 7,
        'col': 1,
        'base': 10,
        'format': 'plain',
        'rnd': 'new'
    }

    # save response to get request with params in response var

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # Log the response text to see how its received
            random_integers = response.text
            # print("Response from Random.org:", random_integers)
            # Additional processing can go here
            return random_integers
        else:
            print("Failed to fetch random numbers:", response.status_code)
            return None
    except requests.RequestException as e:
        print("error: ", e)


print(fetch_random_numbers())
