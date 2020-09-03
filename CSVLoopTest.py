from csv import DictReader

with open('test.csv', 'r', encoding="utf-8-sig") as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        print(row['Name'], row['Location'])