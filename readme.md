# Address Book App

The Address Book app is a RESTful API for managing addresses. It allows you to store, fetch, delete, and update addresses. Additionally, it provides a feature to retrieve addresses that are nearby to a given latitude and longitude within a specified distance.

## Features

-   **Create Address**: You can create a new address by sending a POST request with address details in JSON format.

-   **Fetch Address**: Retrieve an address by its unique ID using a GET request.

-   **Update Address**: Update an existing address by sending a PUT request with updated details.

-   **Delete Address**: Remove an address from the address book using a DELETE request.

-   **Retrieve Nearby Addresses**: Find addresses within a specified distance from a set of coordinates (latitude and longitude).

## API Endpoints

-   **Create Address**:

    -   Endpoint: `/addresses/`
    -   Method: POST
    -   Request Body: JSON object with address details.
    -   Response: JSON object representing the created address.

-   **Fetch Address**:

    -   Endpoint: `/addresses/{address_id}/`
    -   Method: GET
    -   Response: JSON object containing the address information.

-   **Update Address**:

    -   Endpoint: `/addresses/{address_id}/`
    -   Method: PUT
    -   Request Body: JSON object with updated address details.
    -   Response: JSON object representing the updated address.

-   **Delete Address**:

    -   Endpoint: `/addresses/{address_id}/`
    -   Method: DELETE
    -   Response: JSON indicating the success of the deletion.

-   **Retrieve Nearby Addresses**:
    -   Endpoint: `/retrieveAddresses/`
    -   Method: POST
    -   Request Body: JSON object with latitude, longitude, and distance (in kilometers).
    -   Response: JSON array containing nearby addresses.

## Getting Started

### How to install and run the application

    - Clone the repository
    - run `pip install -r requirements.txt`
    - run `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload `
