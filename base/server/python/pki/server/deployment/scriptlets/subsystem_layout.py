# Authors:
#     Matthew Harmsen <mharmsen@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2012 Red Hat, Inc.
# All rights reserved.
#

from __future__ import absolute_import
import logging

# PKI Deployment Imports
from .. import pkiconfig as config
from .. import pkiscriptlet

logger = logging.getLogger('subsystem')


# PKI Deployment Subsystem Layout Scriptlet
class PkiScriptlet(pkiscriptlet.AbstractBasePkiScriptlet):

    def spawn(self, deployer):

        if config.str2bool(deployer.mdict['pki_skip_installation']):
            logger.info('Skipping subsystem creation')
            return

        logger.info('Creating %s subsystem', deployer.mdict['pki_subsystem'])

        # establish instance-based subsystem logs
        deployer.directory.create(deployer.mdict['pki_subsystem_log_path'])
        deployer.directory.create(
            deployer.mdict['pki_subsystem_archive_log_path'])
        deployer.directory.create(
            deployer.mdict['pki_subsystem_signed_audit_log_path'])

        # create /var/lib/pki/<instance>/<subsystem>/conf
        logger.info('Creating %s', deployer.mdict['pki_subsystem_configuration_path'])
        deployer.directory.create(
            deployer.mdict['pki_subsystem_configuration_path'])

        # deployer.directory.copy(
        #   deployer.mdict['pki_source_conf_path'],
        #   deployer.mdict['pki_subsystem_configuration_path'])

        # create /var/lib/pki/<instance>/<subsystem>/conf/CS.cfg
        logger.info('Creating %s', deployer.mdict['pki_target_cs_cfg'])
        deployer.file.copy_with_slot_substitution(
            deployer.mdict['pki_source_cs_cfg'],
            deployer.mdict['pki_target_cs_cfg'])

        # establish instance-based Tomcat specific subsystems

        # establish instance-based Tomcat PKI subsystem base
        if deployer.mdict['pki_subsystem'] == "CA":

            logger.info('Creating %s', deployer.mdict['pki_subsystem_emails_path'])
            deployer.directory.copy(
                deployer.mdict['pki_source_emails'],
                deployer.mdict['pki_subsystem_emails_path'])

            logger.info('Creating %s', deployer.mdict['pki_subsystem_profiles_path'])
            deployer.directory.copy(
                deployer.mdict['pki_source_profiles'],
                deployer.mdict['pki_subsystem_profiles_path'])

            logger.info('Creating %s', deployer.mdict['pki_target_flatfile_txt'])
            deployer.file.copy(
                deployer.mdict['pki_source_flatfile_txt'],
                deployer.mdict['pki_target_flatfile_txt'])

            logger.info('Creating %s', deployer.mdict['pki_target_registry_cfg'])
            deployer.file.copy(
                deployer.mdict['pki_source_registry_cfg'],
                deployer.mdict['pki_target_registry_cfg'])

            logger.info('Creating bootstrap profiles')
            deployer.file.copy(
                deployer.mdict['pki_source_admincert_profile'],
                deployer.mdict['pki_target_admincert_profile'])
            deployer.file.copy(
                deployer.mdict['pki_source_caauditsigningcert_profile'],
                deployer.mdict['pki_target_caauditsigningcert_profile'])
            deployer.file.copy(
                deployer.mdict['pki_source_cacert_profile'],
                deployer.mdict['pki_target_cacert_profile'])
            deployer.file.copy(
                deployer.mdict['pki_source_caocspcert_profile'],
                deployer.mdict['pki_target_caocspcert_profile'])
            deployer.file.copy(
                deployer.mdict['pki_source_servercert_profile'],
                deployer.mdict['pki_target_servercert_profile'])
            deployer.file.copy(
                deployer.mdict['pki_source_subsystemcert_profile'],
                deployer.mdict['pki_target_subsystemcert_profile'])
            deployer.file.copy_with_slot_substitution(
                deployer.mdict['pki_source_proxy_conf'],
                deployer.mdict['pki_target_proxy_conf'])

        elif deployer.mdict['pki_subsystem'] == "TPS":
            deployer.file.copy_with_slot_substitution(
                deployer.mdict['pki_source_registry_cfg'],
                deployer.mdict['pki_target_registry_cfg'])
            deployer.file.copy_with_slot_substitution(
                deployer.mdict['pki_source_phone_home_xml'],
                deployer.mdict['pki_target_phone_home_xml'])

        # establish instance-based subsystem convenience symbolic links
        deployer.symlink.create(
            deployer.mdict['pki_instance_database_link'],
            deployer.mdict['pki_subsystem_database_link'])
        deployer.symlink.create(
            deployer.mdict['pki_subsystem_configuration_path'],
            deployer.mdict['pki_subsystem_conf_link'])
        deployer.symlink.create(
            deployer.mdict['pki_subsystem_log_path'],
            deployer.mdict['pki_subsystem_logs_link'])
        deployer.symlink.create(
            deployer.mdict['pki_instance_registry_path'],
            deployer.mdict['pki_subsystem_registry_link'])

    def destroy(self, deployer):

        logger.info('Removing %s subsystem', deployer.mdict['pki_subsystem'])

        # remove instance-based subsystem base
        if deployer.mdict['pki_subsystem'] == "CA":
            deployer.directory.delete(
                deployer.mdict['pki_subsystem_emails_path'])
            deployer.directory.delete(
                deployer.mdict['pki_subsystem_profiles_path'])
        deployer.directory.delete(deployer.mdict['pki_subsystem_path'])
        # remove instance-based subsystem logs only if --remove-logs flag is specified
        if deployer.mdict['pki_remove_logs']:
            deployer.directory.delete(
                deployer.mdict['pki_subsystem_signed_audit_log_path'])
            deployer.directory.delete(
                deployer.mdict['pki_subsystem_archive_log_path'])
            deployer.directory.delete(
                deployer.mdict['pki_subsystem_log_path'])

        # remove instance-based subsystem configuration
        deployer.directory.delete(
            deployer.mdict['pki_subsystem_configuration_path'])
        # remove instance-based subsystem registry
        deployer.directory.delete(
            deployer.mdict['pki_subsystem_registry_path'])
