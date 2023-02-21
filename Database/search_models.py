class Search:
  def __init__(self, and_or, filters, success, message):
    self.and_or = and_or
    self.filters = filters
    self.success = success
    self.message = message

class Filter:
  def __init__(self, field, operator, value):
    self.field = field
    self.operator = operator
    self.value = value