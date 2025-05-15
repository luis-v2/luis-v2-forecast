from . import fetch_air_data, fetch_available_stations, fetch_available_components

def main():
    stations = fetch_available_stations()
    station_ids = [station['id'] for station in stations if 'id' in station]

    for station_id in station_ids:
        components = fetch_available_components(station_id)
        component_ids = [component['id'] for component in components if 'id' in component]
        for component_id in component_ids:
            data = fetch_air_data(station_id, component_id, 7)

            print("-----------------------------------")
            print(f"Station ID: {station_id}, Component ID: {component_id}")
            print("")
            print(f"Data: {data}")
            print("-----------------------------------")

            # TODO: generate forecast

            # TODO: write data to database


if __name__ == "__main__":
    main()
