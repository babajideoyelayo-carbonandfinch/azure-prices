import requests
import json

RETAIL_API_URL = "https://prices.azure.com/api/retail/prices"

def fetch_azure_prices(currency=None, service_name=None):
    """
    Fetches all Azure pricing data, optionally filtered by currency and/or service name,
    and returns a list of pricing records.

    :param currency: Optional currency filter (e.g., "USD"). If None, no currency filter is applied.
    :param service_name: Optional service name filter (e.g., "Virtual Machines").
    :return: List of pricing records (dictionaries).
    """
    license_data = []

    # Build OData filter query based on provided parameters.
    filters = []
    if currency:
        filters.append(f"currencyCode eq '{currency}'")
    if service_name:
        filters.append(f"serviceName eq '{service_name}'")
    
    params = {}
    if filters:
        params["$filter"] = " and ".join(filters)
    params["$top"] = 100  # Limit per page

    next_url = RETAIL_API_URL
    first_call = True

    while next_url:
        try:
            if first_call:
                response = requests.get(next_url, params=params, timeout=10)
                first_call = False
            else:
                response = requests.get(next_url, timeout=10)

            if response.status_code != 200:
                print(f"API request failed with status {response.status_code}")
                break

            data = response.json()
            license_data.extend(data.get("Items", []))
            next_url = data.get("NextPageLink")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            break
        except ValueError as e:
            print(f"JSON parse error: {e}")
            break

    return license_data

def main():
    """
    Fetches all Azure pricing data (with no filters by default) and saves it to a JSON file.
    """
    try:
        # Fetch all data (without filtering by currency/service name)
        data = fetch_azure_prices()
        print(f"Retrieved {len(data)} pricing records.")

        # Save the full data to a JSON file.
        with open("azure_prices.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Data successfully saved to azure_prices.json")
    except Exception as e:
        print(f"Main execution error: {e}")

if __name__ == "__main__":
    main()
