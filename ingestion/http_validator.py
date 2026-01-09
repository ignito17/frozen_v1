def validate_response(resp):
    if resp.status_code==200:
        return
    elif resp.status_code==401:
        raise RuntimeError("Unathorized: API key missing or invalid")
    elif resp.status_code==403:
        raise RuntimeError("Forbidden: API key blocked or insufficient access")
    elif resp.status_code==404:
        raise RuntimeError("Not Found: invalid endpoint or resource")
    elif resp.status_code==422:
        raise RuntimeError(f"Unprocessable query: {resp.text}")
    elif resp.status_code==429:
        raise RuntimeError("Rate limited: too many requests")
    else:
        raise RuntimeError(f"OpenAQ error {resp.status_code}:{resp.text}")