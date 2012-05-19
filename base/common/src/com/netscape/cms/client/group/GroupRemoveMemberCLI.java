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

import com.netscape.cms.client.cli.CLI;
import com.netscape.cms.client.cli.MainCLI;

/**
 * @author Endi S. Dewata
 */
public class GroupRemoveMemberCLI extends CLI {

    public GroupCLI parent;

    public GroupRemoveMemberCLI(GroupCLI parent) {
        super("remove-member", "Remove group member");
        this.parent = parent;
    }

    public void printHelp() {
        formatter.printHelp(parent.name + "-" + name + " <Group ID> <Member ID> [OPTIONS...]", options);
    }

    public void execute(String[] args) throws Exception {

        if (args.length != 2) {
            printHelp();
            System.exit(1);
        }

        String groupID = args[0];
        String memberID = args[1];

        parent.client.removeGroupMember(groupID, memberID);

        MainCLI.printMessage("Deleted group member \""+memberID+"\"");
    }
}
