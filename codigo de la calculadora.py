import tkinter as tk
import math


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Científica")
        self.geometry("400x600")
        self.configure(bg='#2E2E2E')  # Dark background similar to the calculator

        self.expression = ''
        self.deg_mode = True
        self.history = []

        # Mode label
        self.mode_label = tk.Label(self, text="DEG", font=('Arial', 10), bg='#2E2E2E', fg='white')
        self.mode_label.place(x=320, y=10)

        # Entry field
        self.entry = tk.Entry(self, font=('Arial', 16), bd=2, insertwidth=2, width=25, borderwidth=2, justify='right',
                              bg='#F0F0F0')
        self.entry.place(x=20, y=40, width=360, height=60)

        # Buttons layout inspired by the image
        button_configs = [
            # Row 1: Mode and navigation
            (('Shift', '#FFD700'), (0, 0), lambda: None),
            (('Alpha', '#FFD700'), (0, 1), lambda: None),
            (('←', 'grey'), (0, 2), lambda: self.backspace()),
            (('→', 'grey'), (0, 3), lambda: None),
            (('Mode', 'grey'), (0, 4), lambda: None),
            (('2nd', 'grey'), (0, 5), lambda: None),

            # Row 2: Function keys
            (('Calc', 'grey'), (1, 0), lambda: None),
            (('d/dx', 'grey'), (1, 1), lambda: None),
            (('△', 'grey'), (1, 2), lambda: None),
            (('∇', 'grey'), (1, 3), lambda: None),
            (('x⁻¹', 'grey'), (1, 4), lambda: self.append('**(-1)')),
            (('Logₓ', 'grey'), (1, 5), lambda: self.append('log(')),

            # Row 3: Power and log functions
            (('x²', 'grey'), (2, 0), lambda: self.append('**2')),
            (('x³', 'grey'), (2, 1), lambda: self.append('**3')),
            (('Log', 'grey'), (2, 2), lambda: self.append('log10(')),
            (('Ln', 'grey'), (2, 3), lambda: self.append('log(')),
            (('(', 'grey'), (2, 4), lambda: self.append('(')),
            ((')', 'grey'), (2, 5), lambda: self.append(')')),

            # Row 4: Trigonometric functions
            (('(-)', 'grey'), (3, 0), self.sign),
            (('hyp', 'grey'), (3, 1), lambda: None),
            (('Sin', 'grey'), (3, 2), lambda: self.append('sin(')),
            (('Cos', 'grey'), (3, 3), lambda: self.append('cos(')),
            (('Tan', 'grey'), (3, 4), lambda: self.append('tan(')),
            (('≠0', 'grey'), (3, 5), lambda: None),

            # Row 5: Additional functions
            (('Rcl', 'grey'), (4, 0), lambda: None),
            (('Eng', 'grey'), (4, 1), lambda: None),
            (('(', 'grey'), (4, 2), lambda: self.append('(')),
            ((')', 'grey'), (4, 3), lambda: self.append(')')),
            (('=', 'grey'), (4, 4), self.calculate),
            (('+', 'grey'), (4, 5), lambda: self.append('+')),

            # Row 6: Numbers and basic operations
            (('7', 'grey'), (5, 0), lambda: self.append('7')),
            (('8', 'grey'), (5, 1), lambda: self.append('8')),
            (('9', 'grey'), (5, 2), lambda: self.append('9')),
            (('DEL', '#FFA500'), (5, 3), lambda: self.backspace()),
            (('AC', '#FFA500'), (5, 4), self.clear),
            (('/', 'grey'), (5, 5), lambda: self.append('/')),

            # Row 7: Numbers and operations
            (('4', 'grey'), (6, 0), lambda: self.append('4')),
            (('5', 'grey'), (6, 1), lambda: self.append('5')),
            (('6', 'grey'), (6, 2), lambda: self.append('6')),
            (('×', 'grey'), (6, 3), lambda: self.append('*')),
            (('-', 'grey'), (6, 4), lambda: self.append('-')),
            (('Historial', 'grey'), (6, 5), self.show_history),

            # Row 8: Numbers and operations
            (('1', 'grey'), (7, 0), lambda: self.append('1')),
            (('2', 'grey'), (7, 1), lambda: self.append('2')),
            (('3', 'grey'), (7, 2), lambda: self.append('3')),
            (('+', 'grey'), (7, 3), lambda: self.append('+')),
            (('-', 'grey'), (7, 4), lambda: self.append('-')),
            (('Exp', 'grey'), (7, 5), lambda: self.append('e')),

            # Row 9: Numbers and equals
            (('0', 'grey'), (8, 0), lambda: self.append('0')),
            (('.', 'grey'), (8, 1), lambda: self.append('.')),
            (('Ans', 'grey'), (8, 2), lambda: self.append('ans')),
            (('=', 'grey'), (8, 3), self.calculate),
        ]

        # Debug print to inspect button_configs
        print("Button configs:", button_configs)

        # Create and place buttons
        for (text, color), (row, col), command in button_configs:
            btn = tk.Button(self, text=text, bg=color if color != 'grey' else '#4A4A4A', fg='white',
                            font=('Arial', 10), width=5, height=2, command=command)
            btn.place(x=col * 60 + 20, y=row * 50 + 120)

    def append(self, char):
        self.expression += str(char)
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def clear(self):
        self.expression = ''
        self.entry.delete(0, tk.END)

    def sign(self):
        if self.expression:
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.expression)

    def backspace(self):
        self.expression = self.expression[:-1]
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def toggle_mode(self):
        self.deg_mode = not self.deg_mode
        self.mode_label.config(text="DEG" if self.deg_mode else "RAD")

    def show_history(self):
        history_window = tk.Toplevel(self)
        history_window.title("Historial de Cálculos")
        history_window.geometry("300x200")
        history_window.configure(bg='#2E2E2E')

        history_list = tk.Listbox(history_window, height=10, width=40, font=('Arial', 10), bg='#4A4A4A', fg='white')
        history_list.pack(pady=10, padx=10, fill='both', expand=True)

        clear_button = tk.Button(history_window, text="Limpiar Historial",
                                 command=lambda: self.clear_history(history_list),
                                 bg='#FFA500', fg='white', font=('Arial', 10))
        clear_button.pack(pady=5)

        for calc in self.history:
            history_list.insert(tk.END, calc)

    def clear_history(self, history_list):
        self.history = []
        history_list.delete(0, tk.END)

    # noinspection PyBroadException
    def calculate(self):
        try:
            def sin(x):
                return math.sin(math.radians(x)) if self.deg_mode else math.sin(x)

            def cos(x):
                return math.cos(math.radians(x)) if self.deg_mode else math.cos(x)

            def tan(x):
                return math.tan(math.radians(x)) if self.deg_mode else math.tan(x)

            def asin(x):
                return math.degrees(math.asin(x)) if self.deg_mode else math.asin(x)

            def acos(x):
                return math.degrees(math.acos(x)) if self.deg_mode else math.acos(x)

            def atan(x):
                return math.degrees(math.atan(x)) if self.deg_mode else math.atan(x)

            def log10(x):
                return math.log10(x)

            def log(x):
                return math.log(x)

            def exp(x):
                return math.exp(x)

            def sqrt(x):
                return math.sqrt(x)

            def factorial(x):
                return math.factorial(int(x))

            safe_dict = {
                'sin': sin, 'cos': cos, 'tan': tan,
                'asin': asin, 'acos': acos, 'atan': atan,
                'log10': log10, 'log': log, 'exp': exp,
                'sqrt': sqrt, 'factorial': factorial,
                'pi': math.pi, 'e': math.e,
            }

            result = eval(self.expression, {"__builtins__": {}}, safe_dict)
            self.history.append(f"{self.expression} = {result}")
            self.expression = str(result)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.expression)
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")
            self.expression = ''


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()