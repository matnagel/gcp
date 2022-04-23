.PHONY: test deploy

test:
	tox

billing_nuke.zip: main.py requirements.txt wrapper/cloudbilling.py wrapper/environment_variables.py
	git archive -o billing_nuke.zip HEAD main.py requirements.txt wrapper/cloudbilling.py wrapper/environment_variables.py
	echo "commit hash removed." | zip -qz billing_nuke.zip

deploy: billing_nuke.zip
	sha256sum billing_nuke.zip
