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
        "id": "string",
        "email": "string",
        "seller_info": {
            "organization": "string",
            "phone": "string",
            "address": "string"
        }
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
        "id": "d4a83f44-a5f0-4c1e-9666-6febde8fbf9c",
        "email": "test@example.com",
        "client_info": {
            "name": "string",
            "surname": "string",
            "phone": "string",
            "address": "string",
            "balance": 99388.4
        }
    }
}
```
## Seller Add Product Seller Get all Products
- **GET** /api/seller/{seller_id}/product
<br> response:
```json
{
  "content": [
    {
        "id": "1f154d40-bf20-40ab-90d0-c86740a538dc",
        "name": "product23",
        "price": 122.32,
        "description": "description",
        "image": "https://picsum.photos/id/237/200/300",
        "owner": {
          "email": "string",
            "seller_info": {
                "organization": null
            },
            "average_rating": 5.0,
            "reviews": [
                {
                    "text": "dwa",
                    "rating": 5,
                    "client": {
                        "name": "string",
                        "surname": "string"
                    }
                },
                {
                    // another review
                }
            ]
        },
        "average_rating": 4.0,
        "reviews": [
            {
                "text": "good",
                "rating": 5,
                "client": {
                      "name": "string",
                      "surname": "string"
                }
            },
            {
                // another review
            }
        ],
        "items_available": 3,
        "tags": "test"
    },
    {
        // another product
    }
  ]
}
```
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
  "content": {
    "id": "string"
  }
}
```
# Get Products
## Get Products according to tags and name
- **POST** /api/product
<br> request:
```json
{
    "request": "string"
}
```
response:
```json
{
  "content": [
    {
                        "id": "1f154d40-bf20-40ab-90d0-c86740a538dc",
                        "name": "product23",
                        "price": 122.32,
                        "description": "description",
                        "image": "https://picsum.photos/id/237/200/300",
                        "owner": {
                          "email": "string",
                            "seller_info": {
                                "organization": null
                            },
                            "average_rating": 5.0,
                            "reviews": [
                                {
                                    "text": "dwa",
                                    "rating": 5,
                                    "client": {
                                        "name": "string",
                                        "surname": "string"
                                    }
                                },
                                {
                                    // another review
                                }
                            ]
                        },
                        "average_rating": 4.0,
                        "reviews": [
                            {
                                "text": "good",
                                "rating": 5,
                                "client": {
                                      "name": "string",
                                      "surname": "string"
                                }
                            },
                            {
                                // another review
                            }
                        ],
                        "items_available": 3,
                        "tags": "test"
                    },
                    {
                   // another product
                    }
  ]
}
```
- **GET** /api/product
<br> response:
```json
{
  "content": [
    {
                        "id": "1f154d40-bf20-40ab-90d0-c86740a538dc",
                        "name": "product23",
                        "price": 122.32,
                        "description": "description",
                        "image": "https://picsum.photos/id/237/200/300",
                        "owner": {
                          "email": "string",
                            "seller_info": {
                                "organization": null
                            },
                            "average_rating": 5.0,
                            "reviews": [
                                {
                                    "text": "dwa",
                                    "rating": 5,
                                    "client": {
                                        "name": "string",
                                        "surname": "string"
                                    }
                                },
                                {
                                    // another review
                                }
                            ]
                        },
                        "average_rating": 4.0,
                        "reviews": [
                            {
                                "text": "good",
                                "rating": 5,
                                "client": {
                                      "name": "string",
                                      "surname": "string"
                                }
                            },
                            {
                                // another review
                            }
                        ],
                        "items_available": 3,
                        "tags": "test"
                    },
                    {
                   // another product
                    }
  ]
}
```
## Buy Product
- **POST** /api/client/{client_id}/product/{product_id}
<br> request:
```json
{
    // empty
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
- **PUT** /api/client/{client_id}
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
        "id": "d4a83f44-a5f0-4c1e-9666-6febde8fbf9c",
        "email": "test@example.com",
        "client_info": {
            "name": "string",
            "surname": "string",
            "phone": "string",
            "address": "string",
            "balance": 99388.4
        },
        "cart": {
            "orders": [
                {
                    "quantity": 2,
                    "product": {
                        "id": "1f154d40-bf20-40ab-90d0-c86740a538dc",
                        "name": "product23",
                        "price": 122.32,
                        "description": "description",
                        "image": "https://picsum.photos/id/237/200/300",
                        "owner": {
                          "email": "string",
                            "seller_info": {
                                "organization": null
                            },
                            "average_rating": 5.0,
                            "reviews": [
                                {
                                    "text": "dwa",
                                    "rating": 5,
                                    "client": {
                                        "name": "string",
                                        "surname": "string"
                                    }
                                },
                                {
                                    // another review
                                }
                            ]
                        },
                        "average_rating": 4.0,
                        "reviews": [
                            {
                                "text": "good",
                                "rating": 5,
                                "client": {
                                      "name": "string",
                                      "surname": "string"
                                }
                            },
                            {
                                // another review
                            }
                        ],
                        "items_available": 3,
                        "tags": "test"
                    }
                },
                {
                // another order
                }
            ]
        },
        "purchases": [
            {
                "product": "product23",
                "quantity": 2,
                "date": "2024-05-18T09:23:59.862403Z",
                "cost": 244.64
            },
            {
                // another purchase
            }
        ]
    }
}
```
- **PUT** /api/seller/{seller_id}
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
        "id": "string",
        "email": "string",
        "seller_info": {
            "organization": "string",
            "phone": "string",
            "address": "string"
        },
        "products": [
                  {
                        "id": "1f154d40-bf20-40ab-90d0-c86740a538dc",
                        "name": "product23",
                        "price": 122.32,
                        "description": "description",
                        "image": "https://picsum.photos/id/237/200/300",
                        "owner": {
                          "email": "string",
                            "seller_info": {
                                "organization": null
                            },
                            "average_rating": 5.0,
                            "reviews": [
                                {
                                    "text": "dwa",
                                    "rating": 5,
                                    "client": {
                                        "name": "string",
                                        "surname": "string"
                                    }
                                },
                                {
                                    // another review
                                }
                            ]
                        },
                        "average_rating": 4.0,
                        "reviews": [
                            {
                                "text": "good",
                                "rating": 5,
                                "client": {
                                      "name": "string",
                                      "surname": "string"
                                }
                            },
                            {
                                // another review
                            }
                        ],
                        "items_available": 3,
                        "tags": "test"
                    },
                    {
                      // another product
                    }
                
        ],
        "purchases": [
            {
                "product": "string",
                "quantity": 2,
                "date": "2024-05-18T09:23:59.862403Z",
                "cost": 244.64
            },
            {
            // another purchase
            }
        ]
    }
}
```

# Change and delete Product Info
- **PUT** /api/seller/{seller_id}/product/{product_id}
<br>request:
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
- **DELETE** /api/seller/{seller_id}/product/{product_id}
<br> response:
```json
{
  "content": "success"
}
```


# Client Cart
## get cart
- **GET** /api/client/{client_id}/cart
<br> response:
```json
{
  "content": {
    "orders": [
        {
            "quantity": 2,
            "product": {
                "id": "1f154d40-bf20-40ab-90d0-c86740a538dc",
                "name": "product23",
                "price": 122.32,
                "description": "description",
                "image": "https://picsum.photos/id/237/200/300",
                "owner": {
                  "email": "string",
                    "seller_info": {
                        "organization": null
                    },
                    "average_rating": 5.0,
                    "reviews": [
                        {
                            "text": "dwa",
                            "rating": 5,
                            "client": {
                                "name": "string",
                                "surname": "string"
                            }
                        },
                        {
                            // another review
                        }
                    ]
                },
                "average_rating": 4.0,
                "reviews": [
                    {
                        "text": "good",
                        "rating": 5,
                        "client": {
                              "name": "string",
                              "surname": "string"
                        }
                    },
                    {
                        // another review
                    }
                ],
                "items_available": 3,
                "tags": "test"
            }
        },
        {
            // another order
        }
    ]
  }
}
```
## add products to cart
- **PUT** /api/client/{client_id}/cart
<br> request:
```json
{
    "orders":[
        {
            "product":"1f154d40-bf20-40ab-90d0-c86740a538dc",
            "quantity":2
        },
        {
            "product":"087b5341-8803-4e28-b6f4-7e3ad9949b62",
            "quantity":3
        },
        {
            // another order
        }
    ]
}
```
response:
```json
{
  "content": "success"
}
```
## buy products from cart
- **POST** /api/client/{client_id}/cart
<br> response:
```json
{
  "content": "success"
}
```

# Client Purchases
## get purchases
- **GET** /api/client/{client_id}/purchases
<br> response:
```json
{
  "content": [
    {
        "product_id": "1f154d40-bf20-40ab-90d0-c86740a538dc",
        "product": "product23",
        "quantity": 2,
        "date": "2024-05-18T09:23:59.862403Z",
        "cost": 244.64
    },
    {
        // another purchase
    }
  ]
}
```

# Seller Purchases
## get purchases
- **GET** /api/seller/{seller_id}/purchases
<br> response:
```json
{
  "content": [
    {
        "product_id": "1f154d40-bf20-40ab-90d0-c86740a538dc",
        "product": "product23",
        "quantity": 2,
        "date": "2024-05-18T09:23:59.862403Z",
        "cost": 244.64
    },
    {
        // another purchase
    }
  ]
}
```
# Reviews
## Add Product Review
- **POST** /api/client/{client_id}/product/review/{product_id}
<br> request:
```json
{
    "text": "string",
    "rating": "int"
}
```
response:
```json
{
  "content": "success"
}
```
## Add Seller Review
- **POST** /api/client/{client_id}/seller/review/{seller_id}
<br> request:
```json
{
    "text": "string",
    "rating": "int"
}
```
response:
```json
{
  "content": "success"
}
```

## Get Random Product
- **GET** /api/product/random
<br> response:
```json
{
  "content": {
    "id": "1f154d40-bf20-40ab-90d0-c86740a538dc",
    "name": "product23",
    "price": 122.32,
    "description": "description",
    "image": "https://picsum.photos/id/237/200/300",
    "owner": {
        "email": "string",
        "seller_info": {
            "organization": null
        },
        "average_rating": 5.0,
        "reviews": [
            {
                "text": "dwa",
                "rating": 5,
                "client": {
                    "name": "string",
                    "surname": "string"
                }
            },
            {
                // another review
            }
        ]
    },
    "average_rating": 4.0,
    "reviews": [
        {
            "text": "good",
            "rating": 5,
            "client": {
                  "name": "string",
                  "surname": "string"
            }
        },
        {
            // another review
        }
    ],
    "items_available": 3,
    "tags": "test"
  }
}
```

## Get Product by ID
- **GET** /api/product/id/{product_id}
<br> response:
```json
{
  "content": {
    "id": "1f154d40-bf20-40ab-90d0-c86740a538dc",
    "name": "product23",
    "price": 122.32,
    "description": "description",
    "image": "https://picsum.photos/id/237/200/300",
    "owner": {
        "email": "string",
        "seller_info": {
            "organization": null
        },
        "average_rating": 5.0,
        "reviews": [
            {
                "text": "dwa",
                "rating": 5,
                "client": {
                    "name": "string",
                    "surname": "string"
                }
            },
            {
                // another review
            }
        ]
    },
    "average_rating": 4.0,
    "reviews": [
        {
            "text": "good",
            "rating": 5,
            "client": {
                  "name": "string",
                  "surname": "string"
            }
        },
        {
            // another review
        }
    ],
    "items_available": 3,
    "tags": "test"
  }
}
```