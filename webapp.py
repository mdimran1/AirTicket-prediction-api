# importing necessery class & function
from flask import Flask, redirect, render_template, url_for, request
import pandas as pd
import pickle

    
model = pickle.load(open('price_model.pkl', 'rb'))

# flsk app defining :
app = Flask(__name__)

# function for root page
@app.route('/', methods= ['GET'])  
def root_page():
    return render_template('index.html')


# function for prediction page
@app.route('/predict', methods= ['GET', 'POST'])
def prediction():
    if request.method == 'POST':

        # Date time Picking from departure
        dep_time = request.form['departure']
        dep_day = int(pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").day)
        dep_month = int(pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").month)
        dep_hour = int(pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(dep_time, format="%Y-%m-%dT%H:%M").minute)
                

        ###  Retrieving arrival time :
        arrival_timestamp = request.form['arrival']
        arr_hour = int(pd.to_datetime(arrival_timestamp, format="%Y-%m-%dT%H:%M").hour)
        arr_min = int(pd.to_datetime(arrival_timestamp, format="%Y-%m-%dT%H:%M").minute)
        
                
        # dummy list for airline info [0,0,0,0, for 12 times]
        # further we replace to 1 acording value
        airline_data = [x*0 for x in range(12)]

        ### retrieving airlines data :
        airline = request.form['airlines'] # from form action value
        # assigning values according airlines form input
        if airline == 'Air Asia':
            airline_data[0]=1
        elif airline == 'Air India':
            airline_data[1] = 1
        elif airline == 'GoAir':
            airline_data[2] = 1
        elif airline == 'IndiGo':
            airline_data[3] = 1
        elif airline == 'Jet Airways':
            airline_data[4] = 1
        elif airline == 'Jet Airways Business':
            airline_data[5] = 1
        elif airline == 'Multiple carriers':
            airline_data[6] = 1
        elif airline == 'Multiple carriers Premium economy':
            airline_data[7] = 1
        elif airline == 'SpiceJet':
            airline_data[8] = 1
        elif airline == 'Trujet':
            airline_data[9] = 1
        elif airline == 'Vistara':
            airline_data[10] = 1
        elif airline == 'Vistara Premium economy':
            airline_data[11] = 1
        

        # retrieving Source data
        source = request.form['source']

        # dummy list for Source info =  [0,0,0,0,0]
        source_data = [x*0 for x in range(5)]

        # further we replace to 1 acording value
        if source == "Banglore": source_data[0] = 1
        elif source == "Kolkata": source_data[3] = 1
        elif source == "Delhi": source_data[2] = 1
        elif source == "Chennai": source_data[1] = 1
        elif source == "Mumbai": source_data[4] = 1

        # retrieving destiantion data
        destination = request.form['destination']
        # dummy list for destination info =  [0,0,0,0,0]
        # further we replace to 1 acording value
        destination_data = [x*0 for x in range(5)]

        # assigning or replace new values by destination data
        if destination == "Banglore":
            destination_data[0] = 1
        elif destination == "Delhi":
            destination_data[2] = 1
        elif destination == "Kolkata":
            destination_data[4] = 1
        elif destination == "Cochin":
            destination_data[1] = 1
        elif destination == "Hyderabad":
            destination_data[3] = 1

        # ordinal values
        ## total stops retrieving :
        stops = request.form["stopage"]
        stop_data = [int(stops)]


        ## Duraton retrieving :
        
        #  logic for hour to minute
        if (dep_hour > arr_hour) :
            arrival_hour = arr_hour + 24
            # multiply the difference between starts and ending hours by 60 
            hour_to_min = (arrival_hour - dep_hour)*60
        else:
            hour_to_min = (arr_hour - dep_hour)*60

        # adjust minutes as difference between starts and ending minutes
        if  (dep_min > arr_min) :
            arrival_minute = arr_min + 60
            minutes = arrival_minute - dep_min
        else:
            minutes = arr_min - dep_min
        duration = [hour_to_min + minutes]

        ## data list decortion for passing through model
        data_list = [dep_day,dep_month, dep_hour, dep_min]+[ arr_hour, arr_min]+ airline_data + source_data + destination_data + stop_data + duration
        
        ## prediction :
        prediction = model.predict([data_list])
        prediction_round = round(prediction[0])
        
    

        return render_template('index.html', result_predictive = f'Estimate Price: {prediction_round} usd' )

    else: # redirection to home page for ['GET'] request 
        return redirect('/')
               

if __name__ == '__main__': 
        app.run(debug=True)
        