src_dirs := src tests

quality:
	black --check $(src_dirs)
	isort --check-only $(src_dirs)
	flake8 $(src_dirs)

style:
	black $(src_dirs)
	isort $(src_dirs)
