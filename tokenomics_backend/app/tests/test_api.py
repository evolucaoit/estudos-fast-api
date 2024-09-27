# test_api.py
import requests
import yaml
from datetime import datetime

# URL base da API
BASE_URL = "http://localhost:7777/api"  # Ajuste conforme necessário

# Função para executar os testes
def run_tests():
    # Relatório de testes
    report = {
        "tests": []
    }

    # Testes para Wallets
    # Criar uma nova carteira
    wallet_data = {
        "user_id": 1,
        "public_key": "pk_123456",
        "private_key_hash": "hash_123456",
        "currency": "USD",
        "token_type": "ERC20"
    }
    response = requests.post(f"{BASE_URL}/wallets/", json=wallet_data)
    report["tests"].append({
        "description": "Criar Wallet",
        "curl": f"curl -X POST {BASE_URL}/wallets/ -H 'Content-Type: application/json' -d '{wallet_data}'",
        "expected_status": 200,
        "received_status": response.status_code,
        "verdict": "✅ Sucesso" if response.status_code == 200 else "❌ Falha",
        "response": response.json()
    })

    # Obter a carteira
    wallet_id = 1  # Assume que a carteira criada tem ID 1
    response = requests.get(f"{BASE_URL}/wallets/{wallet_id}")
    report["tests"].append({
        "description": "Obter Wallet",
        "curl": f"curl -X GET {BASE_URL}/wallets/{wallet_id}",
        "expected_status": 200,
        "received_status": response.status_code,
        "verdict": "✅ Sucesso" if response.status_code == 200 else "❌ Falha",
        "response": response.json()
    })

    # Atualizar a carteira
    wallet_update_data = {
        "public_key": "pk_updated",
        "private_key_hash": "hash_updated",
        "currency": "EUR",
        "token_type": "ERC20"
    }
    response = requests.put(f"{BASE_URL}/wallets/{wallet_id}", json=wallet_update_data)
    report["tests"].append({
        "description": "Atualizar Wallet",
        "curl": f"curl -X PUT {BASE_URL}/wallets/{wallet_id} -H 'Content-Type: application/json' -d '{wallet_update_data}'",
        "expected_status": 200,
        "received_status": response.status_code,
        "verdict": "✅ Sucesso" if response.status_code == 200 else "❌ Falha",
        "response": response.json()
    })

    # Deletar a carteira
    response = requests.delete(f"{BASE_URL}/wallets/{wallet_id}")
    report["tests"].append({
        "description": "Deletar Wallet",
        "curl": f"curl -X DELETE {BASE_URL}/wallets/{wallet_id}",
        "expected_status": 200,
        "received_status": response.status_code,
        "verdict": "✅ Sucesso" if response.status_code == 200 else "❌ Falha",
        "response": response.json()
    })

    # Testes para Users (similar aos testes de Wallets)
    user_data = {
        "name": "Elias Andrade",
        "email": "elias@example.com",
        "password_hash": "hash_password",
        "user_type": "admin",
        "creation_date": "2024-09-27",
        "country": "BR",
        "status": "active"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    report["tests"].append({
        "description": "Criar Usuário",
        "curl": f"curl -X POST {BASE_URL}/users/ -H 'Content-Type: application/json' -d '{user_data}'",
        "expected_status": 200,
        "received_status": response.status_code,
        "verdict": "✅ Sucesso" if response.status_code == 200 else "❌ Falha",
        "response": response.json()
    })

    # Gerar relatórios
    generate_reports(report)

# Função para gerar os relatórios
def generate_reports(report):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Gerar relatório em YAML
    with open("app/tests/reports/test_report.yaml", "w", encoding='utf-8') as yaml_file:
        yaml.dump(report, yaml_file, allow_unicode=True)
    
    # Gerar relatório em TXT
    with open("app/tests/reports/test_report.txt", "w", encoding='utf-8') as txt_file:
        txt_file.write(f"Relatório de Testes - {timestamp}\n")
        txt_file.write("=" * 40 + "\n")
        for test in report["tests"]:
            txt_file.write(f"Descrição: {test['description']}\n")
            txt_file.write(f"  CURL: {test['curl']}\n")
            txt_file.write(f"  Status Esperado: {test['expected_status']}\n")
            txt_file.write(f"  Status Recebido: {test['received_status']}\n")
            txt_file.write(f"  Veredito: {test['verdict']}\n")
            txt_file.write(f"  Resposta: {test['response']}\n")
            txt_file.write("-" * 40 + "\n")

if __name__ == "__main__":
    run_tests()
