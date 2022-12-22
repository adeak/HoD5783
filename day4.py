from collections import Counter
from datetime import datetime
import json


def day4():
    # count first on-site purchase per customer that contains only bakery items
    order_counts = Counter()
    last_day = None
    with open('noahs-orders.jsonl') as f:
        for line in f:
            order = json.loads(line)
            if order['shipped'] != order['ordered']:
                # not an on-site purchase
                continue
            if not all(item['sku'].startswith('BKY') for item in order['items']):
                # not only bakery items
                continue

            # use the fact that orders are sorted by time
            current_day = datetime.fromisoformat(order['ordered']).date()
            if last_day is None or current_day > last_day:
                # we have a new first bakery-only purchase of the day
                order_counts[order['customerid']] += 1

    bike_fixer_id = order_counts.most_common()[0][0]

    # find the corresponding customer
    with open('noahs-customers.jsonl') as f:
        for line in f:
            customer = json.loads(line)
            if customer['customerid'] == bike_fixer_id:
                return customer['phone']


if __name__ == "__main__":
    print(day4())
