
from django.db import connections
from django.core.exceptions import ValidationError


def call_db_procedure(name, parameters, using):
    import cx_Oracle
    cursor = connections[using].cursor()
    
    cursor.execute("Set role epic_all identified by writeon;")
    
    Response_Message = cursor.var(cx_Oracle.STRING, 2000).var
    Response_Code = cursor.var(cx_Oracle.STRING, 1).var
    cursor.callproc( name, (Response_Message, Response_Code)+parameters)
    
    if Response_Code.getvalue() != 'S':
        raise ValidationError(Response_Message.getvalue(), code=Response_Code.getvalue())
