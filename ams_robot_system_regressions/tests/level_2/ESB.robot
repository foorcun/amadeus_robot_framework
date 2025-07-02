*** Settings ***
Library             ams
Library             protocols
Library             ams/commons.py
Resource            ../../resources/generic_keywords.resource

Suite Setup         Setup    applications=ESB
Suite Teardown      No Operation


*** Test Cases ***
001_ESB_Agent_Node_Status
    Esb Agent Node Status

002_ESB_Agent_Node_Details
    Esb Agent Node Details

003_ESB_Agent_Cluster_Summary
    Esb Agent Cluster Summary

004_ESB_Agent_Cluster_Validate
    Esb Agent Cluster Validate

005_ESB_Agent_Cluster_Registry
    Esb Agent Cluster Registry

006_ESB_Agent_Queues_Metrics
    Esb Agent Queues Metrics

007_ESB_Agent_Routing_Rules
    Esb Agent Routing Rules

008_ESB_Agent_Interfaces_Descriptor
    Esb Agent Interfaces Descriptor

009_ESB_Agent_All_Interface_Properties
    Esb Agent Interface Properties

010_ESB_Agent_FOM_Interface_Properties
    Precondition Esb Interfaces Deployed    FOM
    Esb Agent Interface Properties    FOM

011_ESB_Agent_Any_Node_FOM_Interface_Metrics
    Precondition Esb Interfaces Deployed    FOM
    ${node}    Esb Agent Find Node Running Interface    interface=FOM    node_selector=any
    Esb Agent Node Interface Metrics    node=${node}    interface=FOM

012_ESB_Agent_All_Nodes_FOM_Interface_Metrics
    Precondition Esb Interfaces Deployed    FOM
    ${nodes}    Esb Agent Find Node Running Interface    interface=FOM    node_selector=all
    FOR    ${node}    IN    @{nodes}
        Esb Agent Node Interface Metrics    node=${node}    interface=FOM
    END

013_ESB_Agent_All_Nodes_All_Interface_Metrics
    ${nodes}    Esb Agent Find Running Nodes
    FOR    ${node}    IN    @{nodes}
        Esb Agent Node Interface Metrics    node=${node}
    END
