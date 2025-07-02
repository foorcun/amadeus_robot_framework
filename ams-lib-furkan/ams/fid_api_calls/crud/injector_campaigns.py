"""Injector for FIDS campaigns keywords"""

# pylint: disable=line-too-long

from ams.fid_api_calls.crud.injector import (
    __base_get_data,
    __base_save_data,
    __base_delete_data,
    fids_get_home_airport,
)


CAMPAIGNS_FIELDS = [
    "fcnId",
    "fcnHomeAirport",
    "fcnName",
    "fcnDescription",
    "fcnOwner",
    "fcnTags",
    "fcnPriority",
    "fcnEffectiveStart",
    "fcnEffectiveEnd",
    "fcnTransitionEffect",
    "fcnTransitionDuration",
    "fcnUpdateTime",
    "fcnUpdateUser",
    "fcnCreateTime",
    "fcnCreateUser",
]
CAMPAIGNS_VIEW_NAME = "FidDelegateBean.Campaigns"


def fids_campaigns_get(session_key="defaultKey", **kwargs):
    """
    Get campaigns

    | *Arguments*      | *Description*                                                                 |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.       |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Campaigns

    """
    return __base_get_data(CAMPAIGNS_VIEW_NAME, CAMPAIGNS_FIELDS, session_key, **kwargs)


def fids_campaigns_save(
    name,
    priority=1,
    transition_effect="none",
    transition_duration=1,
    session_key="defaultKey",
    **kwargs,
):
    """
    Save a campaign entity.

    | *Arguments*             | *Description*                                                                      |
    | ``name``                | Campaign name.                                                                     |
    | ``priority``            | (Optional) Campaign priority. Default is 1.                                        |
    | ``transition_effect``   | (Optional) Transition effect. Default is "none".                                   |
    | ``transition_duration`` | (Optional) Transition duration. Default is 1.                                      |
    | ``session_key``         | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Save Campaign    name=MyCampaign    priority=2    transition_effect=fade    transition_duration=3

    """
    entity = {
        "fcnName": name,
        "fcnPriority": priority,
        "fcnTransitionEffect": transition_effect,
        "fcnTransitionDuration": transition_duration,
        "fcnHomeAirport": fids_get_home_airport(),
    }

    return __base_save_data(
        CAMPAIGNS_VIEW_NAME,
        CAMPAIGNS_FIELDS,
        entity,
        session_key,
        **kwargs,
    )


def fids_campaigns_delete(campaign, session_key="defaultKey", **kwargs):
    """
    Delete a campaign.

    | *Arguments*      | *Description*                                                                 |
    | ``campaign``     | Campaign entity dictionary. Must contain key ``fcnId``.                       |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Delete Campaign    campaign=${campaign}

    """
    entity = {"fcnId": campaign["fcnId"]}

    return __base_delete_data(
        CAMPAIGNS_VIEW_NAME, CAMPAIGNS_FIELDS, entity, session_key, **kwargs
    )


CAMPAIGNS_SCHEDULE_VIEW_NAME = "FidDelegateBean.CampaignSchedules"
CAMPAIGNS_SCHEDULE_FIELDS = [
    "fcsId",
    "fcsFcnId",
    "fcsEffectiveDays",
    "fcsEffectiveStartTime",
    "fcsEffectiveEndTime",
    "fcsUpdateTime",
    "fcsUpdateUser",
    "fcsCreateTime",
    "fcsCreateUser",
]


def fids_camapigns_schedules_save(
    campaign, effective_days, start_time, end_time, session_key="defaultKey", **kwargs
):
    """
    Add a schedule to the campaign.

    | *Arguments*         | *Description*                                                                      |
    | ``campaign``        | Campaign entity dictionary. Must contain key ``fcnId``.                            |
    | ``effective_days``  | String with the day numbers, e.g. "1234567" for every day.                         |
    | ``start_time``      | Start time as string, e.g. "00:00".                                                |
    | ``end_time``        | End time as string, e.g. "23:59".                                                  |
    | ``session_key``     | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Save Campaign Schedule    ${campaign}    effective_days=1234567    start_time=00:00    end_time=23:59

    """
    entity = {
        "fcsEffectiveDays": effective_days,
        "fcsEffectiveStartTime": start_time,
        "fcsEffectiveEndTime": end_time,
        "fcsFcnId": campaign["fcnId"],
    }

    # normally this is deleted in tests by deleting the campaign
    # but if caller wants this entity in the auto clean up can set skip_clean_up to false
    if "skip_clean_up" not in kwargs:
        kwargs["skip_clean_up"] = True

    return __base_save_data(
        CAMPAIGNS_SCHEDULE_VIEW_NAME,
        CAMPAIGNS_SCHEDULE_FIELDS,
        entity,
        session_key,
        **kwargs,
    )


CAMPAIGNS_MEDIA_VIEW_NAME = "FidDelegateBean.CampaignContents"
CAMPAIGNS_MEDIA_FIELDS = [
    "fccId",
    "fccFcnId",
    "fccFmeId",
    "fccDuration",
    "fccOrder",
    "fccUpdateTime",
    "fccUpdateUser",
    "fccCreateTime",
    "fccCreateUser",
    "fidMedia",
]


def fids_campaigns_media_save(
    campaign, media, duration=30, order=1, session_key="defaultKey", **kwargs
):
    """
    Add a media item to a campaign.

    | *Arguments*      | *Description*                                                                      |
    | ``campaign``     | Campaign entity dictionary. Must contain key ``fcnId``.                            |
    | ``media``        | Media entity dictionary. Must contain key ``fmeId``.                               |
    | ``duration``     | (Optional) Duration in seconds. Default is 30.                                     |
    | ``order``        | (Optional) Order of the media item. Default is 1.                                  |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Save Campaign Media    ${campaign}    ${media}    duration=30    order=1

    """
    entity = {
        "fccFmeId": media["fmeId"],
        "fccOrder": order,
        "fccDuration": duration,
        "fccFcnId": campaign["fcnId"],
    }

    # normally this is deleted in tests by deleting the campaign
    # but if caller wants this entity in the auto clean up can set skip_clean_up to false
    if "skip_clean_up" not in kwargs:
        kwargs["skip_clean_up"] = True

    return __base_save_data(
        CAMPAIGNS_MEDIA_VIEW_NAME, CAMPAIGNS_MEDIA_FIELDS, entity, session_key, **kwargs
    )
