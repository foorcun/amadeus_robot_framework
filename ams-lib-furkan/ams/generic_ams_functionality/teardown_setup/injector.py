"""This injector module houses all functions for teardown setup"""

import logging
from protocols import session_manager
from ams.frms_api_calls.injector_plan import frms_delete_plans
from ams.frms_api_calls.injector_rule import frms_delete_rules
from ams.fid_api_calls.crud.injector import __base_delete_data
from ams.mdm_api_calls.sds.injector import sds_delete
from ams.vip_api_calls.leg_periods.delete_leg_period.injector import delete_leg_period
from ams.cds_api_calls.injector import cds_v1_delete_rule
from ams.vip_api_calls.leg_periods.delete_leg_period.responses import (
    validate_delete_leg_period_general_processing,
)
from ams.fom_api_calls.movement_partial_v3.delete_flight.injector import (
    fom_v3_movements_delete,
)


LOGGER = logging.getLogger(__name__)


def automatic_data_cleanup():

    LOGGER.info(
        "============================== Automatic data cleanup =============================="
    )
    # pylint: disable = protected-access
    context_data = session_manager.sessions._get_session_context_data()
    data_to_clean_up = context_data["test_context"]["data_to_clean_up"]

    for entity_type, ids in data_to_clean_up.items():
        try:
            LOGGER.info("Automatic data cleanup - %s: %s", entity_type, ids)
            if entity_type == "movement":
                fom_cleanup_movements(ids)
            elif entity_type == "leg_period":
                vip_cleanup_leg_periods(ids)
            elif entity_type == "bre_rule":
                cds_cleanup_rules(ids)
            elif entity_type == "frms_plan":
                frms_delete_plans(ids)
            elif entity_type == "frms_rule":
                frms_delete_rules(ids)
            elif entity_type == "fids":
                fids_cleanup_entities(ids)
            else:
                for item_id in ids:
                    sds_delete(entity_type, item_id)
        except Exception as e:
            LOGGER.warning("Automatic data cleanup - Failed for %s: %s", entity_type, e)


def fom_cleanup_movements(movement_ids):
    """
    Deletes all the movement data in Operations.

    == Return value ==
    | None

    == Usage ==
    | fom_cleanup_movements    ["C_CPA_1400__20250424_ARRIVAL_XYZA"]

    """
    for movement_id in movement_ids:
        try:
            fom_v3_movements_delete(movement_id)
        except Exception as e:
            LOGGER.warning(
                "Automatic data cleanup - Failed for movement %s: %s", movement_id, e
            )


def vip_cleanup_leg_period(leg_period_id):
    vip_cleanup_leg_periods([leg_period_id])


def vip_cleanup_leg_periods(leg_period_ids):
    """
    Deletes all the flight data in Planning.

    == Return value ==
    | None

    == Usage ==
    | vip_cleanup_leg_periods    [leg_period_id]
    """
    for leg_period_id in leg_period_ids:
        try:
            response = delete_leg_period(leg_period_id)
            validate_delete_leg_period_general_processing(response)
        except Exception as e:
            LOGGER.warning(
                "Automatic data cleanup - Failed for leg period %s: %s",
                leg_period_id,
                e,
            )


def cds_cleanup_rules(rule_ids):
    """
    Deletes all BRE rules.

    == Return value ==
    | None

    == Usage ==
    | cds_cleanup_rules    [rule_id]
    """
    for rule_id in rule_ids:
        try:
            cds_v1_delete_rule(rule_id)
        except Exception as e:
            LOGGER.warning(
                "Automatic data cleanup - Failed for BRE rule %s: %s",
                rule_id,
                e,
            )


def fids_cleanup_entities(entities):
    """Cleans up fids entities"""
    for item in entities:
        try:
            __base_delete_data(
                item["view"], item["fields"], item["entity"], skip_clean_up=True
            )
        except Exception as e:
            # ignore errors here so it goes through all of the list
            LOGGER.error(
                "Failed to clean up FIDS entity %s %s: %s",
                item["view"],
                item["entity"],
                str(e),
            )
        else:
            LOGGER.info("Successfully cleaned up FIDS entity %s", item["entity"])
