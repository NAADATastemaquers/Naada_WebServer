from datetime import date, datetime

from json import dumps




def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))





print(dumps(datetime.now(), default=json_serial))