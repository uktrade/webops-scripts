
import os
import requests
from auditlib.endPoints import EndPoints
from urllib.parse import urlsplit, parse_qsl


class Client:

    def __init__(self):
        self.oauthToken = os.popen('cf oauth-token').read().split('\n')[0]
        self.apiEndpoint = os.popen('cf api').read().split('\n')[0].split()[2]
        self.defaultHeaders = {
            'User-Agent': 'DIT-AuditScript',
            'Accept': 'application/json',
        }

    def __getRequest(self, uri=None, headers={}, query={}):
        return requests.get(uri, headers=headers, params=query)

    @property
    def oauth_token(self):
        return self.oauthToken

    @property
    def appsEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.APPS.value}'

    @property
    def domainsEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.DOMAINS.value}'

    @property
    def routesEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.ROUTES.value}'

    @property
    def servicesEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.SERVICES.value}'

    @property
    def servicePlansEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.SERVICE_PLANS.value}'

    @property
    def serviceOfferingsEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.SERVICE_OFFERINGS.value}'

    @property
    def spacesEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.SPACES.value}'

    @property
    def organizationsEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.ORGS.value}'

    @property
    def serviceRouteBindingsEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.SERVICE_ROUTE_BINDINGS.value}'

    @property
    def serviceBindingsEndpoint_v2(self):
        return f'{self.apiEndpoint}/{EndPoints.SERVICE_BINDINGS.value}'

    @property
    def appsEndpoint_v2(self):
        return f'{self.apiEndpoint}/{EndPoints.APPS_V2.value}'        

    def sendRequest(self, endPoint='', headers={}):
        headers.update(self.defaultHeaders)
        headers.update({'Authorization': f'{self.oauthToken}'})

        endPointData = []
        query = ({'page': '1', 'per_page': '100'})

        while True:
            response_raw = self.__getRequest(
                uri=endPoint, headers=headers, query=query)

            if response_raw.status_code == 200:
                response = response_raw.json()

                if response['pagination']['next'] is not None:
                    endPointData += response['resources']
                    endPoint = response['pagination']['next']['href']
                    query.clear()

                else:
                    query.clear()
                    endPointData += response['resources']
                    return endPointData
            else:
                print(response_raw.status_code)

    def sendRequest_v2(self, endPoint='', headers={}):
        headers.update(self.defaultHeaders)
        headers.update({'Authorization': f'{self.oauthToken}'})

        endPointData = []
        query = ({'page': '1', 'per_page': '100'})

        while True:
            response_raw = self.__getRequest(
                uri=endPoint, headers=headers, query=query)

            if response_raw.status_code == 200:
                response = response_raw.json()

                if response['next_url'] is not None:
                    endPointData += response['resources']
                    query.clear()
                    query.update(
                        dict(parse_qsl(urlsplit(response['next_url']).query)))

                else:
                    query.clear()
                    endPointData += response['resources']
                    return endPointData
            else:
                print(response_raw.status_code)
