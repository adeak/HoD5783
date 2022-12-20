import json


def day2():
    # find coffee and bagels
    skus_food = set()
    with open('noahs-products.jsonl') as f:
        for line in f:
            product = json.loads(line)
            description = product['desc'].lower()
            if description.startswith('coffee') or 'bagel' in description:
                skus_food.add(product['sku'])
            elif 'rug cleaner' in description:
                sku_rugcleaner = product['sku']

    # load relevant orders (coffe or bagel, and rug cleaner), key on customer
    sus_customers = set()  # set of customer IDs who bought these
    with open('noahs-orders.jsonl') as f:
        for line in f:
            order = json.loads(line)
            customerid = order['customerid']
            if customerid in sus_customers:
                # nothing more to do here
                continue
            items = order['items']
            has_food = any(item['sku'] in skus_food for item in items)
            has_rugcleaner = any(sku_rugcleaner in item['sku'] for item in items)
            if has_food and has_rugcleaner:
                sus_customers.add(customerid)

    # look through suspects, find the ones who have JD initials
    suspects = {}  # key -> name mapping
    with open('noahs-customers.jsonl') as f:
        for line in f:
            customer = json.loads(line)
            if customer['customerid'] not in sus_customers:
                continue

            phone_number = customer['phone']
            full_name = customer['name'].rstrip(' I')  # remove any Roman numerals
            initials = [word[0] for word in full_name.split()]
            if initials[0] == 'J' and initials[-1] == 'D':
                suspects[phone_number] = full_name

    if len(suspects) != 1:
        raise ValueError(f'Invalid amount of suspects found. Suspects by phone number: {suspects}')

    return next(iter(suspects))


if __name__ == "__main__":
    print(day2())
