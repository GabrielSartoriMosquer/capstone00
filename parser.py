from datetime import datetime
import sqlite3
import re

API_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

def log_fields_separator(log: str) -> dict:

    regex = r'^(?P<ip>\S+)\s+(?P<ident>\S+)\s+(?P<user>\S+)\s+\[(?P<datetime>[^\]]+)\]\s+"(?P<request>[^"]+)"\s+(?P<status>\d+)\s+(?P<bytes>\d+|-)$'

    match = re.match(regex, log)

    if match:
        fields = match.groupdict()
        return fields

def parse_ip(ip):
    parts = ip.split('.')
    if len(parts) == 4:
        for part in parts:
            try:
                if 0<=int(part)<255: #aqui pode subir um ValueError
                    continue
                else:
                    raise InvalidIP(f'IP: {part} is out of the range (0-255).') #aqui eu subo número inválido
        return ip
    else:
        raise IPParts(f'IP: {ip} has not 4 parts.')
                

def parse_date(date):
    try:
        date = date.strftime('%d/%b/%Y:%H:%M:%S %z')
        return date
    except ValueError as e:
        return f'Error: {e}'

def parse_request(request):
    parts = request.split()
    if request[0] in API_METHODS:
        if re.match(request[1], r'/^[a-zA-Z0-9]+$'):
            if re.match(request[2], r'HTTP/\d+(?:\.\d+)?\s+[1-5]\d\d'):
                return request
    return 'Error: Invalid request.'


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

def parse_bytes(bytes):
    try:
        int(bytes)
        return bytes
    except ValueError as e:
        return f'ERROR: {e}'

def fields_converter(fields: dict) -> dict:
    ip = parse_ip(fields['ip'])
    

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
    '''
    all the workflow comes here
    '''
    

log_fields_separator('192.168.115.158 - - [04/Aug/2026:14:45:30 -0300] "GET /health HTTP/1.1" 200 1692')
