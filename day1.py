import json


def day1():
    letter_to_num = {
        char: str(num)
        for num, group in enumerate(['abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz'], 2)
        for char in group
    }

    with open('noahs-customers.jsonl') as f:
        for line in f:
            customer = json.loads(line)
            phone_raw = customer['phone']
            phone_nums = phone_raw.replace('-', '')
            full_name = customer['name'].lower()
            if '0' in phone_nums or '1' in phone_nums:
                # not mapped text
                continue

            # assume _any_ trailing 10-length name works
            last_name = next((name for name in full_name.split()[::-1] if len(name) == len(phone_nums)), None)
            if last_name is None:
                continue

            phone_expected = ''.join(letter_to_num[char] for char in last_name)
            if phone_expected == phone_nums:
                return phone_raw


if __name__ == "__main__":
    print(day1())
