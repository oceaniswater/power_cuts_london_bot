def search_by_postcode(postcode, json):
    serchedList = []
    # with open('test_jsons/lists.json') as f:  # Использовать джейсон из редиса, который обновляется по апишке раз в
    # 10 минут
    for incident in json['incidents']:
        if incident['ukpnIncident'] is not None:
            for postCodeAffected in incident['ukpnIncident']['postCodesAffected'] + incident['ukpnIncident'][
                'postCodesPlanned']:
                if postcode.replace(" ", "").lower() in postCodeAffected.replace(" ", "").lower():
                    serchedList.append(incident)
                    break

    return serchedList

def get_incident_by_id():
    with open('test_jsons/unplaned_incident.json') as json:
        return json