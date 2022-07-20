.PHONY: all terraform check-env

all: terraform

terraform: terraform/env/backend.conf terraform/env/custom.tvars

terraform/env/backend.conf: check-env secrets/config
	gsutil -q cp gs://${CONFIG_BUCKET}/terraform/terraform-backend.conf secrets/config/terraform-backend.conf

terraform/env/custom.tvars: check-env secrets/config
	gsutil -q cp gs://${CONFIG_BUCKET}/terraform/terraform-custom.tvars secrets/config/terraform-custom.tvars

secrets/config:
	mkdir -p secrets/config

check-env:
ifndef CONFIG_BUCKET
	$(error CONFIG_BUCKET is undefined)
endif

