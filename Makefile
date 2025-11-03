.PHONY: help install test validate verify demo clean

help:
	@echo "AI Mirror System - Available Commands:"
	@echo ""
	@echo "  make install   - Install dependencies"
	@echo "  make verify    - Verify LLM connection"
	@echo "  make validate  - Validate all Python scripts"
	@echo "  make test      - Run all tests"
	@echo "  make demo      - Run basic chat demo"
	@echo "  make demo-tools - Run tools demo"
	@echo "  make interactive - Start interactive chat"
	@echo "  make clean     - Clean cache and temporary files"
	@echo ""

install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Installation complete. Activate venv: source venv/bin/activate"

verify:
	. venv/bin/activate && python scripts/verify_llm.py

validate:
	. venv/bin/activate && python scripts/validate_python.py

test:
	. venv/bin/activate && pytest tests/ -v

demo:
	. venv/bin/activate && python scripts/demo_basic_chat.py

demo-tools:
	. venv/bin/activate && python scripts/demo_with_tools.py

interactive:
	. venv/bin/activate && python main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	@echo "✓ Cleanup complete"
