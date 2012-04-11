
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
try:
    import cx_Oracle
except ImportError:
    pass
def get_version(using):
    cursor = connections[using].cursor()
    ret = cursor.callfunc("ets_compas.get_version", cx_Oracle.STRING)
    cursor.close()
    return ret



try:
    import cx_Oracle
    
    def call_db_procedure(name, parameters, using):
    
        cursor = connections[using].cursor()
        
        cursor.execute("Set role epic_all identified by writeon;")
        
        Response_Message = cursor.var(cx_Oracle.STRING, 2000).var
        Response_Code = cursor.var(cx_Oracle.STRING, 1).var
        cursor.callproc( name, (Response_Message, Response_Code)+parameters)
        
        if Response_Code.getvalue() != 'S':
            errors = reduce_compas_errors(Response_Message.getvalue())

            raise ValidationError(errors, code=Response_Code.getvalue())
    
except ImportError:
    
    def call_db_procedure(name, parameters, using):
        pass
