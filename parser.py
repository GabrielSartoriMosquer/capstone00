from datetime import datetime
import re
import pandas as pd
from dataclasses import dataclass

API_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
DATE_FORMAT = '%d/%b/%Y:%H:%M:%S %z'
PATH = 'logs/log.txt'

class InvalidField(Exception):
    pass
            
def log_fields_separator(log: str) -> dict:

    regex = r'^(?P<ip>\S+)\s+(?P<ident>\S+)\s+(?P<user>\S+)\s+\[(?P<date>[^\]]+)\]\s+"(?P<request>[^"]+)"\s+(?P<status>\S+)\s+(?P<size>\S+|-)$'

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
        if parts[0] in API_METHODS:
            if re.match(r'^(?:/[a-zA-Z0-9]+)+$', parts[1]): # ?: para que o regex apenas valide e não guarde na memória
                if re.match(r'^HTTP/\d+(?:\.\d+)?$', parts[2]): 
                    method, route, protocol = parts[0], parts[1], parts[2]
                    return  method, route, protocol
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

def parse_size(size):
    try:
        size = int(size)
        if size < 0:
            raise InvalidField('size: Number of size below zero.')
        else:
            return size
    except ValueError as e:
        raise InvalidField(f'SIZE: {e}')

def try_except_parse(id, log_dict):
    errors = []

    # IP
    try:
        ip = parse_ip(log_dict['ip'])
    except InvalidField as e:
        errors.append(f'{id} - {str(e)}') 
    
    # DATE
    try:
        date = parse_date(log_dict['date'], DATE_FORMAT)
    except InvalidField as e:
        errors.append(f'{id} - {str(e)}') 

    # REQUEST
    try:
        method, route, protocol = parse_request(log_dict['request'])
    except InvalidField as e:
        errors.append(f'{id} - {str(e)}') 

    # STATUS
    try:
        status = parse_status(log_dict['status'])
    except InvalidField as e:
        errors.append(f'{id} - {str(e)}') 

    # SIZE
    try:
        size = parse_size(log_dict['size'])
    except InvalidField as e:
        errors.append(f'{id} - {str(e)}') 

    # OBJECT
    if not errors:
        log = LogEntry(id, ip, date, method, route, protocol, status, size)
        return log, None
    else:
        return None, errors

@dataclass 
class LogEntry:
    id: int
    ip: str
    date : datetime
    method : str
    route : str
    protocol : str
    status : int
    size : int

def parser_orchestrator(log_path):
    df_logs = pd.DataFrame(columns=(['id', 'ip', 'date', 'method', 'route', 'protocol', 'status', 'size']))
    logs = []
    errors = []
    with open(log_path, 'r', encoding='utf-8') as f:
        for id, line in enumerate(f, start=1):
                log_dict = log_fields_separator(f'{line}')
                if log_dict:
                    log, error = try_except_parse(id, log_dict)
                    if error:
                        errors.append(error)
                    if log:
                        logs.append(log)

    df_logs = pd.concat([df_logs, pd.DataFrame(logs)], ignore_index=True)
    df_logs.to_csv('logs.csv')

    df_errors = pd.DataFrame(errors)
    df_errors.to_csv('errors.csv')


if __name__ == '__main__':
    parser_orchestrator(PATH)