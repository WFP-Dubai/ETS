
from django.db import connections
from django.core.exceptions import ValidationError


def call_db_procedure(name, parameters, using):
    import cx_Oracle
    cursor = connections[using].cursor()
    Response_Message = cursor.var( cx_Oracle.STRING )
    Response_Message.setvalue( 0, u' ' * 200 )
    Response_Code = cursor.var( cx_Oracle.STRING )
    Response_Code.setvalue( 0, u' ' * 2 )
    
    cursor.callproc( name, (Response_Message, Response_Code,)+parameters)
    
    if Response_Code.getvalue() != 'S':
        raise ValidationError(Response_Message.getvalue(), code=Response_Code.getvalue())
    