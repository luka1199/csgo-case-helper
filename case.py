class Case:
	def __init__(self, name, amount, price):
		self.name = name
		self.amount = amount
		self.price = price
		
	def get_name(self):
		return self.name

	def get_amount(self):
		return self.amount

	def get_price(self):
		return self.price

	def __repr__(self):
		return "Case(Name: {}, Amount: {}, Price: {})".format(self.name, self.amount, self.price)

	def __str__(self):
 		return "Case(Name: {}, Amount: {}, Price: {})".format(self.name, self.amount, self.price)
