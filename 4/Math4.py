import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, \
    QGridLayout, QMessageBox
from PyQt5.QtGui import QFont
import math


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.display = None
        self.angle_mode = None
        self.current_memory = None
        self.memory = None
        self.expression = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Scientific Calculator')
        self.expression = ""
        self.memory = [0, 0, 0]
        self.current_memory = 0
        self.angle_mode = 'deg'

        self.display = QLineEdit(self)
        font = QFont('Arial', 36)
        self.display.setFont(font)
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)

        grid = QGridLayout()
        grid.addWidget(self.display, 0, 0, 1, 8)

        buttons = [
            ('DEC', 1, 0, 1, 2), ('OCT', 1, 2, 1, 2), ('HEX', 1, 4, 1, 2), ('BIN', 1, 6, 1, 2),
            ('sin', 2, 0, 1, 1), ('cos', 2, 1, 1, 1), ('tan', 2, 2, 1, 1),
            ('sin⁻¹', 3, 0, 1, 1), ('cos⁻¹', 3, 1, 1, 1), ('tan⁻¹', 3, 2, 1, 1),
            ('ln', 4, 0, 1, 1), ('log', 4, 1, 1, 1), ('x²', 4, 2, 1, 1),
            ('e', 5, 0, 1, 1), ('10^x', 5, 1, 1, 1), ('x³', 5, 2, 1, 1),
            ('7', 2, 3, 1, 1), ('8', 2, 4, 1, 1), ('9', 2, 5, 1, 1), ('/', 2, 6, 1, 1), ('AC', 2, 7, 1, 1),
            ('4', 3, 3, 1, 1), ('5', 3, 4, 1, 1), ('6', 3, 5, 1, 1), ('*', 3, 6, 1, 1), ('CE', 3, 7, 1, 1),
            ('1', 4, 3, 1, 1), ('2', 4, 4, 1, 1), ('3', 4, 5, 1, 1), ('-', 4, 6, 1, 1), ('sqrt', 4, 7, 1, 1),
            ('0', 5, 3, 1, 1), ('.', 5, 4, 1, 1), ('π', 5, 5, 1, 1), ('+', 5, 6, 1, 1), ('inv', 5, 7, 1, 1),
            ('=', 10, 3, 2, 3), ('shift', 10, 6, 2, 2),
            ('M+', 11, 0, 1, 1), ('M-', 11, 1, 1, 1), ('MR', 11, 2, 1, 1),
            ('deg', 12, 0, 1, 1), ('rad', 12, 1, 1, 1), ('gra', 12, 2, 1, 1),
            ('Off', 12, 4, 1, 3)
        ]

        for (text, row, col, rowspan, colspan) in buttons:
            button = QPushButton(text, self)
            button.setFont(QFont('Arial', 18))
            button.clicked.connect(lambda _, t=text: self.on_button_click(t))
            grid.addWidget(button, row, col, rowspan, colspan)

        for i in range(13):
            grid.setRowStretch(i, 1)
        for i in range(8):
            grid.setColumnStretch(i, 1)

        self.setLayout(grid)

    def on_button_click(self, char):
        if char == '=':
            try:
                self.expression = str(eval(self.expression))
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                self.expression = ""
        elif char in ['M+', 'M-', 'MR']:
            self.memory_operations(char)
        elif char == 'AC':
            self.expression = ""
        elif char == 'Off':
            self.close()
        elif char in ['sin', 'cos', 'tan', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹',
                      'ln', 'log', 'x²', '1/x', 'π', 'shift', 'deg', 'rad', 'gra', 'e', '10^x', 'x³', 'sqrt', 'inv']:
            self.expression = self.handle_functions(char)
        else:
            self.expression += char

        self.display.setText(self.expression)

    def memory_operations(self, operation):
        if operation == 'M+':
            self.memory[self.current_memory] += eval(self.expression)
        elif operation == 'M-':
            self.memory[self.current_memory] -= eval(self.expression)
        elif operation == 'MR':
            self.expression = str(self.memory[self.current_memory])
        self.current_memory = (self.current_memory + 1) % len(self.memory)

    def handle_functions(self, function):
        try:
            if function == 'sin':
                return str(math.sin(self.convert_angle(eval(self.expression))))
            elif function == 'cos':
                return str(math.cos(self.convert_angle(eval(self.expression))))
            elif function == 'tan':
                return str(math.tan(self.convert_angle(eval(self.expression))))
            elif function == 'sin⁻¹':
                return str(math.asin(eval(self.expression)))
            elif function == 'cos⁻¹':
                return str(math.acos(eval(self.expression)))
            elif function == 'tan⁻¹':
                return str(math.atan(eval(self.expression)))
            elif function == 'ln':
                return str(math.log(eval(self.expression)))
            elif function == 'log':
                return str(math.log10(eval(self.expression)))
            elif function == 'x²':
                return str(math.pow(eval(self.expression), 2))
            elif function == '1/x':
                return str(1 / eval(self.expression))
            elif function == 'π':
                return str(math.pi)
            elif function == 'shift':
                self.expression += '**'
                return self.expression
            elif function in ['deg', 'rad', 'gra']:
                if function == 'deg':
                    self.angle_mode = 'deg'
                elif function == 'rad':
                    self.angle_mode = 'rad'
                else:
                    self.angle_mode = 'gra'
                return self.expression
            elif function == 'e':
                return str(math.e)
            elif function == '10^x':
                return str(math.pow(10, eval(self.expression)))
            elif function == 'x³':
                return str(math.pow(eval(self.expression), 3))
            elif function == 'sqrt':
                return str(math.sqrt(eval(self.expression)))
            elif function == 'inv':
                return str(1 / eval(self.expression))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return ""

    def convert_angle(self, value):
        if self.angle_mode == 'deg':
            return math.radians(value)
        elif self.angle_mode == 'gra':
            return math.radians(value * 0.9)
        else:
            return value


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
