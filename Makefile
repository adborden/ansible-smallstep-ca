.PHONY: test

test:
	cd roles/smallstep_ca && poetry run molecule test
