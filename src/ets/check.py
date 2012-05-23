from datetime import datetime, timedelta

def is_imported(obj):
    if obj._meta.object_name in ("Waybill", "WaybillAuditLogEntry"):
        waybill = obj
    elif obj._meta.object_name in ("LoadingDetail", "LoadingDetailAuditLogEntry"):
        waybill = obj.waybill
    else:
        return False
    print "date modified: %s" % waybill.date_modified.isoformat(" ")
    print "now - 20 sec: %s" % datetime.now().isoformat(" ")
    if waybill.date_modified < datetime.now() - timedelta(seconds=20):
        return True
    return False
