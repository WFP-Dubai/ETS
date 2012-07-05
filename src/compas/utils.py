
from django.conf import settings
from django.db import connections
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode

COMPAS_ERRORS = {
    "ORA-20104": "QUANTITY NET EXCEEDS THE STORED QUANTITY",
    "ORA-20105": "QUANTITY GROSS EXCEEDS THE STORED QUANTITY",
}

def reduce_compas_errors(error_messages):
    errors = []
            
    if isinstance(error_messages, (str, unicode)):
        error_messages = [error_messages]
        
    for msg in error_messages:
        
        message = force_unicode(msg)
        #HACK to simplify error message
        for code, desc in COMPAS_ERRORS.items():
            if code in message:
                message = desc
                break
        
        errors.append(message)
    
    return errors

def call_db_procedure(name, parameters, using):
    
    connection = connections[using]
    
    if connection.vendor != 'oracle':
        return
    
    import cx_Oracle
    cursor = connection.cursor()
    
    cursor.execute("Set role epic_all identified by writeon;")
    
    Response_Message = cursor.var(cx_Oracle.STRING, 2000).var
    Response_Code = cursor.var(cx_Oracle.STRING, 1).var
    cursor.callproc( name, (Response_Message, Response_Code)+parameters)
    
    if Response_Code.getvalue() != 'S':
        errors = reduce_compas_errors(Response_Message.getvalue())

        raise ValidationError(errors, code=Response_Code.getvalue())

def get_version(using):
    connection = connections[using]
    
    if connection.vendor != 'oracle':
        return '1.3'
    
    import cx_Oracle
    cursor = connection.cursor()
    return cursor.callfunc("ets_compas.get_version", cx_Oracle.STRING)
