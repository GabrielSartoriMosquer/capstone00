from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import random
import sys
from pathlib import Path

IPS = [f'192.168.{random.randint(1,255)}.{random.randint(1,255)}' for _ in range(30)]
IP_WEIGHTS = [10] * 3 + [2] * 27

API_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
API_METHOD_WEIGHTS = [70, 15, 6, 4, 5]

API_ROUTES = ['/api/users', '/api/users/{id}', '/api/orders', '/api/products', '/api/auth/login', '/health']
API_ROUTE_WEIGHTS = [8,6,4,4,2,15]

PROTOCOLS = ['HTTP/1.1', 'HTTP/2', 'HTTP/1.0']
PROTOCOL_WEIGHTS = [80, 18, 2]

STATUS = [200, 404, 500]
STATUS_WEIGHTS = [10, 2.5, 1]

CORRUPTED_SYMBOLS = ['#$', r'%%', '&&*', '@#¨%']

def generate_fields(timestamp: datetime) -> list:
    
    ip = random.choices(IPS, IP_WEIGHTS)[0]

    api_method = random.choices(API_METHODS, API_METHOD_WEIGHTS)[0]

    api_route = random.choices(API_ROUTES, API_ROUTE_WEIGHTS)[0]
    if '{id}' in api_route:
        api_route = api_route.replace('{id}', str(random.randint(1,10)))

    protocol = random.choices(PROTOCOLS, PROTOCOL_WEIGHTS)[0]

    api_call = f'{api_method} {api_route} {protocol}'

    status = random.choices(STATUS, STATUS_WEIGHTS)[0]
    size = random.randint(1, 4096)

    date = timestamp.strftime('%d/%b/%Y:%H:%M:%S %z')
    fields = [ip, date, api_call, status, size]

    return fields 


def corrupt_fields(fields:list) -> list:

    n_fields = random.choices([1,2,3,4,5], [40,30,20,10,5])[0]
    indexes = random.sample(range(len(fields)), k=(n_fields))
    
    for idx in indexes:
        fields[idx] = random.choice(CORRUPTED_SYMBOLS)

    return fields


def format_line(fields) -> str:
        
        return f'{fields[0]} - - [{fields[1]}] "{fields[2]}" {fields[3]} {fields[4]}'


def generate_log(n: int, path: str, corrupted_rate: float = 0.02) -> None:

    clock = datetime.now(ZoneInfo("America/Sao_Paulo"))

    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w') as log:
        for _ in range(n):
            fields = generate_fields(clock)

            if random.random() < corrupted_rate:
                fields = corrupt_fields(fields)

            log.write(f'{format_line(fields)}\n')
            clock += timedelta(seconds=(random.randint(0,5)))

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    
    generate_log(n, 'logs/log.txt')