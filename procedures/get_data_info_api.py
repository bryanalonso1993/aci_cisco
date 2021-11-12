#!/usr/env bin python3.8
from datetime import datetime
import sys
import re
import os

MAIN_PATH = "/opt/space/python/aci"

sys.path.insert(1, os.path.join(MAIN_PATH, "infraestructure"))
sys.path.insert(1, os.path.join(MAIN_PATH, "helpers"))

from Api import ControllerApic
from resources import CREDENTIALS_APIC
from query_params_aci import query_params_aci

# time execute process
time_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cred_api = CREDENTIALS_APIC['production']
apic = ControllerApic(cred_api['ip_address'], cred_api['username'], cred_api['password'])

def concat(str1, str2):
    return "{}-{}".format(str1, str2)

def inventory():
    query_params = query_params_aci['inventory']
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        data = row['fabricNode']['attributes']
        result.append((
            data['adSt'],data['address'],data['annotation'],data['apicType'],data['childAction'],data['delayedHeartbeat'],
            data['dn'],data['extMngdBy'],data['fabricSt'],data['id'],data['lastStateModTs'],data['lcOwn'],data['modTs'],
            data['model'],data['monPolDn'],data['name'],data['nameAlias'],data['nodeType'],data['role'],data['serial'],
            data['status'],data['uid'],data['vendor'],data['version'],time_exec
        ))
    return result

def partitions_controller(node_id):
    query_params = query_params_aci['partitions_controller'](node_id)
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        data = row['eqptStorage']['attributes']
        result.append((
            data['available'],data['blocks'],data['capUtilized'],data['childAction'],data['device'],data['dn'],
            data['failReason'],data['fileSystem'],data['firmwareVersion'],data['lcOwn'],data['mediaWearout'],
            data['modTs'],data['model'],data['monPolDn'],data['mount'],data['name'],data['nameAlias'],data['operSt'],
            data['serial'],data['status'],data['used'], concat(data['name'], node_id),node_id,time_exec
        ))
    return result

def health_nodes(node_id):
    query_params = query_params_aci['health_nodes'](node_id)
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        data = row['fabricNodeHealthHist5min']['attributes']
        result.append((
            data['healthAvg'],data['healthMax'],data['healthMin'],data['repIntvEnd'],data['repIntvStart'],
            node_id,time_exec
        ))
    return result

def supervisora_status(node_id):
    query_params = query_params_aci['supervisora_status'](node_id)
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        data = row['eqptSupC']['attributes']
        result.append((
            data['descr'],data['hwVer'],data['macB'],data['macL'],data['model'],data['operSt'],data['pwrSt'],data['rdSt'],
            data['rev'],data['ser'],data['swCId'],data['type'],data['vendor'],concat(data['ser'], node_id),node_id,time_exec
        ))
    return result

def status_power(node_id):
    query_params = query_params_aci['power_status'](node_id)
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        data = row['eqptPsu']['attributes']
        result.append((
            data['almReg'],data['cap'],data['descr'],data['fanOpSt'],data['hwVer'],data['id'],data['model'],data['operSt'],
            data['rev'],data['ser'],data['status'],data['vSrc'],data['vendor'],data['volt'],concat(data['ser'],node_id),node_id,time_exec
        ))
    return result

def status_fan(node_id):
    query_params = query_params_aci['fan_status'](node_id)
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        data = row['eqptFt']['attributes']
        result.append((
            data['descr'],data['fanName'],data['fanletFailString'],data['id'],data['model'],data['operSt'],data['rev'],
            data['ser'],data['status'],data['vendor'],concat(data['id'],node_id),node_id,time_exec
        ))
    return result

def interfaces_apic(node_id):
    query_params = query_params_aci['interface_node'](node_id)
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        [data1, data2] = [row['l1PhysIf']['attributes'], row['l1PhysIf']['children'][0]['ethpmPhysIf']['attributes']]
        result.append((
            data1['adminSt'],data1['autoNeg'],data1['brkoutMap'],data1['bw'],data1['childAction'],data1['delay'],data1['descr'],data1['dn'],
            data1['dot1qEtherType'],data1['ethpmCfgFailedBmp'],data1['ethpmCfgFailedTs'],data1['ethpmCfgState'],data1['fcotChannelNumber'],
            data1['fecMode'],data1['id'],data1['inhBw'],data1['isReflectiveRelayCfgSupported'],data1['layer'],data1['lcOwn'],data1['linkDebounce'],
            data1['linkLog'],data1['mdix'],data1['medium'],data1['modTs'],data1['mode'],data1['monPolDn'],data1['mtu'],data1['name'],data1['pathSDescr'],
            data1['portT'],data1['prioFlowCtrl'],data1['reflectiveRelayEn'],data1['routerMac'],data1['snmpTrapSt'],data1['spanMode'],data1['speed'],
            data1['status'],data1['switchingSt'],data1['trunkLog'],data1['usage'],data2['accessVlan'],data2['allowedVlans'],data2['backplaneMac'],data2['bundleBupId'],
            data2['bundleIndex'],data2['cfgAccessVlan'],data2['cfgNativeVlan'],data2['currErrIndex'],data2['diags'],data2['encap'],
            data2['errDisTimerRunning'],data2['errVlanStatusHt'],data2['errVlans'],data2['hwBdId'],data2['hwResourceId'],data2['intfT'],
            data2['iod'],data2['lastErrors'],data2['lastLinkStChg'],data2['media'],data2['nativeVlan'],data2['numOfSI'],
            data2['operBitset'],data2['operDceMode'],data2['operDuplex'],data2['operEEERxWkTime'],data2['operEEEState'],data2['operEEETxWkTime'],
            data2['operErrDisQual'],data2['operFecMode'],data2['operFlowCtrl'],data2['operMdix'],data2['operMode'],data2['operModeDetail'],data2['operPhyEnSt'],
            data2['operRouterMac'],data2['operSpeed'],data2['operSt'],data2['operStQual'],data2['operStQualCode'],data2['operVlans'],data2['osSum'],data2['portCfgWaitFlags'],
            data2['primaryVlan'],data2['resetCtr'],data2['rn'],data2['siList'],data2['txT'],data2['userCfgdFlags'],data2['vdcId'],node_id,time_exec
        ))
    return result


def policy_group():
    query_params  = query_params_aci['policy_group']
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        for key, value in row.items():
            if key == 'infraAccBndlGrp':
                result.append((
                    row['infraAccBndlGrp']['attributes']['descr'],
                    row['infraAccBndlGrp']['attributes']['name'],
                    row['infraAccBndlGrp']['attributes']['uid'],
                    time_exec
                ))
            elif key == 'infraAccPortGrp':
                result.append((
                    row['infraAccPortGrp']['attributes']['descr'],
                    row['infraAccPortGrp']['attributes']['name'],
                    row['infraAccPortGrp']['attributes']['name'],
                    time_exec
                ))
    return result

def leaf_access_port():
    query_params = query_params_aci['leaf_access_port']
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        [data1, data2] = [row['infraAccPortGrp']['attributes'], row['infraAccPortGrp']['children']]
        result.append((
            data1['name'],data1['uid'],data2[0]['infraRsCdpIfPol']['attributes']['tnCdpIfPolName'],data2[1]['infraRsHIfPol']['attributes']['tnFabricHIfPolName'],
            data2[2]['infraRsLldpIfPol']['attributes']['tnLldpIfPolName'],data2[3]['infraRsMcpIfPol']['attributes']['tnMcpIfPolName'],data2[4]['infraRsMonIfInfraPol']['attributes']['tnMonInfraPolName'],
            data2[5]['infraRsStormctrlIfPol']['attributes']['tnStormctrlIfPolName'],data2[6]['infraRsStpIfPol']['attributes']['tnStpIfPolName'],time_exec
        ))
    return result

def pc_interface():
    query_params = query_params_aci['pc_interface']
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        [data1, data2] = [row['infraAccBndlGrp']['attributes'], row['infraAccBndlGrp']['children']]
        result.append((
            data1['name'],data1['uid'],data2[0]['infraRsCdpIfPol']['attributes']['tnCdpIfPolName'],data2[1]['infraRsL2IfPol']['attributes']['tnL2IfPolName'],
            data2[2]['infraRsHIfPol']['attributes']['tnFabricHIfPolName'],data2[3]['infraRsLacpPol']['attributes']['tnLacpLagPolName'],data2[4]['infraRsLldpIfPol']['attributes']['tnLldpIfPolName'],time_exec
        ))
    return result

def vpc_interface():
    query_params = query_params_aci['vpc_interface']
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        [data1, data2] = [row['infraAccBndlGrp']['attributes'], row['infraAccBndlGrp']['children']]
        result.append((
            data1['name'],data1['descr'],data1['uid'],data2[0]['infraRsCdpIfPol']['attributes']['tnCdpIfPolName'],data2[1]['infraRsHIfPol']['attributes']['tnFabricHIfPolName'],
            data2[2]['infraRsLacpPol']['attributes']['tnLacpLagPolName'],data2[3]['infraRsLldpIfPol']['attributes']['tnLldpIfPolName'],data2[4]['infraRsStormctrlIfPol']['attributes']['tnStormctrlIfPolName'],
            data2[5]['infraRsStpIfPol']['attributes']['tnStpIfPolName'], time_exec
        ))
    return result

def correlation_profile_interface():
    query_params = query_params_aci['correlation_profile_interface']
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        if 'children' in row['infraAccPortP'].keys():
            for row2 in row['infraAccPortP']['children']:
                result.append((
                    row['infraAccPortP']['attributes']['name'],
                    row2['infraHPortS']['attributes']['name'],
                    "{}/{}".format(row2['infraHPortS']['children'][0]['infraPortBlk']['attributes']['fromCard'], row2['infraHPortS']['children'][0]['infraPortBlk']['attributes']['fromPort']),
                    "{}/{}".format(row2['infraHPortS']['children'][0]['infraPortBlk']['attributes']['toCard'], row2['infraHPortS']['children'][0]['infraPortBlk']['attributes']['toPort']),
                    concat(row['infraAccPortP']['attributes']['name'], row2['infraHPortS']['attributes']['name']),
                    time_exec
                    ))
        #else:
        #    result.append((row['infraAccPortP']['attributes']['name'],"","","",concat(row['infraAccPortP']['attributes']['name'], ""),time_exec))
    return result

def correlation_profile_pg(name_leaf):
    query_params = query_params_aci['correlation_profile_pg'](name_leaf)
    response = apic.execute_method_api('get', query_params)
    result = list()
    for row in response:
        result.append((
            row['infraRsAccBaseGrp']['attributes']['dn'].replace('uni/infra/accportprof-'+name_leaf+'/hports-','').replace('-typ-range/rsaccBaseGrp',''),
            re.sub('uni/infra/funcprof/acc[a-z]{1,7}-','',row['infraRsAccBaseGrp']['attributes']['tDn']),
            name_leaf,
            time_exec
        ))
    return result
