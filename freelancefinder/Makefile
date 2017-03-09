
doccheck:
	pydocstyle --match-dir='(?!migrations).*'

codecheck:
	pycodestyle

lintcheck:
	PYLINTFILES=$$(find . | grep "py$$" | grep -v "lib\|public" | cut -f2 -d"/" | uniq | xargs); pylint $${PYLINTFILES}

check: doccheck codecheck lintcheck
