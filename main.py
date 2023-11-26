import pandas as pd
from geopy.distance import geodesic, distance
import great_circle_calculator.great_circle_calculator as gcc


def calculate_midpoint(p1, p2):
    # Calculate the midpoint between two coordinates
    
    return gcc.midpoint(p1, p2)

def get_distance(coord1, coord2):
    # Calculate the distance between two coordinates
    return geodesic(coord1, coord2).km


def get_radius(coord1, coord2):
    # Calculate the radius between two coordinates
    diameter = geodesic(coord1, coord2).km
    return diameter/2



def get_restaurants(center_point, radius,price):
    # Get all restaurants within a certain radius of a center point
    df = pd.read_csv('archive/yelp_academic_dataset_business.csv')
    if price == '$$$': #filter for price range 4 and 3
        condition_1 = df['attributes'].str.contains("'RestaurantsPriceRange2': '3'", case=False, na=False)
        condition_2 = df['attributes'].str.contains("'RestaurantsPriceRange2': '4'", case=False, na=False)
        condition_3 = df['categories'].str.contains("Restaurants", case=False, na=False)
        df = df[(condition_1 | condition_2) & condition_3]

    elif price == 'Free':
        condition_1 = df['categories'].str.contains('Parks', case=False, na=False)
        condition_0 = df['categories'].str.contains('Active Life', case=False, na=False)
        condition_2 = ~df['categories'].str.contains('Amusement Parks', case=False, na=False)
        condition_3 = ~df['categories'].str.contains('Dog Parks', case=False, na=False) 
        condition_4 = ~df['categories'].str.contains('Skate Parks', case=False, na=False)
        condition_5 = df['categories'].str.contains('Landmarks & Historical Buildings', case=False, na=False)
        condition_6 = ~df['categories'].str.contains('Restaurants', case=False, na=False)

        df= df[((condition_1 & condition_2 & condition_3 & condition_4 & condition_0) | condition_5) & condition_6]

    elif price == '$$': #filter for price range 2
        condition_1 = df['attributes'].str.contains("'RestaurantsPriceRange2': '2'", case=False, na=False)
        condition_2 = df['categories'].str.contains("Restaurants", case=False, na=False)
        condition_3 = df['categories'].str.contains("Cafes", case=False, na=False)
        condition_4 = df['categories'].str.contains("Cafes", case=False, na=False)

        df= df[((condition_1 & condition_2) | condition_3 | condition_4)]

    elif price == '$': #filter for price range 1
        condition_1 = df['attributes'].str.contains("'RestaurantsPriceRange2': '1'", case=False, na=False)
        condition_2 = df['categories'].str.contains("Restaurants", case=False, na=False)
        condition_3 = df['categories'].str.contains("Bubble Tea", case=False, na=False)
        condition_4 = df['categories'].str.contains("Bowling", case=False, na=False)
        condition_5 = df['categories'].str.contains("Cinema", case=False, na=False)


        df= df[((condition_1 & condition_2) | condition_3 | condition_4 | condition_5)]




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

    df['score'] =  (df['rating'] * 500) + (df['review_count'] * 1.1) - (df['distance'] * 100)
    condition1 = df['attributes'].str.contains("'intimate': True", case=False, na=False)
    condition2=df['attributes'].str.contains("'romantic': True", case=False, na=False)
    df.loc[condition1 & condition2, 'score'] += 1000
    df = df.sort_values(by=['score'], ascending=False)
    print(df.head(10))
    return df

def main(coord1, coord2, price):
    midpoint = calculate_midpoint(coord1, coord2)
    radius = get_radius(coord1, coord2)
    restaurants = get_restaurants(midpoint, radius,price)
    restaurants = filter_restaurants(restaurants, 4)
    best_location = get_best_location(restaurants, midpoint)
    df= best_location.head(3)
    distance_user=[get_distance(coord1, (df.iloc[0]['latitude'],df.iloc[0]['longitude'])),get_distance(coord1, (df.iloc[1]['latitude'],df.iloc[1]['longitude'])),get_distance(coord1, (df.iloc[2]['latitude'],df.iloc[2]['longitude']))]
    distance_partner= [get_distance(coord2, (df.iloc[0]['latitude'],df.iloc[0]['longitude'])),get_distance(coord2, (df.iloc[1]['latitude'],df.iloc[1]['longitude'])),get_distance(coord2, (df.iloc[2]['latitude'],df.iloc[2]['longitude']))]
    names = df['name'].tolist()
    addresses = df['address'].tolist()
    ratings= df['rating'].tolist()
    combined = list(zip(names,addresses,ratings,distance_user,distance_partner))

    return combined




# # Example usage:
# coord1 = (40.136966, -75.357208)
# coord2 = (39.798601, -74.948706)
# print(main(coord1, coord2,'Free'))

