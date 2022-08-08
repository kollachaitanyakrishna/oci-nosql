from distutils.command.config import config
from tokenize import single_quoted

from ratecard import delete_ratecard, set_ratecard_limits, revert_ratecard_limits, pull_ratecard
from config import user, fingerprint, region, key_content, tenancy, subscription_id
from oci.identity import IdentityClient
import oci.usage_api.models
import oci
import logging

logging.basicConfig(format = '%(asctime)s %(message)s')
logger = logging.getLogger("billing")
logger.setLevel(logging.DEBUG)

logging.getLogger('oci').setLevel(logging.DEBUG)


# Used for the ratecard calculations.
# isDelete = False, Pass True to delete the old data and insert the new data
# Step1: Fill the details of config.py
def refresh_rate_card(is_delete = False):
    oci_config = {
        "user": user,
        "fingerprint": fingerprint,
        "tenancy": tenancy,
        "region": region,
        "key_content": key_content
    }

    print(oci_config)
    # Step 2: Set the read write limits.
    set_ratecard_limits()
    if(is_delete == True):
        delete_ratecard(tenancy)
    
    # Step 3: Pull the rate card and insert the data to nosql table
    pull_ratecard(config=oci_config, subscription_id=subscription_id, tenant_id=tenancy)

    # Step 4: Revert the rate card read and write limits.
    revert_ratecard_limits()

refresh_rate_card()