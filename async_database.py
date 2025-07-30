"""Async database operations for the banking application."""

import asyncio
import sqlite3
import aiosqlite
from typing import List, Tuple, Optional, Dict, Any
from contextlib import asynccontextmanager
from logging_config import banking_logger
from exceptions import DatabaseError, ConnectionError, ClientNotFoundError
from config import config

logger = banking_logger.get_logger("AsyncDatabase")

class AsyncDatabaseManager:
    """Async database manager for better performance."""
    
    def __init__(self):
        self.db_path = config.get_database_path()
        self.connection_pool = []
        self.max_connections = 5
        self._lock = asyncio.Lock()
    
    async def initialize(self):
        """Initialize the database connection pool."""
        try:
            # Create initial connections
            for _ in range(self.max_connections):
                conn = await aiosqlite.connect(self.db_path)
                await conn.execute("PRAGMA foreign_keys = ON")
                self.connection_pool.append(conn)
            
            # Create tables
            await self.create_tables()
            await self.migrate_database()
            await self.insert_sample_data()
            
            logger.info("Async database manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize async database: {e}")
            raise ConnectionError(f"Database initialization failed: {e}", e)
    
    async def get_connection(self):
        """Get a database connection from the pool."""
        async with self._lock:
            if self.connection_pool:
                return self.connection_pool.pop()
            else:
                # Create new connection if pool is empty
                conn = await aiosqlite.connect(self.db_path)
                await conn.execute("PRAGMA foreign_keys = ON")
                return conn
    
    async def return_connection(self, conn):
        """Return a connection to the pool."""
        async with self._lock:
            if len(self.connection_pool) < self.max_connections:
                self.connection_pool.append(conn)
            else:
                await conn.close()
    
    @asynccontextmanager
    async def get_db_connection(self):
        """Context manager for database connections."""
        conn = await self.get_connection()
        try:
            yield conn
        finally:
            await self.return_connection(conn)
    
    async def create_tables(self):
        """Create database tables asynchronously."""
        async with self.get_db_connection() as conn:
            # Create clients table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT,
                    prenom TEXT,
                    email TEXT,
                    telephone TEXT,
                    adresse TEXT,
                    devis REAL DEFAULT 0.0,
                    dinar REAL DEFAULT 0.0,
                    dette REAL DEFAULT 0.0
                )
            ''')
            
            # Create accounts table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS comptes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER,
                    type_compte TEXT NOT NULL,
                    solde REAL DEFAULT 0.0,
                    date_creation DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
            ''')
            
            # Create transactions table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    compte_id INTEGER,
                    montant REAL NOT NULL,
                    type_transaction TEXT NOT NULL,
                    date_transaction DATETIME DEFAULT CURRENT_TIMESTAMP,
                    description TEXT,
                    FOREIGN KEY (compte_id) REFERENCES comptes (id)
                )
            ''')
            
            await conn.commit()
            logger.info("Database tables created successfully")
    
    async def migrate_database(self):
        """Migrate database schema asynchronously."""
        async with self.get_db_connection() as conn:
            # Check if migration is needed
            cursor = await conn.execute("PRAGMA table_info(clients)")
            columns = [row[1] for row in await cursor.fetchall()]
            
            if 'solde' in columns and 'devis' not in columns:
                # Add new columns
                await conn.execute("ALTER TABLE clients ADD COLUMN devis REAL DEFAULT 0.0")
                await conn.execute("ALTER TABLE clients ADD COLUMN dinar REAL DEFAULT 0.0")
                
                # Migrate existing data
                await conn.execute("UPDATE clients SET devis = solde WHERE devis IS NULL")
                
                await conn.commit()
                logger.info("Database migration completed")
    
    async def insert_sample_data(self):
        """Insert sample data asynchronously."""
        async with self.get_db_connection() as conn:
            # Check if data already exists
            cursor = await conn.execute("SELECT COUNT(*) FROM clients")
            count = await cursor.fetchone()
            
            if count[0] > 0:
                return
            
            # Insert sample clients
            clients = [
                ("Dupont", "Jean", "jean.dupont@email.com", "0123456789", "123 Rue de la Paix, Paris", 5000.0, 750000.0, 0.0),
                ("Martin", "Marie", "marie.martin@email.com", "0987654321", "456 Avenue des Champs, Lyon", 12000.0, 1800000.0, 1500.0),
                ("Bernard", "Pierre", "pierre.bernard@email.com", "0555666777", "789 Boulevard Central, Marseille", 2500.0, 375000.0, 3000.0),
                ("", "", "", "", "", 0.0, 0.0, 0.0),  # Example of empty client
                ("Smith", "", "john.smith@email.com", "", "London, UK", 8000.0, 1200000.0, 0.0),  # Missing first name
                ("", "Alice", "", "1234567890", "", 3000.0, 450000.0, 500.0)  # Missing last name
            ]
            
            await conn.executemany('''
                INSERT INTO clients (nom, prenom, email, telephone, adresse, devis, dinar, dette)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', clients)
            
            # Insert sample accounts
            comptes = [
                (1, "Compte Courant", 1500.0),
                (1, "Compte Épargne", 5000.0),
                (2, "Compte Courant", 2300.0),
                (3, "Compte Courant", 800.0)
            ]
            
            await conn.executemany('''
                INSERT INTO comptes (client_id, type_compte, solde)
                VALUES (?, ?, ?)
            ''', comptes)
            
            # Insert sample transactions
            transactions = [
                (1, 500.0, "Dépôt", "Salaire"),
                (1, -200.0, "Retrait", "Achat"),
                (2, 1000.0, "Dépôt", "Virement"),
                (3, -150.0, "Retrait", "Paiement facture")
            ]
            
            await conn.executemany('''
                INSERT INTO transactions (compte_id, montant, type_transaction, description)
                VALUES (?, ?, ?, ?)
            ''', transactions)
            
            await conn.commit()
            logger.info("Sample data inserted successfully")
    
    async def get_all_clients(self) -> List[Tuple]:
        """Get all clients asynchronously."""
        async with self.get_db_connection() as conn:
            cursor = await conn.execute("SELECT * FROM clients ORDER BY nom, prenom")
            clients = await cursor.fetchall()
            logger.debug(f"Retrieved {len(clients)} clients")
            return clients
    
    async def search_clients(self, search_term: str) -> List[Tuple]:
        """Search clients asynchronously."""
        async with self.get_db_connection() as conn:
            if search_term:
                cursor = await conn.execute('''
                    SELECT * FROM clients 
                    WHERE nom LIKE ? OR prenom LIKE ? OR email LIKE ?
                    ORDER BY nom, prenom
                ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            else:
                cursor = await conn.execute("SELECT * FROM clients ORDER BY nom, prenom")
            
            clients = await cursor.fetchall()
            logger.debug(f"Search returned {len(clients)} clients for term: {search_term}")
            return clients
    
    async def add_client(self, client_data: Tuple) -> int:
        """Add a new client asynchronously."""
        async with self.get_db_connection() as conn:
            cursor = await conn.execute('''
                INSERT INTO clients (nom, prenom, email, telephone, adresse, devis, dinar, dette)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', client_data)
            
            await conn.commit()
            client_id = cursor.lastrowid
            logger.info(f"Client added successfully with ID: {client_id}")
            return client_id
    
    async def update_client(self, client_id: int, client_data: Tuple) -> bool:
        """Update a client asynchronously."""
        async with self.get_db_connection() as conn:
            cursor = await conn.execute('''
                UPDATE clients 
                SET nom=?, prenom=?, email=?, telephone=?, adresse=?, devis=?, dinar=?, dette=?
                WHERE id=?
            ''', (*client_data, client_id))
            
            await conn.commit()
            rows_affected = cursor.rowcount
            
            if rows_affected == 0:
                raise ClientNotFoundError(client_id)
            
            logger.info(f"Client {client_id} updated successfully")
            return True
    
    async def delete_client(self, client_id: int) -> bool:
        """Delete a client asynchronously."""
        async with self.get_db_connection() as conn:
            try:
                cursor = await conn.execute("DELETE FROM clients WHERE id=?", (client_id,))
                await conn.commit()
                rows_affected = cursor.rowcount
                
                if rows_affected == 0:
                    raise ClientNotFoundError(client_id)
                
                logger.info(f"Client {client_id} deleted successfully")
                return True
                
            except Exception as e:
                if "FOREIGN KEY constraint failed" in str(e):
                    raise DatabaseError("Cannot delete client because they have associated accounts or transactions. Please delete the accounts first.", e)
                else:
                    raise e
    
    async def get_client_by_id(self, client_id: int) -> Optional[Tuple]:
        """Get a client by ID asynchronously."""
        async with self.get_db_connection() as conn:
            cursor = await conn.execute("SELECT * FROM clients WHERE id=?", (client_id,))
            client = await cursor.fetchone()
            
            if not client:
                raise ClientNotFoundError(client_id)
            
            return client
    
    async def client_has_accounts(self, client_id: int) -> bool:
        """Check if a client has associated accounts."""
        async with self.get_db_connection() as conn:
            cursor = await conn.execute("SELECT COUNT(*) FROM comptes WHERE client_id=?", (client_id,))
            count = await cursor.fetchone()
            return count[0] > 0 if count else False
    
    async def get_client_accounts(self, client_id: int) -> List[Tuple]:
        """Get all accounts for a client."""
        async with self.get_db_connection() as conn:
            cursor = await conn.execute("SELECT * FROM comptes WHERE client_id=?", (client_id,))
            accounts = await cursor.fetchall()
            return accounts
    
    async def delete_account(self, account_id: int) -> bool:
        """Delete an account and its transactions."""
        async with self.get_db_connection() as conn:
            # Delete transactions first
            await conn.execute("DELETE FROM transactions WHERE compte_id=?", (account_id,))
            
            # Delete account
            cursor = await conn.execute("DELETE FROM comptes WHERE id=?", (account_id,))
            await conn.commit()
            
            rows_affected = cursor.rowcount
            if rows_affected == 0:
                raise DatabaseError(f"Account {account_id} not found")
            
            logger.info(f"Account {account_id} and its transactions deleted successfully")
            return True
    
    async def delete_client_accounts(self, client_id: int) -> bool:
        """Delete all accounts and transactions for a client."""
        async with self.get_db_connection() as conn:
            # Get all account IDs for the client
            cursor = await conn.execute("SELECT id FROM comptes WHERE client_id=?", (client_id,))
            account_ids = [row[0] for row in await cursor.fetchall()]
            
            if not account_ids:
                return True  # No accounts to delete
            
            # Delete transactions for all accounts
            for account_id in account_ids:
                await conn.execute("DELETE FROM transactions WHERE compte_id=?", (account_id,))
            
            # Delete all accounts
            await conn.execute("DELETE FROM comptes WHERE client_id=?", (client_id,))
            await conn.commit()
            
            logger.info(f"Deleted {len(account_ids)} accounts and their transactions for client {client_id}")
            return True
    
    async def close(self):
        """Close all database connections."""
        async with self._lock:
            for conn in self.connection_pool:
                await conn.close()
            self.connection_pool.clear()
            logger.info("All database connections closed")

# Global async database instance
async_db = AsyncDatabaseManager() 