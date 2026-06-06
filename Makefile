.PHONY: smoke-test-legal-imports
smoke-test-legal-imports:
	python legal/scripts/smoke_test_legal_imports.py

.PHONY: check-filed-input-data-hash
check-filed-input-data-hash:
	python legal/scripts/check_filed_input_data_hash.py

.PHONY: check-filed-notebook-lock
check-filed-notebook-lock:
	python legal/scripts/check_filed_exhibit_a_lock.py

.PHONY: check-filed-artifact-locks
check-filed-artifact-locks: check-filed-input-data-hash check-filed-notebook-lock smoke-test-legal-imports

.PHONY: reproduce-filed-exhibit-a
reproduce-filed-exhibit-a:
	bash legal/scripts/reproduce_filed_exhibit_a.sh

.PHONY: check-filed-exhibit-a-lock
check-filed-exhibit-a-lock:
	python legal/scripts/check_filed_exhibit_a_lock.py

.PHONY: update-filed-exhibit-a-lock
update-filed-exhibit-a-lock:
	python legal/scripts/check_filed_exhibit_a_lock.py --update

.PHONY: verify-filed-exhibit-a
verify-filed-exhibit-a:
	python legal/scripts/verify_filed_exhibit_a.py

.PHONY: update-filed-exhibit-a-hash
update-filed-exhibit-a-hash:
	python legal/scripts/verify_filed_exhibit_a.py --update

.PHONY: hash-nontraditional-notebook
hash-nontraditional-notebook:
	python legal/scripts/hash_notebook_stable.py

.PHONY: update-nontraditional-notebook-hash
update-nontraditional-notebook-hash:
	python legal/scripts/hash_notebook_stable.py --update

.PHONY: reproduce-filed-exhibit-a-candidate
reproduce-filed-exhibit-a-candidate:
	bash legal/scripts/reproduce_filed_exhibit_a_candidate.sh

.PHONY: compare-filed-exhibit-a
compare-filed-exhibit-a:
	python legal/scripts/compare_exhibit_pdf_text.py
