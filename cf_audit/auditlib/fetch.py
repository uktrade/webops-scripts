import json
from datetime import datetime

class Fetch:

    def __init__(self, client, store_file,timeformat):
        self.cf_client = client
        self.store_file = store_file
        self.timeformat = timeformat


    def __organizations(self):
        return self.cf_client.sendRequest(
            endPoint=self.cf_client.organizationsEndpoint)

    def __spaces(self):
        return self.cf_client.sendRequest(
            endPoint=self.cf_client.spacesEndpoint)

    def __apps(self):
        return self.cf_client.sendRequest(
            endPoint=self.cf_client.appsEndpoint)

    def __services(self):
        return self.cf_client.sendRequest(
            endPoint=self.cf_client.servicesEndpoint)

    def __service_plans(self):
        return self.cf_client.sendRequest(
            endPoint=self.cf_client.servicePlansEndpoint)

    def __service_offerings(self):
        return self.cf_client.sendRequest(
            endPoint=self.cf_client.serviceOfferingsEndpoint)

    def __service_route_bindings(self):
        return self.cf_client.sendRequest(
            endPoint=self.cf_client.serviceRouteBindingsEndpoint)

    def __domains(self):
        return self.cf_client.sendRequest(
            endPoint=self.cf_client.domainsEndpoint)

    def __routes(self):
        return self.cf_client.sendRequest(
            endPoint=self.cf_client.routesEndpoint)

    def __service_bindings(self):
        return self.cf_client.sendRequest_v2(
            endPoint=self.cf_client.serviceBindingsEndpoint_v2)

    def apps_v2(self):
        return self.cf_client.sendRequest_v2(
            endPoint=self.cf_client.appsEndpoint_v2)

    def __info_store(self, data):
        with open(self.store_file, mode="w") as info_file:
            json.dump(data, info_file)
            info_file.close()

    def __info_gathering(self):
        data = {'organizations': {}, 'spaces': {}, 'services': {}, 'apps': {}, 'routes': {
        }, 'domains': {}, 'service_bindings': {}, 'service_route_bindings': {}, 'timestamp': ''}

        for organization in self.__organizations():
            data['organizations'].update(
                {organization['guid']: organization['name']})

        for space in self.__spaces():
            related_org_id = space['relationships']['organization']['data']['guid']
            data['spaces'].update({space['guid']: {
                                  'name': space['name'], 'organization': data['organizations'][related_org_id]}})

        offerings = {}

        for service_offering in self.__service_offerings():
            offerings.update(
                {service_offering['guid']: service_offering['name']})

        plans = {}
        for service_plan in self.__service_plans():
            related_offering_id = service_plan['relationships']['service_offering']['data']['guid']
            plans.update({
                service_plan['guid']:
                {
                    'name': service_plan['name'],
                    'version': service_plan['broker_catalog']['metadata']['AdditionalMetadata']['version'],
                    'service_name':  offerings[related_offering_id]
                }
            })

        offerings = None

        for service in self.__services():
            related_space_id = service['relationships']['space']['data']['guid']
            for space_id, space_data in data['spaces'].items():
                if space_id == related_space_id:

                    data['services'].update({
                        service['guid']: {
                            'instance_name': service['name'],
                            'type': service['type'],
                            'organization': space_data['organization'],
                            'space': space_data['name'],
                        }
                    })

                    plan_id = None
                    if 'service_plan' in service['relationships']:
                        plan_id = service['relationships']['service_plan']['data']['guid']

                    if plan_id is not None:
                        data['services'][service['guid']].update({
                            'plan_name': plans[plan_id]['name'],
                            'version': plans[plan_id]['version'],
                            'name': plans[plan_id]['service_name']
                        })

        plans = None

        for app in self.__apps():
            related_space_id = app['relationships']['space']['data']['guid']
            for space_id, space_data in data['spaces'].items():
                if space_id == related_space_id:
                    data['apps'].update({
                        app['guid']: {
                            'name': app['name'],
                            'state': app['state'],
                            'organization': space_data['organization'],
                            'space': space_data['name'],
                        }
                    })

        for domain in self.__domains():
            data['domains'].update({domain['guid']: {'name': domain['name']}})

        for route in self.__routes():
            related_space_id = route['relationships']['space']['data']['guid']
            related_domain_id = route['relationships']['domain']['data']['guid']
            related_app_id = None
            for destination in route['destinations']:
                related_app_id = destination['app']['guid']

            data['routes'].update({
                route['guid']: {
                    'host': route['host'],
                    'url': route['url'],
                    'app_id': related_app_id,
                    'organization': data['spaces'][related_space_id]['organization'],
                    'space': data['spaces'][related_space_id]['name'],
                    'domain': data['domains'][related_domain_id]['name']
                }
            })

            data['domains'][related_domain_id].update({
                'organization': data['spaces'][related_space_id]['organization'],
                'space': data['spaces'][related_space_id]['name']
            })

        for service_binding in self.__service_bindings():
            related_app_id = service_binding['entity']['app_guid']
            related_service_id = service_binding['entity']['service_instance_guid']
            if related_app_id not in data['service_bindings']:
                data['service_bindings'].update(
                    {related_app_id: {'service_ids': []}})

            data['service_bindings'][related_app_id]['service_ids'].append(
                related_service_id)

        for service_route_binding in self.__service_route_bindings():
            relate_route_id = service_route_binding['relationships']['route']['data']['guid']
            related_service_id = service_route_binding['relationships']['service_instance']['data']['guid']
            data['service_route_bindings'].update({
                service_route_binding['guid']:
                {
                    'route_id': relate_route_id,
                    'route_service_url': service_route_binding['route_service_url'],
                    'service_id': related_service_id
                }
            })

        data['timestamp'] = datetime.now().strftime(self.timeformat)

        self.__info_store(data)

    def info(self):
        return self.__info_gathering()
