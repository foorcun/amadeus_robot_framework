"""Injector for FIDS import/export keywords"""

import os
import protocols.broker
from ams.fid_api_calls.crud.injector_rest import injector as rest_injector

# pylint: disable=line-too-long


def fids_download_template(session_key="defaultKey", **kwargs):
    """
    Download the FIDS import template.

    | *Arguments*      | *Description*                                                           |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Download FIDS Template

    """
    kwargs["endpoint_type"] = "download_template"
    response = protocols.broker.injector(kwargs, session_key, rest_injector)
    return response


def fids_export(views, session_key="defaultKey", **kwargs):
    """
    Export FIDS data for the specified views.

    | *Arguments*      | *Description*                                                           |
    | ``views``        | List of view names to export.                                           |
    | ``session_key``  | Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    Possible values for ``views``:
        FidCampaigns, FidControllers, RefParametersControllers, FidLayouts, FidMedia,
        SysMsgTemplates, FidMonitors, RefParametersMonitors, RefParametersSystem, FidRules,
        FidScheduledTasks, FidDictionary,RefLanguagesCodes. RefLanguagesAirlines,
        RefLanguagesAirports, FIDTAB, XmWorkstations

    === Usage: ===
    | Export FIDS Data    views=["FidCampaigns", "FidControllers"]

    """
    kwargs["endpoint_type"] = "export"
    kwargs["parameters"] = {"exportViews": views}
    return protocols.broker.injector(kwargs, session_key, rest_injector)


def __base_import_file(
    file_path,
    file_name,
    content_type,
    persist_data=False,
    partial=True,
    session_key="defaultKey",
    **kwargs,
):
    """
    Base function to import a file into FIDS.

    | *Arguments*      | *Description*                                                                      |
    | ``file_path``    | Path to the directory containing the file.                                         |
    | ``file_name``    | Name of the file to import.                                                        |
    | ``content_type`` | MIME type of the file.                                                             |
    | ``persist_data`` | (Optional) Whether to persist data. Default is False.                              |
    | ``partial``      | (Optional) Whether to allow partial import. Default is True.                       |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Import FIDS File    file_path=path    file_name=name.xlsx    content_type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

    """
    full_path = os.getcwd() + os.sep + file_path + os.sep + file_name
    print(f"Loading file for import from {full_path}")
    file = open(full_path, "rb")
    kwargs["payload"] = file.read()
    file.close()

    kwargs["file_name"] = file_name
    kwargs["content_type"] = content_type
    kwargs["parameters"] = {"persistData": persist_data, "partial": partial}
    return protocols.broker.injector(kwargs, session_key, rest_injector)


def fids_import_template(
    file_path,
    file_name,
    persist_data=False,
    partial=True,
    session_key="defaultKey",
    **kwargs,
):
    """
    Import a FIDS template file.

    | *Arguments*      | *Description*                                                                      |
    | ``file_path``    | Path to the directory containing the file.                                         |
    | ``file_name``    | Name of the file to import.                                                        |
    | ``persist_data`` | (Optional) Whether to persist data. Default is False.                              |
    | ``partial``      | (Optional) Whether to allow partial import. Default is True.                       |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Import FIDS Template    file_path=path    file_name=name.xlsx

    """
    kwargs["endpoint_type"] = "import_template"
    return __base_import_file(
        file_path,
        file_name,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        persist_data=persist_data,
        partial=partial,
        session_key=session_key,
        **kwargs,
    )


def fids_import_from_another_system(
    file_path,
    file_name,
    persist_data=False,
    partial=True,
    session_key="defaultKey",
    **kwargs,
):
    """
    Import FIDS data from another system.

    | *Arguments*      | *Description*                                                                      |
    | ``file_path``    | Path to the directory containing the file.                                         |
    | ``file_name``    | Name of the ZIP file to import.                                                    |
    | ``persist_data`` | (Optional) Whether to persist data. Default is False.                              |
    | ``partial``      | (Optional) Whether to allow partial import. Default is True.                       |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Import FIDS From Another System    file_path=path    file_name=name.zip

    """
    kwargs["endpoint_type"] = "import"
    return __base_import_file(
        file_path,
        file_name,
        "application/x-zip-compressed",
        persist_data=persist_data,
        partial=partial,
        session_key=session_key,
        **kwargs,
    )


def fids_import_poll(token, session_key="defaultKey", **kwargs):
    """
    Poll the status of a FIDS import.

    | *Arguments*      | *Description*                                                                      |
    | ``token``        | Import token.                                                                      |
    | ``session_key``  | (Optional) Session alias. If no value specified, default key "defaultKey" is used. |

    Other parameters are passed as couple key=value through ``**kwargs`` (keyword arguments).

    === Usage: ===
    | Import FIDS Poll    ${import_token}

    """
    kwargs["endpoint_type"] = "import_poll"
    kwargs["parameters"] = {"token": token}
    return protocols.broker.injector(kwargs, session_key, rest_injector)
