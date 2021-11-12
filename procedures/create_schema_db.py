#!/usr/env bin python3.8
import sys
import os

# root path
MAIN_PATH = os.path.join(os.getcwd())
# import backend database module's
sys.path.insert(1, os.path.join(MAIN_PATH, "infraestructure"))
sys.path.insert(1, os.path.join(MAIN_PATH, "helpers"))

from Database import ControllerMariaDB
from resources import CREDENTIALS_DATABASE
auth_db = CREDENTIALS_DATABASE['development']
con = ControllerMariaDB(auth_db['hostname'], auth_db['username'], auth_db['password'], auth_db['database'])


schema_sql_inventory = """
    CREATE TABLE IF NOT EXISTS inventory (
        `unique` int(11) not null auto_increment,
        `adSt` varchar(255) default null,
        `address` varchar(255) default null,
        `annotation` varchar(255) default null,
        `apicType` varchar(255) default null,
        `childAction` varchar(255) default null,
        `delayedHeartbeat` varchar(255) default null,
        `dn` varchar(255) default null,
        `extMngdBy` varchar(255) default null,
        `fabricSt` varchar(255) default null,
        `id` int(11) not null default '0',
        `lastStateModTs` varchar(255) default null,
        `lcOwn` varchar(255) default null,
        `modTS` varchar(255) default null,
        `model` varchar(255) default null,
        `monPolDn` varchar(255) default null,
        `name` varchar(255) default null,
        `nameAlias` varchar(255) default null,
        `nodeType` varchar(255) default null,
        `role` varchar(255) default null,
        `serial` varchar(255) default null,
        `status` varchar(255) default null,
        `uid` varchar(255) default null,
        `vendor` varchar(255) default null,
        `version` varchar(255) default null,
        `time_exec` datetime not null default '0000-00-00 00:00:00',
        PRIMARY KEY(`unique`),
        UNIQUE KEY `name` (`name`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

schema_sql_partitions_controller = """
    CREATE TABLE IF NOT EXISTS partitions_controller(
        `unique` int(11) not null auto_increment,
        `available` varchar(255) default null,
        `blocks` varchar(255) default null,
        `capUtilized` varchar(255) default null,
        `childAction` varchar(255) default null,
        `device` varchar(255) default null,
        `dn` varchar(255) default null,
        `failReason` varchar(255) default null,
        `fileSystem` varchar(255) default null,
        `firmwareVersion` varchar(255) default null,
        `lcOwn` varchar(255) default null,
        `mediaWearout` varchar(255) default null,
        `modTs` varchar(255) default null,
        `model` varchar(255) default null,
        `monPolDn` varchar(255) default null,
        `mount` varchar(255) default null,
        `name` varchar(255) default null,
        `nameAlias` varchar(255) default null,
        `operSt` varchar(255) default null,
        `serial` varchar(255) default null,
        `status` varchar(255) default null,
        `used` varchar(255) default null,
        `uid` varchar(255) default null,
        `node_id` int(4) not null default '0',
        `time_exec` datetime not null default '0000-00-00 00:00:00',
        PRIMARY KEY(`unique`),
        UNIQUE KEY `uid` (`uid`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

schema_health_nodes = """
    CREATE TABLE IF NOT EXISTS health_nodes(
        `unique` int(11) not null auto_increment,
        `healthAvg` int(4) not null default 0,
        `healthMax` int(4) not null default 0,
        `healthMin` int(4) not null default 0, 
        `repIntvEnd` varchar(255) default null,
        `repIntvStart` varchar(255) default null,
        `node_id` int(4) not null default 0,
        `time_exec` datetime not null default '0000-00-00 00:00:00',
        PRIMARY KEY(`unique`),
        UNIQUE KEY `node_id` (`node_id`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

schema_supervisora_status = """
    CREATE TABLE IF NOT EXISTS supervisora_status(
        `unique` int(11) not null auto_increment,
        `descr` varchar(255) default null,
        `hwVer` varchar(255) default null,
        `macB` varchar(255) default null,
        `macL` varchar(255) default null,
        `model` varchar(255) default null,
        `operSt` varchar(255) default null,
        `pwrSt` varchar(255) default null,
        `rdSt` varchar(255) default null,
        `rev` varchar(255) default null,
        `ser` varchar(255) default null,
        `swCId` varchar(255) default null,
        `type` varchar(255) default null,
        `vendor` varchar(255) default null,
        `uid` varchar(255) default null,
        `node_id` int(4) default null,
        `time_exec` datetime not null default '0000-00-00 00:00:00',
        PRIMARY KEY(`unique`),
        UNIQUE KEY `uid` (`uid`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

schema_status_power = """
    CREATE TABLE IF NOT EXISTS status_power(
        `unique` int(11) not null auto_increment,
        `almReg` varchar(255) default null,
        `cap` varchar(255) default null,
        `descr` varchar(255) default null,
        `fatOpSt` varchar(255) default null,
        `hwVer` varchar(255) default null,
        `id` int(11) not null default 0,
        `model` varchar(255) default null,
        `operSt` varchar(255) default null,
        `rev` varchar(255) default null,
        `ser` varchar(255) default null,
        `status` varchar(255) default null,
        `vSrc` varchar(255) default null,
        `vendor` varchar(255) default null,
        `volt` varchar(255) default null,
        `uid` varchar(255) default null,
        `node_id` int(11) not null default 0,
        `time_exec` datetime not null default '0000-00-00 00:00:00',
        PRIMARY KEY (`unique`),
        UNIQUE KEY `uid` (`uid`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

schema_status_fan = """
    CREATE TABLE IF NOT EXISTS status_fan(
        `unique` int(11) not null auto_increment,
        `descr` varchar(255) default null,
        `fanName` varchar(255) default null,
        `fanletFailString` varchar(255) default null,
        `id` int(11) not null default 0,
        `model` varchar(255) default null,
        `operSt` varchar(255) default null,
        `rev` varchar(255) default null,
        `ser` varchar(255) default null,
        `status` varchar(255) default null,
        `vendor` varchar(255) default null,
        `uid` varchar(255) default null,
        `node_id` int(4) not null default 0,
        `time_exec` datetime not null default '0000-00-00 00:00:00',
        PRIMARY KEY(`unique`),
        UNIQUE KEY `uid` (`uid`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

schema_interfaces_aci = """
    CREATE TABLE IF NOT EXISTS `interfaces` (
        `unique` int(11) NOT NULL AUTO_INCREMENT,
        `adminSt` varchar(10) DEFAULT NULL,
        `autoNeg` varchar(10) DEFAULT NULL,
        `brkoutMap` varchar(10) DEFAULT NULL,
        `bw` varchar(10) DEFAULT NULL,
        `childAction` varchar(10) DEFAULT NULL,
        `delay` varchar(10) DEFAULT NULL,
        `descr` varchar(100) DEFAULT NULL,
        `dn` varchar(50) DEFAULT NULL,
        `dot1qEtherType` varchar(10) DEFAULT NULL,
        `ethpmCfgFailedBmp` varchar(50) DEFAULT NULL,
        `ethpmCfgFailedTs` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
        `ethpmCfgState` varchar(50) DEFAULT NULL,
        `fcotChannelNumber` varchar(255) DEFAULT NULL,
        `fecMode` varchar(255) DEFAULT NULL,
        `id` varchar(255) DEFAULT NULL,
        `inhBw` varchar(255) DEFAULT NULL,
        `isReflectiveRelayCfgSupported` varchar(255) DEFAULT NULL,
        `layer` varchar(255) DEFAULT NULL,
        `lcOwn` varchar(255) DEFAULT NULL,
        `linkDebounce` varchar(255) DEFAULT NULL,
        `linkLog` varchar(255) DEFAULT NULL,
        `mdix` varchar(255) DEFAULT NULL,
        `medium` varchar(255) DEFAULT NULL,
        `modTs` varchar(255) DEFAULT NULL,
        `mode` varchar(255) DEFAULT NULL,
        `monPolDn` varchar(255) DEFAULT NULL,
        `mtu` varchar(255) DEFAULT NULL,
        `name` varchar(255) DEFAULT NULL,
        `pathSDescr` varchar(255) DEFAULT NULL,
        `portT` varchar(255) DEFAULT NULL,
        `prioFlowCtrl` varchar(255) DEFAULT NULL,
        `reflectiveRelayEn` varchar(255) DEFAULT NULL,
        `routerMac` varchar(255) DEFAULT NULL,
        `snmpTrapSt` varchar(255) DEFAULT NULL,
        `spanMode` varchar(255) DEFAULT NULL,
        `speed` varchar(255) DEFAULT NULL,
        `status` varchar(255) DEFAULT NULL,
        `switchingSt` varchar(25) DEFAULT NULL,
        `trunkLog` varchar(255) DEFAULT NULL,
        `usage` varchar(255) DEFAULT NULL,
        `accessVlan` varchar(255) DEFAULT NULL,
        `allowedVlans` LONGTEXT DEFAULT NULL,
        `backplaneMac` varchar(255) DEFAULT NULL,
        `bundleBupId` varchar(255) DEFAULT NULL,
        `bundleIndex` varchar(255) DEFAULT NULL,
        `cfgAccessVlan` varchar(255) DEFAULT NULL,
        `cfgNativeVlan` varchar(255) DEFAULT NULL,
        `currErrIndex` varchar(255) DEFAULT NULL,
        `diags` varchar(255) DEFAULT NULL,
        `encap` varchar(255) DEFAULT NULL,
        `errDisTimerRunning` varchar(255) DEFAULT NULL,
        `errVlanStatusHt` varchar(255) DEFAULT NULL,
        `errVlans` varchar(255) DEFAULT NULL,
        `hwBdId` varchar(255) DEFAULT NULL,
        `hwResourceId` varchar(255) DEFAULT NULL,
        `intfT` varchar(255) DEFAULT NULL,
        `iod` varchar(255) DEFAULT NULL,
        `lastErrors` varchar(255) DEFAULT NULL,
        `lastLinkStChg` varchar(255) DEFAULT NULL,
        `media` varchar(255) DEFAULT NULL,
        `nativeVlan` varchar(255) DEFAULT NULL,
        `numOfSI` varchar(255) DEFAULT NULL,
        `operBitset` varchar(255) DEFAULT NULL,
        `operDceMode` varchar(255) DEFAULT NULL,
        `operDuplex` varchar(255) DEFAULT NULL,
        `operEEERxWkTime` varchar(255) DEFAULT NULL,
        `operEEEState` varchar(255) DEFAULT NULL,
        `operEEETxWkTime` varchar(255) DEFAULT NULL,
        `operErrDisQual` varchar(255) DEFAULT NULL,
        `operFecMode` varchar(255) DEFAULT NULL,
        `operFlowCtrl` varchar(255) DEFAULT NULL,
        `operMdix` varchar(255) DEFAULT NULL,
        `operMode` varchar(255) DEFAULT NULL,
        `operModeDetail` varchar(255) DEFAULT NULL,
        `operPhyEnSt` varchar(255) DEFAULT NULL,
        `operRouterMac` varchar(255) DEFAULT NULL,
        `operSpeed` varchar(255) DEFAULT NULL,
        `operSt` varchar(255) DEFAULT NULL,
        `operStQual` varchar(255) DEFAULT NULL,
        `operStQualCode` varchar(255) DEFAULT NULL,
        `operVlans` LONGTEXT DEFAULT NULL,
        `osSum` varchar(255) DEFAULT NULL,
        `portCfgWaitFlags` varchar(255) DEFAULT NULL,
        `primaryVlan` varchar(255) DEFAULT NULL,
        `resetCtr` varchar(255) DEFAULT NULL,
        `rn` varchar(255) DEFAULT NULL,
        `siList` varchar(255) DEFAULT NULL,
        `txT` varchar(255) DEFAULT NULL,
        `userCfgdFlags` varchar(255) DEFAULT NULL,
        `vdcId` varchar(255) DEFAULT NULL,
        `node_id` int(4) not null default 0,
        `time_exec` datetime not null default '0000-00-00 00:00:00',
        PRIMARY KEY (`unique`),
        UNIQUE KEY `dn` (`dn`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

schema_correlation_profile_interface = """
    CREATE TABLE IF NOT EXISTS `correlation_profile_interface` (
        `unique` int(11) NOT NULL AUTO_INCREMENT,
        `name_leaf` varchar(100) DEFAULT NULL,
        `name_profile` varchar(100) DEFAULT NULL,
        `int_one` varchar(10) DEFAULT NULL,
        `int_two` varchar(10) DEFAULT NULL,
        `uid` varchar(255) DEFAULT NULL,
        `time_exec` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
        PRIMARY KEY (`unique`),
        UNIQUE KEY `uid` (`uid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

schema_correlation_profile_pg = """
    CREATE TABLE IF NOT EXISTS `correlation_profile_pg` (
        `unique` int(11) NOT NULL AUTO_INCREMENT,
        `name_profile` varchar(100) DEFAULT NULL,
        `name_pg` varchar(100) DEFAULT NULL,
        `name_leaf` varchar(50) DEFAULT NULL,
        `time_exec` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
        PRIMARY KEY (`unique`),
        UNIQUE KEY `name_profile` (`name_profile`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

schema_leaf_access = """
    CREATE TABLE IF NOT EXISTS `leaf_access` (
        `unique` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(100) DEFAULT NULL,
        `uid` int(11) DEFAULT '0',
        `cdp_status` varchar(50) DEFAULT NULL,
        `vel_neg` varchar(50) DEFAULT NULL,
        `lldp_status` varchar(50) DEFAULT NULL,
        `mcp_status` varchar(50) DEFAULT NULL,
        `mon_status` varchar(50) DEFAULT NULL,
        `storm_status` varchar(50) DEFAULT NULL,
        `stp_status` varchar(50) DEFAULT NULL,
        `time_exec` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
        PRIMARY KEY (`unique`),
        UNIQUE KEY `name` (`name`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

def create_schema():
    query_array_schema = [schema_sql_inventory, schema_sql_partitions_controller, schema_health_nodes, schema_supervisora_status, schema_status_power,
                            schema_interfaces_aci, schema_correlation_profile_interface, schema_correlation_profile_pg, schema_leaf_access]
    con.operational_sql_exec_query(*query_array_schema)

# ejecutando consultas para crear los esquemas en la base de datos
if __name__ == '__main__':
    create_schema()
