class CommandError(ValueError):
    pass

class Trie():
    def __init__(self):
        self.trie_dict = {}
        self.attr_dict = {}

    def insert(self, command, func):
        tokens = command.split()
        if len(tokens) == 0:
            raise ValueError("Cannot insert empty command")

        iterator = self.trie_dict
        for token in tokens:
            iterator = iterator.setdefault(token, dict())

        iterator["_callback_"] = func

    def insert_attribute(self, atr_val, check, func):
        self.attr_dict[atr_val] = {}
        self.attr_dict[atr_val]["check"] = check
        self.attr_dict[atr_val]["do"] = func

    def exec(self, command):
        values = []

        tokens = command.split()
        if len(tokens) == 0:
            raise ValueError("Cannot insert empty command")

        iterator = self.trie_dict
        for token in tokens:
            try:
                iterator = iterator[token]
            except KeyError:
                attributed = False

                for attr, funcs in self.attr_dict.items():
                    subtree = iterator.get(attr)
                    if subtree is None:
                        continue
                    if not funcs["check"](token):
                        continue
                    values.append(funcs["do"](token))
                    iterator = subtree
                    attributed = True

                if not attributed:
                    raise CommandError(f"No matching token found: {token}")

        return iterator["_callback_"](*values)
               
                    

