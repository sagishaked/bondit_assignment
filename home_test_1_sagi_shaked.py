import pandas as pd

global SUCCESS_TODAY
SUCCESS_TODAY = 0
FAIL = 'fail'
SUCCESS = 'success'
MAX_PER_DAY = 20
MINIMUM_INTERVAL = 180

flights_df = pd.read_csv('flights.csv')

new_cols = []
for col in flights_df.columns:
    new_cols.append(col.strip())
flights_df.columns = new_cols


def strip_values(row):
    cols = ['flight ID', 'Arrival', 'Departure', 'success']
    for col in cols:
        row[col] = row[col].strip()


flights_df.apply(strip_values, axis=1)
flights_df = flights_df.sort_values(by='Arrival')


def add_success(row):
    global SUCCESS_TODAY
    if SUCCESS_TODAY > MAX_PER_DAY:
        row['success'] = FAIL
    else:
        total_minutes = 0
        arrival_h = int(row['Arrival'].strip()[:2])
        departure_h = int(row['Departure'].strip()[:2])
        total_minutes += 60 * (departure_h - arrival_h)
        arrival_m = int(row['Arrival'].strip()[3:5])
        departure_m = int(row['Departure'].strip()[3:5])
        total_minutes += departure_m
        total_minutes -= arrival_m
        time_success = total_minutes >= MINIMUM_INTERVAL

        if time_success:
            row['success'] = SUCCESS
            SUCCESS_TODAY += 1
        else:
            row['success'] = FAIL


flights_df.apply(add_success, axis=1)


flights_df.to_csv('after_q1_flights.csv', index=False)
### flight_df is ready

### flight_df is ready
