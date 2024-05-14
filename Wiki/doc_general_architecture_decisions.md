# General Architecture Decisions
## Exception Handling
- In case of an exception, the next json will be returned:
```json
{
  "error": "string"
}
```
where "string" is the exception message.
## Status Codes
- The following status codes will be returned:
  - 200: OK
  - 400: Bad Request(handled exceptions, you can show the message to the user)
  - 500: Internal Server Error(unhandled exceptions, you can show a generic message to the user)
- Idk where status code will be located tbh, probably it will be located in the response.status field if you will use response objects, or it will be in the json response body in the status field, or in the status_code field.

## Ports
- The following ports will be used:
  - 8080: For the Backend
  - 8081: For the Frontend

