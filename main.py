import secrets
import string
import sqlite3

NOME_DB = 'senhas_geradas.db'

# Fun - Geração
def gerar_senha(comprimento=16):
    """Gera uma senha aleatória e criptograficamente segura."""
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha_segura = ''.join(secrets.choice(caracteres) for i in range(comprimento))
    return senha_segura

# Fun - Bancco de dados
def configurar_db():
    """Cria a tabela de senhas se ela não existir."""
    conn = sqlite3.connect(NOME_DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS senhas (
            id INTEGER PRIMARY KEY,
            servico TEXT NOT NULL,
            usuario TEXT,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def armazenar_senha(servico, usuario, senha):
    """Armazena a senha no banco de dados."""
    conn = sqlite3.connect(NOME_DB)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO senhas (servico, usuario, senha)
        VALUES (?, ?, ?)
    ''', (servico, usuario, senha))
    conn.commit()
    conn.close()
    print(f"\nSenha para '{servico}' armazenada com sucesso!")

def listar_senhas():
    """Lista todas as senhas armazenadas."""
    conn = sqlite3.connect(NOME_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT servico, usuario, senha FROM senhas')
    registros = cursor.fetchall()
    conn.close()
    
    if registros:
        print("\n--- Senhas Armazenadas ---")
        for servico, usuario, senha in registros:
            print(f"Serviço: {servico} | Usuário: {usuario} | Senha: {senha}")
        print("--------------------------")
    else:
        print("\nNenhuma senha armazenada.")

# MAIN
def main():
    # 1. Onde configura o BD
    configurar_db()
    
    while True:
        print("\n=== Gerenciador de Senhas ===")
        print("1. Gerar e Armazenar Nova Senha")
        print("2. Listar Senhas Armazenadas")
        print("3. Sair")
        
        escolha = input("Escolha uma das opções (1-3): ")
        
        if escolha == '1':
            servico = input("Nome do Serviço (ex: Gmail, Netflix): ")
            usuario = input("Seu E-mail/Usuário: ")
            
            comprimento_senha = 22
            nova_senha = gerar_senha(comprimento_senha)
            
            print(f"\nSenha gerada com {comprimento_senha} caracteres: **{nova_senha}**")
            
            armazenar_senha(servico, usuario, nova_senha)
            
        elif escolha == '2':
            listar_senhas()
            
        elif escolha == '3':
            print("Saindo do programa!")
            break
            
        else:
            print("Opção inválida. Tente novamente.")

# Execução
if __name__ == "__main__":
    main()