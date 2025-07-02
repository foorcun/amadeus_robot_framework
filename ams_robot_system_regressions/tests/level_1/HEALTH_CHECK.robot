*** Settings ***
Library             ams
Resource            ams/keywords.resource

Suite Setup         Open Generic Ams Session    protocol=REST    current_directory=${CURDIR}
Suite Teardown      No Operation


*** Test Cases ***
AAA
    Precondition Applications Deployed    applications=AAA
    ${health_result}    Health Check    component_name=aaa
    Log    AAA - Component Health (readiness): ${health_result}

AFV
    Precondition Applications Deployed    applications=AFV
    ${health_result}    Health Check    component_name=afv
    Log    AFV - Component Health (readiness): ${health_result}

AMG
    Precondition Applications Deployed    applications=AMG
    ${health_result}    Health Check    component_name=amg
    Log    AMG - Component Health (readiness): ${health_result}

AMO
    Precondition Applications Deployed    applications=AMO
    ${health_result}    Health Check    component_name=amo
    Log    AMO - Component Health (readiness): ${health_result}

CDS
    Precondition Applications Deployed    applications=CDS
    ${health_result}    Health Check    component_name=cds
    Log    CDS - Component Health (readiness): ${health_result}

CFG
    Precondition Applications Deployed    applications=CFG
    ${health_result}    Health Check    component_name=cfg
    Log    CFG - Component Health (readiness): ${health_result}

CSV
    Precondition Applications Deployed    applications=CSV
    ${health_result}    Health Check    component_name=csv
    Log    CSV - Component Health (readiness): ${health_result}

DFIB
    Precondition Applications Deployed    applications=DFIB
    ${health_result}    Health Check    component_name=dfib
    Log    DFIB - Component Health (readiness): ${health_result}

ESB
    Precondition Applications Deployed    applications=ESB
    ${health_result}    Health Check    component_name=esb
    Log    ESB - Component Health (readiness): ${health_result}

FDS
    Precondition Applications Deployed    applications=FDS
    ${health_result}    Health Check    component_name=fds
    Log    FDS - Component Health (readiness): ${health_result}

FID
    Precondition Applications Deployed    applications=FID
    ${health_result}    Health Check    component_name=fid
    Log    FID - Component Health (readiness): ${health_result}

FOM
    Precondition Applications Deployed    applications=FOM
    ${health_result}    Health Check    component_name=fom
    Log    FOM - Component Health (readiness): ${health_result}

LCX
    Precondition Applications Deployed    applications=LCX
    ${health_result}    Health Check    component_name=lcx
    Log    LCX - Component Health (readiness): ${health_result}

MB
    Precondition Applications Deployed    applications=MB
    ${health_result}    Health Check    component_name=mb
    Log    MB - Component Health (readiness): ${health_result}

MBL
    Precondition Applications Deployed    applications=MBL
    ${health_result}    Health Check    component_name=mbl
    Log    MBL - Component Health (readiness): ${health_result}

MSC
    Precondition Applications Deployed    applications=MSC
    ${health_result}    Health Check    component_name=msc
    Log    MSC - Component Health (readiness): ${health_result}

PRW
    Precondition Applications Deployed    applications=PRW
    ${health_result}    Health Check    component_name=prw
    Log    PRW - Component Health (readiness): ${health_result}

PSA
    Precondition Applications Deployed    applications=PSA
    ${health_result}    Health Check    component_name=psa
    Log    PSA - Component Health (readiness): ${health_result}

SDS
    Precondition Applications Deployed    applications=SDS
    ${health_result}    Health Check    component_name=sds
    Log    SDS - Component Health (readiness): ${health_result}

SGA
    Precondition Applications Deployed    applications=SGA
    ${health_result}    Health Check    component_name=sga
    Log    SGA - Component Health (readiness): ${health_result}

TAM
    Precondition Applications Deployed    applications=TAM
    ${health_result}    Health Check    component_name=tam
    Log    TAM - Component Health (readiness): ${health_result}

VIP
    Precondition Applications Deployed    applications=VIP
    ${health_result}    Health Check    component_name=vip
    Log    VIP - Component Health (readiness): ${health_result}
