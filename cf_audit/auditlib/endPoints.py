from enum import Enum

class EndPoints(Enum):
    API_VERSION = 'v2'
    APPS = f'{API_VERSION}/apps'
    DOMAINS = f'{API_VERSION}/domains'
    ROUTES = f'{API_VERSION}/routes'
    ROUTE_MAPPINGS = f'{API_VERSION}/route_mappings'
    SERVICES = f'{API_VERSION}/services'
    SERVICE_PLANS = f'{API_VERSION}/service_plans'
    SERVICE_BINDINGS = f'{API_VERSION}/service_bindings'
    SPACES  = f'{API_VERSION}/spaces'
    ORGS = f'{API_VERSION}/organizations'
   
    
    

