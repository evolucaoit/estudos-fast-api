from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
import os
from typing import List

# Definição do roteador
router = APIRouter()

import os

# Caminho do banco de dados
db_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db'))  # Ajuste para um nível acima da pasta 'app'
db_path = os.path.join(db_dir, "network_database.db")


# Modelos para as operações
class WalletCreate(BaseModel):
    user_id: int
    public_key: str
    private_key_hash: str
    currency: str
    token_type: str

class WalletUpdate(BaseModel):
    public_key: str
    private_key_hash: str
    currency: str
    token_type: str

class UserCreate(BaseModel):
    name: str
    email: str
    password_hash: str
    user_type: str
    creation_date: str
    country: str
    status: str

class UserUpdate(BaseModel):
    name: str
    email: str
    password_hash: str
    country: str
    status: str

# Rotas para Wallets
@router.post("/wallets/", response_model=dict)
def create_wallet(wallet: WalletCreate):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO wallets (user_id, public_key, private_key_hash, currency, token_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (wallet.user_id, wallet.public_key, wallet.private_key_hash, wallet.currency, wallet.token_type))
        
        conn.commit()
        return {"message": "Carteira criada com sucesso"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Chave pública já existe.")
    finally:
        conn.close()

@router.get("/wallets/{wallet_id}", response_model=dict)
def get_wallet(wallet_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM wallets WHERE id = ?', (wallet_id,))
    wallet = cursor.fetchone()
    conn.close()

    if wallet:
        return {
            "id": wallet[0],
            "user_id": wallet[1],
            "public_key": wallet[2],
            "private_key_hash": wallet[3],
            "token_balance": wallet[4],
            "currency": wallet[5],
            "token_type": wallet[6]
        }
    else:
        raise HTTPException(status_code=404, detail="Carteira não encontrada.")

@router.put("/wallets/{wallet_id}", response_model=dict)
def update_wallet(wallet_id: int, wallet: WalletUpdate):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE wallets SET public_key = ?, private_key_hash = ?, currency = ?, token_type = ?
        WHERE id = ?
    ''', (wallet.public_key, wallet.private_key_hash, wallet.currency, wallet.token_type, wallet_id))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Carteira não encontrada.")
    
    conn.commit()
    conn.close()
    return {"message": "Carteira atualizada com sucesso"}

@router.delete("/wallets/{wallet_id}", response_model=dict)
def delete_wallet(wallet_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM wallets WHERE id = ?', (wallet_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Carteira não encontrada.")
    
    conn.commit()
    conn.close()
    return {"message": "Carteira deletada com sucesso"}

# Rotas para Users
@router.post("/users/", response_model=dict)
def create_user(user: UserCreate):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (name, email, password_hash, user_type, creation_date, country, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user.name, user.email, user.password_hash, user.user_type, user.creation_date, user.country, user.status))
        
        conn.commit()
        return {"message": "Usuário criado com sucesso"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email já existe.")
    finally:
        conn.close()

@router.get("/users/{user_id}", response_model=dict)
def get_user(user_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "user_type": user[3],
            "creation_date": user[4],
            "country": user[5],
            "status": user[6]
        }
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

@router.put("/users/{user_id}", response_model=dict)
def update_user(user_id: int, user: UserUpdate):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users SET name = ?, email = ?, password_hash = ?, country = ?, status = ?
        WHERE id = ?
    ''', (user.name, user.email, user.password_hash, user.country, user.status, user_id))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    conn.commit()
    conn.close()
    return {"message": "Usuário atualizado com sucesso"}

@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    conn.commit()
    conn.close()
    return {"message": "Usuário deletado com sucesso"}

# Aqui você pode adicionar mais rotas CRUD para outras tabelas, como tokens, transactions, etc.

# Por exemplo, aqui estão as rotas para a tabela de tokens
class TokenCreate(BaseModel):
    token_name: str
    token_symbol: str
    total_supply: float
    decimal_places: int = 18
    token_type: str
    creation_date: str

@router.post("/tokens/", response_model=dict)
def create_token(token: TokenCreate):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tokens (token_name, token_symbol, total_supply, decimal_places, token_type, creation_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (token.token_name, token.token_symbol, token.total_supply, token.decimal_places, token.token_type, token.creation_date))
    
    conn.commit()
    conn.close()
    return {"message": "Token criado com sucesso"}

@router.get("/tokens/{token_id}", response_model=dict)
def get_token(token_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tokens WHERE id = ?', (token_id,))
    token = cursor.fetchone()
    conn.close()

    if token:
        return {
            "id": token[0],
            "token_name": token[1],
            "token_symbol": token[2],
            "total_supply": token[3],
            "decimal_places": token[4],
            "token_type": token[5],
            "creation_date": token[6]
        }
    else:
        raise HTTPException(status_code=404, detail="Token não encontrado.")

@router.put("/tokens/{token_id}", response_model=dict)
def update_token(token_id: int, token: TokenCreate):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE tokens SET token_name = ?, token_symbol = ?, total_supply = ?, decimal_places = ?, token_type = ?, creation_date = ?
        WHERE id = ?
    ''', (token.token_name, token.token_symbol, token.total_supply, token.decimal_places, token.token_type, token.creation_date, token_id))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Token não encontrado.")
    
    conn.commit()
    conn.close()
    return {"message": "Token atualizado com sucesso"}

@router.delete("/tokens/{token_id}", response_model=dict)
def delete_token(token_id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM tokens WHERE id = ?', (token_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Token não encontrado.")
    
    conn.commit()
    conn.close()
    return {"message": "Token deletado com sucesso"}
