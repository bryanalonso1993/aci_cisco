#!/usr/env bin python3.8

# define query params aci

query_params_aci = {
    "inventory": "mo/topology/pod-1.json?query-target=children&target-subtree-class=fabricNode&query-target-filter=and"
                "(not(wcard(fabricNode.dn,%22__ui_%22)),and(ne(fabricNode.role,\"controller\")))",
    "leaf_access_port": "mo/uni/infra/funcprof.json?query-target=subtree&target-subtree-class=infraAccPortGrp&"
                        "query-target-filter=not(wcard(infraAccPortGrp.dn,\"__ui_\"))&rsp-subtree=children&"
                        "rsp-subtree-class=infraRsCdpIfPol,infraRsHIfPol,infraRsLldpIfPol,infraRsMonIfInfraPol,"
                        "infraRsStpIfPol,infraRsMcpIfPol,infraRsStormctrlIfPol",
    "policy_group": "class/infraAccBaseGrp.json?",
    "interface_node": lambda node_id: "class/topology/pod-1/node-{}/l1PhysIf.json?rsp-subtree=children&"
                                    "rsp-subtree-class=ethpmPhysIf&order-by=l1PhysIf.monPolDn|asc".format(node_id),
    "supervisora_status": lambda node_id: "mo/topology/pod-1/node-{}.json?query-target=subtree&"
                                        "target-subtree-class=eqptSupC".format(node_id),
    "power_status": lambda node_id: "mo/topology/pod-1/node-{}/sys/ch.json?query-target=subtree&target-subtree-class"
                                    "=eqptPsu".format(node_id),
    "fan_status": lambda node_id: "mo/topology/pod-1/node-{}/sys/ch.json?query-target=subtree&target-subtree-class"
                                "=eqptFt".format(node_id),
    "partitions_controller": lambda node_id: "class/topology/pod-1/node-{}/eqptStorage.json?".format(node_id),
    "health_nodes": lambda node_id: "mo/topology/pod-1/node-{}/sys/HDfabricNodeHealth5min-0.json".format(node_id),
    "traffic_egr_total": lambda node_id, interface_id: "mo/topology/pod-1/node-{}/sys/phys-[{}]/"
                                                    "HDeqptEgrTotal5min-0.json".format(node_id, interface_id),
    "traffic_ingr_total": lambda node_id, interface_id: "mo/topology/pod-1/node-{}/sys/phys-[{}]/"
                                                        "HDeqptIngrTotal5min-0.json".format(node_id, interface_id),
    "pc_interface": "mo/uni/infra/funcprof.json?query-target=subtree&target-subtree-class=infraAccBndlGrp&"
                    "query-target-filter=and(not(wcard(infraAccBndlGrp.dn,\"__ui_\")),"
                    "not(eq(infraAccBndlGrp.lagT,\"node\")))&rsp-subtree=children&rsp-subtree-class=infraRsCdpIfPol,"
                    "infraRsMcpIfPol,infraRsHIfPol,infraRsLldpIfPol,infraRsLacpPol,infraAccBndlSubgrp,infraRsStpIfPol,"
                    "infraRsSpanVSrcGrp,infraRsSpanVDestGrp,infraRsL2IfPol,infraRsStormctrlIfPol",
    "vpc_interface": "mo/uni/infra/funcprof.json?query-target=subtree&target-subtree-class=infraAccBndlGrp"
                    "&query-target-filter=and(not(wcard(infraAccBndlGrp.dn,\"__ui_\")),"
                    "not(eq(infraAccBndlGrp.lagT,\"link\")))&rsp-subtree=children&rsp-subtree-class=infraRsCdpIfPol,"
                    "infraRsHIfPol,infraRsLldpIfPol,infraRsLacpPol,infraAccBndlSubgrp,infraRsStpIfPol,"
                    "infraRsSpanVSrcGrp,infraRsSpanVDestGrp,infraRsStormctrlIfPol",
    "correlation_profile_interface": "mo/uni/infra.json?query-target=children&target-subtree-class=infraAccPortP,"
                                    "infraFexP&query-target-filter=and(not(wcard(infraAccPortP.dn,%22__ui_%22)),"
                                    "not(wcard(infraFexP.dn,%22__ui_%22)))&rsp-subtree=full&rsp-subtree-class="
                                    "infraHPortS,infraPortBlk,infraSubPortBlk",
    "correlation_profile_pg": lambda node_id: "mo/uni/infra/accportprof-{}.json?query-target=subtree&"
                                            "query-target-filter=not(wcard(infraHPortS.dn,\"__ui_\"))&target-"
                                            "subtree-class=infraRsAccBaseGrp&query-target=subtree".format(node_id)
}
