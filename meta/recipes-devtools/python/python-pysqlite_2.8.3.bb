SUMMARY = "Python library used by bitbake for DB-API 2.0 for SQLite 3.x"
HOMEPAGE = "http://github.com/gitpython-developers/GitPython"
SECTION = "devel/python"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=28ad4f115e06c88bd737372a453369d8"

inherit setuptools pypi

SRC_URI[md5sum] = "033f17b8644577715aee55e8832ac9fc"

DEPENDS = "${PYTHON_PN}-pip"

FILES_${PN} += "${datadir}/*"

BBCLASSEXTEND = "nativesdk"
