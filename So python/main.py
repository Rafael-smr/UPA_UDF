import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class AgendamentoClinica:
    def __init__(self, master):
        self.master = master
        master.title("Agendamento de Consultas")

        self.consultorios = {
            "1": "Clinico Geral (CG)",
            "2": "Ginecologia (GIN)",
            "3": "Pediatria (PED)",
            "4": "Geriatria (GER)",
            "5": "Ortopedia (ORT)"
        }

        self.filas = {
            "CG": {"normal": [], "preferencial": []},
            "GIN": {"normal": [], "preferencial": []},
            "PED": {"normal": [], "preferencial": []},
            "GER": {"normal": [], "preferencial": []},
            "ORT": {"normal": [], "preferencial": []}
        }

        self.label = tk.Label(master, text="Escolha um consultório:")
        self.label.pack()

        self.var_consultorio = tk.StringVar(value="1")
        for key, value in self.consultorios.items():
            tk.Radiobutton(master, text=value, variable=self.var_consultorio, value=key).pack(anchor=tk.W)

        self.label_preferencial = tk.Label(master, text="Você é preferencial?")
        self.label_preferencial.pack()

        self.var_preferencial = tk.BooleanVar()
        tk.Checkbutton(master, text="Sim", variable=self.var_preferencial).pack()

        self.agendar_button = tk.Button(master, text="Gerar Senha", command=self.gerar_senha)
        self.agendar_button.pack()

        self.chamar_button = tk.Button(master, text="Chamar Próximo", command=self.chamar_proximo)
        self.chamar_button.pack()

    def gerar_senha(self):
        hora_atual = datetime.now().hour

        if hora_atual >= 18:
            messagebox.showerror("Erro", "Após as 18h não é permitido emitir novas senhas.")
            return

        consultorio = self.var_consultorio.get()
        preferencial = self.var_preferencial.get()

        sigla = self.consultorios[consultorio].split(' ')[-1][1:-1]

        if preferencial:
            self.filas[sigla]["preferencial"].append(f"{sigla}{len(self.filas[sigla]['preferencial']) + 1}-P")
            senha = self.filas[sigla]["preferencial"][-1]
        else:
            self.filas[sigla]["normal"].append(f"{sigla}{len(self.filas[sigla]['normal']) + 1}")
            senha = self.filas[sigla]["normal"][-1]

        messagebox.showinfo("Senha Gerada", f"Sua senha para {self.consultorios[consultorio]} é: {senha}")

    def chamar_proximo(self):
        consultorio = self.var_consultorio.get()
        sigla = self.consultorios[consultorio].split(' ')[-1][1:-1]

        if self.filas[sigla]["preferencial"]:
            senha_atual = self.filas[sigla]["preferencial"].pop(0)
        elif self.filas[sigla]["normal"]:
            senha_atual = self.filas[sigla]["normal"].pop(0)
        else:
            senha_atual = "Nenhum paciente na fila"

        messagebox.showinfo("Atendimento Atual", f"Próximo paciente para {self.consultorios[consultorio]}: {senha_atual}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendamentoClinica(root)
    root.mainloop()
