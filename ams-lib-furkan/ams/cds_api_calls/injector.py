"""Injector module to handle GET http calls from CDS"""

import logging
from ams.data_model.common_libs.injectors.injector import _http_call
from ams.data_model.common_libs.utils.generic_helpers import add_data_to_clean_up
from ams.data_model.common_libs.request_response_handler.request_generator import (
    PayloadGenerator,
)

LOGGER = logging.getLogger(__name__)

# pylint: disable=line-too-long, protected-access


def cds_v1_get_rule_template_by_id(template_id="TEST"):
    """
    Executes a HTTP GET call to retrieve CDS v1 rule template by id.

    This function calls the endpoint /cds/services/v1/rule-template/{id}.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | ``template_id``                  | The template Id.                                                |

    === Usage: ===
    | ${response}    Cds V1 Get Rule Template By Id

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rule-template/{id}"

    kwargs = {"path_params": {"id": template_id}}

    return _http_call(cds_endpoint, **kwargs)


def cds_v1_get_rule_templates():
    """
    Executes a HTTP GET call to retrieve CDS v1 rule templates.

    This function calls the endpoint /cds/services/v1/rule-templates.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Cds V1 Get Rule Templates

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rule-templates"

    kwargs = {}

    return _http_call(cds_endpoint, **kwargs)


def cds_v1_get_rule_by_id(rule_id="TEST"):
    """
    Executes a HTTP GET call to retrieve CDS v1 rule by id.

    This function calls the endpoint /cds/services/v1/rule/{id}.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | ``rule_id``                      | The rule id.                                                    |

    === Usage: ===
    | ${response}    Cds V1 Get Rule By Id

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rule/{id}"

    kwargs = {"path_params": {"id": rule_id}}

    response_json = _http_call(cds_endpoint, **kwargs)
    return response_json


def cds_v1_get_rules():
    """
    Executes a HTTP GET call to retrieve CDS v1 rules.

    This function calls the endpoint /cds/services/v1/rules.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Cds V1 Get Rules

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rules"

    kwargs = {}

    return _http_call(cds_endpoint, **kwargs)


def cds_v1_get_rules_for_template(template_id="TEST"):
    """
    Executes a HTTP GET call to retrieve CDS v1 rules for template.

    This function calls the endpoint /cds/services/v1/rules/{template_id}.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | ``template_id``                  | The template Id.                                                |

    === Usage: ===
    | ${response}    Cds V1 Get Rules For Template

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rules/{template_id}"

    kwargs = {
        "path_params": {"template_id": template_id},
    }

    return _http_call(cds_endpoint, **kwargs)


def cds_v1_get_rule_group_by_id(group_id="TEST"):
    """
    Executes a HTTP GET call to retrieve CDS v1 rule group by id.

    This function calls the endpoint /cds/services/v1/rule-group/{id}.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | ``group_id``                     | The group Id.                                               |

    === Usage: ===
    | ${response}    Cds V1 Get Rule Group By Id

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rule-group/{id}"

    kwargs = {"path_params": {"id": group_id}}

    return _http_call(cds_endpoint, **kwargs)


def cds_v1_get_rule_groups():
    """
    Executes a HTTP GET call to retrieve CDS v1 rule groups.

    This function calls the endpoint /cds/services/v1/rule-groups.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Cds V1 Get Rule Groups

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rule-groups"

    kwargs = {}

    return _http_call(cds_endpoint, **kwargs)


def cds_v1_get_rule_groups_for_template(template_id="TEST"):
    """
    Executes a HTTP GET call to retrieve CDS v1 rule groups for template.

    This function calls the endpoint /cds/services/v1/rule-groups/{template_id}.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | ``template_id``                  | The template Id.                                                |

    === Usage: ===
    | ${response}    Cds V1 Get Rule Groups For Template

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rule-groups/{template_id}"

    kwargs = {
        "path_params": {"template_id": template_id},
    }

    return _http_call(cds_endpoint, **kwargs)


def cds_v1_get_tags():
    """
    Executes a HTTP GET call to retrieve CDS v1 tags.

    This function calls the endpoint /cds/services/v1/rules/tags.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Cds V1 Get Tags

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rules/tags"

    kwargs = {}

    return _http_call(cds_endpoint, **kwargs)


def cds_v1_get_tags_for_template(template_id="TEST"):
    """
    Executes a HTTP GET call to retrieve CDS v1 tags for template.

    This function calls the endpoint /cds/services/v1/rules/tags/{template_id}.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | ``template_id``                  | The template Id.                                                |

    === Usage: ===
    | ${response}    Cds V1 Get Tags For Template

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rules/tags/{template_id}"

    kwargs = {
        "path_params": {"template_id": template_id},
    }

    return _http_call(cds_endpoint, **kwargs)


def cds_v1_get_statistics(
    template_id="TEST", nb_minutes_backwards="10", types="PER_TEMPLATE"
):
    """
    Executes a HTTP GET call to retrieve CDS v1 statistics.

    This function calls the endpoint /cds/services/v1/statistics.
    The function returns the JSON response from the API.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | ``template_id``                  | The template Id.                                                |
    | ``nb_minutes_backwards``         | The number of minutes from now to look back.                    |
    | ``types``                        | The statistics types.                                           |

    === Usage: ===
    | ${response}    Cds V1 Get Statistics

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/statistics"

    kwargs = {
        "query_params": {
            "templateUuid": template_id,
            "nbMinutesBackwards": nb_minutes_backwards,
            "types": types,
        },
    }

    return _http_call(cds_endpoint, **kwargs)


def cds_v1_create_rule():
    """
    Creates a CDS v1 rule using the first available 'Operations' rule template's UUID.

    This function calls cds_v1_get_rule_templates to get the list of templates,
    uses the first template's uuid as the ruleTemplateUuid, and posts the rule.
    If no templates are found, the process is aborted.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | None                             | This function takes no arguments.                               |

    === Usage: ===
    | ${response}    Cds V1 Create Rule

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If no rule templates are found, or if the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rule"

    # Get the rule templates and find the first with product == "Operations"
    templates_response = cds_v1_get_rule_templates()
    templates = (
        templates_response
        if isinstance(templates_response, list)
        else templates_response.get("content", [])
    )

    template = next((t for t in templates if t.get("product") == "Operations"), None)

    if not template:
        raise ValueError(
            'No rule template with product "Operations" found. Cannot create rule.'
        )

    template_uuid = template.get("uuid")
    if not template_uuid:
        raise ValueError(
            "Selected rule template does not have a uuid. Cannot create rule."
        )

    LOGGER.info("Creating rule for template: %s", template_uuid)

    data = {"ruleTemplateUuid": template_uuid}

    gen_payload = PayloadGenerator(data, "payloads/rule.jinja", __file__)
    entity = gen_payload.construct_generic_payload()

    kwargs = {"operation": "POST", "payload": entity}

    response = _http_call(cds_endpoint, **kwargs)

    LOGGER.info("Rule created for template: %s, response: %s", template_uuid, response)

    add_data_to_clean_up("bre_rule", response)

    return response


def cds_v1_delete_rule(rule):
    """
    Executes a HTTP DELETE call to remove a CDS v1 rule.

    This function calls the endpoint /cds/services/v1/rule-batch using the provided rule's UUID and ruleTemplateUuid.
    The function generates the payload using the a template and sends the request.

    | *Arguments*                      | *Description*                                                   |
    |----------------------------------|-----------------------------------------------------------------|
    | ``rule``                         | A dictionary containing at least "uuid" and "ruleTemplateUuid" for the rule to delete. |

    === Usage: ===
    | ${response}    Cds V1 Delete Rule    ${rule}

    === Returns: ===
    | dict or None | The JSON response from the API if the call is successful, or None if the response status code is 204 (No Content).

    === Raises: ===
    | ValueError | If the response status code is not 200 or 204.
    """
    cds_endpoint = "/cds/services/v1/rule-batch"

    data = {"ruleTemplateUuid": rule["ruleTemplateUuid"], "ruleUuid": rule["uuid"]}

    gen_payload = PayloadGenerator(data, "payloads/delete_rule.jinja", __file__)
    entity = gen_payload.construct_generic_payload()

    kwargs = {"operation": "DELETE", "payload": entity}

    response = _http_call(cds_endpoint, **kwargs)

    LOGGER.info(
        "Deleted rule: %s, from template: %s", rule["uuid"], rule["ruleTemplateUuid"]
    )

    return response
