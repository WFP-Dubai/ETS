"""
Pretty important file since it contains code for preparing data for datatable (server-side mode).
Actually get_datatables_records is the function that does most of work.
DataTables' server-side processing for Django:
    http://www.datatables.net/development/server-side/django
Link for file:
    http://www.assembla.com/code/datatables_demo/subversion/nodes/trunk/1_6_2/datatables_demo/demo/utils.py?rev=5
"""


from django.db.models import Q
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers
from django.utils import simplejson

def get_sorted_columns(request, columnIndexNameMap):
    """Get ordered fields"""
    iSortingCols =  int(request.GET.get('iSortingCols',0))
    asortingCols = []

    if iSortingCols:
        for sortedColIndex in range(0, iSortingCols):
            sortedColID = int(request.GET.get('iSortCol_'+str(sortedColIndex),0))
            if request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':  # make sure the column is sortable first
                sortedColName = columnIndexNameMap[sortedColID]
                sortingDirection = request.GET.get('sSortDir_'+str(sortedColIndex), 'asc')
                if sortingDirection == 'desc':
                    sortedColName = '-'+sortedColName
                asortingCols.append(sortedColName)
    return asortingCols

def get_searchable_columns(request, columnIndexNameMap, cols):
    """Returns searchable columns"""
    searchableColumns = []
    for col in range(0,cols):
        if request.GET.get('bSearchable_{0}'.format(col), False) == 'true': searchableColumns.append(columnIndexNameMap[col])
    return searchableColumns

def get_search_filter(request, searchableColumns):
    """Apply filtering by value sent by user"""
    customSearch = request.GET.get('sSearch', '').encode('utf-8')
    outputQ = None
    if customSearch != '':
        for searchableColumn in searchableColumns:
            kwargz = {searchableColumn+"__icontains" : customSearch}
            outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)
    return outputQ


def get_datatables_records(request, querySet, columnIndexNameMap, aa_data=None, *args):
    """
    Usage: 
        querySet: query set to draw data from.
        columnIndexNameMap: field names in order to be displayed.
        jsonTemplatePath: optional template file to generate custom json from.  If not provided it will generate the data directly from the model.

    """
    cols = int(request.GET.get('iColumns',0)) # Get the number of columns
    iDisplayLength =  min(int(request.GET.get('iDisplayLength',10)),100)     #Safety measure. If someone messes with iDisplayLength manually, we clip it to the max value of 100.
    startRecord = int(request.GET.get('iDisplayStart',0)) # Where the data starts from (page)
    endRecord = startRecord + iDisplayLength  # where the data ends (end of page)

    # Pass sColumns
    keys = columnIndexNameMap.keys()
    keys.sort()
    colitems = [columnIndexNameMap[key] for key in keys]
    sColumns = ",".join(map(str,colitems))

    # Ordering data
    asortingCols = get_sorted_columns(request, columnIndexNameMap)
    if asortingCols:
        querySet = querySet.order_by(*asortingCols)
        
    # Determine which columns are searchable
    searchableColumns = get_searchable_columns(request, columnIndexNameMap, cols)

    # Apply filtering by value sent by user
    outputQ = get_search_filter(request, searchableColumns)
    if outputQ:
        querySet = querySet.filter(outputQ)

    # Individual column search 
    outputQ = None
    for col in range(0,cols):
        if request.GET.get('sSearch_{0}'.format(col), False) > '' and request.GET.get('bSearchable_{0}'.format(col), False) == 'true':
            kwargz = {columnIndexNameMap[col]+"__icontains" : request.GET['sSearch_{0}'.format(col)]}
            outputQ = outputQ & Q(**kwargz) if outputQ else Q(**kwargz)
    if outputQ: querySet = querySet.filter(outputQ)

    iTotalRecords = iTotalDisplayRecords = querySet.count() #count how many records match the final criteria
    querySet = querySet[startRecord:endRecord] #get the slice
    sEcho = int(request.GET.get('sEcho',0)) # required echo response
    
    aaData = []
    if not aa_data:
    
        a = querySet.values()
        for row in a:
            rowkeys = row.keys()
            rowvalues = row.values()
            rowlist = []
            for col in range(0,len(colitems)):
                for idx, val in enumerate(rowkeys):
                    if val == colitems[col]:
                        rowlist.append(str(rowvalues[idx]))
            aaData.append(rowlist)
    else:
        for item in querySet:
            aaData.append(aa_data(item))
        
    response_dict = {
        'aaData': aaData,
        'sEcho': sEcho, 
        'iTotalRecords': iTotalRecords, 
        'iTotalDisplayRecords':iTotalDisplayRecords, 
        'sColumns':sColumns
    }
    
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

    #prevent from caching datatables result
    add_never_cache_headers(response)
    return response
