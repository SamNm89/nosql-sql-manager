# Banking Management System

A modern desktop banking management system with advanced features including async operations, internationalization, comprehensive logging, robust error handling, and real-time SQL preview for learning and debugging.

## ✨ Features

- **🌍 Internationalization**: Support for English and French languages with dynamic switching
- **⚡ Async Operations**: High-performance database operations with connection pooling
- **📝 Comprehensive Logging**: Detailed logging with file and console output
- **🛡️ Error Handling**: Robust error handling with custom exceptions
- **⚙️ Configuration Management**: Flexible configuration system
- **🔧 Easy Deployment**: Automated deployment scripts and setup tools
- **💾 Client Management**: Add, edit, delete, and search clients with validation
- **💰 Financial Tracking**: Track balances in Euros (Devis), Algerian Dinars (DZD), and debt
- **🔍 Real-Time SQL Preview**: Live SQL command preview with syntax highlighting
- **🎨 Modern UI**: Clean interface with dark SQL preview theme
- **🔄 Manual Control**: No automatic refreshes - full user control over operations
- **📊 Account Management**: Separate client records and banking accounts
- **🔒 Safe Operations**: Smart delete operations with account protection

## 🚀 Quick Start

### Option 1: Automated Deployment
```bash
# Run the deployment script
python deploy.py
```

### Option 2: Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

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

## 🏗️ Project Structure

```
banking-app/
├── main.py                 # Main application entry point
├── async_database.py       # Async database operations
├── logging_config.py       # Logging configuration
├── exceptions.py           # Custom exception classes
├── i18n.py                # Internationalization support
├── config.py              # Configuration management
├── deploy.py              # Deployment automation
├── setup.py               # Package setup
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── config.json            # Application configuration (auto-generated)
├── banque.db              # SQLite database (auto-generated)
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

### **Financial Tracking**
- **Devis (€)**: Euro balances
- **Dinar (DZD)**: Algerian Dinar balances  
- **Debt (€)**: Outstanding debt tracking
- **Account Separation**: Individual banking accounts separate from client records

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

Language can be changed dynamically through the UI dropdown without restarting the application.

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

### Edit Client
```sql
UPDATE clients SET nom='Smith', prenom='John', email='john@email.com', 
telephone='1234567890', adresse='123 Main St', devis=5000.0, dinar=750000.0, dette=0.0 
WHERE id=1;
```

### Delete Account (Full Delete)
```sql
-- Delete client accounts first
DELETE FROM comptes WHERE client_id=1;

-- Then delete the client
DELETE FROM clients WHERE id=1;
```

### Search Clients
```sql
SELECT * FROM clients WHERE nom LIKE '%Smith%' OR prenom LIKE '%John%' 
OR email LIKE '%john%' ORDER BY nom, prenom;
```

## 🛡️ Error Handling

The application includes robust error handling:

- **Custom Exceptions**: Specific exception types for different error scenarios
- **Graceful Degradation**: Application continues running even if some operations fail
- **User-Friendly Messages**: Translated error messages
- **Detailed Logging**: All errors are logged with stack traces
- **SQL Preview Errors**: Automatic recovery from SQL preview window issues

## ⚡ Performance Features

- **Async Database Operations**: Non-blocking database operations
- **Connection Pooling**: Efficient database connection management
- **Background Processing**: UI remains responsive during operations
- **Caching**: Optional caching for frequently accessed data
- **No Auto-Refresh**: Manual control prevents unnecessary database calls

## 🚀 Deployment

### Automated Deployment
```bash
# Run deployment script
python deploy.py
```

This will:
- Create a virtual environment
- Install all dependencies
- Create necessary directories
- Generate configuration files
- Create launcher scripts
- Run basic tests

### Manual Deployment
```bash
# Create virtual environment
python -m venv banking_env

# Activate virtual environment
# Windows:
banking_env\Scripts\activate
# Unix/macOS:
source banking_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 📦 Package Installation

```bash
# Install as a package
pip install -e .

# Run from anywhere
banking-app
```

## 🔧 Development

### Adding New Features
1. Follow the existing code structure
2. Add proper logging using `banking_logger.get_logger("ModuleName")`
3. Use custom exceptions from `exceptions.py`
4. Add translations to `locales/en.json` and `locales/fr.json`
5. Update configuration in `config.py` if needed
6. Include SQL preview for database operations

### Testing
```bash
# Run basic tests
python -c "import main; print('Import test passed')"

# Test database operations
python -c "import asyncio; from async_database import async_db; asyncio.run(async_db.initialize()); print('Database test passed')"
```

## 🎯 User Guide

### Getting Started
1. **Launch Application**: Run `python main.py`
2. **Connect Database**: Click "Connect Database" button
3. **Language Selection**: Choose your preferred language from the dropdown
4. **SQL Preview**: Toggle "Show SQL Preview" to see database operations

### Client Operations
1. **Add Client**: Click "Add Client" → Fill form → See INSERT SQL
2. **Edit Client**: Select client → Click "Edit Client" → Modify → See UPDATE SQL
3. **Delete Client**: Select client → Click "Delete Client" → See DELETE SQL
4. **Delete Account**: Select client → Click "Delete Account" → See comprehensive DELETE SQL
5. **Search**: Type in search box → See SELECT SQL with WHERE clauses
6. **Refresh**: Click "Refresh" → See SELECT SQL for all clients

### SQL Preview Features
- **Dark Theme**: Easy-to-read SQL commands
- **Stay on Top**: Window remains visible during operations
- **Close Button**: Easy to hide when not needed
- **Toggle**: Show/hide with button or toggle function

## 📝 License

This project is open source. Feel free to modify and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Include SQL preview for new database operations
6. Submit a pull request

## 📞 Support

For issues and questions:
- Check the logs in the `logs/` directory
- Review the configuration in `config.json`
- Ensure all dependencies are installed
- Verify Python version (3.8+)
- Check SQL preview for operation details

## 🔄 Updates

The application includes automatic database migration and will handle schema updates automatically when new versions are released. The SQL preview feature helps users understand database changes and operations. 