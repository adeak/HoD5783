from datetime import date
import json

from day2 import day2


def day3():
    contractor_phone = day2()
    suspects = {}
    with open('noahs-customers.jsonl') as f:
        for line in f:
            customer = json.loads(line)
            phone_number = customer['phone']
            if phone_number == contractor_phone:
                # grab address for neighbourhood lookup later
                contractor_zip = customer['citystatezip']
                continue
            
            # look for suspects: Aries born in year of the Dog
            birth_date = date.fromisoformat(customer['birthdate'])
            aries = date(birth_date.year, 3, 20) <= birth_date <= date(birth_date.year, 4, 20)
            dogyeared = birth_date.year in range(1946, 2022, 12)
            if aries and dogyeared:
                suspects[phone_number] = customer

    # choose suspects from same ZIP
    suspects = {
        phone_number: suspect
        for phone_number, suspect in suspects.items()
        if suspect['citystatezip'] == contractor_zip
    }

    if len(suspects) != 1:
        raise ValueError(f'Invalid amount of suspects found. Suspects by phone number: {suspects}')

    return next(iter(suspects))


if __name__ == "__main__":
    print(day3())
