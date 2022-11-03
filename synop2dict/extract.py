import os
import re
from datetime import date
from datetime import datetime


def message_extract(data):
    """This function separates the SYNOP tac and returns the individual SYNOP messages, ready for conversion
    Args:
        data (str): The SYNOP tac.
    """

    # Separate the messages based on the FM type and the time/wind indicator, using regex
    data = re.split('(\D{4})\s(\d{5})\s', data)
    # Determine section 0 of all the messages
    s0 = data[1] + " " + data[2]

    # Determine the section 1 messages, removing the delimiter "="
    s1_list = data[3]
    s1_list = s1_list.split("=")

    # Create the list of messages by combining the section 0 part, section 1 part
    # with new lines removed, and the "=" to end each message.
    messages = []
    messages[:] = [s0 + " " + x.replace('\n', '') + "=" for x in s1_list if x]

    # Return the messages
    return messages


def is_name_valid(name):
    """This function checks whether the input file name conforms to
        the standards, and if so returns the datetime of the file, otherwise defaults 
        to returning the current year and month.

    Args:
        name (str): The file path basename.

    Returns:
        datetime: The datetime of the file.
    """

    # File format is: pflag_productidentifier_oflag_originator_yyyyMMddhhmmss.extension
    try:
        # Returns the part of the string that should be the datetime of the file
        # (begins with an underscore, but doesn't end with one)
        # Note: \d represents the decimal part, {8} means it checks for 8 digits
        # the condition is failed.
        match = re.search(r"_(\d{8})", name)
        # Strip the datetime from the part of the string
        d = datetime.strptime(match.group(1), '%Y%m%d')
        year = d.year
        month = d.month
        return year, month

    except ValueError:
        print(
            f"File {name} is in wrong file format. The current year and month will be used for the conversion.")
        year = date.today().year
        month = date.today().month
        return year, month


def file_extract(file):
    """This function extracts the contents of the file and the date of the file

    Args:
        file (str): The file directory or file name of the SYNOP message.
    """

    # Open and read the file, stripping any new lines
    try:
        with open(file, "r") as fp:
            data = fp.read()
    except:
        return "Error: The file path is incorrect."

    # Obtain the year and month of the data from the file name
    file_name = os.path.basename(file)
    file_year, file_month = is_name_valid(file_name)

    # Obtain the individual SYNOP messages from the file contents
    messages = message_extract(data)

    # Return the list of messages and the date of the file
    return messages, file_year, file_month


file_extract(
    "example_data/A_SIID20WIIX020900_C_EDZW_20221102091604_64941181.txt")
