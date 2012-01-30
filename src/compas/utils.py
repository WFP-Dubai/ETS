
from django.db import connections
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode

QUANTITY_EXCEEDS = "QUANTITY NET EXCEEDS THE STORED QUANTITY"

try:
    import cx_Oracle
    
    def call_db_procedure(name, parameters, using):
    
        cursor = connections[using].cursor()
        
        cursor.execute("Set role epic_all identified by writeon;")
        
        Response_Message = cursor.var(cx_Oracle.STRING, 2000).var
        Response_Code = cursor.var(cx_Oracle.STRING, 1).var
        cursor.callproc( name, (Response_Message, Response_Code)+parameters)
        
        if Response_Code.getvalue() != 'S':
            errors = []
            
            for msg in Response_Message.getvalue():
                
                #HACK to simplify error message
                if QUANTITY_EXCEEDS in msg:
                    msg = QUANTITY_EXCEEDS
                
                errors.append(msg)
            
            raise ValidationError(errors, code=Response_Code.getvalue())

except ImportError:
    
    def call_db_procedure(name, parameters, using):
        pass
