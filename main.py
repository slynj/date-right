import pandas as pd
from geopy.distance import geodesic, distance
import great_circle_calculator.great_circle_calculator as gcc
from hugchat import hugchat
from hugchat.login import Login


def calculate_midpoint(p1, p2):
    # Calculate the midpoint between two coordinates
    
    return gcc.midpoint(p1, p2)



def get_radius(coord1, coord2):
    # Calculate the radius between two coordinates
    diameter = geodesic(coord1, coord2).km
    return diameter



def get_restaurants(center_point, radius):
    # Get all restaurants within a certain radius of a center point
    df = pd.read_csv('archive/yelp_academic_dataset_business.csv')
    df = df[df['categories'].str.contains('Restaurant', case=False, na=False)]
    df = df[df['latitude'].notna()]
    df = df[df['longitude'].notna()]
    df['coordinates'] = list(zip(df['latitude'], df['longitude']))
    df['distance'] = df['coordinates'].apply(lambda x: geodesic(center_point, x).km)
    
    df = df[df['distance'] <= radius]

    return df

# filter restaurants by price range and ratings
def filter_restaurants(df, rating):
    df = df[df['stars'] >= rating]
    df = df[df['review_count'] >= 50]
    return df

# now get the best possible location for the restaurant by min-maxing the distance from the centre point and the rating
def get_best_location(df, center_point):
    df['distance'] = df['coordinates'].apply(lambda x: geodesic(center_point, x).km)
    df['rating'] = df['stars']

    df['score'] = -(df['distance'] * 0.6) + (df['rating'] * 0.5) + (df['review_count'] * 0.8)
    df = df.sort_values(by=['score'], ascending=False)
    print(df.head(10))
    return df

def main(coord1, coord2):
    midpoint = calculate_midpoint(coord1, coord2)
    radius = get_radius(coord1, coord2)
    restaurants = get_restaurants(midpoint, radius)
    restaurants = filter_restaurants(restaurants, 4)
    best_location = get_best_location(restaurants, midpoint)
    top10= best_location['name'].head(10).to_string(index=False)


    # Log in to huggingface and grant authorization to huggingchat
    sign = Login('bhuvnesh112005@gmail.com', 'xowfud-nexgud-teKmu6')
    cookies = sign.login()

    # Save cookies to the local directory
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)

    # Load cookies when you restart your program:
    # sign = login(email, None)
    # cookies = sign.loadCookiesFromDir(cookie_path_dir) # This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.

    # Create a ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"

    # non stream response
    query_result = chatbot.query(top10 +" which one is the best for a romantic date? reply with just the name of the restaurant and average price per head.")
    return (query_result) 
    













# Example usage:
coord1 = (40.136966, -75.357208)
coord2 = (39.798601, -74.948706)
print(main(coord1, coord2))
