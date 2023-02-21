from Database.database import connect_to_database
import re
from Database.data_models import Customer, Product, Transaction, ProductTransaction

class DataHelper:
  def __init__(self, authority, port, database_name, username, password):
    self.session = connect_to_database(authority, port, database_name, username, password)
  
  def close(self):
    self.session.close()

  # Used for updates to patch the old object with the new object's information
  def delta_patch(self, existing, new):
    for attr, value in new.__dict__.items():
      if attr != "id" and attr != "_sa_instance_state":
        if (type(existing).__name__ == "Transaction" and attr == "products"):
          continue
        else:
          setattr(existing, attr, value)

  # Check to make sure that the passed in required fields are not None in the object
  def validate_required(self, object, required_fields):
    missing = []
    for required in required_fields:
      if self.is_null_or_whitespace(getattr(object, required)):
        missing.append(required)
    return missing

  def is_valid_postal_code(self, country, postal_code):
    regex = re.compile("[a-zA-Z]\d[a-zA-Z] \d[a-zA-Z]\d")
    if country.upper() == "USA":
      regex = re.compile("\d\d\d\d\d")
    search = regex.search(postal_code)
    if search is not None and len(postal_code) == len(search.group()):
      return True
    return False
    
  # Validate address
  def validate_address(self, customer, invalid):
    # Postal code and state validation for USA and Canada
    if customer.country.upper() == "UNITED STATES" or customer.country.upper() == "U.S.A":
      customer.country = "USA"
    if customer.country.upper() == "USA" or customer.country.upper() == "CANADA":
      if self.is_null_or_whitespace(customer.postal_code):
        invalid.append("Postal code is required for USA and Canada.")
      elif customer.country.upper() == "USA" and not self.is_valid_postal_code(customer.country, customer.postal_code):
        invalid.append("Invalid postal code. USA postal code must be 5 digits.")
      elif customer.country.upper() == "CANADA" and not self.is_valid_postal_code(customer.country, customer.postal_code):
        invalid.append("Invalid postal code. Canada postal code must be in 'A1A 1A1' format.")
      if self.is_null_or_whitespace(customer.state):
        invalid.append("State is required for USA and Canada.")
    else:
      if self.is_null_or_whitespace(customer.postal_code):
        customer.postal_code = ""
      if self.is_null_or_whitespace(customer.state):
        customer.state = ""

  # Checks if a string is null or whitespace and returns a boolean
  def is_null_or_whitespace(self, string):
    if string is None or len(str(string).strip()) == 0:
      return True
    else:
      return False

  # Combines search results based on the and_or property
  def combine_search_results(self, and_or, results, ids):
    if and_or == "and":
      return results if len(ids) == 0 else ids.intersection(results)
    elif and_or == "or":
      return results if len(ids) == 0 else ids.union(results)

  # Searches the database based on the object type and filters. Throws an exception if invalid filters or operators are passed
  def search(self, class_name, search_model):
    ids = set()
    invalid = []
    for filter in search_model.filters:
      # Operator validation
      if filter.operator != "equals" and (filter.operator != "contains any" and class_name == Transaction):
        raise KeyError(class_name.__name__ + " search doesn't support '" + filter.operator + "' operator.")
      valid = False
      for attr in class_name.__dict__.keys():
        if attr != "_sa_instance_state" and attr != "success" and attr != "message":
          if filter.field == attr:
            results = set()
            valid = True
            # Search logic specifically for searching by Transaction products
            if class_name == Transaction and attr == "products":
              for product in filter.value:
                product_transactions = self.session.query(ProductTransaction).filter(ProductTransaction.product_id == product)
                if product_transactions is not None:
                  for product_transaction in product_transactions:
                    results.add(product_transaction.transaction_id)
              if filter.operator == "contains any":
                ids = self.combine_search_results(search_model.and_or, results, ids)
              elif filter.operator == "equals":
                # At this point we have all of the transactions that contains all of the products. Now we need to remove the ones that don't contain EXACTLY ALL of the products
                transaction_count = {}
                for transaction_id in results:
                  transaction_count[transaction_id] = self.session.query(ProductTransaction).filter(ProductTransaction.transaction_id == transaction_id).count()
                for transaction_id, count in transaction_count.items():
                  if count != len(filter.value):
                    results.remove(transaction_id)
                ids = self.combine_search_results(search_model.and_or, results, ids)
            else:
              # Search logic for every other case
              for object in self.session.query(class_name).filter(getattr(class_name, attr) == filter.value):
                results.add(object.id)
            ids = self.combine_search_results(search_model.and_or, results, ids)
      if not valid:
        invalid.append(filter.field)
    if len(invalid) > 0:
      raise KeyError("Cannot search " + class_name.__name__ + "s by " + ", ".join(invalid))
    return ids

  #region Get one

  def customers_getone(self, customer_id):
    customer = self.session.query(Customer).filter(Customer.id == customer_id).first()
    if customer != None:
      customer.success = True
    else:
      customer = Customer(success=False, message="A customer with customer ID " + str(customer_id) + " does not exist.")
    return customer

  def products_getone(self, product_id):
    product = self.session.query(Product).filter(Product.id == product_id).first()
    if product != None:
      product.success = True 
    else:
      product = Product(success=False, message="A product with product ID " + str(product_id) + " does not exist.")
    return product

  def product_transaction_getone(self, transaction_id, product_id):
    product_transaction = self.session.query(ProductTransaction).filter(ProductTransaction.transaction_id == transaction_id).filter(ProductTransaction.product_id == product_id).first() 
    if product_transaction != None:
      product_transaction.success = True
    else:
      product_transaction = ProductTransaction(success=False, message="A product ID of " + str(product_id) + " does not exist on transaction " + str(transaction_id) + ".") 
    return product_transaction

  def transactions_getone(self, transaction_id):
    transaction = self.session.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction != None:
      transaction.success = True
    else:
      transaction = Transaction(success=False, message="A transaction with transaction ID " + str(transaction_id) + " does not exist.")
    return transaction

  #endregion

  #region Save (create/update) methods

  def customers_save(self, customer):
    try:
      required_fields = ["first_name", "last_name", "address", "city", "country"]
      invalid = []
      missing = self.validate_required(customer, required_fields)
      if len(missing) > 0:
        raise ValueError("Missing required fields: " + ", ".join(missing) + ".")
      self.validate_address(customer, invalid)
      # Email validation
      if self.is_null_or_whitespace(customer.email):
        customer.email = ""
      elif len(customer.email) > 0 and "@" not in customer.email:
        invalid.append("Email is invalid.")
      if len(invalid) > 0:
        raise ValueError(" ".join(invalid))
      # If an addition
      if customer.id is None:
        self.session.add(customer)
      else:
        # If an update
        existing = self.customers_getone(customer.id)
        self.delta_patch(existing, customer)
      self.session.commit()
      customer.success = True
      return customer
    except Exception as ex:
      customer.success = False
      customer.message = str(ex)
      return customer

  def products_save(self, product):
    try:
      required_fields = ["price", "name"]
      missing = self.validate_required(product, required_fields)
      if len(missing) > 0:
        raise ValueError("Missing required fields: " + ", ".join(missing) + ".")
      # If an addition
      if product.id is None:
        self.session.add(product)
      else:
        # If an update
        existing = self.products_getone(product.id)
        self.delta_patch(existing, product)
      self.session.commit()
      product.success = True
      return product
    except Exception as ex:
      product.success = False
      product.message = str(ex)
      return product

  def product_transaction_save(self, product_transaction):
    if not self.product_transaction_getone(product_transaction.transaction_id, product_transaction.product_id).success:
      self.session.add(product_transaction)
    self.session.commit()
    product_transaction = self.product_transaction_getone(product_transaction.transaction_id, product_transaction.product_id)
    if product_transaction.success:
      product_transaction.success = True
    else:
      product_transaction.success = False
    return product_transaction

  def transactions_save(self, transaction, products):
    try:
      required_fields = ["customer_id", "date"]
      invalid = []
      missing = self.validate_required(transaction, required_fields)
      if len(missing) > 0:
        raise ValueError("Missing required fields: " + ", ".join(missing) + ".")
      if not self.customers_getone(transaction.customer_id).success:
        invalid.append("A customer with customer ID of " + str(transaction.customer_id) + " does not exist.")
      if len(invalid) > 0:
        raise ValueError(" ".join(invalid))
      # If an addition
      if transaction.id is None:
        self.session.add(transaction)
      else:
        # If an update
        existing = self.transactions_getone(transaction.id)
        self.delta_patch(existing, transaction)
      self.session.commit()
      transaction.success = True
      # If the transaction save was successful then save all the products
      for existing_product in self.get_products_by_transaction_id(transaction.id):
        self.product_transactions_delete(transaction.id, existing_product.id)
      if products is not None:
        for product_dict in products:
          product_id = product_dict.get("product_id")
          quantity = product_dict.get("quantity")
          # Product/quantity validation
          if product_id is None:
            raise ValueError("Each product in list of 'products' requires a 'product_id'.")
          if quantity is None:
            raise ValueError("Each product in list of 'products' requires a 'quantity'.")
          self.product_transaction_save(ProductTransaction(transaction_id=transaction.id, product_id=product_id, quantity=quantity))
      return transaction
    except ValueError as ex:
      transaction.success = False
      transaction.message = str(ex)
      return transaction

  #endregion

  #region Get all methods

  def get_customers(self):
    return self.session.query(Customer)

  def get_products(self):
    return self.session.query(Product)

  def get_transactions(self):
    return self.session.query(Transaction)

  def get_products_by_transaction_id(self, transaction_id):
    lst_products = []
    for product_transaction in self.get_product_transactions_by_transaction_id(transaction_id):
      lst_products.append(self.products_getone(product_transaction.product_id))
    return lst_products

  def get_product_transactions_by_transaction_id(self, transaction_id):
    return self.session.query(ProductTransaction).filter(ProductTransaction.transaction_id == transaction_id)

  #endregion

  #region Delete methods

  def products_delete(self, product_id):
    product = self.products_getone(product_id)
    if product.success:
      self.session.query(Product).filter(Product.id == product_id).delete()
      self.session.commit()
    else:
      return Product(success=False, message=product.message)
    if not self.products_getone(product_id).success:
      return Product(success=True)
    else:
      return Product(success=False, message="Deletion failed.")

  def customers_delete(self, customer_id):
    customer = self.customers_getone(customer_id)
    if customer.success:
      self.session.query(Customer).filter(Customer.id == customer_id).delete()
      self.session.commit()
    else:
      return Customer(success=False, message=customer.message)
    if not self.customers_getone(customer_id).success:
      return Customer(success=True)
    else:
      return Customer(success=False, message="Deletion failed.")

  def transactions_delete(self, transaction_id):
    transaction = self.transactions_getone(transaction_id)
    if transaction.success:
      self.session.query(Transaction).filter(Transaction.id == transaction_id).delete()
      self.session.commit()
    else:
      return Transaction(success=False, message=transaction.message)
    if not self.transactions_getone(transaction_id).success:
      return Transaction(success=True)
    else:
      return Transaction(success=False, message="Deletion failed.")

  def product_transactions_delete(self, transaction_id, product_id):
    product_transaction = self.product_transaction_getone(transaction_id, product_id)
    if product_transaction.success:
      self.session.query(ProductTransaction).filter(ProductTransaction.transaction_id == transaction_id).filter(ProductTransaction.product_id == product_id).delete()
      self.session.commit()
    else:
      return ProductTransaction(success=False, message=product_transaction.message)
    if not self.transactions_getone(transaction_id).success:
      return ProductTransaction(success=True)
    else:
      return ProductTransaction(success=False, message="Deletion failed.")

  #endregion

  #region Search methods

  def products_search(self, search):
    try:
      product_ids = self.search(Product, search)
      products = []
      for id in product_ids:
        products.append(self.products_getone(id))
      return products
    except KeyError as ex:
      return [Product(success=False, message=str(ex).strip("\""))]

  def customers_search(self, search):
    try:
      customer_ids = self.search(Customer, search)
      customers = []
      for id in customer_ids:
        customers.append(self.customers_getone(id))
      return customers
    except KeyError as ex:
      return [Customer(success=False, message=str(ex).strip("\""))]

  def transactions_search(self, search):
    try:
      transaction_ids = self.search(Transaction, search)
      transactions = []
      for id in transaction_ids:
        transactions.append(self.transactions_getone(id))
      return transactions
    except KeyError as ex:
      return [Transaction(success=False, message=str(ex).strip("\""))]

  #endregion