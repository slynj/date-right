from flask import Flask, request, render_template
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAkkUCXPqslmWCAMVhnAmHyk_IfkYl5EN8')

# # Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#
# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')



global userLocationInputCoord
global partnerLocationInputCoord
@app.route('/', methods=['POST'])
def testing():
    userLocationInput = request.form['userLocationInput']
    partnerLocationInput = request.form['partnerLocationInput']

    # Geocoding an address
    userLocationInput_result = gmaps.geocode(userLocationInput)
    partnerLocationInput_result = gmaps.geocode(partnerLocationInput)

    userLocationInputCoord = [userLocationInput_result[0]["geometry"]["location"]["lat"],
                              userLocationInput_result[0]["geometry"]["location"]["lng"]]

    partnerLocationInputCoord = (partnerLocationInput_result[0]["geometry"]["location"]["lat"],
                              partnerLocationInput_result[0]["geometry"]["location"]["lng"])

    #midpoint = (int(userLocationInput) + int(partnerLocationInput)) / 2
    return render_template("index.html")





if __name__ == '__main__':
    app.run(debug=True)
