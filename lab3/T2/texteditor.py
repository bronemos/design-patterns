from abc import ABC
import tkinter as tk
import tkinter.font as tkfont
from typing import Iterator, Union, List


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


class CursorObserver:
    def update_cursor_location(self, loc: Location) -> None:
        raise NotImplementedError


class TextObserver:
    def update_text(self) -> None:
        raise NotImplementedError


class TextEditorModel:
    def __init__(self, lines_string: str):
        self.__lines = lines_string.split("\n")
        self.__selection_range = Location(0, 0)
        self.__cursor_location = Location(0, 0)
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

    def move_cursor_left(self, event) -> None:
        print(event)
        self.__cursor_location.x -= 1
        self.notify_cursor()

    def move_cursor_right(self, event) -> None:
        print(event)
        self.__cursor_location.x += 1
        self.notify_cursor()

    def move_cursor_up(self, event) -> None:
        print(event)
        self.__cursor_location.y -= 1
        self.notify_cursor()

    def move_cursor_down(self, event) -> None:
        print(event)
        self.__cursor_location.y += 1
        self.notify_cursor()

    def delete_before(self, event) -> None:
        self.notify_text()

    def delete_after(self, event) -> None:
        self.notify_text()

    def delete_range(self, range: LocationRange) -> None:
        self.notify_text()

    def attach_cursor_observer(self, cursor_observer: CursorObserver) -> None:
        self.__cursor_observers.append(cursor_observer)

    def attach_text_observer(self, text_observer: TextObserver) -> None:
        self.__text_observers.append(text_observer)

    def notify_cursor(self) -> None:
        [
            cursor_observer.update_cursor_location(self.__cursor_location)
            for cursor_observer in self.__cursor_observers
        ]

    def notify_text(self) -> None:
        [text_observer.update_text() for text_observer in self.__text_observers]


class TextEditor(tk.Tk, CursorObserver, TextObserver):
    def __init__(self, text_editor_model: TextEditorModel):
        super().__init__()
        self.__font = tkfont.Font(family="Consolas", size=12, weight="normal")
        self.__font_width = self.__font.measure("a")
        self.__font_height = self.__font.metrics("ascent")
        self.__canvas = tk.Canvas(self)
        self.__text_editor_model = text_editor_model
        self.__text_editor_model.attach_cursor_observer(self)
        self.__cursor = self.__canvas.create_line(0, 0, 0, 13,)
        self.update_text()
        self.bind("<Up>", self.__text_editor_model.move_cursor_up)
        self.bind("<Down>", self.__text_editor_model.move_cursor_down)
        self.bind("<Right>", self.__text_editor_model.move_cursor_right)
        self.bind("<Left>", self.__text_editor_model.move_cursor_left)
        self.bind("<BackSpace>", self.__text_editor_model.delete_before)
        self.__canvas.pack()

    def update_cursor_location(self, loc: Location) -> None:
        print(loc.x, loc.y)
        self.__canvas.delete(self.__cursor)
        self.__cursor = self.__canvas.create_line(
            loc.x * self.__font_width,
            loc.y * self.__font_height,
            loc.x * self.__font_width,
            loc.y * self.__font_height + self.__font_height,
        )

    def update_text(self) -> None:
        begin = self.__font_width
        line_height = 0
        for line in self.__text_editor_model.all_lines():
            self.__canvas.create_text(0, line_height, text=line, font=self.__font)
            line_height += self.__font_height


def main():
    model = TextEditorModel("test\ntest\ntest")
    editor = TextEditor(model)
    editor.mainloop()


if __name__ == "__main__":
    main()
