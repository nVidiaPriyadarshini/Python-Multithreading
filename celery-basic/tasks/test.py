class SalaryError(Exception):
	pass


while True:
	try:
		salary = input("Please enter your salary")
		if not salary.isdigit():
			raise SalaryError()
		print(salary)
		break
	except SalaryError:
		print("invalid salary amount, please enter valid type")
	finally:
		print("This executes no matter what, ideal for releasing resources")
