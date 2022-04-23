.PHONY: test deploy

test:
	tox

FILES := main.py requirements.txt wrapper/cloud_billing.py wrapper/environment_variables.py

billing_nuke.zip: ${FILES}
	git archive -o billing_nuke.zip HEAD ${FILES}
	echo "commit hash removed." | zip -qz billing_nuke.zip

deploy: billing_nuke.zip
	sha256sum billing_nuke.zip
