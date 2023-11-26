from flask import Flask, request, render_template, jsonify
from filter import mains
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBgfO7mb91JqcGlSLJVjdf-EFWs6l_MSQU')

# # Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#
# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

app = Flask(__name__)



@app.route('/')
def home():
    # index.html
    return render_template('index.html')


@app.route('/home')
def backhome():
    return render_template('index.html')


global userLocationInputCoord
global partnerLocationInputCoord
global my_lat_global
global my_lng_global
global pt_lat_global
global pt_lng_global
global places_lst
global priceSelectInput
@app.route('/', methods=['POST'])
def testing():
    userLocationInput = request.form['userLocationInput']
    partnerLocationInput = request.form['partnerLocationInput']
    priceSelectInput = request.form['priceSelect']

    # Geocoding an address
    userLocationInput_result = gmaps.geocode(userLocationInput)
    partnerLocationInput_result = gmaps.geocode(partnerLocationInput)

    userLocationInputCoord = [userLocationInput_result[0]["geometry"]["location"]["lat"],
                              userLocationInput_result[0]["geometry"]["location"]["lng"]]

    partnerLocationInputCoord = [partnerLocationInput_result[0]["geometry"]["location"]["lat"],
                              partnerLocationInput_result[0]["geometry"]["location"]["lng"]]

    #midpoint = (int(userLocationInput) + int(partnerLocationInput)) / 2

    my_lat_global = userLocationInputCoord[0]
    my_lng_global = userLocationInputCoord[1]
    pt_lat_global = partnerLocationInputCoord[0]
    pt_lng_global = partnerLocationInputCoord[1]
    combined = mains((my_lat_global, my_lng_global), (pt_lat_global, pt_lng_global), priceSelectInput)
    places_lst = []

    for i in range(len(combined)):
        places_lst.append((combined[i][1], combined[i][-2], combined[i][-1]))
    
    print('DON', places_lst)
    print('DON2', combined)

    # print(userLocationInputCoord)
    # print(partnerLocationInputCoord)
    return render_template("second.html",
                           my_lat=my_lat_global,
                           my_lng=my_lng_global,
                           pt_lat=pt_lat_global,
                           pt_lng=pt_lng_global,
                           my_places=places_lst,
                           combined_data=combined,
                           )



# @app.route('/get_list', methods=['GET'])
# def get_list():
#     # Call your Python function that returns a list
#     result_list = filter.mains((my_lat_global, my_lng_global), (pt_lat_global, pt_lng_global), 'free')
#     print(result_list)
#     # Return the list as JSON
#     return jsonify(result=result_list)



if __name__ == '__main__':
    app.run(debug=True)
