"""Injector for FIDS media keywords"""

import os
import protocols.broker
from ams.fid_api_calls.crud.injector import (
    __add_to_automatic_clean_up,
    __base_get_data,
    __base_save_data,
    __base_delete_data,
    rest_injector,
)

# pylint: disable=line-too-long

MEDIA_VIEW_NAME = "FidDelegateBean.Media"
MEDIA_DELETED_VIEW_NAME = "FidDelegateBean.DeletedMedia"
MEDIA_EXTERNAL_VIEW_NAME = "FidDelegateBean.DeletedMedia"
MEDIA_EXTERNAL_DELETED_VIEW_NAME = "FidDelegateBean.DeletedMedia"
MEDIA_FIELDS = [
    "fmeId",
    "fmeHomeAirport",
    "fmeTags",
    "fmeName",
    "fmeMetadata",
    "fmeSize",
    "fmeDimensions",
    "fmeEffectiveDate",
    "fmeDiscontinueDate",
    "fmeFileName",
    "fmeCreateTime",
    "fmeCreateUser",
    "fmeUpdateTime",
    "fmeUpdateUser",
    "fmeDeletedInd",
    "fmeDuration",
    "fmeOwner",
    "fmeRefreshInterval",
    "fmeRefreshUnit",
    "fmeExternalInd",
    "fmeExternalUrl",
]


def fids_media_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS media.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used.      |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Media

    """
    return __base_get_data(MEDIA_VIEW_NAME, MEDIA_FIELDS, session_key, **kwargs)


def fids_media_upload(
    file_path, file_name, content_type, session_key="defaultKey", **kwargs
):
    """
    Upload a media file.

    | *Arguments*      | *Description*                                                                |
    | ``file_path``    | Path to the directory containing the file.                                   |
    | ``file_name``    | Name of the file to upload.                                                  |
    | ``content_type`` | MIME type of the file.                                                       |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Upload FIDS Media    file_path=media    file_name=image.png    content_type=image/png

    """
    kwargs["endpoint_type"] = "media_upload"

    # read file
    full_path = os.getcwd() + os.sep + file_path + os.sep + file_name
    print(f"Loading file for media save from {full_path}")
    file = open(full_path, "rb")
    kwargs["payload"] = file.read()
    file.close()

    kwargs["file_name"] = file_name
    kwargs["content_type"] = content_type

    response = protocols.broker.injector(kwargs, session_key, rest_injector)
    kwargs["view"] = MEDIA_VIEW_NAME
    kwargs["fields"] = MEDIA_FIELDS
    __add_to_automatic_clean_up(response, **kwargs)
    return response


def fids_media_save(media, session_key="defaultKey", **kwargs):
    """
    Save a FIDS media.

    | *Arguments*      | *Description*                                                                |
    | ``media``        | Media entity dictionary.                                                     |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Save FIDS Media    ${media}

    """
    entity = media.copy()

    return __base_save_data(
        MEDIA_VIEW_NAME, MEDIA_FIELDS, entity, session_key, **kwargs
    )


def fids_media_delete(media, session_key="defaultKey", **kwargs):
    """
    Delete a FIDS media.

    | *Arguments*      | *Description*                                                                |
    | ``media``        | Media entity dictionary. Must contain key ``fmeId``.                         |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Delete FIDS Media    ${media}

    """
    entity = {"fmeId": media["fmeId"]}

    return __base_delete_data(
        MEDIA_VIEW_NAME, MEDIA_FIELDS, entity, session_key, **kwargs
    )


def fids_media_deleted_get(session_key="defaultKey", **kwargs):
    """
    Get deleted FIDS media.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Deleted FIDS Media

    """
    return __base_get_data(MEDIA_DELETED_VIEW_NAME, MEDIA_FIELDS, session_key, **kwargs)


def fids_external_media_get(session_key="defaultKey", **kwargs):
    """
    Get external FIDS media.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get External FIDS Media

    """
    return __base_get_data(
        MEDIA_EXTERNAL_VIEW_NAME, MEDIA_FIELDS, session_key, **kwargs
    )


def fids_external_media_deleted_get(session_key="defaultKey", **kwargs):
    """
    Get deleted external FIDS media.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get Deleted External FIDS Media

    """
    return __base_get_data(
        MEDIA_EXTERNAL_DELETED_VIEW_NAME, MEDIA_FIELDS, session_key, **kwargs
    )


FIDS_MEDIA_CAMPAIGN_TAGS_VIEW_NAME = "FidDelegateBean.MediaCampaignTags"
FIDS_MEDIA_CAMPAIGN_TAGS_FIELDS = ["uniqueId", "tag"]


def fids_media_compaign_tags_get(session_key="defaultKey", **kwargs):
    """
    Get FIDS media campaign tags.

    | *Arguments*      | *Description*                                                                |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Get FIDS Media Campaign Tags

    """
    return __base_get_data(
        FIDS_MEDIA_CAMPAIGN_TAGS_VIEW_NAME,
        FIDS_MEDIA_CAMPAIGN_TAGS_FIELDS,
        session_key,
        **kwargs,
    )
