.PHONY: test

test:
	cd roles/smallstep_ca && poetry run molecule test
	cd roles/smallstep_cli && poetry run molecule test
