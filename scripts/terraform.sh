#!/bin/sh

set -e
cd terraform/env
terraform init -backend-config="backend.conf"
terraform plan -var-file="custom.tvars" -out deployment-plan
terraform apply deployment-plan
