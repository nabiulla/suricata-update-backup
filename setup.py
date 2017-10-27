from setuptools import setup

import suricata

setup(
    name="suricata-updater",
    version=suricata.version,
    description="Suricata Update Tool",
    author="Jason Ish",
    author_email="ish@unx.ca",
    packages=[
        "suricata",
        "suricata.update",
        "suricata.update.rulecat",
        "suricata.update.rulecat.configs",
        "suricata.update.scripts",
        "suricata.update.compat",
        "suricata.update.compat.argparse",
    ],
    url="https://github.com/jasonish/suricata-updater",
    license="BSD",
    classifiers=[
        'License :: OSI Approved :: BSD License',
    ],
    scripts = [
        "bin/suricata-update",
    ],
)
