
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
    def spacesEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.SPACES.value}'

    @property
    def organizationsEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.ORGS.value}'

    @property
    def serviceBindingsEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.SERVICE_BINDINGS.value}'

    @property
    def routeMappingsEndpoint(self):
        return f'{self.apiEndpoint}/{EndPoints.ROUTE_MAPPINGS.value}'

    def sendRequest(self, endPoint='', headers={}, query={}):
        headers.update(self.defaultHeaders)
        headers.update({'Authorization': f'{self.oauthToken}'})

        endPointData = []

        while True:
            response_raw = self.__getRequest(
                uri=endPoint, headers=headers, query=query)
            if response_raw.status_code == 200:
                response = response_raw.json()

                endPointData += response['resources']

                next_url = response['next_url']

                if next_url is None:
                    return endPointData

                query.clear()
                query.update(dict(parse_qsl(urlsplit(next_url).query)))

    def sendSingleResponseRequest(self, endPoint='', headers={}):
        headers.update(self.defaultHeaders)
        headers.update({'Authorization': f'{self.oauthToken}'})

        response_raw = self.__getRequest(uri=endPoint, headers=headers)

        if response_raw.status_code == 200:
            return response_raw.json()
