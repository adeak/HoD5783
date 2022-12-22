from collections import Counter, defaultdict
import json


def day5():
    # load all cat product names
    cat_products = set()
    with open('noahs-products.jsonl') as f:
        for line in f:
            product = json.loads(line)
            sku = product['sku']
            desc = product['desc']
            if sku.startswith('PET') and 'Cat' in desc:
                cat_products.add(sku)

    # collect all orders by customerid
    orders = defaultdict(list)
    with open('noahs-orders.jsonl') as f:
        for line in f:
            order = json.loads(line)
            orders[order['customerid']].append(order)

    # find cattiest customer, key on phone number
    cattiness = Counter()
    with open('noahs-customers.jsonl') as f:
        for line in f:
            customer = json.loads(line)
            customerid = customer['customerid']
            if not customer['citystatezip'].startswith('Queens Village'):
                continue
            for order in orders[customer['customerid']]:
                for item in order['items']:
                    sku = item['sku']
                    if sku in cat_products:
                        cattiness[customer['phone']] += item['qty']
    cattiest = cattiness.most_common()[0][0]
    return cattiest


if __name__ == "__main__":
    print(day5())
