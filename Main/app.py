from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import unquote

app = Flask(__name__)

fila_preferencial = []
fila_normal = []
historico = []
senha_atual = None
contador_pref = 1
contador_norm = 1

def gerar_senha(tipo, preferencial=False):
    global contador_pref, contador_norm
    prefixo = tipo[:3].upper()

    if preferencial:
        senha = f"{prefixo}{str(contador_pref).zfill(3)}-A"
        contador_pref += 1
        fila_preferencial.append(senha)
    else:
        senha = f"{prefixo}{str(contador_norm).zfill(3)}"
        contador_norm += 1
        fila_normal.append(senha)
    return senha

@app.route('/')
def mostrar_senhas():
    return render_template('mostrar_senhas.html', senha_atual=senha_atual, historico=historico)

@app.route('/medico', methods=['GET', 'POST'])
def formulario_medico():
    global senha_atual

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        sus = request.form['sus']
        sintomas = request.form['sintomas']
        prescricao = request.form['prescricao']

        if fila_preferencial:
            senha_atual = fila_preferencial.pop(0)
        elif fila_normal:
            senha_atual = fila_normal.pop(0)
        else:
            senha_atual = "Nenhuma senha na fila"

        if senha_atual != "Nenhuma senha na fila":
            historico.append(senha_atual)

        return redirect(url_for('mostrar_senhas'))

    return render_template('formulario_medico.html', senha_atual=senha_atual)

@app.route('/add/<tipo>/<preferencial>')
def add_fila(tipo, preferencial):
    tipo = unquote(tipo)
    gerar_senha(tipo, preferencial.lower() == 's')
    return redirect(url_for('mostrar_senhas'))

@app.route('/cadastro')
def cadastro_paciente():
    return render_template('cadastro_paciente.html')

if __name__ == '__main__':
    app.run(debug=True)
