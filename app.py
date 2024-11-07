from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para calcular o IMC
def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    if imc < 18.5:
        classificacao = "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        classificacao = "Peso normal"
    elif 25 <= imc < 29.9:
        classificacao = "Sobrepeso"
    else:
        classificacao = "Obesidade"
    return imc, classificacao

# Função para salvar no banco de dados
def salvar_no_banco(nome, peso, altura, imc, classificacao):
    conn = sqlite3.connect('imc.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        peso REAL,
                        altura REAL,
                        imc REAL,
                        classificacao TEXT)''')
    cursor.execute('''INSERT INTO registros (nome, peso, altura, imc, classificacao)
                    VALUES (?, ?, ?, ?, ?)''', (nome, peso, altura, imc, classificacao))
    conn.commit()
    conn.close()

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        try:
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])
        except ValueError:
            return "Erro: Os campos 'peso' e 'altura' devem ser números válidos.", 400
        
        if peso <= 0 or altura <= 0:
            return "Erro: O peso e a altura devem ser números positivos.", 400

        imc, classificacao = calcular_imc(peso, altura)
        salvar_no_banco(nome, peso, altura, imc, classificacao)
        
        return render_template('resultado.html', imc=imc, classificacao=classificacao, nome=nome)

    return render_template('index.html')

# Rota para exibir os registros armazenados no banco
@app.route('/registros')
def registros():
    conn = sqlite3.connect('imc.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros')
    dados = cursor.fetchall()
    conn.close()
    
    return render_template('registro.html', registros=dados)

if __name__ == '__main__':
    app.run(debug=True)
