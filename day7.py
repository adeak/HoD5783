from collections import defaultdict
from datetime import datetime, timedelta
import json

from day6 import day6


def day7():
    # toucan girl
    girl_phone = day6()

    # load all customers, find girl's customerid
    customers = {}
    with open('noahs-customers.jsonl') as f:
        for line in f:
            customer = json.loads(line)
            phone_num = customer['phone']
            customerid = customer['customerid']
            customers[customerid] = customer
            if phone_num == girl_phone:
                girl_id = customerid

    # load all products
    products = {}  # sku -> desc mapping
    with open('noahs-products.jsonl') as f:
        for line in f:
            product = json.loads(line)
            products[product['sku']] = product['desc']

    # load all in-person orders, find girl's orders
    orders = defaultdict(list)
    this_day_orders = []  # orders on a given day
    interesting_orders = {}  # orders on days of interest (when girl bought anything)
    have_girl = False  # whether girl bought something on a given day
    with open('noahs-orders.jsonl') as f:
        for line in f:
            order = json.loads(line)
            if order['ordered'] != order['shipped']:
                # not an in-person order
                continue

            # some useful post-processing on the fly
            order['dt'] = datetime.fromisoformat(order['ordered'])
            order['items'] = [products[item['sku']] for item in order['items']]

            # logic to group orders by date, when relevant
            if not this_day_orders or this_day_orders[-1]['dt'].date() == order['dt'].date():
                # we're still on the same day, collect data
                this_day_orders.append(order)
                if order['customerid'] == girl_id:
                    have_girl = True
            else:
                # we have a full day and starting a new one with this order
                if not have_girl:
                    # this day was irrelevant
                    this_day_orders = []
                    continue
                # otherwise store this day's orders for safe keeping, key on date
                interesting_orders[this_day_orders[-1]['dt'].date()] = this_day_orders

                # prepare for next day with "this" new order
                this_day_orders = [order]
                have_girl = order['customerid'] == girl_id
        # assume that last day is irrelevant out of sheer laziness

    matches = []
    for date, orders in interesting_orders.items():
        # find girl's order, verify that there's only one (for simplicity)
        girl_orders = [
            order
            for order in orders
            if order['customerid'] == girl_id
        ]
        assert len(girl_orders) == 1
        girl_order = girl_orders[0]
        orders.remove(girl_order)

        # assume that the color variation is in parentheses -> ignore order if no parens in basket
        if not any('(' in item for item in girl_order['items']):
            continue

        # find items with parentheses, only keep prefix due to colour mismatch
        interesting_items = {
            item[:item.index('(') - 1]
            for item in girl_order['items']
            if '(' in item
        }

        # restrict orders to times within 30 minutes of girl's order
        # and items that overlap with interesting items
        orders = [
            order
            for order in orders
            if abs(order['dt'] - girl_order['dt']) < timedelta(minutes=30)
            and any(
                any(
                    item.startswith(interesting_prefix)
                    for interesting_prefix in interesting_items
                )
                for item in order['items']
            )
        ]
        matches.extend(orders)

    # check that we've hit the mark
    if len(matches) != 1:
        raise ValueError(f'Too many matches: {len(matches)}.')

    # grab corresponding customer
    guy_order = matches[0]
    guy_phone = customers[guy_order['customerid']]['phone']
    return guy_phone


if __name__ == "__main__":
    print(day7())
