FULL_NUMBER_TO_ID = {
    "EST_001": 1,
    "EST_002": 2,
    "CHE_001": 3,
    "CHE_002": 4,
    "EST_003": 14,
}


def get_heatpump_id(full_number):
    return FULL_NUMBER_TO_ID.get(full_number)
