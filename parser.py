from datetime import datetime
import sqlite3

def log_fields_separator(log: str) -> dict:
    '''
    separation of the log fields in a dict
    '''
    pass


def fields_converter(fields: dict) -> dict:
    '''
    converts and validates each field to the corret datatype
    '''
    pass

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