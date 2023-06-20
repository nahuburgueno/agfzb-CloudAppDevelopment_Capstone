import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data  

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    # print('json_result from line 31', json_result)    

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    print(json_result,"96")
    if json_result:
        reviews = json_result["data"]["docs"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]
            
            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/6e1e7167-2d75-4597-b4ce-71498a9d8bd8"

    # Set the required parameters for the Watson NLU API
    params = {
        "text": dealerreview,
        "version": "2021-09-01",
        "features": "sentiment",
        "return_analyzed_text": True
    }

    # Make the API call to Watson NLU using the get_request method
    response = get_request(url, api_key="8tBycdwAx523ePDxxaQETF8UyQEOYydECMf3e-pilzKM", **params)

    # Check if the response is valid
    if response is not None:
        sentiment = response.get("sentiment")
        if sentiment is not None:
            sentiment_label = sentiment.get("document").get("label")
            return sentiment_label

    return None





  


    
def get_dealer_by_id_from_cf(url, id):
    results = []

    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        print(dealers,"63")

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            if dealer_doc["id"] == id:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], 
                                       city=dealer_doc["city"], 
                                       full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], 
                                       lat=dealer_doc["lat"], 
                                       long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"], 
                                       zip=dealer_doc["zip"])                    
                results.append(dealer_obj)

    return results[0]