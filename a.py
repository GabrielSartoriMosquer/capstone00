def parse_status(status):
    try:
        if len(str(status))==3 and 100<=int(status)<=599:
            return status
        else:
            return 'ERROR: Invalid status code.'
    except ValueError as e:
        return f'ERROR: {e}'
    except Exception as e:
        return f'ERROR: {e}'

print(parse_status(100))


