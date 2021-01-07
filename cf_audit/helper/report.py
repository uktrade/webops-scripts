from tqdm import tqdm
import re
import json
import os
from datetime import datetime
import pprint


class Report:

    def __init__(self, client, options, fetch, store_file,timeformat):
        self.client = client
        self.options = options
        self.store_file = store_file
        self.fetch = fetch
        self.timeformat = timeformat
        self.filter_orgs = []
        self.filter_spaces = []

    def __read_info(self):
        data = {}
        with open(self.store_file, 'r') as json_file:
            data = json.load(json_file)
            json_file.close()
        return data

    def __get_info(self):
        # if file exist , update file only if it is older than one hour
        if os.path.exists(self.store_file):
            data = self.__read_info()
            file_time = datetime.strptime(data['timestamp'], self.timeformat)
            current_time = datetime.strptime(
                datetime.now().strftime(self.timeformat), self.timeformat
            )

            if (current_time - file_time).seconds >= 3600:
                self.fetch.info()
        else:
            if os.path.exists(self.store_file):
                os.remove(self.store_file)
            self.fetch.info()

    def __filtered_data(self):

        if self.options.organizations:
            self.filter_orgs = self.options.organizations.split(',')
        if self.options.spaces:
            self.filter_spaces = self.options.spaces.split(',')

        if self.options.scan_env_variables:
            filter_env_variables = self.options.scan_env_variables.split(',')
        if self.options.scan_env_values:
            filter_env_values = self.options.scan_env_values.split(',')

        data = self.__read_info()

        # remove filterd orgs and spaces
        if self.filter_orgs:
            new_orgs = {}
            new_spaces = {}
            for org_id, org_name in data['organizations'].items():
                if org_name in self.filter_orgs:
                    new_orgs.update({org_id: org_name})

                    for space_id, space_data in data['spaces'].items():
                        if space_data['organization'] in org_name:
                            new_spaces.update({space_id: space_data})

            data['organizations'] = new_orgs
            data['spaces'] = new_spaces

        else:
            self.filter_orgs = data['organizations'].values()

        if self.filter_spaces:
            new_spaces = {}
            for space_id, space_data in data['spaces'].items():
                if space_data['name'] in self.filter_spaces:
                    new_spaces.update({space_id: space_data})

            data['spaces'] = new_spaces
        else:
            for space_id, space_data in data['spaces'].items():
                self.filter_spaces.append(space_data['name'])

        return data

    def build_service_report_data(self, data):
        filter_services = []
        filter_service_versions = []

        if self.options.services:
            filter_services = self.options.services.split(',')

        if self.options.exclude_service_versions:
            filter_service_versions = self.options.exclude_service_versions.split(
                ',')
        if self.options.service_versions:
            filter_service_versions = self.options.service_versions.split(',')

        new_services_temp = {}
        for service_id, service_data in data['services'].items():
            if service_data['organization'] in self.filter_orgs and service_data['space'] in self.filter_spaces:
                if filter_services:
                    if 'name' in service_data:
                        if service_data['name'] in filter_services:
                            new_services_temp.update(
                                {service_id: service_data})
                else:
                    new_services_temp.update({service_id: service_data})

        new_services = {}

        if self.options.exclude_service_versions:
            for service_id, service_data in new_services_temp.items():
                if service_data['version'] not in filter_service_versions:
                    new_services.update({service_id: service_data})

        else:
            if self.options.service_versions:
                for service_id, service_data in new_services_temp.items():
                    if service_data['version'] in filter_service_versions:
                        new_services.update({service_id: service_data})
            else:
                new_services = new_services_temp

        service_report = [['Service Report', '', '', '', '', ''],
                          ['organization', 'space', 'instance_name',
                           'service', 'version', 'service_plan']
                          ]

        for service in new_services.values():
            name = None
            version =  None
            plan_name = None
            if 'name' in service:
                name = service['name']
                version = service['version']
                plan_name = service['plan_name']

            service_report.append([
                service['organization'], service['space'],service['instance_name'], name, version, plan_name
            ])

        return service_report

    def build_route_report_data(self, data):

        new_routes = {}

        # filter routes

        for route_id, route_data in data['routes'].items():
            if route_data['organization'] in self.filter_orgs and route_data['space'] in self.filter_spaces:
                new_routes.update({route_id: route_data})

        # add binding if route has it

        rote_ids = new_routes.keys()

        for service_route_binding_id, service_route_binding_data in data['service_route_bindings'].items():
            related_route_id = service_route_binding_data['route_id']
            related_service_instance_name = data['services'][service_route_binding_data['service_id']]['instance_name']

            if related_route_id in rote_ids:
                data['routes'][related_route_id].update({'route_service_url': data['service_route_bindings'][service_route_binding_id]['route_service_url'],
                                                         'route_instance_name': related_service_instance_name
                                                         })

        # generate_report
        routes_report = [['Route Report', '', '', '', '', ''],
                         ['organization', 'space', 'app', 'app_url',
                          'route_service_name', 'route_service_url']
                         ]

        for route_id, route_data in new_routes.items():

            related_app = None
            if route_data['app_id'] is not None:
                related_app = data['apps'][route_data['app_id']]['name']

            related_service_instance_name = None
            related_route_service_url = None

            if 'route_service_url' in route_data:
                related_service_instance_name = route_data['route_instance_name']
                related_route_service_url = route_data['route_service_url']

            routes_report.append([
                route_data['organization'],
                route_data['space'],
                related_app,
                route_data['url'],
                related_service_instance_name,
                related_route_service_url
            ])

        return routes_report

    def build_scanenv_report_data(self, data):

        filter_env_variables = []
        filter_env_values = []

        if self.options.scan_env_variables:
            filter_env_variables = self.options.scan_env_variables.split(',')
        if self.options.scan_env_values:
            filter_env_values = self.options.scan_env_values.split(',')

        new_apps = {}
       
        for app_id,app_data in data['apps'].items():
            if app_data['organization'] in self.filter_orgs and app_data['space'] in self.filter_spaces:
                new_apps.update({app_id:app_data})

        for app in self.fetch.apps_v2():
            app_id = app['metadata']['guid']
            if app_id in new_apps:
                new_apps[app_id].update({'vars':app['entity']['environment_json']})


        #Process filtered variables
        if filter_env_variables:
            for app_id,app_data in new_apps.items():
                found_vars = []
                for filter_env_var in filter_env_variables:
                    if filter_env_var in new_apps[app_id]['vars']:
                        found_vars.append({filter_env_var:new_apps[app_id]['vars'][filter_env_var]})
                new_apps[app_id].update({'vars':found_vars})

        if filter_env_values:
            for app_id,app_data in new_apps.items():
                found_vals = []
                for filter_env_val in filter_env_values:
                    pattern = re.compile(f".*{filter_env_val}.*")
                    for env_var,env_val in new_apps[app_id]['vars'].items():
                        if pattern.match(env_val):
                            found_vals.append({env_var:env_val})
                new_apps[app_id].update({'vars':found_vals})

        # generate_report
        scanenv_report = [['Scan Env Variables Report', '', '', '', ''],
                         ['organization', 'space', 'app', 'Variable',
                          'Value']
                         ]

        for app_id,app_data in new_apps.items():
            if app_data['vars']:
                for variable in app_data['vars']:
                    pprint.pp(app_data)
                    var_name = list(variable.keys())[0]
                    var_value = list(variable.values())[0]
                    scanenv_report.append(
                        [ app_data['organization'],app_data['space'],app_data['name'],var_name,var_value ]
                    )

        return scanenv_report

    def run(self):

        report_progress_bar = tqdm(total=3, position=0, leave=True)

        # Collect information
        report_progress_bar.set_description('Collecting information')
        report_progress_bar.update()

        self.__get_info()

        # filter information
        report_progress_bar.set_description('Filtering information')
        report_progress_bar.update()
        filtered_data = self.__filtered_data()

        report_progress_bar.set_description('Generating Reports')
        report_progress_bar.update()

        # send report
        reports = {}

        # if nothing is specified , defualt is to print service and route report
        if ( (not self.options.services_only) and (not self.options.routes_only) ) and ( not self.options.scanenv_only):
            reports.update(
                {'services': self.build_service_report_data(data=filtered_data)})
            reports.update(
                {'routes': self.build_route_report_data(data=filtered_data)})

        else:
            # if service options is specified
            if self.options.services_only:
                reports.update(
                    {'services': self.build_service_report_data(data=filtered_data)})

            if self.options.routes_only:
                reports.update(
                    {'routes': self.build_route_report_data(data=filtered_data)})

            if self.options.scan_env_variables or self.options.scan_env_values:
                reports.update({'scanenv': self.build_scanenv_report_data(data=filtered_data)})

        report_progress_bar.clear()
        report_progress_bar.close()

        return reports