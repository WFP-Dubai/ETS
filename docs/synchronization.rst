.. sync_procedure:

**********************
Synchronization procedure
**********************

Here is a quick and dirty guide, that will help you to understand sync workflow.


.. _dependencies:

Client
============

All methods are supposed to exec asynchronously depend on status.
There are couple of statuses:

  - new - waybill created
  - signed - validated by authorized person
  - sent - sent to central server
  - informed - received by recipient
  - delivered - food delivered
  - complete - delivered waybill synchronized with central server

Workflow:
Waybill is created. status is NEW. We do nothing.
Auth. person signs the waybill. status becomes SIGNED. System exec. send_new method. Status becomes SENT
Meanwhile recipient asks central server about new waybill going to its warehouse. Method get_receiving.
Recipient sends signal, that he received a waybill. method send_informed. status becomes INFORMED
Meanwhile dispatcher asks the server about informed waybill. Method get_informed. status of dispatched waybill becomes INFORMED
When recipient receives a food and fills, validates waybill, status becomes DELIVERED. 
Method send_delivered ends updated waybill back to dispatcher through the server (method get_delivered). status of received waybill becomes DELIVERED to prevent further sync actions.