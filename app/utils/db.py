import re
from sqlalchemy.exc import IntegrityError

def get_conflicting_field(err: IntegrityError):
    """
    Parses the IntegrityError message and returns tuple with conflicting field name and value.
    """
    pattern = re.compile(r'DETAIL\:\s+Key \((?P<field>.+?)\)=\((?P<value>.+?)\) already exists')
    match = pattern.search(str(err))
    if match is not None:
        return match['field'], match['value']