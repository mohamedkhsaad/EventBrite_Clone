import csv
import json

def write_json_to_csv(json_list, filename):
    # extract field names from the first JSON object in the list
    fieldnames = list(json_list[0].keys())

    # open the CSV file for writing
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # write the header row to the CSV file
        writer.writeheader()

        # write each JSON object to a row in the CSV file
        for json_obj in json_list:
            writer.writerow(json_obj)
json_data = [
    {
        "ticket_class_id": 62497278,
        "quantity": 3,
        "order_id": 97671187,
        "ticket_price": 999.0,
        "user_id": 1,
        "event_id": 646052652
    },
    {
        "ticket_class_id": 70680153,
        "quantity": 1,
        "order_id": 97671187,
        "ticket_price": 999.0,
        "user_id": 1,
        "event_id": 646052652
    }
]

write_json_to_csv(json_data, 'output.csv')
