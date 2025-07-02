"""Injector rules for FIDS display and selection rule keywords"""

from ams.fid_api_calls.crud.injector import __base_get_data

# pylint: disable=line-too-long

DISPLAY_RULES_VIEW_NAME_SCREEN = "RefDelegateBean.RulesWithLayoutRef"
DISPLAY_RULES_FIELDS_SCREEN = [
    "fdrId",
    "fdrRemark",
    "fdrType",
    "fdrName",
    "fdrOobInd",
    "fdrCreateTime",
    "fdrCreateUser",
    "fdrUpdateTime",
    "fdrUpdateUser",
    "layoutCount",
]


def fids_display_rules_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS display rules.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Display Rules

    """
    kwargs["where"] = "([fdrType@@][EQ]['D'])"
    return __base_get_data(
        DISPLAY_RULES_VIEW_NAME_SCREEN,
        DISPLAY_RULES_FIELDS_SCREEN,
        session_key,
        **kwargs,
    )


SELECTION_RULES_VIEW_NAME_SCREEN = "RefDelegateBean.RulesWithLayoutRef"
SELECTION_RULES_FIELDS_SCREEN = [
    "fdrId",
    "fdrRemark",
    "fdrType",
    "fdrName",
    "fdrOobInd",
    "fdrCreateTime",
    "fdrCreateUser",
    "fdrUpdateTime",
    "fdrUpdateUser",
    "layoutCount",
]


def fids_selection_rules_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS selection rules.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Selection Rules

    """
    kwargs["where"] = "([fdrType@@][EQ]['S'])"
    return __base_get_data(
        SELECTION_RULES_VIEW_NAME_SCREEN,
        SELECTION_RULES_FIELDS_SCREEN,
        session_key,
        **kwargs,
    )


SELECTION_RULES_VIEW_NAME = "RefDelegateBean.Rules"
SELECTION_RULES_FIELDS = [
    "fdrId",
    "fdrRemark",
    "fdrType",
    "fdrName",
    "fdrOobInd",
    "fdrCreateTime",
    "fdrCreateUser",
    "fdrUpdateTime",
    "fdrUpdateUser",
    "fdrRule",
    "fdrClearRule",
]


def fids_selection_rule_get_by_name(name, session_key="defaultKey", **kwargs):
    """
    Get a FIDS selection rule by name.

    | *Arguments*      | *Description*                                                                |
    | ``name``         | Name of the selection rule.                                                  |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Selection Rule By Name    MyRule

    """
    kwargs["where"] = f"([fdrType@@][EQ]['S']) AND ([fdrName@@][EQ]['{name}'])"
    return __base_get_data(
        SELECTION_RULES_VIEW_NAME, SELECTION_RULES_FIELDS, session_key, **kwargs
    )
