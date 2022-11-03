from synop2dict import to_json

# Example with a txt file containing SYNOP messages
# NOTE: This works for any file extension, not just txt
file = "example_data/A_SIID20WIIX020900_C_EDZW_20221002091604_64941181.txt"

to_json(file)

# Example of directly inputting a SYNOP message
tac = """SIID20 WIIX 020900

AAXX 02094

96009 32459 60105 10278 20241 30040 40074 57026 83221

  333 56000 57803 83816 80860=

96011 32560 71808 10268 20234 30052 40076 57021 85521

  333 56000 84620="""

to_json(tac)
