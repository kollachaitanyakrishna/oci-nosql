from borneo import DeleteRequest, MultiDeleteRequest, GetRequest, NoSQLHandle, NoSQLHandleConfig, Regions
from borneo.iam import SignatureProvider
from borneo import TableLimits, TableRequest, TableUsageRequest
from borneo import QueryRequest, PutRequest
from config import user, fingerprint, key_content, tenancy
import logging

# to-learn: https://blogs.oracle.com/nosql/post/oracle-nosql-database-cloud-service-10-minutes-to-hello-world-in-python
# cloud service and return it


def get_connection():
    region = Regions.US_ASHBURN_1
    at_provider = SignatureProvider(
        tenant_id=tenancy,
        user_id=user,
        private_key=key_content,
        fingerprint=fingerprint)
    
    config = NoSQLHandleConfig(
        region, at_provider).set_default_compartment("usagebilling")
    return(NoSQLHandle(config))


def nosql_getlist(query):
    handle = get_connection()
    list = []
    try:
        list_request = QueryRequest().set_statement(query)
        # loop until request is done, handling results as they arrive
        while True:
            list_result = handle.query(list_request)
            # handle results
            list.extend(list_result.get_results())
            if list_request.is_done():
                break
    except Exception as ex:
        print("error occured in method nosql_getlist")
        logging.error("error occcured in nosql_getlist. ", exc_info=True)
    finally:
        if handle is not None:
            handle.close()
    return list


def nosql_add_update_row(tablename, value):
    handle = get_connection()
    try:
        add_update_request = PutRequest().set_table_name(tablename)
        add_update_request.set_value(value)
        result = handle.put(add_update_request)
    except:
        print("error occured in method add_update_table")
        logging.error("error occcured in add_update_table. ", exc_info=True)
    finally:
        if handle is not None:
            handle.close()

    return result


def nosql_add_update_list(tablename, values):
    handle = get_connection()
    try:
        for eachValue in values:
            each_request = PutRequest().set_table_name(tablename)
            each_request.set_value(eachValue)
            result = handle.put(each_request)
    except:
        print("error occured in method add_update_list")
        logging.error("error occcured in add_update_list. ", exc_info=True)
    finally:
        if handle is not None:
            handle.close()


def nosql_delete_data(tablename, primarykey, querystatement):
    data_list = nosql_getlist(querystatement)
    handle = get_connection()
    try:
        for each_processed in data_list:
            deleteRequest = DeleteRequest().set_table_name(tablename)
            # set the value
            deleteRequest.set_key({primarykey: each_processed[primarykey]})
            deleteResult = handle.delete(deleteRequest)
    except:
        print("error occured in method delete_data")
        logging.error("error occcured in delete_data. ", exc_info=True)
    finally:
        if handle is not None:
            handle.close()


def nosql_set_ratelimit(tablename, wirtelimits, readlimits, disksize):
    handle = get_connection()
    try:
        # in this path the table name is required, as there is no DDL statement
        request = TableRequest().set_table_name(tablename)
        request.set_table_limits(TableLimits(
            readlimits, wirtelimits, disksize))
        result = handle.table_request(request)

        # table_request is asynchronous, so wait for the operation to complete, wait
        # for 400 seconds, polling every 3 seconds
        result.wait_for_completion(handle, 400000, 3000)
        logging.info("Rating limits for table: {table_name}, limits are {limits}".format(
            table_name=tablename, limits=request.get_table_limits()))
    except:
        print("error occured in method nosql_set_ratelimit")
        logging.error("error occcured in nosql_set_ratelimit. ", exc_info=True)
    finally:
        if handle is not None:
            handle.close()


def nosql_delete_list(tablename, primarykey, value):
    handle = get_connection()
    try:
        request = MultiDeleteRequest().set_table_name(tablename).set_key(
            {primarykey: value})
        result = handle.multi_delete(request)
        print('After multiple delete: ' + str(result))
    except:
        print("error occured in method nosql_delete_list")
        logging.error("error occcured in nosql_delete_list. ", exc_info=True)
    finally:
        if handle is not None:
            handle.close()
