from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)


@app.route('/flight_info/<string:flight_id>', methods=['GET'])
def return_info(flight_id):
    flights_data = pd.read_csv('flights_1.csv')
    d = flights_data[flights_data['flight ID'] == flight_id].to_dict(orient='index')
    if len(d) == 0:
        ret_info = jsonify({flight_id: "flight ID does not exist"})
    else:
        ret_info = jsonify(d[0])
    return ret_info


@app.route('/add_flight', methods=['POST'])
def add_flight():
    needed_keys = ['flight ID', 'Arrival', 'Departure', 'success']
    missed_keys = []
    json_keys = request.json.keys()
    for k in needed_keys:
        if k not in json_keys:
            missed_keys.append(k)
    if len(missed_keys) != 0:
        return jsonify({'missing flight details': missed_keys})
    else:
        flights_data = pd.read_csv('flights_1.csv')
        new_flight = {'flight ID': request.json['flight ID'], 'Arrival': request.json['Arrival'],
                      'Departure': request.json['Departure'], 'success': request.json['success']}
        flights_data = flights_data.append(new_flight, ignore_index=True)
        flights_data.to_csv('flights_1.csv', index=False)

        return jsonify({'flights': [flights_data.to_dict()]})



@app.route('/remove_flight/<string:flight_id>', methods=['POST'])
def remove_flight(flight_id):
    flights_data = pd.read_csv('flights_1.csv')
    flights_data_after_drop = flights_data.loc[flights_data["flight ID"] != flight_id]
    if flights_data.equals(flights_data_after_drop):
        return jsonify({flight_id: 'no flight id to remove'})
    else:
        flights_data_after_drop.to_csv('flights_1.csv', index=False)
        return jsonify({'flights': [flights_data_after_drop.to_dict()]})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
