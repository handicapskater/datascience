.PHONY: smoke-test-legal-imports
smoke-test-legal-imports:
	python legal/scripts/smoke_test_legal_imports.py

.PHONY: reproduce-filed-exhibit-a
reproduce-filed-exhibit-a:
	bash legal/scripts/reproduce_filed_exhibit_a.sh

.PHONY: check-filed-exhibit-a-lock
check-filed-exhibit-a-lock:
	python legal/scripts/check_filed_exhibit_a_lock.py

.PHONY: update-filed-exhibit-a-lock
update-filed-exhibit-a-lock:
	python legal/scripts/check_filed_exhibit_a_lock.py --update
