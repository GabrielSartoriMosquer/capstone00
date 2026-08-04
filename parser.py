from datetime import datetime
import sqlite3
import re

def log_fields_separator(log: str) -> dict:

    regex = r'^(?P<ip>\S+)\s+(?P<ident>\S+)\s+(?P<user>\S+)\s+\[(?P<datetime>[^\]]+)\]\s+"(?P<request>[^"]+)"\s+(?P<status>\d+)\s+(?P<bytes>\d+|-)$'

    match = re.match(regex, log)

    if match:
        # Returns a dict with the group names as keys
        fields = match.groupdict()
        return fields


def fields_converter(fields: dict) -> dict:
    ip_parts = fields['ip'].split('.')
    if (len(ip_parts)) == 4 and (p for p in ip_parts if p<255 and p>0):
        if 

class LogEntry:
    '''
    stores all valid logs
    '''
    def __init__(self, id:str, ip:int, date:datetime, method:str, route:str, protocol:str, status:int, size:int):
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
