test:
	flake8 badgificator --ignore=E501,E122,E126,E128,E127
	coverage run --branch --source=badgificator `which django-admin.py` test --settings=badgificator.test_settings badgificator
	coverage report --omit=badgificator/test*

.PHONY: test
