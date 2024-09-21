.PHONY: run

run:
	@python src/todocli_python/tasks.py $(ARGS)

help:
	@echo "Usage:"
	@echo "make run ARGS='arg1 arg2 ...' - to run the Python script with arguments"
