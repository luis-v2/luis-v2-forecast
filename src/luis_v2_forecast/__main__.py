from . import fetch_air_data, fetch_available_stations, fetch_available_components



def main():
    stations = fetch_available_stations()
    components = fetch_available_components()

    for station in stations:
        for component in components:
            data = fetch_air_data(station, component, 7)

            # TODO: generate forecast

            # TODO: write data to database


if __name__ == "__main__":
    main()
