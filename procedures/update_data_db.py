#!/usr/env bin python3.8
from get_data_info_api import inventory, partitions_controller, \
    health_nodes, supervisora_status, status_power, status_fan, interfaces_apic, policy_group, \
    correlation_profile_pg, vpc_interface, leaf_access_port, pc_interface, correlation_profile_interface
import sys
import os

MAIN_PATH = "/opt/space/python/aci"

sys.path.insert(1, os.path.join(MAIN_PATH, "infraestructure"))
sys.path.insert(1, os.path.join(MAIN_PATH, "helpers"))
from Database import ControllerMariaDB
from resources import CREDENTIALS_DATABASE

auth_db = CREDENTIALS_DATABASE['production']
con = ControllerMariaDB(auth_db['hostname'], auth_db['username'], auth_db['password'], auth_db['database'])

# metodo para extraer los id's de los nodos
def list_node_id():
    sql_queries = ["select distinct(id) from `inventory`"]
    data = con.operational_sql_return_data(*sql_queries)
    return data

# metodo para extraer el nombre de los leaf
def list_name_leaf():
    sql_queries = ["select distinct(name) from `inventory`"]
    data = con.operational_sql_return_data(*sql_queries)
    return data

def update_data_inventory():
    datasets = inventory()
    con.operational_sql_insert_rows("""insert into inventory (`adSt`,`address`,`annotation`,`apicType`,`childAction`,
                                    `delayedHeartbeat`,`dn`,`extMngdBy`,`fabricSt`,`id`,`lastStateModTs`,`lcOwn`,`modTS`,
                                    `model`,`monPolDn`,`name`,`nameAlias`,`nodeType`,`role`,`serial`,`status`,`uid`,`vendor`,`version`,
                                    `time_exec`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                    on duplicate key update `adSt`=VALUES(`adSt`),`address`=VALUES(`address`),`annotation`=VALUES(`annotation`),
                                    `apicType`=VALUES(`apicType`),`childAction`=VALUES(`childAction`),`delayedHeartbeat`=VALUES(`delayedHeartbeat`),
                                    `dn`=VALUES(`dn`),`extMngdBy`=VALUES(`extMngdBy`),`fabricSt`=VALUES(`fabricSt`),`id`=VALUES(`id`),`lastStateModTs`=VALUES(`lastStateModTs`),
                                    `lcOwn`=VALUES(`lcOwn`),`modTS`=VALUES(`modTS`),`model`=VALUES(`model`),`monPolDn`=VALUES(`monPolDn`),`name`=VALUES(`name`),`nameAlias`=VALUES(`nameAlias`),
                                    `nodeType`=VALUES(`nodeType`),`role`=VALUES(`role`),`serial`=VALUES(`serial`),`status`=VALUES(`status`),`uid`=VALUES(`uid`),
                                    `vendor`=VALUES(`vendor`),`version`=VALUES(`version`),`time_exec`=VALUES(`time_exec`)""", *datasets)

def update_data_partitions_controller():
    list_nodes = ["1","2","3"]
    for node_id in list_nodes:
        datasets = partitions_controller(node_id)
        con.operational_sql_insert_rows("""insert into partitions_controller (`available`,`blocks`,`capUtilized`,`childAction`,`device`,`dn`,`failReason`,`fileSystem`,
                                        `firmwareVersion`,`lcOwn`,`mediaWearout`,`modTs`,`model`,`monPolDn`,`mount`,`name`,`nameAlias`,`operSt`,`serial`,`status`,`used`,
                                        `uid`,`node_id`,`time_exec`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                        on duplicate key update `available`=VALUES(`available`),`blocks`=VALUES(`blocks`),`capUtilized`=VALUES(`capUtilized`),`childAction`=VALUES(`childAction`),
                                        `device`=VALUES(`device`),`dn`=VALUES(`dn`),`failReason`=VALUES(`failReason`),`fileSystem`=VALUES(`fileSystem`),`firmwareVersion`=VALUES(`firmwareVersion`),
                                        `lcOwn`=VALUES(`lcOwn`),`mediaWearout`=VALUES(`mediaWearout`),`modTs`=VALUES(`modTs`),`model`=VALUES(`model`),`monPolDn`=VALUES(`monPolDn`),`mount`=VALUES(`mount`),
                                        `name`=VALUES(`name`),`nameAlias`=VALUES(`nameAlias`),`operSt`=VALUES(`operSt`),`serial`=VALUES(`serial`),`status`=VALUES(`status`),`used`=VALUES(`used`),
                                        `uid`=VALUES(`uid`),`node_id`=VALUES(`node_id`),`time_exec`=VALUES(`time_exec`)""", *datasets)

def update_health_nodes():
    list_nodes = list_node_id()
    for node_id in list_nodes:
        datasets = health_nodes(node_id)
        con.operational_sql_insert_rows("""insert into health_nodes(`healthAvg`,`healthMax`,`healthMin`,`repIntvEnd`,`repIntvStart`,`node_id`,`time_exec`) values (%s,%s,%s,%s,%s,%s,%s)
                                        on duplicate key update `healthAvg`=VALUES(`healthAvg`),`healthMax`=VALUES(`healthMax`),`healthMin`=VALUES(`healthMin`),`repIntvEnd`=VALUES(`repIntvEnd`),
                                        `repIntvStart`=VALUES(`repIntvStart`),`node_id`=VALUES(`node_id`), `time_exec`=VALUES(`time_exec`)""", *datasets)
    
def update_supervisora_status():
    list_nodes = list_node_id()
    for node_id in list_nodes:
        datasets = supervisora_status(node_id)
        con.operational_sql_insert_rows("""insert into supervisora_status(`descr`,`hwVer`,`macB`,`macL`,`model`,`operSt`,`pwrSt`,`rdSt`,`rev`,`ser`,`swCId`,`type`,`vendor`,`uid`,`node_id`,`time_exec`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                        on duplicate key update `descr`=VALUES(`descr`),`hwVer`=VALUES(`hwVer`),`macB`=VALUES(`macB`),`macL`=VALUES(`macL`),`model`=VALUES(`model`),`operSt`=VALUES(`operSt`),
                                        `pwrSt`=VALUES(`pwrSt`),`rdSt`=VALUES(`rdSt`),`rev`=VALUES(`rev`),`ser`=VALUES(`ser`),`swCId`=VALUES(`swCId`),`type`=VALUES(`type`),
                                        `vendor`=VALUES(`vendor`),`node_id`=VALUES(`node_id`),`time_exec`=VALUES(`time_exec`)""", *datasets)

def update_status_power():
    list_nodes = list_node_id()
    for node_id in list_nodes:
        datasets = status_power(node_id)
        con.operational_sql_insert_rows("""insert into status_power(`almReg`,`cap`,`descr`,`fatOpSt`,`hwVer`,`id`,`model`,`operSt`,`rev`,`ser`,
                                        `status`,`vSrc`,`vendor`,`volt`,`uid`,`node_id`,`time_exec`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                        on duplicate key update `almReg`=VALUES(`almReg`),`cap`=VALUES(`cap`),`descr`=VALUES(`descr`),`fatOpSt`=VALUES(`fatOpSt`),
                                        `hwVer`=VALUES(`hwVer`),`id`=VALUES(`id`),`model`=VALUES(`model`),`operSt`=VALUES(`operSt`),`rev`=VALUES(`rev`),`ser`=VALUES(`ser`),
                                        `status`=VALUES(`status`),`vSrc`=VALUES(`vSrc`),`vendor`=VALUES(`vendor`),`volt`=VALUES(`volt`),`uid`=VALUES(`uid`),
                                        `node_id`=VALUES(`node_id`),`time_exec`=VALUES(`time_exec`)""", *datasets)

def update_status_fan():
    list_nodes = list_node_id()
    for node_id in list_nodes:
        datasets = status_fan(node_id)
        con.operational_sql_insert_rows("""insert into status_fan(`descr`,`fanName`,`fanletFailString`,`id`,`model`,`operSt`,`rev`,`ser`,`status`,`vendor`,`uid`,`node_id`,`time_exec`) values 
                                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update `descr`=VALUES(`descr`),`fanName`=VALUES(`fanName`),`fanletFailString`=VALUES(`fanletFailString`),
                                        `id`=VALUES(`id`),`model`=VALUES(`model`),`operSt`=VALUES(`operSt`),`rev`=VALUES(`rev`),`ser`=VALUES(`ser`),`status`=VALUES(`status`),`vendor`=VALUES(`vendor`),`uid`=VALUES(`uid`),
                                        `node_id`=VALUES(`node_id`),`time_exec`=VALUES(`time_exec`)""",*datasets)

def update_interfaces():
    list_nodes = list_node_id()
    for node_id in list_nodes:
        datasets = interfaces_apic(node_id)
        con.operational_sql_insert_rows("""insert into interfaces(`adminSt`,`autoNeg`,`brkoutMap`,`bw`,`childAction`,`delay`,`descr`,`dn`,`dot1qEtherType`,`ethpmCfgFailedBmp`,`ethpmCfgFailedTs`,
                                        `ethpmCfgState`,`fcotChannelNumber`,`fecMode`,`id`,`inhBw`,`isReflectiveRelayCfgSupported`,`layer`,`lcOwn`,`linkDebounce`,`linkLog`,`mdix`,`medium`,`modTs`,`mode`,`monPolDn`,`mtu`,`name`,`pathSDescr`,
                                        `portT`,`prioFlowCtrl`,`reflectiveRelayEn`,`routerMac`,`snmpTrapSt`,`spanMode`,`speed`,`status`,`switchingSt`,`trunkLog`,`usage`,`accessVlan`,`allowedVlans`,`backplaneMac`,`bundleBupId`,`bundleIndex`,
                                        `cfgAccessVlan`,`cfgNativeVlan`,`currErrIndex`,`diags`,`encap`,`errDisTimerRunning`,`errVlanStatusHt`,`errVlans`,`hwBdId`,`hwResourceId`,`intfT`,`iod`,`lastErrors`,`lastLinkStChg`,`media`,`nativeVlan`,
                                        `numOfSI`,`operBitset`,`operDceMode`,`operDuplex`,`operEEERxWkTime`,`operEEEState`,`operEEETxWkTime`,`operErrDisQual`,`operFecMode`,`operFlowCtrl`,`operMdix`,`operMode`,`operModeDetail`,`operPhyEnSt`,
                                        `operRouterMac`,`operSpeed`,`operSt`,`operStQual`,`operStQualCode`,`operVlans`,`osSum`,`portCfgWaitFlags`,`primaryVlan`,`resetCtr`,`rn`,`siList`,`txT`,`userCfgdFlags`,`vdcId`,`node_id`,`time_exec`) 
                                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                        on duplicate key update `adminSt`=VALUES(`adminSt`),`autoNeg`=VALUES(`autoNeg`),`brkoutMap`=VALUES(`brkoutMap`),`bw`=VALUES(`bw`),`childAction`=VALUES(`childAction`),`delay`=VALUES(`delay`),`descr`=VALUES(`descr`),
                                        `dn`=VALUES(`dn`),`dot1qEtherType`=VALUES(`dot1qEtherType`),`ethpmCfgFailedBmp`=VALUES(`ethpmCfgFailedBmp`),`ethpmCfgFailedTs`=VALUES(`ethpmCfgFailedTs`),`ethpmCfgState`=VALUES(`ethpmCfgState`),`fcotChannelNumber`=VALUES(`fcotChannelNumber`),
                                        `fecMode`=VALUES(`fecMode`),`id`=VALUES(`id`),`inhBw`=VALUES(`inhBw`),`isReflectiveRelayCfgSupported`=VALUES(`isReflectiveRelayCfgSupported`),`layer`=VALUES(`layer`),`lcOwn`=VALUES(`lcOwn`),`linkDebounce`=VALUES(`linkDebounce`),
                                        `linkLog`=VALUES(`linkLog`),`mdix`=VALUES(`mdix`),`medium`=VALUES(`medium`),`modTs`=VALUES(`modTs`),`mode`=VALUES(`mode`),`monPolDn`=VALUES(`monPolDn`),`mtu`=VALUES(`mtu`),`name`=VALUES(`name`),`pathSDescr`=VALUES(`pathSDescr`),
                                        `portT`=VALUES(`portT`),`prioFlowCtrl`=VALUES(`prioFlowCtrl`),`reflectiveRelayEn`=VALUES(`reflectiveRelayEn`),`routerMac`=VALUES(`routerMac`),`snmpTrapSt`=VALUES(`snmpTrapSt`),`spanMode`=VALUES(`spanMode`),`speed`=VALUES(`speed`),
                                        `status`=VALUES(`status`),`switchingSt`=VALUES(`switchingSt`),`trunkLog`=VALUES(`trunkLog`),`usage`=VALUES(`usage`),`accessVlan`=VALUES(`accessVlan`),`allowedVlans`=VALUES(`allowedVlans`),`backplaneMac`=VALUES(`backplaneMac`),`bundleBupId`=VALUES(`bundleBupId`),
                                        `bundleIndex`=VALUES(`bundleIndex`),`cfgAccessVlan`=VALUES(`cfgAccessVlan`),`cfgNativeVlan`=VALUES(`cfgNativeVlan`),`currErrIndex`=VALUES(`currErrIndex`),`diags`=VALUES(`diags`),`encap`=VALUES(`encap`),`errDisTimerRunning`=VALUES(`errDisTimerRunning`),
                                        `errVlanStatusHt`=VALUES(`errVlanStatusHt`),`errVlans`=VALUES(`errVlans`),`hwBdId`=VALUES(`hwBdId`),`hwResourceId`=VALUES(`hwResourceId`),`intfT`=VALUES(`intfT`),`iod`=VALUES(`iod`),`lastErrors`=VALUES(`lastErrors`),`lastLinkStChg`=VALUES(`lastLinkStChg`),
                                        `media`=VALUES(`media`),`nativeVlan`=VALUES(`nativeVlan`),`numOfSI`=VALUES(`numOfSI`),`operBitset`=VALUES(`operBitset`),`operDceMode`=VALUES(`operDceMode`),`operDuplex`=VALUES(`operDuplex`),`operEEERxWkTime`=VALUES(`operEEERxWkTime`),`operEEEState`=VALUES(`operEEEState`),
                                        `operEEETxWkTime`=VALUES(`operEEETxWkTime`),`operErrDisQual`=VALUES(`operErrDisQual`),`operFecMode`=VALUES(`operFecMode`),`operFlowCtrl`=VALUES(`operFlowCtrl`),`operMdix`=VALUES(`operMdix`),`operMode`=VALUES(`operMode`),`operModeDetail`=VALUES(`operModeDetail`),
                                        `operPhyEnSt`=VALUES(`operPhyEnSt`),`operRouterMac`=VALUES(`operRouterMac`),`operSpeed`=VALUES(`operSpeed`),`operSt`=VALUES(`operSt`),`operStQual`=VALUES(`operStQual`),`operStQualCode`=VALUES(`operStQualCode`),`operVlans`=VALUES(`operVlans`),
                                        `osSum`=VALUES(`osSum`),`portCfgWaitFlags`=VALUES(`portCfgWaitFlags`),`primaryVlan`=VALUES(`primaryVlan`),`resetCtr`=VALUES(`resetCtr`),`rn`=VALUES(`rn`),`siList`=VALUES(`siList`),`txT`=VALUES(`txT`),`userCfgdFlags`=VALUES(`userCfgdFlags`),`vdcId`=VALUES(`vdcId`),
                                        `node_id`=VALUES(`node_id`),`time_exec`=VALUES(`time_exec`)""",*datasets)

def update_policy_group():
    datasets = policy_group()
    con.operational_sql_insert_rows("""insert into policy_group()
                                    """, *datasets)

def update_leaf_access_port():
    datasets = leaf_access_port()
    con.operational_sql_insert_rows("""insert into leaf_access(`name`,`uid`,`cdp_status`,`vel_neg`,`lldp_status`,`mcp_status`,`mon_status`,`storm_status`,`stp_status`,`time_exec`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                    on duplicate key update `name`=VALUES(`name`),`uid`=VALUES(`uid`),`cdp_status`=VALUES(`cdp_status`),`vel_neg`=VALUES(`vel_neg`),`lldp_status`=VALUES(`lldp_status`),`mcp_status`=VALUES(`mcp_status`),
                                    `mon_status`=VALUES(`mon_status`),`storm_status`=VALUES(`storm_status`),`stp_status`=VALUES(`stp_status`),`time_exec`=VALUES(`time_exec`)""", *datasets)

def update_pc_interface():
    datasets = pc_interface()
    con.operational_sql_insert_rows("""insert into pc_interface(`name`,`uid`,`cdp_status`,`l2_status`,`vel_neg`,`lacp_status`,`lldp_status`,`time_exec`) values (%s,%s,%s,%s,%s,%s,%s,%s) 
                                    on duplicate key update `name`=VALUES(`name`),`uid`=VALUES(`uid`),`cdp_status`=VALUES(`cdp_status`),`l2_status`=VALUES(`l2_status`),`vel_neg`=VALUES(`vel_neg`),`lacp_status`=VALUES(`lacp_status`),
                                    `lldp_status`=VALUES(`lldp_status`),`time_exec`=VALUES(`time_exec`)""",*datasets)

def update_vpc_interfaces():
    datasets = vpc_interface()
    con.operational_sql_insert_rows("""insert into vpc_interface(`name`,`descr`,`uid`,`cdp_status`,`vel_neg`,`lacp_status`,`lldp_status`,`storm`,`bpdu_status`,`time_exec`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on
                                    duplicate key update `name`=VALUES(`name`),`uid`=VALUES(`uid`),`cdp_status`=VALUES(`cdp_status`),`vel_neg`=VALUES(`vel_neg`),`lacp_status`=VALUES(`lacp_status`),`lldp_status`=VALUES(`lldp_status`),
                                    `storm`=VALUES(`storm`),`bpdu_status`=VALUES(`bpdu_status`),`time_exec`=VALUES(`time_exec`)""", *datasets)

def update_correlation_profile_pg():
    list_nodes = list_name_leaf()
    for node_id in list_nodes:
        datasets = correlation_profile_pg(node_id)
        con.operational_sql_insert_rows("""insert into correlation_profile_pg(`name_profile`,`name_pg`,`name_leaf`,`time_exec`) values (%s, %s, %s, %s) on duplicate key update `name_profile`=VALUES(`name_profile`),`name_pg`=VALUES(`name_pg`),
                                        `name_leaf`=VALUES(`name_leaf`),`time_exec`=VALUES(`time_exec`)""", *datasets)

def update_correlation_profile_interface():
    datasets = correlation_profile_interface()
    con.operational_sql_insert_rows("""insert into correlation_profile_interface(`name_leaf`,`name_profile`,`int_one`,`int_two`,`uid`,`time_exec`) values (%s,%s,%s,%s,%s,%s) on duplicate key update `name_leaf`=VALUES(`name_leaf`),
                                    `name_profile`=VALUES(`name_profile`),`int_one`=VALUES(`int_one`),`int_two`=VALUES(`int_two`),`uid`=VALUES(`uid`),`time_exec`=VALUES(`time_exec`)""", *datasets)

def update_components():
    update_data_inventory()
    update_data_partitions_controller()
    update_health_nodes()
    update_supervisora_status()
    update_status_power()
    update_status_fan()
    update_interfaces()
    update_correlation_profile_pg()
    update_correlation_profile_interface()
    update_vpc_interfaces()
    update_pc_interface()
    update_leaf_access_port()


if __name__ == '__main__':
    update_components()
