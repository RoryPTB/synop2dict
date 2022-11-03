import os
import json
from datetime import date
from .extract import file_extract
from .extract import message_extract
from .convert import convert_to_dict


def to_json(input):
    """This function determines whether the input is raw SYNOP tac data or a file. If the former, 
    it converts the SYNOP messages into a dictionary directly with the current year and month. If the latter, it extracts 
    each SYNOP message as well as the year and month from the file name, and then converts the messages.

    Args:
        input (str): This string is either the raw SYNOP data or the path directory to the file.
    """

    # *Begin by checking if the input is the SYNOP messages or the file directory
    if os.path.isdir(input) or os.path.isfile(input):
        messages, year, month = file_extract(input)
    else:
        # Extract the message and default to the current year and month
        messages = message_extract(input)
        year = date.today().year
        month = date.today().month

    # *Now convert each message into a dictionary and write it to a json file
    i = 0
    for msg in messages:
        new_dict = convert_to_dict(msg, year, month)
        with open(f"outputs/dict_{i}.json", "w") as fp:
            json.dump(new_dict, fp, indent=1)
        i += 1

    return "Conversion completed."
