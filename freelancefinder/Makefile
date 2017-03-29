
all: check

doccheck:
	pydocstyle --match-dir='(?!migrations).*'

codecheck:
	pycodestyle --ignore=E501 .

lintcheck:
	PYLINTFILES=$$(find . | grep "py$$" | grep -v "lib\|public" | cut -f2 -d"/" | uniq | xargs); pylint $${PYLINTFILES}

reqcheck:
	pip list --outdated --format=columns; NUM=$$(pip list --outdated --format=columns | wc -l); [ $$NUM -lt 5 ] && (echo "Requirements test: pass" && exit 0) || (echo "Requirements test: fail" && exit 1)

serve:
        python manage.py runserver 0.0.0.0:8181

check: reqcheck doccheck codecheck lintcheck
