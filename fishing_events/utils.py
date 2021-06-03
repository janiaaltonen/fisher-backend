import json



def parse_request_payload(payload):
    """
    :param payload: request's body in json
    :return: tuple containing event, techniques as list and catches as list containing list of catches
    """
    json_data = payload.decode('utf-8')
    dict_data = json.loads(json_data)
    catches = dict_data.pop('catches', None)
    fishing_event = dict_data
    return fishing_event, catches
