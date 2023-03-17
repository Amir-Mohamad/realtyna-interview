## API Endpoints

The following API endpoints are provided by the application:

### `POST /reservations/`

Create a new reservation.

#### Request Body

The request body must be a JSON object with the following properties:

- `listing_id` (integer): The ID of the listing for which the reservation is being made.
- `name` (string): The name of the person making the reservation.
- `start_date` (string, in the format `YYYY-MM-DD`): The start date of the reservation.
- `end_date` (string, in the format `YYYY-MM-DD`): The end date of the reservation.

#### Response

If the reservation is successfully created, the server will respond with a JSON object containing the following properties:

- `id` (integer): The ID of the reservation.
- `listing_id` (integer): The ID of the listing for which the reservation was made.
- `name` (string): The name of the person making the reservation.
- `start_date` (string, in the format `YYYY-MM-DD`): The start date of the reservation.
- `end_date` (string, in the format `YYYY-MM-DD`): The end date of the reservation.
- `created_at` (string, in ISO 8601 format): The timestamp when the reservation was created.

If there is an error in the request body, the server will respond with a `400 Bad Request` status code and a JSON object containing an `errors` property with an array of error messages.

### `GET /reservations/check/`

Check if a number of rooms are available at a certain time.

#### Query Parameters

The following query parameters must be provided:

- `listing_id` (integer): The ID of the listing for which the availability is being checked.
- `start_date` (string, in the format `YYYY-MM-DD`): The start date of the availability check.
- `end_date` (string, in the format `YYYY-MM-DD`): The end date of the availability check.

#### Response

If the availability check is successful, the server will respond with a JSON object containing the following properties:

- `listing_id` (integer): The ID of the listing for which the availability was checked.
- `start_date` (string, in the format `YYYY-MM-DD`): The start date of the availability check.
- `end_date` (string, in the format `YYYY-MM-DD`): The end date of the availability check.
- `available` (boolean): Whether or not the requested number of rooms are available during the specified time period.

If there is an error in the query parameters, the server will respond with a `400 Bad Request` status code and a JSON object containing an `errors` property with an array of
error messages.

### `GET /reports/`

Get an overview of the booked rooms.

#### Query Parameters

The following query parameters are optional:

- `listing_id` (integer): The ID of the listing for which the report is being generated.
- `format` (string): The format of the report. Valid values are `html` and `text`. If no format is provided, the server will respond with a JSON object.

#### Response

If the report is successfully generated, the server will respond with the requested format.

If no format is provided or if an invalid format is requested, the server will respond with a JSON object containing the following properties:

- `listing_id` (integer): The ID of the listing for which the report was generated.
- `report` (string): The report in plain text format.

## Celery Tasks

The following Celery tasks are used by the application:

### `reservations.tasks.send_reservation_email`

Sends an email to the listing owner when a new reservation is made.

#### Arguments

The task expects the following arguments:

- `reservation_id` (integer): The ID of the reservation that was made.

### `reservations.tasks.check_availability`

Checks the availability of a listing at a certain time.

#### Arguments

The task expects the following arguments:

- `listing_id` (integer): The ID of the listing for which the availability is being checked.
- `start_date` (string, in the format `YYYY-MM-DD`): The start date of the availability check.
- `end_date` (string, in the format `YYYY-MM-DD`): The end date of the availability check.

#### Return Value

The task returns a boolean value indicating whether or not the requested number of rooms are available during the specified time period.

## Redis

The application uses Redis as a message broker for Celery tasks.

## Conclusion

In this technical challenge, we have built a Django application that provides REST API endpoints for making and tracking reservations. The application uses Redis and Celery to handle the background tasks associated with making reservations, and it includes error handling, data validation, and documentation for its API endpoints.

This implementation can be further enhanced with additional features, such as user authentication and authorization, support for multiple languages, and more detailed reporting and analytics capabilities. However, as a starting point, this implementation provides a solid foundation for building a robust and scalable reservation system that can be used by multiple listings.
