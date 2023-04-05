from flask import jsonify, request, Flask
from flask.json import JSONEncoder
from datetime import date
from Database.data_helper import DataHelper
from Database.data_models import Transaction, Product, Customer
from Database.search_models import Filter, Search
from dotenv import load_dotenv
import os

load_dotenv()

# This method prevents the transaction date from being formatted other than UTC
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


data_helper = DataHelper(os.environ.get('DB_HOST'), os.environ.get('DB_PORT', 3306), os.environ.get('DB_DATABASE', 'store'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'))

# Serializes an object (product, person, etc.) into a dictionary
def serialize(object, class_name):
  dictionary = {field.name: getattr(object, field.name) for field in object.__table__.columns}
  # Transactions need special logic to pull in the products
  if class_name == Transaction:
    lst_products = []
    transaction_id = dictionary.get("id")
    for product_transaction in data_helper.get_product_transactions_by_transaction_id(transaction_id):
      product_dict = {"product_id":product_transaction.product_id, "quantity":product_transaction.quantity}
      lst_products.append(product_dict)
    dictionary['products'] = lst_products
  return dictionary


# Deserializes a dictionary into an object of the passed in class 
def deserialize(dictionary, class_name):
  if class_name != Search:
    object = class_name()
    for key in dictionary:
      # This throws off the add logic if transaction has this
      if not (class_name == Transaction and key == "products"):
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

@app.route('/products', methods=['GET'])
def products_all():
  lst_products = data_helper.get_products()
  results = []
  for product in lst_products:
    results.append(serialize(product, Product))
  return jsonify(results)

@app.route('/transactions', methods=['GET'])
def transactions_all():
  lst_transactions = data_helper.get_transactions()
  results = []
  for transaction in lst_transactions:
    transaction_dict = serialize(transaction, Transaction)
    results.append(transaction_dict)
  return jsonify(results)

#endregion

#region Get one endpoints

@app.route('/transactions/<id>', methods=['GET'])
def transactions_getone(id):
  if id is not None:
    transaction = data_helper.transactions_getone(id)
    transaction_dict = serialize(transaction, Transaction)
    return jsonify(transaction_dict)
  else:
    return jsonify(serialize(Transaction(success=False, message="No transaction ID provided")))

@app.route('/customers/<id>', methods=['GET'])
def customers_getone(id):
  if id is not None:
    customer = data_helper.customers_getone(id)
    customers_dict = serialize(customer, Customer)
    return jsonify(customers_dict)
  else:
    return jsonify(serialize(Customer(success=False, message="No customer ID provided")))

@app.route('/products/<id>', methods=['GET'])
def products_getone(id):
  if id is not None:
    product = data_helper.products_getone(id)
    product_dict = serialize(product, Product)
    return jsonify(product_dict)
  else:
    return jsonify(serialize(Product(success=False, message="No product ID provided")))

#endregion

#region Save (create/update) endpoints

@app.route('/transactions', methods=['POST'])
def transactions_save():
  transaction = deserialize(request.json, Transaction)
  transaction = data_helper.transactions_save(transaction, request.json.get('products'))
  transaction_dict = serialize(transaction, Transaction)
  return jsonify(transaction_dict)

@app.route('/customers', methods=['POST'])
def customers_save():
  customer = deserialize(request.json, Customer)
  customer = data_helper.customers_save(customer)
  customer_dict = serialize(customer, Customer)
  return jsonify(customer_dict)

@app.route('/products', methods=['POST'])
def products_save():
  product = deserialize(request.json, Product)
  product = data_helper.products_save(product)
  product_dict = serialize(product, Product)
  return jsonify(product_dict)

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

@app.route('/products/<id>', methods=['DELETE'])
def products_delete(id):
  if id is not None:
    product = data_helper.products_delete(id)
    product_dict = serialize(product, Product)
    return jsonify(product_dict)
  else:
    return jsonify(serialize(Product(success=False, message="No product ID provided")))

@app.route('/transactions/<id>', methods=['DELETE'])
def transactions_delete(id):
  if id is not None:
    transaction = data_helper.transactions_delete(id)
    transaction_dict = serialize(transaction, Transaction)
    return jsonify(transaction_dict)
  else:
    return jsonify(serialize(Transaction(success=False, message="No transaction ID provided")))

#endregion

#region Search endpoints

@app.route('/products/search', methods=['POST'])
def products_search():
  search = deserialize(request.json, Search)
  if not search.success:
    return jsonify(serialize(Product(success=False, message=search.message), Product))
  products = data_helper.products_search(search)
  results = []
  for product in products:
    results.append(serialize(product, Product))
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

@app.route('/transactions/search', methods=['POST'])
def transactions_search():
  search = deserialize(request.json, Search)
  if not search.success:
    return jsonify(serialize(Transaction(success=False, message=search.message), Transaction))
  transactions = data_helper.transactions_search(search)
  results = []
  for transaction in transactions:
    results.append(serialize(transaction, Transaction))
  return jsonify(results)

#endregion

app.run()