def search_by_postcode(postcode, json):
    serchedList = []
    listOfId = []
    for incident in json['incidents']:
        if incident['ukpnIncident'] is not None:
            for postCodeAffected in incident['ukpnIncident']['postCodesAffected'] + incident['ukpnIncident'][
                'postCodesPlanned']:
                if postcode.replace(" ", "").lower() in postCodeAffected.replace(" ", "").lower():
                    serchedList.append(incident)
                    listOfId.append(incident['incidentReference'])
                    break

    return serchedList, listOfId

# def get_incident_by_id():
#     with open('test_jsons/unplaned_incident.json') as json:
#         return json