products = [{"name": "bread", "price": 100},
    {"name": "wine", "price": 138},
    {"name": "meat", "price": 15},
    {"name": "water", "price": 1}]

result = []
top_size = 2


for y in range(top_size):
	max_price = 0
	product_index = -1
	for i in range(len(products)):
		product = products[i]
		if i not in result:
			if product['price'] > max_price:
				max_price = product['price']
				product_index = i
				#print(product_index,max_price)

	result += [product_index]


print([products[i] for i in result])

