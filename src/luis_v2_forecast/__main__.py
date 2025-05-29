from . import fetch_air_data, fetch_available_stations, fetch_available_components
from prophet import Prophet
import pandas as pd
from datetime import datetime
from src.luis_v2_forecast.database import database

# --- Forecast config ---
HISTORY_DAYS = 30
FORECAST_PERIODS = 96  # 2 days * 48 half-hours
TABLE_NAME = "FORECASTS"

# --- Prophet Model ---
def generate_forecast(data: list) -> pd.DataFrame:
    if not data:
        raise ValueError("No data provided")

    # Get the dynamic key (component name) from the first entry
    value_key = next(k for k in data[0] if k != "timestamp")

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
    df = df[['timestamp', value_key]].rename(columns={
        'timestamp': 'ds',
        value_key: 'y'
    })
    df = df.dropna().sort_values('ds')

    if len(df) < 100:
        raise ValueError("Not enough data points to train the model.")

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=FORECAST_PERIODS, freq='30min')
    forecast = model.predict(future)

    return forecast[['ds', 'yhat']].tail(FORECAST_PERIODS)


def main():
    stations = fetch_available_stations()
    station_ids = [station['id'] for station in stations if 'id' in station]


    db = database(
        username="forecast_user",
        password="forecast_pass",
        host="localhost",
        port="5432",
        dbname='forecasts'
    )

    for station_id in station_ids:
        components = fetch_available_components(station_id)
        component_ids = [component['id'] for component in components if 'id' in component]
        for component_id in component_ids:
            try:
                data = fetch_air_data(station_id, component_id, HISTORY_DAYS)

                if not data:
                    print(f"⚠ No data for station {station_id}, component {component_id}")
                    continue

                predictions = generate_forecast(data)

                for _, row in predictions.iterrows():
                    db.insert_data(TABLE_NAME, {
                        "FC_STATION": station_id,
                        "FC_COMPONENT": component_id,
                        "FC_TIMESTAMP": row['ds'],
                        "FC_VALUE": float(row['yhat'])
                    })

                print(f"✅ Forecast saved for station {station_id}, component {component_id}")
            except Exception as e:
                print(f"❌ Error for station {station_id}, component {component_id}: {e}")
    db.close()

            # TODO: generate forecast

            # TODO: write data to database


if __name__ == "__main__":
    main()
