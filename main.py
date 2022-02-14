# This is a python snake game
from enum import Enum
from turtle import pos
from typing import List, Tuple, Dict
from tkinter import *
from time import sleep
import keyboard

master = Tk()

canvas_width = 1000
canvas_height = 1000
backgroundColor = "black"
snakeColor = "white"
pizelSize = 20
pixelMargin = 5
gridSize = (canvas_width // pizelSize, canvas_height // pizelSize)


w = Canvas(
    master,
    width=canvas_width,
    height=canvas_height,
    bg=backgroundColor,
)

w.pack()

Vector2 = Tuple[int, int]
# [(id, (x, y))]


def drawPixel(canvas: Canvas, position: Vector2, color: str):
    x, y = position
    left = x * (pizelSize + pixelMargin)
    top = y * (pizelSize + pixelMargin)
    right = left + pizelSize
    bottom = top + pizelSize

    pixelId = canvas.create_rectangle(
        left,
        top,
        right,
        bottom,
        fill=color,
    )

    return pixelId


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


def getPosFrom(position: Vector2, direction: Direction):
    x, y = position
    if direction == Direction.RIGHT:
        return x + 1, y
    elif direction == Direction.LEFT:
        return x - 1, y
    elif direction == Direction.UP:
        return x, y - 1
    elif direction == Direction.DOWN:
        return x, y + 1


def clamp(value: int, minValue: int, maxValue: int):
    return max(min(value, maxValue - 1), minValue)


def clampPosition(position: Vector2, limit: Vector2):
    x, y = position
    xLim, yLim = limit
    return (
        clamp(x, 0, xLim),
        clamp(y, 0, yLim),
    )


class Snake:
    positions = dict()
    order = list()
    color = snakeColor
    direction = Direction.RIGHT

    def add(self, canvas: Canvas, position: Vector2):
        pixelId = drawPixel(canvas, position, self.color)
        self.order.append(pixelId)
        self.positions[pixelId] = position
        return pixelId

    def remove(self, canvas: Canvas, pixelId: int):
        canvas.delete(pixelId)
        del self.positions[pixelId]
        if pixelId in self.order:
            self.order.remove(pixelId)

    def removeTail(self, canvas: Canvas):
        self.remove(canvas, self.order.pop())

    def getHeadPosition(self):
        return self.positions[self.order[-1]]

    def move(self, canvas: Canvas):
        headPosition = self.getHeadPosition()
        self.removeTail(canvas)
        self.add(canvas, clampPosition(getPosFrom(
            headPosition, self.direction), gridSize))
        print(self.positions)


def main():

    snake = Snake()

    # Add the head
    snake.add(w, (2, 2))

    def getDirectionSetter(snake: Snake, d: Direction):
        def setDir(_):
            print(d)
            snake.direction = d
        return setDir

    keyboard.on_press_key("right", getDirectionSetter(snake, Direction.RIGHT))
    keyboard.on_press_key("left", getDirectionSetter(snake, Direction.LEFT))
    keyboard.on_press_key("up", getDirectionSetter(snake, Direction.UP))
    keyboard.on_press_key("down", getDirectionSetter(snake, Direction.DOWN))

    while True:
        snake.move(w)
        w.update()
        sleep(0.1)
    w.mainloop()


if __name__ == '__main__':
    main()
