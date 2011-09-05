import zlib, base64, string

#from ets import models as ets_models


def viewLog(logfile = 'logg.txt'):
    try:
        with open( logfile, "r" ) as f:
            return f.read()
    except IOError, msg:
        return msg


#=======================================================================================================================
# def un64unZip(data):
#    """
#    Unzip data
#    
#    >>> data = "eJztWG1zokgQ/iuUn7MpQI1mv6GgUlFxgWySulxRExh1LgjuMG4udbX//RpmhAExuW9XV2fKygvd0zz99NM9M+n89tdzZ//63PmqaFfKc2eXRjjO/3ruYJZdv6H3FxLDg9y2JjiOstwIa4Rledi9YMoXGKqq3nJXRlGS7VPKvuMtCWPs4g3J4CEjacKdG37jNIHfQ5aKWDNjYTw5zlIxlqYydrh3RLI9YuHWxTtEXzM5UIQYdtamcOAWXdW0L+rNF03nPhSHZE9wwgxKyU8Um7Am90wOcVyzA5iMJBuMeZwHx52bysRxTGXlOlPXWCysBnzv8NLMoOFh4pj8xPTdI5sERz7Z4Yyh3b71/ZAGQ0nYDm6Jdlh+AzpEBBDvdmDjz1eUJEw5cqE4lGxIguI6h5hyJPkSRg84t4marmga4izD0SSlK/R+DLxGcYZrUD7IpXqNT1gsAM+dqe359thTnMnEHlsuhxQCc4gk4PqWehjVNPUhizVUchQhEBeA4j2TI8WMyOG/GctHVdXyj6YPdf1m1YDkJPh8sApWnm24beFDVqGidb9q+tdeV1oNgoGW8N/3R63ZPreSBBRKcll/mmZd9Q2ttzDVDlsWAu+meYoiaINPmslKIogTbhHd4LMd1dKxQmweWP0U9LtH2RmVMVRAbX9FS6Xa+JDd2jUm8HxvZb2krKqUKoiIoNjQXnkZHxDF2/SQCQ/HGuTiavA1T0NpDHr3d3eze7cGAZR2lpWqdjRvhOYwqNqustjeCGDoMJzV/vCmqdwizJyEGOaNbZ6j7JSuMh+pv0/b+SzNkCMme/YZ2xSRGNO23ePXryvlw60r5uqNMIBp28CSAtp9Qlg2TdNIFJU7HvKnJtqhDbSzqPhRcIVtnmagaZRxPEeTFDJ3qIV8e6m4KOCmwHuOEUfFghoBtUC5Cw/V56FSGmEaEIZ3ZTAZ8CmuEnIzF8GRWXB0VnM5Ume9zp0/hCreX6ZdK5H+/yiRpv6HayTth/JXX9cGs2/wvG64Hfa0nphuzcJCp9ZOHbWyclMQi0EYhLBYvN7UH/mCjAQwYYDFgAiwnyCoggZJOfogHdOYGeU5I8KNNBvbvjTLW+HBMu7444ASRth7kGChIe160C/nX4ZhR8XSStOxjElj6YamWVYuvtGPq3dAZm6vVi+8sWfMWyG2JKuMbf/pOKR/HMAfR8FxYwgisX8WO7r6Jd/Uu409QYqpLO69ub1QfNdYeivH9avmC94w2WxZxUBfbcZJD6G8BdUr9bYNmgXRyzNaWfWzguSuXNlBug4OR9U/d7r9U5QS2X31ututyA6gzHiT0gbhTaynPAcPM+6E/9wTWH7KrNbjDnua/oFDwPKSBTjG1Uk935RvuteCmHC3q95iO6btWaYChfcrWlqqpzdVV8UwrZXh+gtr6cOBW7HM+7Hh2/mdajKdGUs4ihtLOU0GkycAfYmiSaeZelklnppFZeXxSC/7uHIf6rddOIh0L2PnMnYuY+cydv7tsXNnuI+q3i9+8GLf9npDVVvYj/CZWaPxVOuXd6bGsMF7EmYsDV9bRs0/GyO3/cHt8Hx3qtdw5S7NMVhzksRlip+HT1I95nBuXOQxa8wd8Z1wII7EcrcIuoS4UPgKJ8mq6mOoubO8Uib2yLVGjuGaVwrEUx6L71N3oYyM6Sf6tx+l1x4SRt+5YWXcSbIBa1y7RAMwYzyzj8NnjWl+mw0S6fKpqkNIbaCqvTIGhVtlWmwVxWV9MapxXaGaliuqZO/ssf/B4CzEU+NJsuaiEv+6i1umfam3liGjfdbW2mDQ2tYzezpTrKXlTp+Uke2N723fu7TDpR0u7VBrh987fwMaNdo5"
#    >>> un64unZip(data)
#    asdfa
#    """
#    
#    data = string.replace( data, ' ', '+' )
#    try:
#        return zlib.decompress( base64.b64decode( data ) )
#    except (zlib.error, TypeError):
#        pass
#=======================================================================================================================


#=======================================================================================================================
# def default_json_dump(obj):
#    if hasattr(obj, 'isoformat'):
#        return obj.isoformat()
# #    elif isinstance(obj, ...):
# #        return ...
#    else:
#        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))
#=======================================================================================================================
