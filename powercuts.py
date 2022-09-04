import json


def search_by_postcode(postcode):
    serchedDict = dict()
    with open('test_jsons/lists.json') as f:  # Использовать джейсон из редиса, который обновляется по апишке раз в 10 минут
        templates = json.load(f)
        for incident in templates['incidents']:
            if incident['ukpnIncident'] is not None:
                for postCodeAffected in incident['ukpnIncident']['postCodesAffected'] + incident['ukpnIncident']['postCodesPlanned']:
                    if postcode.replace(" ", "") in postCodeAffected.replace(" ", ""):
                        serchedDict[incident['incidentReference']] = incident

    return serchedDict