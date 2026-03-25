import tkinter as tk
from tkinter import ttk, messagebox
import math
import re
from datetime import datetime

class SmartCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Calculator")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Calculator state
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.history = []
        
        # Color scheme
        self.colors = {
            'bg': '#2c3e50',
            'display': '#34495e',
            'button_normal': '#3498db',
            'button_operator': '#e67e22',
            'button_scientific': '#9b59b6',
            'button_clear': '#e74c3c',
            'button_equal': '#2ecc71',
            'text': 'black'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Display frame
        display_frame = tk.Frame(main_frame, bg=self.colors['display'])
        display_frame.pack(fill='x', pady=(0, 10))
        
        # Result display
        self.result_display = tk.Entry(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', 24),
            bg=self.colors['display'],
            fg=self.colors['text'],
            borderwidth=0,
            justify='right',
            state='readonly'
        )
        self.result_display.pack(fill='x', padx=10, pady=10)
        
        # History button
        history_btn = tk.Button(
            display_frame,
            text="📜 History",
            font=('Arial', 10),
            bg=self.colors['button_scientific'],
            fg=self.colors['text'],
            command=self.show_history
        )
        history_btn.pack(pady=(0, 5))
        
        # Notebook for tabbed interface
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Basic calculator tab
        basic_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(basic_frame, text="Basic")
        
        # Scientific calculator tab
        scientific_frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(scientific_frame, text="Scientific")
        
        self.setup_basic_calculator(basic_frame)
        self.setup_scientific_calculator(scientific_frame)
        
    def setup_basic_calculator(self, parent):
        # Button layout for basic calculator
        buttons = [
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', '⌫'],
            ['1', '2', '3', '-', '±'],
            ['0', '.', '=', '+', '%']
        ]
        
        for i, row in enumerate(buttons):
            btn_frame = tk.Frame(parent, bg=self.colors['bg'])
            btn_frame.pack(pady=2)
            
            for j, btn_text in enumerate(row):
                if btn_text == '=':
                    bg_color = self.colors['button_equal']
                elif btn_text in ['C', '⌫', '±']:
                    bg_color = self.colors['button_clear']
                elif btn_text in ['/', '*', '-', '+', '%']:
                    bg_color = self.colors['button_operator']
                else:
                    bg_color = self.colors['button_normal']
                    
                btn = tk.Button(
                    btn_frame,
                    text=btn_text,
                    font=('Arial', 14, 'bold'),
                    width=5,
                    height=2,
                    bg=bg_color,
                    fg=self.colors['text'],
                    command=lambda x=btn_text: self.button_click(x)
                )
                btn.pack(side='left', padx=2)
                
    def setup_scientific_calculator(self, parent):
        # Scientific functions
        scientific_buttons = [
            ['sin', 'cos', 'tan', '√', 'log'],
            ['asin', 'acos', 'atan', 'ln', 'π'],
            ['x²', 'x³', 'xʸ', '1/x', 'e'],
            ['(', ')', 'abs', 'fact', 'mod']
        ]
        
        for i, row in enumerate(scientific_buttons):
            btn_frame = tk.Frame(parent, bg=self.colors['bg'])
            btn_frame.pack(pady=2)
            
            for j, btn_text in enumerate(row):
                btn = tk.Button(
                    btn_frame,
                    text=btn_text,
                    font=('Arial', 10, 'bold'),
                    width=5,
                    height=2,
                    bg=self.colors['button_scientific'],
                    fg=self.colors['text'],
                    command=lambda x=btn_text: self.scientific_click(x)
                )
                btn.pack(side='left', padx=2)
                
    def button_click(self, value):
        if value == 'C':
            self.current_input = ""
            self.result_var.set("")
        elif value == '⌫':
            self.current_input = self.current_input[:-1]
            self.result_var.set(self.current_input)
        elif value == '=':
            self.calculate_result()
        elif value == '±':
            if self.current_input:
                if self.current_input[0] == '-':
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.result_var.set(self.current_input)
        else:
            self.current_input += value
            self.result_var.set(self.current_input)
            
    def scientific_click(self, func):
        if func == 'π':
            self.current_input += str(math.pi)
            self.result_var.set(self.current_input)
        elif func == 'e':
            self.current_input += str(math.e)
            self.result_var.set(self.current_input)
        elif func in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sqrt', 'log', 'ln', 'abs', 'fact']:
            self.current_input += f"{func}("
            self.result_var.set(self.current_input)
        elif func == 'x²':
            self.current_input += "²"
            self.result_var.set(self.current_input)
        elif func == 'x³':
            self.current_input += "³"
            self.result_var.set(self.current_input)
        elif func == 'xʸ':
            self.current_input += "^"
            self.result_var.set(self.current_input)
        elif func == '1/x':
            self.current_input = f"1/({self.current_input})" if self.current_input else "1/x"
            self.result_var.set(self.current_input)
        elif func == 'mod':
            self.current_input += "%"
            self.result_var.set(self.current_input)
        elif func in ['(', ')']:
            self.current_input += func
            self.result_var.set(self.current_input)
            
    def calculate_result(self):
        try:
            expression = self.current_input
            
            # Replace scientific function names
            expression = self.parse_scientific_functions(expression)
            
            # Evaluate the expression
            result = eval(expression)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
                    
            # Add to history
            self.add_to_history(self.current_input, result)
            
            self.result_var.set(str(result))
            self.current_input = str(result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {str(e)}")
            self.result_var.set("Error")
            self.current_input = ""
            
    def parse_scientific_functions(self, expression):
        # Replace scientific notations
        replacements = {
            'sin': 'math.sin',
            'cos': 'math.cos',
            'tan': 'math.tan',
            'asin': 'math.asin',
            'acos': 'math.acos',
            'atan': 'math.atan',
            'sqrt': 'math.sqrt',
            'log': 'math.log10',
            'ln': 'math.log',
            'abs': 'abs',
            'fact': 'math.factorial',
            'π': 'math.pi',
            'e': 'math.e',
            '²': '**2',
            '³': '**3',
            '^': '**'
        }
        
        for old, new in replacements.items():
            expression = expression.replace(old, new)
            
        return expression
        
    def add_to_history(self, expression, result):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history.append({
            'timestamp': timestamp,
            'expression': expression,
            'result': result
        })
        
        # Keep only last 50 calculations
        if len(self.history) > 50:
            self.history.pop(0)
            
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("400x500")
        history_window.configure(bg=self.colors['bg'])
        
        # Create listbox
        listbox_frame = tk.Frame(history_window, bg=self.colors['bg'])
        listbox_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=('Courier', 10),
            bg=self.colors['display'],
            fg=self.colors['text']
        )
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Add history items
        if self.history:
            for item in reversed(self.history):
                listbox.insert('end', f"{item['timestamp']} - {item['expression']} = {item['result']}")
        else:
            listbox.insert('end', "No history available")
            
        # Buttons
        button_frame = tk.Frame(history_window, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear History",
            command=lambda: self.clear_history(listbox),
            bg=self.colors['button_clear'],
            fg=self.colors['text']
        )
        clear_btn.pack(side='left', padx=5)
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=history_window.destroy,
            bg=self.colors['button_normal'],
            fg=self.colors['text']
        )
        close_btn.pack(side='left', padx=5)
        
    def clear_history(self, listbox):
        self.history.clear()
        listbox.delete(0, 'end')
        listbox.insert('end', "History cleared")
        
    def key_press(self, event):
        # Keyboard shortcuts
        key = event.char
        if key.isdigit() or key in ['+', '-', '*', '/', '.', '(', ')']:
            self.button_click(key)
        elif key == '\r':  # Enter key
            self.calculate_result()
        elif key == '\x08':  # Backspace
            self.button_click('⌫')
        elif key == '\x1b':  # Escape
            self.button_click('C')

def main():
    root = tk.Tk()
    app = SmartCalculator(root)
    
    # Bind keyboard shortcuts
    root.bind('<Key>', app.key_press)
    
    root.mainloop()

if __name__ == "__main__":
    main()
