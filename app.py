from ApiPowerCuts import ApiPowerCuts

result = ApiPowerCuts.get_incidents_list()
print(result.json())