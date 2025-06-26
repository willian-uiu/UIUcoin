import csv
import os
import time
from web3 import Web3
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# --- 1. CONFIGURAÇÃO ---
# Obtenha as variáveis de ambiente
rpc_url = os.getenv("RPC")
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")

# Verificações de segurança
if not all([rpc_url, private_key, contract_address]):
    raise ValueError("Certifique-se de que RPC, PRIVATE_KEY, e CONTRACT_ADDRESS estão definidos no arquivo .env")

# Defina o ABI do seu contrato aqui.
# Este é um exemplo de ABI mínimo para um contrato ERC20 com uma função mint().
# **SUBSTITUA PELO ABI REAL DO SEU CONTRATO**
CONTRACT_ABI = open('uiucoinabi.json','r').read()

# Nome do arquivo CSV
CSV_FILE = 'destinatarios.csv'


# --- 2. CONEXÃO COM A BLOCKCHAIN ---
try:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print("🔴 Falha ao conectar ao nó Ethereum.")
        exit()
    print("✅ Conectado à rede Ethereum!")
except Exception as e:
    print(f"🔴 Erro ao conectar via RPC: {e}")
    exit()

# --- 3. CONFIGURAÇÃO DA CONTA E CONTRATO ---
# Carrega a conta que fará o mint (a partir da chave privada)
minter_account = w3.eth.account.from_key(private_key)
w3.eth.default_account = minter_account.address
print(f"🔧 Usando a carteira do minter: {minter_account.address}")

# Instancia o contrato
contract = w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)

# Obtém a quantidade de casas decimais do token (importante para conversão)
try:
    TOKEN_DECIMALS = contract.functions.decimals().call()
    print(f"Token decimals: {TOKEN_DECIMALS}")
except Exception as e:
    print("⚠️ Não foi possível chamar a função decimals(). Usando 18 como padrão. Erro:", e)
    TOKEN_DECIMALS = 18

# --- 4. LÓGICA DE MINT AUTOMATIZADO ---
def mint_tokens():
    """
    Lê o arquivo CSV e envia as transações de mint.
    """
    try:
        # Pega o nonce inicial ANTES do loop para garantir a ordem correta
        nonce = w3.eth.get_transaction_count(minter_account.address)
        print(f"Nonce inicial da conta: {nonce}")

        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    recipient_address = Web3.to_checksum_address(row['carteira'])
                    amount_to_mint = int(row['quantidade'])
                    
                    # Converte a quantidade para a unidade correta (ex: 100 -> 100 * 10**18)
                    amount_in_wei = amount_to_mint * (10 ** TOKEN_DECIMALS)

                    print(f"\n🚀 Preparando para mintar {amount_to_mint} tokens para {recipient_address}...")

                    # 1. Constrói a transação
                    tx_params = {
                        'from': minter_account.address,
                        'nonce': nonce,
                        'gas': 200000,  # Limite de gás (pode precisar de ajuste)
                        'gasPrice': w3.eth.gas_price,
                        'chainId': 11155111
                    }
                    
                    transaction = contract.functions.mint(recipient_address, amount_in_wei).build_transaction(tx_params)

                    # 2. Assina a transação
                    signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
                
                    # 3. Envia a transação
                    #tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                    # Linha correta para web3 v6+
                    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                    print(f"⏳ Transação enviada! Hash: {w3.to_hex(tx_hash)}")

                    # 4. (Opcional, mas recomendado) Espera pelo recibo da transação
                    print("... Aguardando confirmação da transação ...")
                    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                    
                    if tx_receipt['status'] == 1:
                        print(f"✅ Sucesso! Transação confirmada no bloco: {tx_receipt.blockNumber}")
                    else:
                        print(f"❌ Falha! A transação falhou. Verifique o Etherscan para mais detalhes.")

                    # Incrementa o nonce para a próxima transação
                    nonce += 1
                    time.sleep(1) # Pequena pausa para não sobrecarregar o nó RPC
                    
                except Exception as e:
                    print(f"🔴 Erro ao processar a linha {row}: {e}")
                    continue # Continua para a próxima linha do CSV

    except FileNotFoundError:
        print(f"🔴 Erro: Arquivo '{CSV_FILE}' não encontrado.")
    except Exception as e:
        print(f"🔴 Um erro inesperado ocorreu: {e}")

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    mint_tokens()
    print("\n🎉 Script finalizado.")