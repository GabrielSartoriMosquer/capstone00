from datetime import datetime
from zoneinfo import ZoneInfo
import random

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

def generate_line(timestamp: datetime) -> str:
    
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

    return f'{ip} - - [{date}] "{api_call}" {status} {size}'

def generate_log(n: int, path: str, corrupted_rate: float = 0.02) -> None:
    pass

for _ in range(30):
    print(generate_line(datetime.now(ZoneInfo("America/Sao_Paulo")))) 