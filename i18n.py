"""Internationalization support for French and English."""

import json
import os
from typing import Dict, Any

class I18nManager:
    """Manages internationalization for the banking application."""
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load translation files for the current language."""
        try:
            # Load English translations
            with open("locales/en.json", "r", encoding="utf-8") as f:
                self.translations["en"] = json.load(f)
            
            # Load French translations
            with open("locales/fr.json", "r", encoding="utf-8") as f:
                self.translations["fr"] = json.load(f)
                
        except FileNotFoundError:
            # Create default translations if files don't exist
            self.create_default_translations()
    
    def create_default_translations(self):
        """Create default translation files."""
        os.makedirs("locales", exist_ok=True)
        
        # English translations
        en_translations = {
            "app_title": "Banking Management System",
            "connect_database": "Connect to Database",
            "connected": "Connected",
            "add_client": "Add Client",
            "edit_client": "Edit Client",
            "delete_client": "Delete Client",
            "refresh": "Refresh",
            "search_client": "Search for a client",
            "show_sql_preview": "Show/Hide SQL Preview",
            "last_name": "Last Name",
            "first_name": "First Name",
            "email": "Email",
            "phone": "Phone",
            "address": "Address",
            "devis_eur": "Devis (€)",
            "dinar_dzd": "Dinar (DZD)",
            "debt_eur": "Debt (€)",
            "ok": "OK",
            "cancel": "Cancel",
            "confirm": "Confirm",
            "warning": "Warning",
            "error": "Error",
            "success": "Success",
            "info": "Information",
            "client_management": "Client Management",
            "sql_preview": "SQL Preview",
            "generated_sql": "Generated SQL Command:",
            "database_connection_successful": "Database connection successful!",
            "database_connection_failed": "Failed to connect to database!",
            "please_connect_first": "Please connect to database first!",
            "select_client_to_edit": "Please select a client to edit.",
            "select_client_to_delete": "Please select a client to delete.",
            "confirm_delete_client": "Are you sure you want to delete this client?",
            "last_name_required": "Last name and first name are required!",
            "invalid_numbers": "Devis, Dinar and Debt must be valid numbers!",
            "client_added": "Client added successfully!",
            "client_updated": "Client updated successfully!",
            "client_deleted": "Client deleted successfully!",
            "id": "ID",
            "devis": "Devis (€)",
            "dinar": "Dinar (DZD)",
            "debt": "Debt (€)",
            "cannot_delete_client_with_accounts": "Cannot delete client because they have associated accounts or transactions. Please delete the accounts first.",
            "confirm_delete_client_with_accounts": "This will delete the client AND ALL THEIR ACCOUNTS AND TRANSACTIONS. Are you sure?",
            "client_and_accounts_deleted": "Client and all accounts deleted successfully!"
        }
        
        # French translations
        fr_translations = {
            "app_title": "Système de Gestion Bancaire",
            "connect_database": "Se connecter à la base de données",
            "connected": "Connecté",
            "add_client": "Ajouter Client",
            "edit_client": "Modifier Client",
            "delete_client": "Supprimer Client",
            "refresh": "Actualiser",
            "search_client": "Rechercher un client",
            "show_sql_preview": "Afficher/Masquer Aperçu SQL",
            "last_name": "Nom de famille",
            "first_name": "Prénom",
            "email": "Email",
            "phone": "Téléphone",
            "address": "Adresse",
            "devis_eur": "Devis (€)",
            "dinar_dzd": "Dinar (DZD)",
            "debt_eur": "Dette (€)",
            "ok": "OK",
            "cancel": "Annuler",
            "confirm": "Confirmer",
            "warning": "Attention",
            "error": "Erreur",
            "success": "Succès",
            "info": "Information",
            "client_management": "Gestion des Clients",
            "sql_preview": "Aperçu SQL",
            "generated_sql": "Commande SQL générée :",
            "database_connection_successful": "Connexion à la base de données réussie !",
            "database_connection_failed": "Échec de la connexion à la base de données !",
            "please_connect_first": "Veuillez d'abord vous connecter à la base de données !",
            "select_client_to_edit": "Veuillez sélectionner un client à modifier.",
            "select_client_to_delete": "Veuillez sélectionner un client à supprimer.",
            "confirm_delete_client": "Êtes-vous sûr de vouloir supprimer ce client ?",
            "last_name_required": "Le nom de famille et le prénom sont requis !",
            "invalid_numbers": "Devis, Dinar et Dette doivent être des nombres valides !",
            "client_added": "Client ajouté avec succès !",
            "client_updated": "Client mis à jour avec succès !",
            "client_deleted": "Client supprimé avec succès !",
            "id": "ID",
            "devis": "Devis (€)",
            "dinar": "Dinar (DZD)",
            "debt": "Dette (€)",
            "cannot_delete_client_with_accounts": "Impossible de supprimer le client car il a des comptes ou transactions associés. Veuillez supprimer les comptes d'abord.",
            "confirm_delete_client_with_accounts": "Cela supprimera le client ET TOUS LEURS COMPTES ET TRANSACTIONS. Êtes-vous sûr ?",
            "client_and_accounts_deleted": "Client et tous les comptes supprimés avec succès !"
        }
        
        # Save translations to files
        with open("locales/en.json", "w", encoding="utf-8") as f:
            json.dump(en_translations, f, indent=2, ensure_ascii=False)
        
        with open("locales/fr.json", "w", encoding="utf-8") as f:
            json.dump(fr_translations, f, indent=2, ensure_ascii=False)
        
        self.translations["en"] = en_translations
        self.translations["fr"] = fr_translations
    
    def set_language(self, language: str):
        """Set the current language."""
        if language in ["en", "fr"]:
            self.language = language
        else:
            self.language = "en"  # Default to English
    
    def get_text(self, key: str, **kwargs) -> str:
        """Get translated text for the given key."""
        try:
            text = self.translations[self.language].get(key, key)
            # Replace placeholders if any
            for k, v in kwargs.items():
                text = text.replace(f"{{{k}}}", str(v))
            return text
        except KeyError:
            # Fallback to English if translation not found
            return self.translations.get("en", {}).get(key, key)
    
    def get_current_language(self) -> str:
        """Get the current language code."""
        return self.language

# Global i18n instance
i18n = I18nManager() 