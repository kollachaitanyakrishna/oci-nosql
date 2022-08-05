from hmac import compare_digest
from pickle import FALSE, TRUE
from datetime import date, datetime, timedelta, timezone

# use for the imports api
import oci
import oci.usage_api.models
from oci.usage_api.models import (Dimension, Filter,
                                  RequestSummarizedUsagesDetails)
import logging
from nosql import nosql_getlist, nosql_delete_data, nosql_set_ratelimit, nosql_add_update_list


def pull_ratecard(config, subscription_id, tenant_id):
    osub_subscription_client = oci.osub_subscription.RatecardClient(config)
    list_rate_cards_response = osub_subscription_client.list_rate_cards(
        subscription_id=subscription_id,
        compartment_id=tenant_id)
    logging.info("Got the list of rate card items for tenant: {tenantid}".format(
        tenantid=tenant_id))
    list_rate_cards = []
    for row in list_rate_cards_response.data:
        if(len(row.rate_card_tiers) > 0):
            for each_rate_card_tier in row.rate_card_tiers:
                queryMultiple = "select tenant_id from oci_client_reatecard where up_to_quantity={up_to_quantity} and time_start = '{time_start}' and time_end = '{time_end}' and subscription_id='{subscription_id}' and tenant_id='{tenant_id}' and product_part_number='{product_part_number}'".format(
                    tenant_id=tenant_id,
                    subscription_id=subscription_id,
                    product_part_number=row.product.part_number,
                    time_end=row.time_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    time_start=row.time_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    up_to_quantity=each_rate_card_tier.up_to_quantity)

                # Get the data from response
                if(len(nosql_getlist(query=queryMultiple)) == 0):
                    value = {
                        "subscription_id": subscription_id,
                        "tenant_id": tenant_id,
                        "currency_iso_code": row.currency.iso_code,
                        "currency_name": row.currency.name,
                        "currency_std_precision": row.currency.std_precision,
                        "discretionary_discount_percentage": row.discretionary_discount_percentage,
                        "net_unit_price": float(each_rate_card_tier.net_unit_price),
                        "overage_price": float(each_rate_card_tier.overage_price),
                        "product_billing_category": row.product.billing_category,
                        "product_name": row.product.name,
                        "product_part_number": row.product.part_number,
                        "product_product_category": row.product.product_category,
                        "product_ucm_rate_card_part_type": row.product.ucm_rate_card_part_type,
                        "product_unit_of_measure": row.product.unit_of_measure,
                        "time_end": row.time_end,
                        "time_start": row.time_start,
                        "is_active": True if(row.time_start <= datetime.now(timezone.utc) <= row.time_end) else False,
                        "up_to_quantity": int(each_rate_card_tier.up_to_quantity),
                        "last_executed_time": datetime.now(timezone.utc)
                    }
                    list_rate_cards.append(value)
                    # nosql_add_update_row("oci_client_reatecard", value)
                else:
                    print("not inserted multiple")
        else:
            # print(row.time_end.strftime("%Y-%m-%dT%H:%M:%SZ"))
            query = "select tenant_id from oci_client_reatecard where time_start = '{time_start}' and time_end = '{time_end}' and subscription_id='{subscription_id}' and tenant_id='{tenant_id}' and product_part_number='{product_part_number}'".format(
                tenant_id=tenant_id,
                subscription_id=subscription_id,
                product_part_number=row.product.part_number,
                time_end=row.time_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                time_start=row.time_start.strftime("%Y-%m-%dT%H:%M:%SZ"))

            # Get the data from response
            if(len(nosql_getlist(query=query)) == 0):
                value = {
                    "subscription_id": subscription_id,
                    "tenant_id": tenant_id,
                    "currency_iso_code": row.currency.iso_code,
                    "currency_name": row.currency.name,
                    "currency_std_precision": row.currency.std_precision,
                    "discretionary_discount_percentage": row.discretionary_discount_percentage,
                    "net_unit_price": float(row.net_unit_price),
                    "overage_price": float(row.overage_price),
                    "product_billing_category": row.product.billing_category,
                    "product_name": row.product.name,
                    "product_part_number": row.product.part_number,
                    "product_product_category": row.product.product_category,
                    "product_ucm_rate_card_part_type": row.product.ucm_rate_card_part_type,
                    "product_unit_of_measure": row.product.unit_of_measure,
                    "time_end": row.time_end,
                    "time_start": row.time_start,
                    "is_active": True if(row.time_start <= datetime.now(timezone.utc) <= row.time_end) else False,
                    # "up_to_quantity": None,
                    "last_executed_time": datetime.now(timezone.utc)
                }
                list_rate_cards.append(value)
                # nosql_add_update_row("oci_client_reatecard", value)
            else:
                print("not inserted single")
    nosql_add_update_list("oci_client_reatecard", list_rate_cards)


def delete_ratecard(tenant_id):
    query = "select id from oci_client_reatecard where tenant_id='{tenantid}'".format(
        tenantid=tenant_id)
    print(query)
    nosql_delete_data("oci_client_reatecard", "id", query)


def set_ratecard_limits():
    nosql_set_ratelimit(tablename="oci_client_reatecard",
                        wirtelimits=200, readlimits=200, disksize=5)


def revert_ratecard_limits():
    nosql_set_ratelimit(tablename="oci_client_reatecard",
                        wirtelimits=1, readlimits=200, disksize=5)