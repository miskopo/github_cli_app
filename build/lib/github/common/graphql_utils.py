from json import loads


def check_qraphql_response(response) -> (bool, str):
    """
    Method checks for error message in response, as github return 200 even in case of error
    :param response: response to be checked
    :return: True if there is no error in response, False otherwise
    """
    if response and response.ok:
        try:
            error_message = loads(response.text)['errors']
        except (TypeError, KeyError):
            return True, None
        else:
            return False, error_message
    else:
        return False, "No response"
