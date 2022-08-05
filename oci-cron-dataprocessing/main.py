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
# refresh_rate_card(config_demo_signer["tenancy"], isDelete = False)
def refresh_rate_card(is_delete = False):
    oci_config = {
        "user": user,
        "fingerprint": fingerprint,
        "tenancy": tenancy,
        "region": region,
        "key_content": key_content
    }

    print(oci_config)
    set_ratecard_limits()
    if(is_delete == True):
        delete_ratecard(tenancy)
    pull_ratecard(config=oci_config, subscription_id=subscription_id, tenant_id=tenancy)
    revert_ratecard_limits()

refresh_rate_card()