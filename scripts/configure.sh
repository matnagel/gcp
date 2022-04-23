#!/bin/sh

set -e
[ -z "$CONFIG_BUCKET" ] && echo "Need to set CONFIG_BUCKET" && exit 1;
echo "Loading terraform configuration from bucket: $CONFIG_BUCKET"
gsutil -q cp gs://$CONFIG_BUCKET/terraform-backend.conf terraform/env/backend.conf
gsutil -q cp gs://$CONFIG_BUCKET/terraform-custom.tvars terraform/env/custom.tvars
