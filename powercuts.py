import json
# from cashews import cache
#
# cache.setup("mem://")


# use a decorator-based API
# @cache(ttl="3h", key="user:{request}")
# async def long_running_function(request):
#     ...

# or for fine-grained control, use it directly in a function
# async def cache_using_function(request):
#     await cache.set(key="request", value=request, expire=60)




def search_by_postcode(postcode, f):
        serchedList = []
        uniqueSet = set()
    # with open('test_jsons/lists.json') as f:  # Использовать джейсон из редиса, который обновляется по апишке раз в 10 минут
        templates = f
        for incident in templates['incidents']:
            if incident['ukpnIncident'] is not None:
                for postCodeAffected in incident['ukpnIncident']['postCodesAffected'] + incident['ukpnIncident']['postCodesPlanned']:
                    if postcode.replace(" ", "").lower() in postCodeAffected.replace(" ", "").lower():
                        # uniqueSet.add(incident['incidentReference'])
                        # if incident['incidentReference'] not in uniqueSet:
                        serchedList.append(incident)
                        break

        return serchedList