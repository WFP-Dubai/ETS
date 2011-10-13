
#=======================================================================================================================
# # TODO: get old wb for current ltis.... (filter local)
# def get_old_waybills():
#    all_ltis = LtiOriginal.objects.all()
# #    all_items = DispatchMaster.objects.using( 'compas' ).filter( dispatch_date__gt = '2011-01-01' ).filter( document_code = 'WB' ).filter( offid = 'ISBX002' )
#    for lti in all_ltis:
#        all_items = DispatchMaster.objects.using( 'compas' ).filter( lti_id = lti.lti_id )
#        for master in all_items:
#            waybill_id = master.code[9:-1]
#            try:
#                Waybill.objects.get( waybillNumber = waybill_id )
#            except:
#            #check if save & get DispatchDetails
#            #dispatch_details.code like 'ISBX002%' and dispatch_date > '01-FEB-2011' and dispatch_date < '17-FEB-2011'
#                try:
#                    DispatchMaster.objects.get( code = master.code )
#                except:
#                    master.save( using = 'default' )
#                    cursor = connections['compas'].cursor()
#                    all_lines = cursor.execute( 'select * from dispatch_details where code = %s', [master.code] )
#                    for line in all_lines:
#                        print line
#                        myline = DispatchDetail()
#                        myline.code = master
#                        myline.document_code = line[1]
#                        myline.si_record_id = line[2]
#                        myline.origin_id = line[3]
#                        myline.comm_category_code = line[4]
#                        myline.commodity_code = line[5]
#                        myline.package_code = line[6]
#                        myline.allocation_destination_code = line[7]
#                        myline.quality = line[8]
#                        myline.quantity_net = line[9]
#                        myline.quantity_gross = line[10]
#                        myline.number_of_units = line[11]
#                        myline.unit_weight_net = line[12]
#                        myline.unit_weight_gross = line[13]
#                        myline.save()
#=======================================================================================================================
