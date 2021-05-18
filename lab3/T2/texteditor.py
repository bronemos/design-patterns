from abc import ABC
import tkinter as tk
import tkinter.font as tkfont
from typing import Iterator, List
from copy import deepcopy


class Location:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x):
        self.__x = x

    @y.setter
    def y(self, y):
        self.__y = y


class LocationRange:
    def __init__(self, start: Location, end: Location):
        self.__start = start
        self.__end = end

    @property
    def start(self) -> Location:
        return self.__start

    @property
    def end(self) -> Location:
        return self.__end


class ClipboardObserver:
    def update_clipboard(self):
        raise NotImplementedError


class ClipboardStack:
    def __init__(self):
        self.__clipboard_observers: List[ClipboardObserver] = list()
        self.__stack: List[str] = list()

    def push(self, text: str) -> None:
        self.__stack.append(text)

    def pop(self) -> str:
        return self.__stack.pop()

    def top(self) -> str:
        return self.__stack[-1]

    def is_empty(self) -> bool:
        return len(self.__stack) == 0

    def attach_clipboard_observer(self, clipboard_observer: ClipboardObserver) -> None:
        self.__clipboard_observers.append(clipboard_observer)

    def detach_clipboard_observer(self, clipboard_observer: ClipboardObserver) -> None:
        self.__clipboard_observers.remove(clipboard_observer)

    def notify_clipboard(self):
        [
            clipboard_observer.update_clipboard()
            for clipboard_observer in self.__clipboard_observers
        ]


class EditAction:
    def execute_do(self):
        raise NotImplementedError

    def execute_undo(self):
        raise NotImplementedError


class UndoManager:
    def __init__(self):
        self.__undo_stack: List[EditAction] = list()
        self.__redo_stack: List[EditAction] = list()

    def undo(self) -> None:
        fun = self.__undo_stack.pop()
        fun.execute_undo()
        self.__redo_stack.append(fun)

    def push(self, fun: EditAction) -> None:
        self.__redo_stack = list()
        self.__undo_stack.append(fun)


class CursorObserver:
    def update_cursor_location(self, loc: Location) -> None:
        raise NotImplementedError


class TextObserver:
    def update_text(self) -> None:
        raise NotImplementedError


class TextEditorModel:
    def __init__(self, lines_string: str):
        self.__lines = lines_string.split("\n")
        self.__selection_range = LocationRange(Location(0, 0), Location(0, 0))
        self.__cursor_location = Location(len(self.__lines[-1]), len(self.__lines) - 1)
        self.__cursor_observers: List[CursorObserver] = list()
        self.__text_observers: List[TextObserver] = list()

    @property
    def selection_range(self) -> LocationRange:
        return self.__selection_range

    @selection_range.setter
    def selection_range(self, range: LocationRange) -> None:
        self.__selection_range = range

    def all_lines(self) -> Iterator:
        return iter(self.__lines)

    def lines_range(self, index_1: int, index_2: int) -> Iterator:
        return iter(self.__lines[index_1:index_2])

    def attach_cursor_observer(self, cursor_observer: CursorObserver) -> None:
        self.__cursor_observers.append(cursor_observer)
        self.notify_cursor()

    def detach_cursor_observer(self, cursor_observer: CursorObserver) -> None:
        self.__cursor_observers.remove(cursor_observer)

    def attach_text_observer(self, text_observer: TextObserver) -> None:
        self.__text_observers.append(text_observer)
        self.notify_text()

    def detach_text_observer(self, text_observer: TextObserver) -> None:
        self.__text_observers.remove(text_observer)

    def notify_cursor(self) -> None:
        [
            cursor_observer.update_cursor_location(self.__cursor_location)
            for cursor_observer in self.__cursor_observers
        ]

    def notify_text(self) -> None:
        [text_observer.update_text() for text_observer in self.__text_observers]

    def move_cursor_left(self, event: tk.Event) -> None:
        if self.__cursor_location.x > 0:
            self.__cursor_location.x -= 1
            self.notify_cursor()
        elif self.__cursor_location.x == 0 and self.__cursor_location.y > 0:
            self.__cursor_location.y -= 1
            self.notify_cursor()
        print(self.selection_range.start.x, self.selection_range.end.x)
        self.selection_range = LocationRange(
            deepcopy(self.__cursor_location), deepcopy(self.__cursor_location)
        )

    def move_cursor_right(self, event: tk.Event) -> None:
        if self.__cursor_location.x < len(self.__lines[self.__cursor_location.y]):
            self.__cursor_location.x += 1
            self.selection_range = LocationRange(
                deepcopy(self.__cursor_location), deepcopy(self.__cursor_location)
            )
            print(self.selection_range.start.x, self.selection_range.end.x)
            self.notify_cursor()

    def move_cursor_up(self, event: tk.Event) -> None:
        if self.__cursor_location.y > 0:
            self.__cursor_location.y -= 1
            if len(
                self.__lines[self.__cursor_location.y + 1][: self.__cursor_location.x]
            ) > len(self.__lines[self.__cursor_location.y]):
                self.__cursor_location.x = len(self.__lines[self.__cursor_location.y])
            self.selection_range = LocationRange(
                deepcopy(self.__cursor_location), deepcopy(self.__cursor_location)
            )
            self.notify_cursor()

    def move_cursor_down(self, event: tk.Event) -> None:
        if self.__cursor_location.y < len(self.__lines) - 1:
            self.__cursor_location.y += 1
            if len(
                self.__lines[self.__cursor_location.y - 1][: self.__cursor_location.x]
            ) > len(self.__lines[self.__cursor_location.y]):
                self.__cursor_location.x = len(self.__lines[self.__cursor_location.y])
            self.selection_range = LocationRange(
                deepcopy(self.__cursor_location), deepcopy(self.__cursor_location)
            )
            self.notify_cursor()

    def delete_before(self, event: tk.Event) -> None:
        if (
            self.selection_range.end.x - self.selection_range.start.x == 0
            and self.selection_range.end.y - self.selection_range.start.y == 0
        ):
            if self.__cursor_location.x > 0:
                self.__lines[self.__cursor_location.y] = (
                    self.__lines[self.__cursor_location.y][
                        : self.__cursor_location.x - 1
                    ]
                    + self.__lines[self.__cursor_location.y][self.__cursor_location.x :]
                )
                if (
                    len(self.__lines[self.__cursor_location.y]) == 0
                    and self.__cursor_location.y != 0
                    and self.__cursor_location.x != 0
                ):
                    del self.__lines[self.__cursor_location.y]
                    self.__cursor_location.y -= 1
                    self.__cursor_location.x = (
                        len(self.__lines[self.__cursor_location.y]) + 1
                    )
                self.move_cursor_left(event)
        else:
            print("here2")
        self.notify_text()

    def delete_after(self, event: tk.Event) -> None:
        if (
            self.selection_range.end.x - self.selection_range.start.x == 0
            and self.selection_range.end.y - self.selection_range.start.y == 0
        ):
            self.__lines[self.__cursor_location.y] = (
                self.__lines[self.__cursor_location.y][: self.__cursor_location.x]
                + self.__lines[self.__cursor_location.y][self.__cursor_location.x + 1 :]
            )
            if (
                len(self.__lines[self.__cursor_location.y]) == 0
                and self.__cursor_location.y != 0
                and self.__cursor_location.x != 0
            ):
                del self.__lines[self.__cursor_location.y]
                self.__cursor_location.y -= 1
                self.__cursor_location.x = len(self.__lines[self.__cursor_location.y])
            self.notify_cursor()
            self.notify_text()
        else:
            pass

    def delete_range(self, range: LocationRange) -> None:

        self.notify_text()

    def insert(self, event: tk.Event):
        string = event.char
        if string == "\r":
            self.__lines.insert(
                self.__cursor_location.y + 1,
                self.__lines[self.__cursor_location.y][self.__cursor_location.x :],
            )
            self.__lines[self.__cursor_location.y] = self.__lines[
                self.__cursor_location.y
            ][: self.__cursor_location.x]
            self.__cursor_location.x = 0
            self.__cursor_location.y += 1
        else:
            self.__lines[self.__cursor_location.y] = (
                self.__lines[self.__cursor_location.y][: self.__cursor_location.x]
                + string
                + self.__lines[self.__cursor_location.y][self.__cursor_location.x :]
            )
            self.__cursor_location.x += len(string)
        self.notify_text()
        self.notify_cursor()


class TextEditor(tk.Tk, CursorObserver, TextObserver):
    def __init__(self, text_editor_model: TextEditorModel):
        super().__init__()
        self.__lines = list()
        self.__padding = 4
        self.__font = tkfont.Font(family="Consolas", size=10, weight="normal")
        self.__font_width = self.__font.measure("a")
        self.__font_height = self.__font.metrics("linespace")
        self.__canvas = tk.Canvas(self)
        self.__text_editor_model = text_editor_model
        self.__cursor = self.__canvas.create_line(
            self.__padding,
            self.__padding,
            self.__padding,
            self.__font_height + self.__padding,
        )
        self.__text_editor_model.attach_cursor_observer(self)
        self.__text_editor_model.attach_text_observer(self)
        self.bind("<Up>", self.__text_editor_model.move_cursor_up)
        self.bind("<Down>", self.__text_editor_model.move_cursor_down)
        self.bind("<Right>", self.__text_editor_model.move_cursor_right)
        self.bind("<Left>", self.__text_editor_model.move_cursor_left)
        self.bind("<Shift-Up>", self.__text_editor_model.move_cursor_up)
        self.bind("<Shift-Down>", self.__text_editor_model.move_cursor_down)
        self.bind("<Shift-Right>", self.__text_editor_model.move_cursor_right)
        self.bind("<Shift-Left>", self.__text_editor_model.move_cursor_left)
        self.bind("<BackSpace>", self.__text_editor_model.delete_before)
        self.bind("<Delete>", self.__text_editor_model.delete_after)
        self.bind("<Key>", self.__text_editor_model.insert)
        self.__canvas.pack()

    def update_cursor_location(self, loc: Location) -> None:
        self.__canvas.delete(self.__cursor)
        self.__cursor = self.__canvas.create_line(
            loc.x * self.__font_width + self.__padding,
            loc.y * self.__font_height + self.__padding,
            loc.x * self.__font_width + self.__padding,
            (loc.y + 1) * self.__font_height + self.__padding,
        )

    def update_text(self) -> None:
        [self.__canvas.delete(line) for line in self.__lines]
        line_height = self.__padding
        for line in self.__text_editor_model.all_lines():
            self.__lines.append(
                self.__canvas.create_text(
                    self.__padding,
                    line_height,
                    text=line,
                    font=self.__font,
                    anchor="nw",
                )
            )
            line_height += self.__font_height


def main():
    model = TextEditorModel(
        "danas je sunce\nsutra ce kisa\npreksutra pada snijeg\nuvijek je hladno"
    )
    editor = TextEditor(model)
    editor.mainloop()


if __name__ == "__main__":
    main()
