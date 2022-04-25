.PHONY: test deploy

test:
	tox

FILES := main.py requirements.txt wrapper/cloud_billing.py wrapper/environment_variables.py

billing_nuke.zip: ${FILES}
	touch -t 202204251730 ${FILES}
	zip -o billing_nuke.zip ${FILES}

deploy: billing_nuke.zip
	sha256sum billing_nuke.zip
