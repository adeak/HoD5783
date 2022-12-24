from collections import defaultdict
import json


def day6():
    # load all product wholesale prices
    wholesale_prices = {}
    with open('noahs-products.jsonl') as f:
        for line in f:
            product = json.loads(line)
            wholesale_prices[product['sku']] = product['wholesale_cost']

    # collect all order items at or below wholesale price by customer
    orders = defaultdict(list)
    with open('noahs-orders.jsonl') as f:
        for line in f:
            order = json.loads(line)
            # keep _any_ item being on sale
            items_on_sale = [
                item
                for item in order['items']
                if item['unit_price'] <= wholesale_prices[item['sku']]
            ]
            if items_on_sale:
                orders[order['customerid']].extend(items_on_sale)

    # find customer with the most sale-containing orders
    saleiest_id = max(orders, key=lambda customerid: len(orders[customerid]))

    # grab corresponding customer
    with open('noahs-customers.jsonl') as f:
        for line in f:
            customer = json.loads(line)
            customerid = customer['customerid']
            if customerid == saleiest_id:
                phone_num = customer['phone']
                break
    return phone_num


if __name__ == "__main__":
    print(day6())
