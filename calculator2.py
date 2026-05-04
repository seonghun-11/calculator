import os
import subprocess
import sys

# 1. 고품질의 계산기 소스 코드 정의
calculator_code = """
import tkinter as tk
from tkinter import messagebox, ttk
import math

class ProfessionalCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Tabbed Calculator")
        self.root.geometry("450x650")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(True, True)

        # 탭 스타일 설정
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background="#2c3e50", borderwidth=0)
        style.configure("TNotebook.Tab", background="#34495e", foreground="white", padding=[10, 5], font=("Helvetica", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#16a085")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # 일반 계산기 탭
        self.basic_tab = tk.Frame(self.notebook, bg="#2c3e50")
        self.notebook.add(self.basic_tab, text=" 일반 계산기 ")
        self._setup_calc(self.basic_tab, "basic")

        # 공학용 계산기 탭
        self.sci_tab = tk.Frame(self.notebook, bg="#2c3e50")
        self.notebook.add(self.sci_tab, text=" 공학용 계산기 ")
        self._setup_calc(self.sci_tab, "scientific")

    def _setup_calc(self, parent, mode):
        # 각 탭의 상태를 독립적으로 관리
        state = {"expr": "", "var": tk.StringVar()}
        setattr(self, f"{mode}_state", state)

        display_frame = tk.Frame(parent, bg="#2c3e50", pady=20)
        display_frame.pack(fill="both")

        entry = tk.Entry(display_frame, textvariable=state["var"], font=("Helvetica", 32),
                        bg="#34495e", fg="#ecf0f1", justify='right', bd=10, relief="flat")
        entry.pack(fill="both", padx=20)

        button_frame = tk.Frame(parent, bg="#2c3e50")
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if mode == "basic":
            buttons = [
                ('7', 0, 0, "#34495e"), ('8', 0, 1, "#34495e"), ('9', 0, 2, "#34495e"), ('/', 0, 3, "#f39c12"),
                ('4', 1, 0, "#34495e"), ('5', 1, 1, "#34495e"), ('6', 1, 2, "#34495e"), ('*', 1, 3, "#f39c12"),
                ('1', 2, 0, "#34495e"), ('2', 2, 1, "#34495e"), ('3', 2, 2, "#34495e"), ('-', 2, 3, "#f39c12"),
                ('C', 3, 0, "#e74c3c"), ('0', 3, 1, "#34495e"), ('=', 3, 2, "#27ae60"), ('+', 3, 3, "#f39c12"),
            ]
        else:
            buttons = [
                ('sin', 0, 0, "#16a085"), ('cos', 0, 1, "#16a085"), ('tan', 0, 2, "#16a085"), ('log', 0, 3, "#16a085"), ('ln', 0, 4, "#16a085"),
                ('sqrt', 1, 0, "#16a085"), ('(', 1, 1, "#7f8c8d"), (')', 1, 2, "#7f8c8d"), ('^', 1, 3, "#16a085"), ('pi', 1, 4, "#16a085"),
                ('7', 2, 0, "#34495e"), ('8', 2, 1, "#34495e"), ('9', 2, 2, "#34495e"), ('/', 2, 3, "#f39c12"), ('C', 2, 4, "#e74c3c"),
                ('4', 3, 0, "#34495e"), ('5', 3, 1, "#34495e"), ('6', 3, 2, "#34495e"), ('*', 3, 3, "#f39c12"), ('e', 3, 4, "#16a085"),
                ('1', 4, 0, "#34495e"), ('2', 4, 1, "#34495e"), ('3', 4, 2, "#34495e"), ('-', 4, 3, "#f39c12"), ('=', 4, 4, "#27ae60"),
                ('0', 5, 0, "#34495e"), ('.', 5, 1, "#34495e"), ('+', 5, 2, "#f39c12"),
            ]

        for (text, row, col, color) in buttons:
            btn = tk.Button(button_frame, text=text, font=("Helvetica", 12, "bold"),
                           bg=color, fg="white", relief="flat", activebackground="#95a5a6",
                           command=lambda t=text, m=mode: self._on_click(t, m))
            btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
            button_frame.grid_columnconfigure(col, weight=1, uniform="equal")
            button_frame.grid_rowconfigure(row, weight=1)

    def _on_click(self, char, mode):
        state = getattr(self, f"{mode}_state")
        if char == "=":
            try:
                full_expr = state["expr"].replace('^', '**')
                full_expr = full_expr.replace('pi', 'math.pi').replace('e', 'math.e')
                full_expr = full_expr.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
                full_expr = full_expr.replace('log', 'math.log10').replace('ln', 'math.log').replace('sqrt', 'math.sqrt')
                
                res_val = eval(full_expr, {"math": math, "__builtins__": None}, {})
                result = f"{res_val:.8g}" if isinstance(res_val, float) else str(res_val)
                state["var"].set(result)
                state["expr"] = result
            except ZeroDivisionError:
                messagebox.showerror("에러", "0으로 나눌 수 없습니다.")
                self._clear(mode)
            except Exception:
                messagebox.showerror("에러", "잘못된 수식입니다.")
                self._clear(mode)
        elif char == "C":
            self._clear(mode)
        elif char in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt']:
            state["expr"] += char + "("
            state["var"].set(state["expr"])
        else:
            state["expr"] += str(char)
            state["var"].set(state["expr"])

    def _clear(self, mode):
        state = getattr(self, f"{mode}_state")
        state["expr"] = ""
        state["var"].set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalCalculator(root)
    root.mainloop()
"""

def main():
    # 현재 실행 중인 파일과 이름이 겹치지 않도록 설정 (권한 충돌 방지)
    target_file_name = "calculator_app.py"
    # 현재 스크립트가 있는 폴더의 절대 경로를 가져옵니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, target_file_name)
    
    # 1. 파일 저장
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(calculator_code.strip())
        print(f"✅ [성공] '{file_path}' 파일이 저장되었습니다.")
        
        # 2. 저장된 파일 즉시 실행
        print(f"🚀 [실행] 계산기 창을 엽니다...")
        subprocess.Popen([sys.executable, file_path])
        
    except Exception as e:
        print(f"❌ [오류] 작업을 수행할 수 없습니다: {e}")

if __name__ == "__main__":
    main()