
class Fetch:

    def __init__(self, client):
        self.cf_client = client

    def __filter(self, data, filter):
        for index, item in enumerate(data):
            if item['entity']['name'] not in filter:
                data[index] = ''

        data[:] = (item for item in data if item != '')
        return data

    def __filter_services(self, data, filter_services, filter_service_plans, exclude_service_plans):

        if filter_services:
            for index, item in enumerate(data):

                if not item['service']:
                    data[index] = ''
                else:
                    if item['service']['entity']['label'] not in filter_services:
                        data[index] = ''
            data[:] = (item for item in data if item != '')

        if filter_service_plans:
            for index, item in enumerate(data):

                if not item['service_plan']:
                    data[index] = ''
                else:
                    # if plan is in filter?
                    result = any(plan in item['service_plan']['entity']['name']
                                 for plan in filter_service_plans)

                    # if plan is in filter and, we want to exclude it, remove it
                    if exclude_service_plans:
                        if result:
                            data[index] = ''
                    # if we want include matching plan and delete rest of it
                    else:
                        if not result:
                            data[index] = ''

            data[:] = (item for item in data if item != '')

        return data

    def organizations(self, filter_organizations=[]):
        organizations = []
        query = {'order-by': 'name'}

        organizations = self.cf_client.sendRequest(
            endPoint=self.cf_client.organizationsEndpoint, query=query)

        if filter_organizations:
            return self.__filter(
                data=organizations, filter=filter_organizations)

        return organizations

    def spaces(self, filter_spaces=[], organization_guid=''):
        spaces = []
        query = {'order-by': 'name'}

        if organization_guid:
            query.update({'q': f'organization_guid:{organization_guid}'})

        spaces = self.cf_client.sendRequest(
            endPoint=self.cf_client.spacesEndpoint, query=query)

        if filter_spaces:
            space = self.__filter(data=spaces, filter=filter_spaces)

        return spaces

    def apps(self, filter_apps=[], space_guid=''):
        apps = []
        query = {'order-direction': 'asc'}

        if space_guid:
            query.update({'q': f'space_guid:{space_guid}'})

        apps = self.cf_client.sendRequest(
            endPoint=self.cf_client.appsEndpoint, query=query)

        if filter_apps:
            apps = self.__filter(data=apps, filter=filter)

        return apps

    def __service_info(self, url=''):
        return self.cf_client.sendRequest(
            endPoint=f"{self.cf_client.apiEndpoint}{url}")

    def bound_services(self, app_guid='', filter_services=[], filter_service_plans=[], exclude_service_plans=bool):
        service_list = []
        query = {'order-direction': 'asc'}

        if app_guid:
            query.update({'q': f'app_guid:{app_guid}'})

        for binding in self.cf_client.sendRequest(endPoint=self.cf_client.serviceBindingsEndpoint, query=query):
            services_instance_url = binding['entity']['service_instance_url']
            service_instance = self.__service_info(url=services_instance_url)

            service_details = ''
            service_plan_details = ''

            if 'service_url' in service_instance['entity']:
                service_url = service_instance['entity']['service_url']
                service_details = self.__service_info(url=service_url)
                service_plan_url = service_instance['entity']['service_plan_url']
                service_plan_details = self.__service_info(url=service_plan_url)

            service_list.append({'service_instance': service_instance,
                                 'service': service_details, 'service_plan': service_plan_details})

        
        if filter_services or filter_service_plans:
            return self.__filter_services(data=service_list, filter_services=filter_services, filter_service_plans=filter_service_plans, exclude_service_plans=exclude_service_plans)

        return service_list

    def __routes_info(self, url=''):
        return self.cf_client.sendRequest(
            endPoint=f"{self.cf_client.apiEndpoint}{url}")

    def mapped_routes(self, app_guid=''):
        route_mappings = []
        query = {'order-direction': 'asc'}

        if app_guid:
            query.update({'q': f'app_guid:{app_guid}'})

        for route_mapping in self.cf_client.sendRequest(endPoint=self.cf_client.routeMappingsEndpoint, query=query):

            route_url = route_mapping['entity']['route_url']

            route_details = self.__routes_info(route_url)

            domain_url = route_details['entity']['domain_url']

            domain_details = self.__routes_info(url=domain_url)

            route_service_instance = ''

            if route_details['entity']['service_instance_guid']:
                route_service_instance_url = route_details['entity']['service_instance_url']

                route_service_instance = self.__service_info(
                    url=route_service_instance_url)

            route_mappings.append({'route': route_details,
                                   'domain': domain_details,
                                   'route_service_instance': route_service_instance
                                   })
        return route_mappings
