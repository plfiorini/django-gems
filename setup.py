#!/usr/bin/env python

from distutils.core import setup

setup(name="django-gems",
	version="0.2.4",
	description="Django utilities library",
	author="Pier Luigi Fiorini",
	author_email="pierluigi.fiorini@gmail.com",
	packages=["django_gems", "django_gems.utils", "django_gems.templatetags"],
	package_dir={"django_gems": "django_gems"},
	license="BSD",
	platforms="Posix; MacOS X; Windows",
	classifiers=["Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Framework :: Django",
		"License :: OSI Approved :: BSD License",
		"Operating System :: OS Independent",
		"Topic :: Internet"],
	)
