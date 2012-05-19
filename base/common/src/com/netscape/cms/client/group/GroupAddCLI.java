// --- BEGIN COPYRIGHT BLOCK ---
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; version 2 of the License.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with this program; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//
// (C) 2012 Red Hat, Inc.
// All rights reserved.
// --- END COPYRIGHT BLOCK ---

package com.netscape.cms.client.group;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.Option;

import com.netscape.certsrv.group.GroupData;
import com.netscape.cms.client.cli.CLI;
import com.netscape.cms.client.cli.MainCLI;

/**
 * @author Endi S. Dewata
 */
public class GroupAddCLI extends CLI {

    public GroupCLI parent;

    public GroupAddCLI(GroupCLI parent) {
        super("add", "Add group");
        this.parent = parent;
    }

    public void printHelp() {
        formatter.printHelp(parent.name + "-" + name + " <Group ID> [OPTIONS...]", options);
    }

    public void execute(String[] args) throws Exception {

        Option option = new Option(null, "description", true, "Description");
        option.setArgName("description");
        option.setRequired(true);
        options.addOption(option);

        CommandLine cmd = null;

        try {
            cmd = parser.parse(options, args);

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            printHelp();
            System.exit(1);
        }

        String[] cmdArgs = cmd.getArgs();

        if (cmdArgs.length != 1) {
            printHelp();
            System.exit(1);
        }

        String groupID = cmdArgs[0];

        GroupData groupData = new GroupData();
        groupData.setID(groupID);
        groupData.setDescription(cmd.getOptionValue("description"));

        groupData = parent.client.addGroup(groupData);

        MainCLI.printMessage("Added group \""+groupID+"\"");

        GroupCLI.printGroup(groupData);
    }
}
