from datetime import datetime
import sqlite3
import re

API_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
DATE_FORMAT = '%d/%b/%Y:%H:%M:%S %z'

class InvalidField(Exception):
    pass
            
def log_fields_separator(log: str) -> dict:

    regex = r'^(?P<ip>\S+)\s+(?P<ident>\S+)\s+(?P<user>\S+)\s+\[(?P<datetime>[^\]]+)\]\s+"(?P<request>[^"]+)"\s+(?P<status>\S+)\s+(?P<bytes>\S+|-)$'

    match = re.match(regex, log)

    if match:
        fields = match.groupdict()
        return fields

def parse_ip(ip):
    parts = ip.split('.')
    if len(parts) == 4:
        for part in parts:
            try:
                if not 0<=int(part)<=255: 
                    raise InvalidField(f'IP: {part} is out of the range (0-255).')  
            except ValueError as e:
                raise InvalidField(f'IP: {e}')
        return ip
    else:
        raise InvalidField(f'IP: {ip} has not 4 parts.')
                
def parse_date(date, format):
    try:
        date = datetime.strptime(date, format)
        return date
    except ValueError as e:
        raise InvalidField(f'DATE: {e}')

def parse_request(request):
    parts = request.split()
    if len(parts) == 3:
        print(1)
        if parts[0] in API_METHODS:
            print(2)
            if re.match(r'^(?:/[a-zA-Z0-9]+)+$', parts[1]): # ?: para que o regex apenas valide e não guarde na memória
                print(3)
                if re.match(r'^HTTP/\d+(?:\.\d+)?$', parts[2]): 
                    method, path, protocol = parts[0], parts[1], parts[2]
                    return  method, path, protocol
    raise InvalidField('REQUEST: the request is wrong.')

def parse_status(status):
    try:
        status = str(status).strip()
        if len(str(status))==3 and 100<=int(status)<=599:
            return int(status)
        else:
            raise InvalidField('STATUS: number of digits or incorrect status number.')
    except ValueError as e:
        raise InvalidField(f'STATUS: {e}')

def parse_bytes(bytes):
    try:
        bytes = int(bytes)
        if bytes < 0:
            raise InvalidField('BYTES: Number of bytes below zero.')
        else:
            return bytes
    except ValueError as e:
        raise InvalidField(f'BYTES: {e}')

class LogEntry:

    def __init__(self, id:int, ip:str, date:datetime, method:str, route:str, protocol:str, status:int, size:int):
        self.id = id
        self.ip = ip
        self.date = date
        self.method = method
        self.route = route
        self.protocol = protocol
        self.status = status
        self.size = size

def parser_orchestrator():
    pass
    # all the workflow comes here
