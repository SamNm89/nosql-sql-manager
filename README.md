# Banking Management System

A modern desktop banking management system with advanced features including async operations, internationalization, comprehensive logging, and robust error handling.

## ✨ Features

- **🌍 Internationalization**: Support for English and French languages
- **⚡ Async Operations**: High-performance database operations with connection pooling
- **📝 Comprehensive Logging**: Detailed logging with file and console output
- **🛡️ Error Handling**: Robust error handling with custom exceptions
- **⚙️ Configuration Management**: Flexible configuration system
- **🔧 Easy Deployment**: Automated deployment scripts and setup tools
- **💾 Client Management**: Add, edit, delete, and search clients
- **💰 Financial Tracking**: Track balances in Euros (Devis) and Algerian Dinars (DZD)
- **🔍 SQL Preview**: Real-time SQL command preview for learning
- **🎨 Modern UI**: Clean interface with language switching

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
- **Dependencies**: See `requirements.txt`
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
├── locales/               # Translation files
│   ├── en.json           # English translations
│   └── fr.json           # French translations
└── logs/                  # Log files (auto-generated)
```

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
  "performance": {
    "async_operations": true,
    "cache_enabled": true,
    "cache_size": 100,
    "batch_size": 50
  }
}
```

## 🌍 Internationalization

The application supports multiple languages:

- **English** (en): Default language
- **French** (fr): Complete French translation

Language can be changed dynamically through the UI dropdown.

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

### Accounts Table
- `id`: Unique identifier
- `client_id`: Reference to client
- `type_compte`: Account type
- `solde`: Account balance
- `date_creation`: Creation date

### Transactions Table
- `id`: Unique identifier
- `compte_id`: Reference to account
- `montant`: Transaction amount
- `type_transaction`: Transaction type
- `date_transaction`: Transaction date/time
- `description`: Transaction description

## 🔍 Logging

The application provides comprehensive logging:

- **File Logging**: Daily log files in `logs/` directory
- **Console Logging**: Real-time console output
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Log Rotation**: Automatic log file rotation

Example log output:
```
2024-01-15 10:30:15 - BankingApp.Main - INFO - Starting Banking Management System...
2024-01-15 10:30:16 - BankingApp.AsyncDatabase - INFO - Database initialized successfully
2024-01-15 10:30:17 - BankingApp.Main - INFO - Language changed to: en
```

## 🛡️ Error Handling

The application includes robust error handling:

- **Custom Exceptions**: Specific exception types for different error scenarios
- **Graceful Degradation**: Application continues running even if some operations fail
- **User-Friendly Messages**: Translated error messages
- **Detailed Logging**: All errors are logged with stack traces

## ⚡ Performance Features

- **Async Database Operations**: Non-blocking database operations
- **Connection Pooling**: Efficient database connection management
- **Background Processing**: UI remains responsive during operations
- **Caching**: Optional caching for frequently accessed data

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

### Testing
```bash
# Run basic tests
python -c "import main; print('Import test passed')"
```

## 📝 License

This project is open source. Feel free to modify and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the logs in the `logs/` directory
- Review the configuration in `config.json`
- Ensure all dependencies are installed
- Verify Python version (3.8+)

## 🔄 Updates

The application includes automatic database migration and will handle schema updates automatically when new versions are released. 