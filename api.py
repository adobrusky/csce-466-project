from flask import jsonify, request, Flask
from flask.json import JSONEncoder
from datetime import date
from Database.data_helper import DataHelper
from Database.data_models import Order, Inventory, Customer
from Database.search_models import Filter, Search
from dotenv import load_dotenv
import os

load_dotenv()

# This method prevents the order date from being formatted other than UTC
class CustomJSONEncoder(JSONEncoder):
  def default(self, obj):
    try:
      if isinstance(obj, date):
        return obj.isoformat()
      iterable = iter(obj)
    except TypeError:
      pass
    else:
      return list(iterable)
    return JSONEncoder.default(self, obj)

# Basic API setup
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config["DEBUG"] = True

data_helper = DataHelper(os.environ.get('DB_HOST'), os.environ.get('DB_PORT', 3306), os.environ.get('DB_DATABASE', 'warehouse'), os.environ.get('DB_USER', 'root'), os.environ.get('DB_PASS'))

# Serializes an object (inventory, person, etc.) into a dictionary
def serialize(object, class_name):
  dictionary = {field.name: getattr(object, field.name) for field in object.__table__.columns}
  # Orders need special logic to pull in the inventory
  if class_name == Order:
    lst_inventory = []
    order_id = dictionary.get("id")
    for inventory_order in data_helper.get_inventory_orders_by_order_id(order_id):
      inventory_dict = {"inventory_id":inventory_order.inventory_id, "quantity":inventory_order.quantity}
      lst_inventory.append(inventory_dict)
    dictionary['inventory'] = lst_inventory
  return dictionary


# Deserializes a dictionary into an object of the passed in class 
def deserialize(dictionary, class_name):
  if class_name != Search:
    object = class_name()
    for key in dictionary:
      # This throws off the add logic if order has this
      if not (class_name == Order and key == "inventory"):
        setattr(object, key, dictionary[key])
    return object
  else:
    # Searches need special deserialization logic and validation
    filters_dict = dictionary.get('filters')
    and_or = dictionary.get('and_or')
    if filters_dict is None or and_or is None:
      return Search(and_or="", filters=[], message="Invalid search model. Each search model should have 'filters', and 'and/or' properties.", success=False)
    if and_or != "and" and and_or != "or":
      return Search(and_or="", filters=[], message="Invalid search model. The 'and_or' property should be either 'and' or 'or'.", success=False)
    filters = []
    for filter in filters_dict:
      field = filter.get('field')
      operator = filter.get('operator')
      value = filter.get('value')
      if field is None or operator is None or value is None:
        return Search(and_or="", filters=[], message="Invalid search filter. Each filter should have 'field', 'operator', and 'value' properties.", success=False)
      filters.append(Filter(field=field, operator=operator, value=value))
    return Search(and_or=and_or, filters=filters, message="", success=True)

#region Get all endpoints

@app.route('/customers', methods=['GET'])
def customers_all():
  lst_customers = data_helper.get_customers()
  results = []
  for customer in lst_customers:
    results.append(serialize(customer, Customer))
  return jsonify(results)

@app.route('/inventory', methods=['GET'])
def inventory_all():
  lst_inventory = data_helper.get_inventory()
  results = []
  for inventory in lst_inventory:
    results.append(serialize(inventory, Inventory))
  return jsonify(results)

@app.route('/orders', methods=['GET'])
def orders_all():
  lst_orders = data_helper.get_orders()
  results = []
  for order in lst_orders:
    order_dict = serialize(order, Order)
    results.append(order_dict)
  return jsonify(results)

#endregion

#region Get one endpoints

@app.route('/orders/<id>', methods=['GET'])
def orders_getone(id):
  if id is not None:
    order = data_helper.orders_getone(id)
    order_dict = serialize(order, Order)
    return jsonify(order_dict)
  else:
    return jsonify(serialize(Order(success=False, message="No order ID provided")))

@app.route('/customers/<id>', methods=['GET'])
def customers_getone(id):
  if id is not None:
    customer = data_helper.customers_getone(id)
    customers_dict = serialize(customer, Customer)
    return jsonify(customers_dict)
  else:
    return jsonify(serialize(Customer(success=False, message="No customer ID provided")))

@app.route('/inventory/<id>', methods=['GET'])
def inventory_getone(id):
  if id is not None:
    inventory = data_helper.inventory_getone(id)
    inventory_dict = serialize(inventory, Inventory)
    return jsonify(inventory_dict)
  else:
    return jsonify(serialize(Inventory(success=False, message="No inventory ID provided")))

#endregion

#region Save (create/update) endpoints

@app.route('/orders', methods=['POST'])
def orders_save():
  order = deserialize(request.json, Order)
  order = data_helper.orders_save(order, request.json.get('inventory'))
  order_dict = serialize(order, Order)
  return jsonify(order_dict)

@app.route('/customers', methods=['POST'])
def customers_save():
  customer = deserialize(request.json, Customer)
  customer = data_helper.customers_save(customer)
  customer_dict = serialize(customer, Customer)
  return jsonify(customer_dict)

@app.route('/inventory', methods=['POST'])
def inventory_save():
  inventory = deserialize(request.json, Inventory)
  inventory = data_helper.inventory_save(inventory)
  inventory_dict = serialize(inventory, Inventory)
  return jsonify(inventory_dict)

#endregion

#region Delete endpoints

@app.route('/customers/<id>', methods=['DELETE'])
def customers_delete(id):
  if id is not None:
    customer = data_helper.customers_delete(id)
    customer_dict = serialize(customer, Customer)
    return jsonify(customer_dict)
  else:
    return jsonify(serialize(Customer(success=False, message="No customer ID provided")))

@app.route('/inventory/<id>', methods=['DELETE'])
def inventory_delete(id):
  if id is not None:
    inventory = data_helper.inventory_delete(id)
    inventory_dict = serialize(inventory, Inventory)
    return jsonify(inventory_dict)
  else:
    return jsonify(serialize(Inventory(success=False, message="No inventory ID provided")))

@app.route('/orders/<id>', methods=['DELETE'])
def orders_delete(id):
  if id is not None:
    order = data_helper.orders_delete(id)
    order_dict = serialize(order, Order)
    return jsonify(order_dict)
  else:
    return jsonify(serialize(Order(success=False, message="No order ID provided")))

#endregion

#region Search endpoints

@app.route('/inventory/search', methods=['POST'])
def inventory_search():
  search = deserialize(request.json, Search)
  if not search.success:
    return jsonify(serialize(Inventory(success=False, message=search.message), Inventory))
  inventory = data_helper.inventory_search(search)
  results = []
  for inventory in inventory:
    results.append(serialize(inventory, Inventory))
  return jsonify(results)

@app.route('/customers/search', methods=['POST'])
def customers_search():
  search = deserialize(request.json, Search)
  if not search.success:
    return jsonify(serialize(Customer(success=False, message=search.message), Customer))
  customers = data_helper.customers_search(search)
  results = []
  for customer in customers:
    results.append(serialize(customer, Customer))
  return jsonify(results)

@app.route('/orders/search', methods=['POST'])
def orders_search():
  search = deserialize(request.json, Search)
  if not search.success:
    return jsonify(serialize(Order(success=False, message=search.message), Order))
  orders = data_helper.orders_search(search)
  results = []
  for order in orders:
    results.append(serialize(order, Order))
  return jsonify(results)

#endregion

app.run()