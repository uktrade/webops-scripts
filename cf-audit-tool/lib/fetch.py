
class Fetch:

    def __init__(self, client):
        self.cf_client = client

    def organizations(self, filter_organizations=[]):
        organizations_list = []
        query = {'order-by': 'name'}

        for organization in self.cf_client.sendRequest(endPoint=self.cf_client.organizationsEndpoint, query=query):
            name = organization['entity']['name']
            id = organization['metadata']['guid']

            organizations_list.append(
                {'name': name,
                 'organization_guid': id})

            if filter_organizations:
                if organization['entity']['name'] not in filter_organizations:
                    organizations_list.pop()

        return organizations_list

    def spaces(self, filter_spaces=[], organization_guid=''):
        spaces_list = []
        query = {'order-by': 'name'}

        if organization_guid:
            query.update({'q': f'organization_guid:{organization_guid}'})

        for space in self.cf_client.sendRequest(endPoint=self.cf_client.spacesEndpoint, query=query):
            name = space['entity']['name']
            id = space['metadata']['guid']
            orgnization_id = space['entity']['organization_guid']
            spaces_list.append({'name': name,
                                'space_guid': id,
                                'organization_guid': orgnization_id})

            if filter_spaces:
                if name not in filter_spaces:
                    spaces_list.pop()

        return spaces_list

    def apps(self, filter_apps=[], space_guid=''):
        apps_list = []
        query = {'order-direction': 'asc'}

        if space_guid:
            query.update({'q': f'space_guid:{space_guid}'})

        for app in self.cf_client.sendRequest(endPoint=self.cf_client.appsEndpoint, query=query):
            name = app['entity']['name']
            guid = app['metadata']['guid']
            space_guid = app['entity']['space_guid']

            apps_list.append(
                {'name': name, 'app_guid': guid, 'space_guid': space_guid})
            if filter_apps:
                name = app['entity']['name']
                if name not in filter_apps:
                    apps_list.pop()

        return apps_list

    def services_bound_to_app(self, app_guid=''):
        service_list = []
        query = {'order-direction': 'asc'}

        if app_guid:
            query.update({'q': f'app_guid:{app_guid}'})

        for binding in self.cf_client.sendRequest(endPoint=self.cf_client.serviceBindingsEndpoint, query=query):
            service_instance = self.cf_client.sendSingleResponseRequest(
                endPoint=f"{self.cf_client.apiEndpoint}{binding['entity']['service_instance_url']}")

            service = ''
            service_plan = ''
            if 'service_url' in service_instance['entity']:
                service_details = self.cf_client.sendSingleResponseRequest(
                    endPoint=f"{self.cf_client.apiEndpoint}{service_instance['entity']['service_url']}")
                service_plan_details = self.cf_client.sendSingleResponseRequest(
                    endPoint=f"{self.cf_client.apiEndpoint}{service_instance['entity']['service_plan_url']}")

                service = service_details['entity']['label']
                service_plan = service_plan_details['entity']['name']

            service_instance_name = service_instance['entity']['name']
          
            service_list.append({'service_instance_name': service_instance_name,'service':service,'service_plan':service_plan,'app_guid':app_guid})

        return service_list


    def routes_bound_to_app(self, app_guid=''):
        routes_list = []
        query = {'order-direction': 'asc'}

        if app_guid:
            query.update({'q': f'app_guid:{app_guid}'})

        for route_mapping in self.cf_client.sendRequest(endPoint=self.cf_client.routeMappingsEndpoint, query=query):
            route = self.cf_client.sendSingleResponseRequest(
                endPoint=f"{self.cf_client.apiEndpoint}{route_mapping['entity']['route_url']}")

            route_host = route['entity']['host']
            route_path = route['entity']['path']
            domain_name = self.cf_client.sendSingleResponseRequest(
                f"{self.cf_client.apiEndpoint}{route['entity']['domain_url']}")['entity']['name']

     
            route_service_url = ''
            route_service_instance_name = ''   

            if route['entity']['service_instance_guid']:
                service_instance = self.cf_client.sendSingleResponseRequest(
                    f"{self.cf_client.apiEndpoint}{route['entity']['service_instance_url']}")

                if 'route_service_url' in service_instance['entity']:
                    route_service_url = service_instance['entity']['route_service_url']

                if 'service_url' in service_instance['entity']:
                    service_details = self.cf_client.sendSingleResponseRequest(
                        endPoint=f"{self.cf_client.apiEndpoint}{service_instance['entity']['service_url']}")
                    service_plan_details = self.cf_client.sendSingleResponseRequest(
                        endPoint=f"{self.cf_client.apiEndpoint}{service_instance['entity']['service_plan_url']}")

                    route_service = service_details['entity']['label']
                    route_service_plan = service_plan_details['entity']['name']

                route_service_instance_name = service_instance['entity']['name']

            routes_list.append({'route_url': f'{route_host}.{domain_name}{route_path}',
                                'route_service_instance_name': route_service_instance_name,
                                'route_service_url': route_service_url
                                })
        return routes_list


    def servicePlans(self, filter_servicePlans=[]):
        servicePlans_list = []
        servicePlans = self.cf_client.sendRequest(
            self.cf_client.servicePlansEndpoint)

    def services(self, filter_services=[]):
        services_list = []
        query = {'order-direction': 'asc'}
        for service in self.cf_client.sendRequest(endPoint=self.cf_client.servicesEndpoint, query=query):
            services_list.append(app)
            if filter_services:
                name = service['entity']['name']
                if name not in filter_services:
                    services_list.pop()

        return services_list


    def routes(self, filter_services=[]):
        routes_list = []
        query = {'order-direction': 'asc'}

        return self.cf_client.sendRequest(
            endPoint=self.cf_client.routesEndpoint, query=query)

    def domains(self, filter_domains=[]):
        domains_list = []
        query = {'order-direction': 'asc'}
        return self.cf_client.sendRequest(
            endPoint=self.cf_client.domainsEndpoint, query=query)
