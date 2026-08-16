PYTHON_BIN ?= /Users/hassan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3

.PHONY: materialize-sources validate-sources audit-book validate-reader-bridge validate-print-interior qrcodes site template book master-pdf preflight release-manifest

materialize-sources:
	./scripts/materialize-sources.sh

validate-sources:
	$(PYTHON_BIN) scripts/validate_sources.py

audit-book:
	$(PYTHON_BIN) scripts/audit_book.py

validate-reader-bridge:
	$(PYTHON_BIN) scripts/validate_reader_bridge.py

qrcodes:
	$(PYTHON_BIN) scripts/generate_qr_codes.py

site:
	cd site && npm run build

template:
	./scripts/create_interior_template.sh

book: template
	./scripts/build-book.sh

master-pdf: book
	./scripts/export-interior-pdf.sh

preflight:
	$(PYTHON_BIN) scripts/preflight_pdf.py book/build/memearcade-interior.pdf

validate-print-interior:
	$(PYTHON_BIN) scripts/validate_print_interior.py

release-manifest: validate-print-interior
	$(PYTHON_BIN) scripts/release_manifest.py
