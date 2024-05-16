# Endpoints
## Register
- **POST** /api/seller/register
<br> request:
```json
{
    "email": "string",
    "password": "string"
}

```

response:
```json
{
  "content": {
    "email": "string",
    "id": "string"
  }
}
```
- **POST** /api/client/register
<br> request:
```json
{
    "email": "string",
    "password": "string"
}
```
response:
```json
{
  "content": {
    "email": "string",
    "id": "string"
  }
}
```
## Login
- **POST** /api/seller/login
<br> request:
```json
{
    "email": "string",
    "password": "string"
}
```
response:
```json
{
  "content": {
    "email": "string",
    "id": "string"
  }
}
```
- **POST** /api/client/login
<br> request:
```json
{
  "content": {
    "email": "string",
    "id": "string"
  }
}
```
response:
```json
{
  "content": {
    "email": "string",
    "id": "string"
  }
}
```
## Add Product
- **POST** /api/seller/{seller_id}/product
<br> request:
```json
{
    "name": "string",
    "price": "float",
    "description": "string",
    "image": "string",
    "tags": "string",
    "items_available": "int"
}
```
response:
```json
{
  "content": "success"
}
```
## Get Products
- **GET** /api/product
<br> response:
```json
{
  "content": [
    {
      "id": "string",
      "name": "string",
      "price": "float",
      "description": "string",
      "image": "string",
      "tags": "string",
      "items_available": "int"
    }
  ]
}
```
## Buy Product
- **POST** /api/client/{client_id}/product/{product_id}
<br> request:
```json
{
    /// empty for now
}
```
response:
```json
{
  "content": "success"
}
```
## Add Balance
- **POST** /api/client/{client_id}/balance
<br> request:
```json
{
    "balance": "float"
}
```
response:
```json
{
  "content": "success"
}
```
## Change Info
- **POST** /api/client/{client_id}
<br> request:
```json
{
    "name": "string",
    "surname": "string",
    "address": "string",
    "phone": "string"
}
```
response:
```json
{
  "content": "success"
}
```
- **GET** /api/client/{client_id}
<br> response:
```json
{
  "content": {
    "name": "string",
    "surname": "string",
    "address": "string",
    "phone": "string",
    "balance": "float",
    "email": "string",
    "id": "string"
  }
}
```
- **POST** /api/seller/{seller_id}
<br> request:
```json
{
    "organization": "string",
    "address": "string",
    "phone": "string"
}
```
response:
```json
{
  "content": "success"
}
```
- **GET** /api/seller/{seller_id}
<br> response:
```json
{
  "content": {
    "organization": "string",
    "address": "string",
    "phone": "string",
    "email": "string",
    "id": "string"
  }
}
```
