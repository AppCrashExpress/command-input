import command_line.trie as trie

class CommandLine():
    def __init__(self, commands=None, attributes=None):
        self.command_trie = trie.Trie()
        self.help_strings = dict()
        self.should_exit = False

        if commands is not None:
            for comm in commands:
                self.insert_command(comm["command"], 
                                    comm["function"],
                                    comm["help_string"])

        self.insert_command("help",
                            lambda self=self : self.print_help(),
                            "Outputs help")

        self.insert_command("exit",
                            lambda self=self : self.toggle_exit(),
                            "Exit the command line")

        if attributes is not None:
            for attr in attributes:
                self.insert_attribute(attr["value"],
                                      attr["checker"],
                                      attr["function"])

    def insert_command(self, command, function, help_string):
        self.command_trie.insert(command, function)
        self.append_help(command, help_string)

    def insert_attribute(self, value, checker, function):
        self.command_trie.insert_attribute(value, checker, function)

    def append_help(self, command, help_str):
        self.help_strings[command] = help_str

    def print_help(self):
        s     = [[comm, help_str] for comm, help_str in self.help_strings.items()]
        lens  = [max(map(len, col)) for col in zip(*s)]
        fmt   = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))

    def do(self, command):
        try:
            return self.command_trie.exec(command)
        except trie.CommandError as err:
            print(err)

    def toggle_exit(self):
        self.should_exit = not self.should_exit

    def check_exit(self):
        return self.should_exit
