from collections import defaultdict
import json


def day8():
    # load all products named "Noah's ..." with parentheses
    interesting_products = set()  # bag of all relevant skus
    product_collections = defaultdict(set)  # name prefix -> variant skus mapping
    with open('noahs-products.jsonl') as f:
        for line in f:
            product = json.loads(line)
            desc = product['desc']
            if not desc.startswith("Noah's ") or '(' not in desc:
                continue
            prefix = desc[:desc.index('(') - 1]
            sku = product['sku']
            product_collections[prefix].add(sku)
            interesting_products.add(sku)

    # load all orders containing interesting products
    orders = defaultdict(set)  # customerid -> bought interesting skus mapping
    with open('noahs-orders.jsonl') as f:
        for line in f:
            order = json.loads(line)
            items = order['items']
            interesting_skus = {
                item['sku']
                for item in items
                if item['sku'] in interesting_products
            }
            if not interesting_skus:
                # uninteresting order
                continue

            orders[order['customerid']] |= interesting_skus

    # find customers who have a complete collection of at least one thing
    collectors = set()
    for customerid, owned_products in orders.items():
        if any(
            collection <= owned_products
            for collection in product_collections.values()
        ):
            collectors.add(customerid)

    # check that we've hit the mark
    if len(collectors) != 1:
        raise ValueError(f'Too many matches: {len(collectors)}.')
    collector = collectors.pop()

    # load all customers, find collector's phone number
    customers = {}
    with open('noahs-customers.jsonl') as f:
        for line in f:
            customer = json.loads(line)
            if customer['customerid'] == collector:
                phone_num = customer['phone']
                break

    return phone_num


if __name__ == "__main__":
    print(day8())
