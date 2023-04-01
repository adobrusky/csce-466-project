from Database.database import connect_to_database
import re
from Database.data_models import Customer, Inventory, Order, InventoryOrder

class DataHelper:
  def __init__(self, authority, port, database_name, username, password):
    self.session = connect_to_database(authority, port, database_name, username, password)
  
  def close(self):
    self.session.close()

  # Used for updates to patch the old object with the new object's information
  def delta_patch(self, existing, new):
    for attr, value in new.__dict__.items():
      if attr != "id" and attr != "_sa_instance_state":
        if (type(existing).__name__ == "Order" and attr == "inventory"):
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
      if filter.operator != "equals" and (filter.operator != "contains any" and class_name == Order):
        raise KeyError(class_name.__name__ + " search doesn't support '" + filter.operator + "' operator.")
      valid = False
      for attr in class_name.__dict__.keys():
        if attr != "_sa_instance_state" and attr != "success" and attr != "message":
          if filter.field == attr:
            results = set()
            valid = True
            # Search logic specifically for searching by Order inventory
            if class_name == Order and attr == "inventory":
              for inventory in filter.value:
                inventory_orders = self.session.query(InventoryOrder).filter(InventoryOrder.inventory_id == inventory)
                if inventory_orders is not None:
                  for inventory_order in inventory_orders:
                    results.add(inventory_order.order_id)
              if filter.operator == "contains any":
                ids = self.combine_search_results(search_model.and_or, results, ids)
              elif filter.operator == "equals":
                # At this point we have all of the orders that contains all of the inventory. Now we need to remove the ones that don't contain EXACTLY ALL of the inventory
                order_count = {}
                for order_id in results:
                  order_count[order_id] = self.session.query(InventoryOrder).filter(InventoryOrder.order_id == order_id).count()
                for order_id, count in order_count.items():
                  if count != len(filter.value):
                    results.remove(order_id)
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

  def inventory_getone(self, inventory_id):
    inventory = self.session.query(Inventory).filter(Inventory.id == inventory_id).first()
    if inventory != None:
      inventory.success = True 
    else:
      inventory = Inventory(success=False, message="A inventory with inventory ID " + str(inventory_id) + " does not exist.")
    return inventory

  def inventory_order_getone(self, order_id, inventory_id):
    inventory_order = self.session.query(InventoryOrder).filter(InventoryOrder.order_id == order_id).filter(InventoryOrder.inventory_id == inventory_id).first() 
    if inventory_order != None:
      inventory_order.success = True
    else:
      inventory_order = InventoryOrder(success=False, message="A inventory ID of " + str(inventory_id) + " does not exist on order " + str(order_id) + ".") 
    return inventory_order

  def orders_getone(self, order_id):
    order = self.session.query(Order).filter(Order.id == order_id).first()
    if order != None:
      order.success = True
    else:
      order = Order(success=False, message="A order with order ID " + str(order_id) + " does not exist.")
    return order

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

  def inventory_save(self, inventory):
    try:
      required_fields = ["price", "name"]
      missing = self.validate_required(inventory, required_fields)
      if len(missing) > 0:
        raise ValueError("Missing required fields: " + ", ".join(missing) + ".")
      # If an addition
      if inventory.id is None:
        self.session.add(inventory)
      else:
        # If an update
        existing = self.inventory_getone(inventory.id)
        self.delta_patch(existing, inventory)
      self.session.commit()
      inventory.success = True
      return inventory
    except Exception as ex:
      inventory.success = False
      inventory.message = str(ex)
      return inventory

  def inventory_order_save(self, inventory_order):
    if not self.inventory_order_getone(inventory_order.order_id, inventory_order.inventory_id).success:
      self.session.add(inventory_order)
    self.session.commit()
    inventory_order = self.inventory_order_getone(inventory_order.order_id, inventory_order.inventory_id)
    if inventory_order.success:
      inventory_order.success = True
    else:
      inventory_order.success = False
    return inventory_order

  def orders_save(self, order, inventory):
    try:
      required_fields = ["customer_id", "date"]
      invalid = []
      missing = self.validate_required(order, required_fields)
      if len(missing) > 0:
        raise ValueError("Missing required fields: " + ", ".join(missing) + ".")
      if not self.customers_getone(order.customer_id).success:
        invalid.append("A customer with customer ID of " + str(order.customer_id) + " does not exist.")
      if len(invalid) > 0:
        raise ValueError(" ".join(invalid))
      # If an addition
      if order.id is None:
        self.session.add(order)
      else:
        # If an update
        existing = self.orders_getone(order.id)
        self.delta_patch(existing, order)
      self.session.commit()
      order.success = True
      # If the order save was successful then save all the inventory
      for existing_inventory in self.get_inventory_by_order_id(order.id):
        self.inventory_orders_delete(order.id, existing_inventory.id)
      if inventory is not None:
        for inventory_dict in inventory:
          inventory_id = inventory_dict.get("inventory_id")
          quantity = inventory_dict.get("quantity")
          # Inventory/quantity validation
          if inventory_id is None:
            raise ValueError("Each inventory in list of 'inventory' requires a 'inventory_id'.")
          if quantity is None:
            raise ValueError("Each inventory in list of 'inventory' requires a 'quantity'.")
          self.inventory_order_save(InventoryOrder(order_id=order.id, inventory_id=inventory_id, quantity=quantity))
      return order
    except ValueError as ex:
      order.success = False
      order.message = str(ex)
      return order

  #endregion

  #region Get all methods

  def get_customers(self):
    return self.session.query(Customer)

  def get_inventory(self):
    return self.session.query(Inventory)

  def get_orders(self):
    return self.session.query(Order)

  def get_inventory_by_order_id(self, order_id):
    lst_inventory = []
    for inventory_order in self.get_inventory_orders_by_order_id(order_id):
      lst_inventory.append(self.inventory_getone(inventory_order.inventory_id))
    return lst_inventory

  def get_inventory_orders_by_order_id(self, order_id):
    return self.session.query(InventoryOrder).filter(InventoryOrder.order_id == order_id)

  #endregion

  #region Delete methods

  def inventory_delete(self, inventory_id):
    inventory = self.inventory_getone(inventory_id)
    if inventory.success:
      self.session.query(Inventory).filter(Inventory.id == inventory_id).delete()
      self.session.commit()
    else:
      return Inventory(success=False, message=inventory.message)
    if not self.inventory_getone(inventory_id).success:
      return Inventory(success=True)
    else:
      return Inventory(success=False, message="Deletion failed.")

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

  def orders_delete(self, order_id):
    order = self.orders_getone(order_id)
    if order.success:
      self.session.query(Order).filter(Order.id == order_id).delete()
      self.session.commit()
    else:
      return Order(success=False, message=order.message)
    if not self.orders_getone(order_id).success:
      return Order(success=True)
    else:
      return Order(success=False, message="Deletion failed.")

  def inventory_orders_delete(self, order_id, inventory_id):
    inventory_order = self.inventory_order_getone(order_id, inventory_id)
    if inventory_order.success:
      self.session.query(InventoryOrder).filter(InventoryOrder.order_id == order_id).filter(InventoryOrder.inventory_id == inventory_id).delete()
      self.session.commit()
    else:
      return InventoryOrder(success=False, message=inventory_order.message)
    if not self.orders_getone(order_id).success:
      return InventoryOrder(success=True)
    else:
      return InventoryOrder(success=False, message="Deletion failed.")

  #endregion

  #region Search methods

  def inventory_search(self, search):
    try:
      inventory_ids = self.search(Inventory, search)
      inventory = []
      for id in inventory_ids:
        inventory.append(self.inventory_getone(id))
      return inventory
    except KeyError as ex:
      return [Inventory(success=False, message=str(ex).strip("\""))]

  def customers_search(self, search):
    try:
      customer_ids = self.search(Customer, search)
      customers = []
      for id in customer_ids:
        customers.append(self.customers_getone(id))
      return customers
    except KeyError as ex:
      return [Customer(success=False, message=str(ex).strip("\""))]

  def orders_search(self, search):
    try:
      order_ids = self.search(Order, search)
      orders = []
      for id in order_ids:
        orders.append(self.orders_getone(id))
      return orders
    except KeyError as ex:
      return [Order(success=False, message=str(ex).strip("\""))]

  #endregion