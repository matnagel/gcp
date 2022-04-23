.PHONY: all terraform check-env

all: terraform

terraform: terraform/env/backend.conf terraform/env/custom.tvars

terraform/env/backend.conf: check-env
	gsutil -q cp gs://$CONFIG_BUCKET/terraform/terraform-backend.conf terraform/env/backend.conf

terraform/env/custom.tvars: check-env
	gsutil -q cp gs://$CONFIG_BUCKET/terraform/terraform-custom.tvars terraform/env/custom.tvars

check-env:
ifndef CONFIG_BUCKET
	$(error CONFIG_BUCKET is undefined)
endif

