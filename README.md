# Banking Management System

A modern desktop banking management system with advanced features including async operations, internationalization, comprehensive logging, robust error handling, and real-time SQL preview for learning and debugging.

## ✨ Features

- **🌍 Internationalization**: Support for English and French languages with dynamic switching
- **💾 Client Management**: Add, edit, delete, and search clients with validation
- **🔍 Real-Time SQL Preview**: Live SQL command preview with syntax highlighting

## 🚀 Quick Start

### Option 1: Using the Batch File (Recommended)
```bash
# Simply double-click or run:
run_app.bat
```

### Option 2: Manual Installation
```bash
# Activate virtual environment
banking_env\Scripts\activate

# Run the application
python main.py
```

## 📋 Requirements

- **Python**: 3.8 or higher
- **Dependencies**: 
  - `aiosqlite==0.19.0` - Async SQLite operations
  - `asyncio-mqtt==0.16.1` - Async messaging
  - `aiofiles==23.2.1` - Async file operations
- **OS**: Windows, macOS, Linux
- 
## 🎯 User Guide

### Getting Started
1. **Launch Application**: Run `run_app.bat` or `python main.py`
2. **Connect Database**: Click "Connect Database" button
3. **Language Selection**: Choose your preferred language from the dropdown
4. **SQL Preview**: Toggle "Show SQL Preview" to see database operations


## 🏗️ Project Structure

```
banking-app/
├── main.py                 # Main application entry point
├── async_database.py       # Async database operations
├── logging_config.py       # Logging configuration
├── exceptions.py           # Custom exception classes
├── i18n.py                # Internationalization support
├── config.py              # Configuration management
├── requirements.txt        # Python dependencies
├── run_app.bat            # Application launcher
├── README.md              # This file
├── config.json            # Application configuration
├── banque.db              # SQLite database
├── banking_env/           # Virtual environment
├── locales/               # Translation files
│   ├── en.json           # English translations
│   └── fr.json           # French translations
└── logs/                  # Log files (auto-generated)
```

## 🎯 Key Features

### **Real-Time SQL Preview**
- **Live SQL Commands**: See exactly what SQL is being executed
- **Dark Theme**: Black background with white text for better readability
- **Stay on Top**: SQL preview window stays visible during operations
- **Comprehensive Coverage**: Shows SQL for all operations (INSERT, UPDATE, DELETE, SELECT)
- **Manual Control**: No automatic refreshes - you control when to update

### **Smart Client Management**
- **Add Client**: Shows INSERT SQL with all client details
- **Edit Client**: Shows UPDATE SQL with modified fields
- **Delete Client**: Safe delete with account protection
- **Delete Account**: Destructive delete (removes client and all accounts)
- **Search**: Real-time search with SQL preview
- **Refresh**: Manual refresh with SQL preview

## 🔧 Configuration

The application automatically creates a `config.json` file with default settings:

```json
{
  "database": {
    "path": "banque.db",
    "backup_enabled": true,
    "backup_interval": 24,
    "max_backups": 7
  },
  "ui": {
    "language": "en",
    "theme": "default",
    "window_size": "1600x800",
    "auto_save": true
  },
  "logging": {
    "level": "INFO",
    "file_enabled": true,
    "console_enabled": true,
    "max_file_size": 10,
    "backup_count": 5
  },
  "security": {
    "encrypt_sensitive_data": false,
    "session_timeout": 30,
    "max_login_attempts": 3
  },
  "performance": {
    "cache_enabled": true,
    "cache_size": 100,
    "async_operations": true,
    "batch_size": 50
  }
}
```

## 🌍 Internationalization

The application supports multiple languages with dynamic switching:

- **English** (en): Default language
- **French** (fr): Complete French translation

Language can be changed through the UI dropdown without restarting the application.

## 📊 Database Structure

### Clients Table
- `id`: Unique identifier
- `nom`: Last name
- `prenom`: First name
- `email`: Email address
- `telephone`: Phone number
- `adresse`: Address
- `devis`: Balance in Euros
- `dinar`: Balance in Algerian Dinars
- `dette`: Debt amount

### Comptes Table (Banking Accounts)
- `id`: Unique identifier
- `client_id`: Reference to client
- `type_compte`: Account type (e.g., "Compte Courant", "Compte Épargne")
- `solde`: Account balance
- `date_creation`: Creation date

### Transactions Table
- `id`: Unique identifier
- `compte_id`: Reference to account
- `montant`: Transaction amount
- `type_transaction`: Transaction type
- `date_transaction`: Transaction date/time
- `description`: Transaction description

## 🔍 SQL Preview Examples

### Add Client
```sql
INSERT INTO clients (nom, prenom, email, telephone, adresse, devis, dinar, dette) 
VALUES ('Smith', 'John', 'john@email.com', '1234567890', '123 Main St', 5000.0, 750000.0, 0.0);
```



