import requests
import json

class AtlassianAdmin:

    def __init__(self,url,token):
        self.base_url = url
        self.headers = headers = { "Accept": "application/json", "Authorization": f"Bearer {token}" }


    def __apiCall(self,url):

        response_data = []
        original_url = url

        while True:
            response = requests.request('GET',url,headers=self.headers)

            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                break

            response_json = json.loads(response.text)
        
            response_data += response_json['data']

            response_links = response_json['links']

            #check if there is more data to fetch!
            if "next" in response_links:
                if response_links['next']:
                    url = response_links['next']
                else:
                    break

            #break if next key is not found!
            else:
                break

        url = original_url
        return response_data

    def getAccountOrgs(self):
        return self.__apiCall(self.base_url)

    def getOrgIdbyOrgName(self,orgName):

        orgId = ''

        accountOrgs = self.getAccountOrgs()

        for org in accountOrgs:
            if (org['attributes']['name']).lower() == orgName.lower():
                orgId = org['id']
                break

        return orgId

    def getOrgUsers(self,orgName):
        orgId = self.getOrgIdbyOrgName(orgName)
        url = f'{self.base_url}/{orgId}/users'
        return self.__apiCall(url=url)