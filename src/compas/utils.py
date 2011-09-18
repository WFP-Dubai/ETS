
from django.db import connections
from django.core.exceptions import ValidationError


def call_db_procedure(name, parameters, using):
    import cx_Oracle
    cursor = connections[using].cursor()
    Response_Message = cursor.var(cx_Oracle.STRING).var
    Response_Message.setvalue( 0, u' ' * 200 )
    print Response_Message.bufferSize
    Response_Code = cursor.var(cx_Oracle.STRING).var
    Response_Code.setvalue( 0, u'x' * 2 )
    print Response_Code.bufferSize
    print "parameters --> ", parameters
    cursor.callproc( name, (Response_Message, Response_Code)+parameters)
    
    if Response_Code.getvalue() != 'S':
        print "%s: %s " % (Response_Code.getvalue(), Response_Message.getvalue())
        raise ValidationError(Response_Message.getvalue(), code=Response_Code.getvalue())
