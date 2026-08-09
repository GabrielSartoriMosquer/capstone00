class InvalidField(Exception):
    pass
from datetime import datetime
import re

def log_fields_separator(log: str) -> dict:

    regex = r'^(?P<ip>\S+)\s+(?P<ident>\S+)\s+(?P<user>\S+)\s+\[(?P<datetime>[^\]]+)\]\s+"(?P<request>[^"]+)"\s+(?P<status>\S+)\s+(?P<bytes>\S+|-)$'

    match = re.match(regex, log)

    if match:
        fields = match.groupdict()
        return fields

a = log_fields_separator('192.168.35.32 - - [06/Aug/2026:22:15:02 -0300] "POST /health HTTP/1.1" 62 2a42')


def parse_bytes(bytes):
    try:
        bytes = int(bytes)
        if bytes < 0:
            raise InvalidField('BYTES: Number of bytes below zero.')
        else:
            return bytes
    except ValueError as e:
        raise InvalidField(f'BYTES: {e}')

b = parse_bytes(a['bytes'])
print(b)
