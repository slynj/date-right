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
    return diameter / 2


def get_restaurants(center_point, radius, price):
    # Get all restaurants within a certain radius of a center point
    if price == '$$$':  # filter for price range 4 and 3
        df = pd.read_csv('archive/filtered_business_3.csv')

    elif price == 'Free':
        df = pd.read_csv('archive/filtered_business_0.csv')

    elif price == '$$':  # filter for price range 2
        df = pd.read_csv('archive/filtered_business_2.csv')

    elif price == '$':  # filter for price range 1
        df = pd.read_csv('archive/filtered_business_1.csv')
    else:
        df = pd.read_csv('archive/filtered_business_1.csv')

    df = df[df['latitude'].notna()]
    df = df[df['longitude'].notna()]
    df['coordinates'] = list(zip(df['latitude'], df['longitude']))
    df['distance'] = df['coordinates'].apply(lambda x: geodesic(center_point, x).km)

    df = df[df['distance'] <= radius]

    return df


# now get the best possible location for the restaurant by min-maxing the distance from the centre point and the rating
def get_best_location(df, center_point):
    df['distance'] = df['coordinates'].apply(lambda x: geodesic(center_point, x).km)
    df['rating'] = df['stars']

    df['score'] = (df['rating'] * 500) + (df['review_count'] * 1.1) - (df['distance'] * 100)
    condition1 = df['attributes'].str.contains("'intimate': True", case=False, na=False)
    condition2 = df['attributes'].str.contains("'romantic': True", case=False, na=False)
    df.loc[condition1 & condition2, 'score'] += 1000
    df = df.sort_values(by=['score'], ascending=False)

    return df


def mains(coord1, coord2, price):
    midpoint = calculate_midpoint((coord1[1],coord1[0]), (coord2[1],coord2[0]))
    midpoint = (midpoint[1], midpoint[0])
    radius = get_radius(coord1, coord2)
    restaurants = get_restaurants(midpoint, radius, price)
    best_location = get_best_location(restaurants, midpoint)
    df = best_location.head(5)
    distance_user=[]
    distance_partner=[]
    for i in range(len(df)):
        distance_user.append(get_distance(coord1, (df.iloc[i]['latitude'], df.iloc[i]['longitude'])))
        distance_partner.append(get_distance(coord2, (df.iloc[i]['latitude'], df.iloc[i]['longitude'])))

    names = df['name'].tolist()
    addresses = df['address'].tolist()
    ratings = df['rating'].tolist()
    latitude = df['latitude'].tolist()
    longitude = df['longitude'].tolist()
    combined = list(zip(names, addresses, ratings, distance_user, distance_partner,latitude,longitude))
    print(combined)

    return combined

# Example usage:
# coord1 = (40.136966, -75.357208)
# coord2 = (39.798601, -74.948706)
# print(mains(coord1, coord2, 'Free'))
