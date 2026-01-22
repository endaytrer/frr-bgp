from typing import override
from mininet.cli import CLI
from mininet.log import error
import sys

class FrrCLI(CLI):
    helpStr = (
        'You may also send a network command to a node using:\n'
        '  <node> command {args}\n'
        'For example:\n'
        '  mininet> h1 show ip bgp\n'
        '\n'
        'If you want to send a shell command to node, use `sh` beforehands:\n'
        '  <node> bash command {args}\n'
        'For example:\n'
        '  mininet> h1 sh ifconfig\n'
        '\n'
        'The interpreter automatically substitutes IP addresses\n'
        'for node names when a node is the first arg, so commands\n'
        'like\n'
        '  mininet> h2 ping h3\n'
        'should work.\n'
        '\n'
        'Some character-oriented interactive commands require\n'
        'noecho:\n'
        '  mininet> noecho h2 vi foo.py\n'
        'However, starting up an xterm/gterm is generally better:\n'
        '  mininet> xterm h2\n\n'
    )
    def __init__(self, mininet, stdin=sys.stdin, script=None,
                 *args, **kwargs):
        super().__init__(mininet, stdin, script, *args, **kwargs)
        
    @override
    def default(self, line):
        first, args, line = self.parseline( line )
        
        if first in self.mn:
            if not args:
                error( '*** Please enter a command for node: %s <cmd>\n'
                       % first )
                return
            node = self.mn[ first ]
            rest = args.split( ' ' )
            
            if rest[0] != 'sh':
                rest = f"vtysh -c '{' '.join(rest)}'"
                node.sendCmd( rest )
                self.waitForNode( node )
                return
            else:
                rest = rest[1:]
                # Substitute IP addresses for node names in command
                # If updateIP() returns None, then use node name
                rest = [ self.mn[ arg ].defaultIntf().updateIP() or arg
                         if arg in self.mn else arg
                         for arg in rest ]
                rest_cmd = ' '.join(rest).replace("'", "\\'")
                rest = f"sh -c '{rest_cmd}'"
                node.sendCmd( rest )
                self.waitForNode( node )

        else:
            error( '*** Unknown command: %s\n' % line )