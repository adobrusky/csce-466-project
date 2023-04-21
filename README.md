# Warehouse API Project

## Installation

### Set up the database

1. This installation makes use of XAMPP. Instructions for installing XAMPP can be found [here](https://www.apachefriends.org/download.html).
2. Launch XAMPP from the desktop and navigate to the “Manage Servers” tab. Select “Start All” at the bottom to start all servers.
3. Navigate back to the “Welcome” tab and click the “Go to Application” button in the XAMPP interface.
4. Once on the website, click on “phpMyAdmin” in the upper-right corner.
5. Navigate to the "Import" tab once phpMyAdmin loads.
6. Upload the `Database/database.sql` file and leave all other settings as is. Scroll to the bottom of the page and click “Import”. This will create the `warehouse` database and populate its tables: `customers`, `inventory`, `orders`, and `inventory_orders`.

### Install Python dependencies

1. Run the following command:
```
pip install Flask SQLAlchemy mysql-connector requests pytest
```

## Starting the API

Copy the `sample.env` file to `.env` and change the values to connect to your locally running database

1. Navigate to the project root.
2. Run the following command:
```
python ./api.py
```
3. If the API starts successfully, you should see something like this:
```
 * Serving Flask app 'api' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
```

## Testing the API
1. Start the API before running tests. See above for more details.
2. Navigate to the project root.
3. Run the following command:
```
python -m pytest ./Database/test.py
```

## Available Endpoints
Customers, inventory, and orders each have their own get one, get all, save, delete, and search endpoints. The `message` and `success` properties on each of the models are used to tell the consuming app whether the API call was successful or not. If an API call is unsuccessful, or an error occurs, the `message` will explain what happened.
### Read [GET]

Customers:

Gets a list of all customers - http://127.0.0.1:5000/customers

Gets one customer based on the id passed - http://127.0.0.1:5000/customers/{id}

Example of returned Customer JSON (http://127.0.0.1:5000/customers/1):
```
{
  "id": 1,
  "first_name": "David",
  "last_name": "Garcia",
  "address": "181 East Avenue",
  "city": "Tempe",
  "country": "USA",
  "state": "AZ",
  "postal_code": "85281",
  "email": "DavidMGarcia@teleworm.us",
  "message": null,
  "success": true
}
```

Inventory:

Gets a list of all inventory - http://127.0.0.1:5000/inventory

Gets one inventory based on the id passed - http://127.0.0.1:5000/inventory/{id}

Example of returned Inventory JSON (http://127.0.0.1:5000/inventory/1):
```
{
  "id": 1,
  "name": "Large Chocolate Chip Cookie",
  "price": 3.99,
  "message": null,
  "success": true
}
```

Orders:

Gets a list of all orders - http://127.0.0.1:5000/orders

Gets one order based on the id passed - http://127.0.0.1:5000/orders/{id}

Example of returned Order JSON (http://127.0.0.1:5000/orders/2):
```
{
  "id": 2,
  "customer_id": 7,
  "date": "2022-02-14",
  "inventory": [
    {
      "inventory_id": 7,
      "quantity": 3
    },
    {
      "inventory_id": 11,
      "quantity": 8
    }
  ],
  "message": null,
  "success": true
}
```

### Save (create/update) [POST]
Save endpoints handle both creating and updating data. Use the same JSON structures from the get endpoints above for saving. 

If the model that is POSTed to the save endpoint has an `id` then an update will occur, if no `id` is specificed then an addition will occur. Successful additions will return the same model with the newly assigned ID.

Create or update a customer - http://127.0.0.1:5000/customers

Create or update a inventory - http://127.0.0.1:5000/inventory

Create or update a order - http://127.0.0.1:5000/orders

### Delete [DELETE]
Delete endpoints will delete the customer, inventory, or order based on the passed in id.

Delete a customer - http://127.0.0.1:5000/customers/{id}

Delete a inventory - http://127.0.0.1:5000/inventory/{id}

Delete a order - http://127.0.0.1:5000/orders/{id}

### Search [POST]
Search endpoints require a search model to be POSTed. The search model JSON takes on the following structure:
```
{
  "and_or": "",
  "filters":[
    {
      "field":"",
      "operator":"",
      "value":""
    }
  ]
}
```
The `and_or` property specifies whether the search results should match **all** of the filters (and), or the results should match **any**  of the filters (or).

The `filters` property is a list of search filters. Each filter must specify a `field`, an `operator`, and a `value`.

All customer, inventory, and order properties support the `equals` operator. If searching by orders' `inventory` then the `contains any` operator is also supported.

Search customers - http://127.0.0.1:5000/customers/search

Search inventory - http://127.0.0.1:5000/inventory/search

Search orders - http://127.0.0.1:5000/orders/search

Customer search example JSON. Searching for customers where last name is "Garcia" or "Pruitt":

```
{
  "and_or": "or",
  "filters":[
    {
      "field":"last_name",
      "operator":"equals",
      "value":"Garcia"
    },
    {
      "field":"last_name",
      "operator":"equals",
      "value":"Pruitt"
    }
  ]
}
```
Example of returned JSON:
```
[
  {
    "id": 1,
    "first_name": "David",
    "last_name": "Garcia",
    "address": "181 East Avenue",
    "city": "Tempe",
    "state": "AZ",
    "postal_code": "85281",
    "country": "USA",
    "email": "DavidMGarcia@teleworm.us",
    "message": null,
    "success": true
  },
  {
    "id": 3,
    "first_name": "Sheryl",
    "last_name": "Pruitt",
    "address": "3970 Dominion St",
    "city": "Williamsburg",
    "state": "ON",
    "postal_code": "K0C 2H0",
    "country": "Canada",
    "email": "SherylAPruitt@teleworm.us",
    "message": null,
    "success": true
  }
]
```

Order search example JSON with `contains any` operator. This will return all orders that contain any of the inventory in the filter:

```
{
  "and_or": "and",
  "filters":[
    {
      "field":"inventory",
      "operator":"contains any",
      "value":[1, 2]
    }
  ]
}
```

Example of returned JSON:

```
[
  {
    "id": 1,
    "customer_id": 1,
    "date": "2022-02-09",
    "inventory": [
      {
        "inventory_id": 1,
        "quantity": 3
      },
      {
        "inventory_id": 2,
        "quantity": 1
      },
      {
        "inventory_id": 3,
        "quantity": 2
      }
    ],
    "message": null,
    "success": true
  },
  {
    "id": 70,
    "customer_id": 6,
    "date": "2022-04-18",
    "inventory": [
      {
        "inventory_id": 2,
        "quantity": 1
      },
      {
        "inventory_id": 11,
        "quantity": 3
      }
    ],
    "message": null,
    "success": true
  }
]
```
