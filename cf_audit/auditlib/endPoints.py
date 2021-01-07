from enum import Enum


class EndPoints(Enum):
    API_VERSION = 'v3'
    APPS = f'{API_VERSION}/apps'
    DOMAINS = f'{API_VERSION}/domains'
    ROUTES = f'{API_VERSION}/routes'
    ROUTE_MAPPINGS = f'{API_VERSION}/route_mappings'
    SERVICES = f'{API_VERSION}/service_instances'
    SERVICE_PLANS = f'{API_VERSION}/service_plans'
    SERVICE_OFFERINGS = f'{API_VERSION}/service_offerings'
    SERVICE_ROUTE_BINDINGS = f'{API_VERSION}/service_route_bindings'
    SPACES = f'{API_VERSION}/spaces'
    ORGS = f'{API_VERSION}/organizations'
    SERVICE_BINDINGS = 'v2/service_bindings'
    APPS_V2 ='v2/apps'
