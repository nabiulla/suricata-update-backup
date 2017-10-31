suricata-update - A Suricata rule update tool
=============================================

Synopsis
--------

``suricata-update`` [OPTIONS]

Description
-----------

``suricata-update`` aims to be a simple to use rule download and
management tool for Suricata.

Options
-------

.. option:: -h, --help

   Show help.

.. option:: -v, --verbose

   Be more verbose.

.. option:: -c <filename>, --config <filename>
   
   Path to the suricata-update config file.

   Default: */etc/suricata/update.yaml*

.. option:: -o, --output

   The directory to output the rules to.

   Default: */var/lib/suricata/rules*

.. option:: --cache-dir <directory>

   Directory where files are cached, such as files downloaded from a
   URL.

   Default: */var/lib/suricata/cache*

.. option:: --suricata=<path>

   The path to the Suricata program used to determine which version of
   the ET pro rules to download if not explicitly set in a ``--url``
   argument.

.. option:: --suricata-version <version>

   Set the Suricata version to a specific version instead of checking
   the version of Suricata on the path.

.. option:: --force

   Force remote rule files to be downloaded if they otherwise wouldn't
   be due to just recently downloaded, or the remote checksum matching
   the cached copy.

.. option:: --merged=<filename>

   Write a single file containing all rules. This can be used in
   addition to ``--output`` or instead of ``--output``.

.. option:: --no-merge

   Do not merge the rules into a single rule file.

   *Warning: No attempt is made to resolve conflicts if 2 input rule files have the same name.*

.. option:: --yaml-fragment=<filename.yaml>

   Output a fragment of YAML containing the *rule-files* section will
   all downloaded rule files listed for inclusion in your
   *suricata.yaml*.

.. option:: --url=<url>

   A URL to download rules from. This option can be used multiple
   times.

.. option:: --local=<filename or directory>

   A path to a filename or directory of local rule files to include.

   If the path is a directory all files ending in *.rules* will be
   loaded.

   Wildcards are accepted but to avoid shell expansion the argument
   must be quoted, for example::

     --local '/etc/suricata/custom-*.rules'

   This option can be specified multiple times.

.. option:: --sid-msg-map=<filename>

   Output a v1 style sid-msg.map file.

.. option:: --sid-msg-map-2=<filename>

   Output a v2 style sid-msg.map file.

.. option:: --disable-conf=<disable.conf>

   Specify the configuration file for disable filters.

   See :ref:`example-disable-conf`

.. option:: --enable-conf=<enable.conf>

   Specify the configuration file for enable rules.

   See :ref:`example-enable-conf`

.. option:: --modify-conf=<modify.conf>

   Specify the configuration file for rule modification filters.

   See :ref:`example-modify-conf`

.. option:: --drop-conf=<drop.conf>

   Specify the configuration file for drop filters.

   See :ref:`example-drop-conf`

.. option:: --ignore=<pattern>

   Filenames to ignore. This is a pattern that will be matched against
   the basename of a rule files.

   This argument may be specified multiple times.

   Default: *\*deleted.rules*

   Example::

     --ignore dnp3-events.rules --ignore deleted.rules --ignore "modbus*"

   .. note::

     If specified the default value of *\*deleted.rules* will no longer
     be used, so add it as an extra ignore if needed.

.. option:: --no-ignore

   Disable the --ignore option. Most useful to disable the default
   ignore pattern without adding others.

.. option:: --etopen

   Download the ET open ruleset. This is the default if ``--url`` or
   ``--etpro`` are not provided.

   If one of ``etpro`` or ``--url`` is also specified, this option
   will at the ET open URL to the list of remote ruleset to be
   downloaded.

.. option:: --etpro=<code>

   Download the ET pro ruleset using the provided code.

.. option:: -q, --quiet

   Run quietly. Only warning and error message will be displayed.

.. option:: --dump-sample-configs

   Output sample configuration files for the ``--disable``,
   ``--enable``, ``--modify`` and ``--threshold-in`` commands.

.. option:: --threshold-in=<threshold.conf.in>

   Specify the threshold.conf input template.

.. option:: --threshold-out=<threshold.conf>

   Specify the name of the processed threshold.conf to output.

.. option:: -T <command>, --test-command <command>

   Specifies a custom test command to test the rules before reloading
   Suricata. This overrides the default command and can also be
   specified in the configuration file under ``test-command``.

.. option:: --no-test

   Disables the test command and proceed as if it had passed.

.. option:: --reload-command=<command>

   A command to run after the rules have been updated; will not run if
   no change to the output files was made.  For example::

     --post-hook=sudo kill -USR2 $(cat /var/run/suricata.pid)

   will tell Suricata to reload its rules.

.. option:: --no-reload

   Disable Suricata rule reload.
	    
.. option:: -V, --version

   Display the version of **suricata-update**.

Example Configuration Files
---------------------------

Example Configuration File (/etc/suricata/update.yaml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # Configuration with disable filters.
   # - Overrided by --disable-conf
   # - Default: /etc/suricata/disable.conf
   disable-conf: /etc/suricata/disable.conf

   # Configuration with enable filters.
   # - Overrided by --enable-conf
   # - Default: /etc/suricata/enable.conf
   enable-conf: /etc/suricata/enable.conf

   # Configuration with drop filters.
   # - Overrided by --drop-conf
   # - Default: /etc/suricata/drop.conf
   drop-conf: /etc/suricata/drop.conf

   # Configuration with modify filters.
   # - Overrided by --modify-conf
   # - Default: /etc/suricata/modify.conf
   modify-conf: /etc/suricata/modify.conf

   # List of files to ignore. Overrided by the --ignore command line option.
   ignore:
     - "*deleted.rules"

   # Provide an alternate command to the default test command.
   #
   # The following environment variables can be used.
   # SURICATA_PATH - The path to the discovered suricata program.
   # OUTPUT_DIR - The directory the rules are written to.
   # OUTPUT_FILENAME - The name of the rule file. Will be empty if the rules
   #                   were not merged.
   #test-command: ${SURICATA_PATH} -T -S ${OUTPUT_FILENAME} -l /tmp

   # Provide a command to reload the Suricata rules.
   # May be overrided by the --reload-command command line option.
   #reload-command: sudo systemctl reload suricata

.. _example-enable-conf:

Example Configuration to Enable Rules (--enable-conf)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../suricata/update/configs/enable.conf

.. _example-disable-conf:

Example Configuration to Enable Disable (--disable-conf)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../suricata/update/configs/disable.conf

.. _example-drop-conf:

Example Configuration to convert Rules to Drop (--drop-conf)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../suricata/update/configs/drop.conf

.. _example-modify-conf:

Example Configuration to modify Rules (--modify-conf)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../suricata/update/configs/modify.conf
