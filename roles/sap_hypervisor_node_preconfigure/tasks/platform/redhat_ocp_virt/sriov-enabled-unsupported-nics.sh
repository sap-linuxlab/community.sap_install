#!/bin/bash
# in order to allow unsupported SRIOV nics such as Mellanox
oc patch sriovoperatorconfig default --type=merge  -n openshift-sriov-network-operator  --patch '{ "spec": { "enableOperatorWebhook": false } }'
