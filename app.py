from flask import Flask, redirect, render_template, request, url_for
import sqlite3
from datetime import datetime


app = Flask(__name__)

def criar_banco():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            mes_referencia TEXT,
            convenio TEXT,
            profissional_assistente TEXT,
            tipo_atendimento TEXT
        )
    ''')
    conn.commit()
    conn.close()
    

criar_banco()
from flask import Flask, redirect, render_template, request, url_for
import sqlite3
from datetime import datetime


app = Flask(__name__)

def criar_banco():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            mes_referencia TEXT,
            convenio TEXT,
            profissional_assistente TEXT,
            tipo_atendimento TEXT
        )
    ''')
    conn.commit()
    conn.close()

    criar_banco()   
''

def criar_tabela_detalhes():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalhes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            anotacoes TEXT,
            data TEXT,  -- Adicionando um campo 'data'
            frequencias TEXT,
            evolucao TEXT,
            anamnese TEXT,
            FOREIGN KEY(id_paciente) REFERENCES pacientes(id)
        )
    ''')
    conn.commit()
    conn.close()

criar_tabela_detalhes()

def criar_tabela_frequencia():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS frequencia(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            n_sessoes INT,
            data DATE,
            assinatura TEXT,
            horario_atendimento TIME,
            FOREIGN KEY(id_paciente) REFERENCES pacientes(id)
                   
        )
    ''')
    conn.commit()
    conn.close()

criar_tabela_frequencia()

@app.route('/')
def index():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes')
    pacientes = cursor.fetchall()
    conn.close()
    return render_template('index.html', pacientes=pacientes)

@app.route('/salvar_anotacao', methods=['POST'])
def salvar_anotacao():
    if request.method == 'POST':
        anotacao = request.form['anotacao']
        id_paciente = request.form['id_paciente']
        data = datetime.now().strftime("%d-%m-%Y %H:%M")  

        conn = sqlite3.connect('pacientes.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO detalhes (id_paciente, anotacoes, data)
            VALUES (?, ?, ?)
        ''', (id_paciente, anotacao, data))

        conn.commit()
        conn.close()

        return redirect(url_for('exibir_anotacoes', paciente_id=id_paciente))

@app.route('/anotacao/<int:paciente_id>')
def exibir_anotacoes(paciente_id):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()

    cursor.execute('SELECT anotacoes, data FROM detalhes WHERE id_paciente = ?', (paciente_id,))
    anotacoes = cursor.fetchall()

    print(anotacoes)  

    conn.close()
    paciente = {'id': paciente_id}  

    return render_template('anotacao.html', paciente=paciente, anotacoes=anotacoes)


@app.route('/salvar_frequencia', methods=['POST'])
def salvar_frequencia():
    if request.method == 'POST':
        n_sessoes = request.form['n_sessoes']
        data = request.form['data']
        assinatura = request.form['assinatura']
        horario_atendimento = request.form['horario_atendimento']
        id_paciente = request.form['id_paciente']

        conn = sqlite3.connect('pacientes.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO frequencia (id_paciente, n_sessoes, data, assinatura, horario_atendimento)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_paciente, n_sessoes, data, assinatura, horario_atendimento))

        conn.commit()
        conn.close()

        return redirect(url_for('exibir_frequencia', paciente_id=id_paciente))
    






@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/evolucao')
def evolucao():
    return render_template('evolucao.html')

@app.route('/anamnese')
def anamnese():
    return render_template('anamnese.html')


@app.route('/pacientes/<int:paciente_id>')
def paciente(paciente_id):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes WHERE id = ?', (paciente_id,))
    paciente = cursor.fetchone()
    conn.close()
    return render_template('pacientes.html', paciente=paciente)


@app.route('/salvar_cadastro', methods=['POST'])
def salvar_cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        mes_referencia = request.form['mes_referencia']
        convenio = request.form['convenio']
        profissional_assistente = request.form['profissional_assistente']
        tipo_atendimento = request.form['tipo_atendimento']

        conn = sqlite3.connect('pacientes.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO pacientes (nome, mes_referencia, convenio, profissional_assistente, tipo_atendimento)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, mes_referencia, convenio, profissional_assistente, tipo_atendimento))

        conn.commit()
        conn.close()

        return redirect(url_for('index')) 
    

@app.route('/apagar_cadastro/<int:paciente_id>', methods=['POST'])
def apagar_cadastro(paciente_id):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()

    # Deletando o paciente do banco de dados
    cursor.execute('DELETE FROM pacientes WHERE id = ?', (paciente_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

    

if __name__ == '__main__':
    app.run(debug=True)

def criar_tabela_detalhes():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalhes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            anotacoes TEXT,
            data TEXT,  -- Adicionando um campo 'data'
            frequencias TEXT,
            evolucao TEXT,
            anamnese TEXT,
            FOREIGN KEY(id_paciente) REFERENCES pacientes(id)
        )
    ''')
    conn.commit()
    conn.close()

criar_tabela_detalhes()

@app.route('/salvar_anotacao', methods=['POST'])
def salvar_anotacao():
    if request.method == 'POST':
        anotacao = request.form['anotacao']
        id_paciente = request.form['id_paciente']
        data = datetime.now().strftime("%d-%m-%Y %H:%M")  

        conn = sqlite3.connect('pacientes.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO detalhes (id_paciente, anotacoes, data)
            VALUES (?, ?, ?)
        ''', (id_paciente, anotacao, data))

        conn.commit()
        conn.close()

        return redirect(url_for('exibir_anotacoes', paciente_id=id_paciente))

@app.route('/anotacao/<int:paciente_id>')
def exibir_anotacoes(paciente_id):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()

    cursor.execute('SELECT anotacoes, data FROM detalhes WHERE id_paciente = ?', (paciente_id,))
    anotacoes = cursor.fetchall()

    conn.close()
    paciente = {'id': paciente_id} 

    return render_template('anotacao.html', paciente=paciente, anotacoes=anotacoes)




@app.route('/evolucao')
def evolucao():
    return render_template('evolucao.html')

@app.route('/anamnese')
def anamnese():
    return render_template('anamnese.html')


@app.route('/frequencia')
def frequencia():
    return render_template('frequencia.html')


@app.route('/pacientes/<int:paciente_id>')
def paciente(paciente_id):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes WHERE id = ?', (paciente_id,))
    paciente = cursor.fetchone()
    conn.close()
    return render_template('pacientes.html', paciente=paciente)


@app.route('/salvar_cadastro', methods=['POST'])
def salvar_cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        mes_referencia = request.form['mes_referencia']
        convenio = request.form['convenio']
        profissional_assistente = request.form['profissional_assistente']
        tipo_atendimento = request.form['tipo_atendimento']

        conn = sqlite3.connect('pacientes.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO pacientes (nome, mes_referencia, convenio, profissional_assistente, tipo_atendimento)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, mes_referencia, convenio, profissional_assistente, tipo_atendimento))

        conn.commit()
        conn.close()

        return redirect(url_for('index')) 
    

@app.route('/apagar_cadastro/<int:paciente_id>', methods=['POST'])
def apagar_cadastro(paciente_id):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM pacientes WHERE id = ?', (paciente_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

    

if __name__ == '__main__':
    app.run(debug=True)
