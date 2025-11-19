def sum_orders_total(orders):
    total = 0
    for order in orders:
        for item in order.product_list:
            total += item.product.price * item.quantity
    return total