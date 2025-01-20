class UndoRedoError(Exception):
    def __init__(self):
        super().__init__("No operation to undo/redo")


class Command:
    def __init__(self, fun_name, *fun_params):
        self.__fun_name = fun_name
        self.__fun_params = fun_params

    def call(self):
        return self.__fun_name(*self.__fun_params)

    def __call__(self, *args, **kwargs):
        return self.call()


class Operation:
    def __init__(self, undo_command: Command, redo_command: Command):
        self.__undo = undo_command
        self.__redo = redo_command

    def undo(self):
        return self.__undo()

    def redo(self):
        return self.__redo()


class UndoService:
    def __init__(self):
        self.__undo = []
        self.__redo = []

    def clear(self):
        self.__undo.clear()
        self.__redo.clear()

    def register(self, operation: Operation):
        self.__undo.append(operation)
        self.__redo.clear()

    def undo(self):
        if not self.__undo:
            raise UndoRedoError

        o = self.__undo.pop()
        self.__redo.append(o)
        o.undo()

    def redo(self):
        if not self.__redo:
            raise UndoRedoError

        o = self.__redo.pop()
        self.__undo.append(o)
        o.redo()
