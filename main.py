import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import asyncio
import threading
from typing import Optional, Tuple
import traceback

# Import our new modules
from logging_config import banking_logger
from exceptions import BankingAppError, DatabaseError, ValidationError, ClientNotFoundError
from i18n import i18n
from config import config
from async_database import async_db

logger = banking_logger.get_logger("Main")

class SQLPreviewWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title(i18n.get_text("sql_preview"))
        self.window.geometry("600x400")
        self.window.resizable(True, True)
        
        # Make window stay on top
        self.window.attributes('-topmost', True)
        
        # Prevent window from being destroyed when parent is closed
        self.window.protocol("WM_DELETE_WINDOW", self.hide)
        
        # SQL Text Area
        self.sql_text = tk.Text(self.window, font=("Courier", 10), wrap=tk.WORD, bg="black", fg="white")
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.sql_text.yview)
        self.sql_text.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        ttk.Label(self.window, text=i18n.get_text("generated_sql"), font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        self.sql_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Add a close button
        close_button = ttk.Button(self.window, text="Close", command=self.hide)
        close_button.pack(pady=5)
        
        self.window.withdraw()  # Hide initially
        
    def update_sql(self, sql_command):
        try:
            # Check if window and text widget still exist
            if hasattr(self, 'window') and self.window.winfo_exists():
                self.sql_text.delete(1.0, tk.END)
                self.sql_text.insert(1.0, sql_command)
                self.window.deiconify()  # Show window
                self.window.lift()  # Bring to front
                self.window.focus_force()  # Give focus
                logger.debug(f"SQL preview updated: {sql_command[:100]}...")
        except tk.TclError as e:
            # Window might be destroyed, recreate it
            logger.warning(f"SQL preview window error, recreating: {e}")
            try:
                self.__init__(self.window.master)
                self.update_sql(sql_command)
            except:
                pass
        
    def hide(self):
        """Hide the SQL preview window."""
        try:
            self.window.withdraw()
        except tk.TclError:
            pass
        
    def toggle(self):
        try:
            if self.window.state() == 'withdrawn':
                self.window.deiconify()
                self.window.lift()
            else:
                self.window.withdraw()
        except tk.TclError:
            # Window might be destroyed, ignore the error
            pass

class ClientDialog:
    def __init__(self, parent, client_id=None):
        self.dialog = tk.Toplevel(parent)
        self.client_id = client_id
        self.dialog.title(i18n.get_text("add_client") if client_id is None else i18n.get_text("edit_client"))
        self.dialog.geometry("450x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Store data before dialog is destroyed
        self.result_data = None
        self.result = False
        
        self.setup_ui()
        if client_id:
            self.load_client_data()
            
    def setup_ui(self):
        # Form fields
        ttk.Label(self.dialog, text=i18n.get_text("last_name")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.nom_input = ttk.Entry(self.dialog, width=30)
        self.nom_input.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text=i18n.get_text("first_name")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.prenom_input = ttk.Entry(self.dialog, width=30)
        self.prenom_input.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text=i18n.get_text("email")).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.email_input = ttk.Entry(self.dialog, width=30)
        self.email_input.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text=i18n.get_text("phone")).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.telephone_input = ttk.Entry(self.dialog, width=30)
        self.telephone_input.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text=i18n.get_text("address")).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.adresse_input = ttk.Entry(self.dialog, width=30)
        self.adresse_input.grid(row=4, column=1, padx=5, pady=5)
        
        # Financial fields
        ttk.Label(self.dialog, text=i18n.get_text("devis_eur")).grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.devis_input = ttk.Entry(self.dialog, width=30)
        self.devis_input.insert(0, "0.0")
        self.devis_input.grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text=i18n.get_text("dinar_dzd")).grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.dinar_input = ttk.Entry(self.dialog, width=30)
        self.dinar_input.insert(0, "0.0")
        self.dinar_input.grid(row=6, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text=i18n.get_text("debt_eur")).grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.dette_input = ttk.Entry(self.dialog, width=30)
        self.dette_input.insert(0, "0.0")
        self.dette_input.grid(row=7, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text=i18n.get_text("ok"), command=self.accept).pack(side="left", padx=5)
        ttk.Button(button_frame, text=i18n.get_text("cancel"), command=self.reject).pack(side="left", padx=5)
        
    def load_client_data(self):
        """Synchronous wrapper for loading client data."""
        if self.client_id:
            # Use threading to avoid asyncio.run() in event loop
            def load_async():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    client = loop.run_until_complete(async_db.get_client_by_id(self.client_id))
                    
                    # Update UI in main thread
                    self.dialog.after(0, self.populate_fields, client)
                    
                except Exception as e:
                    logger.error(f"Error loading client data: {e}")
                    self.dialog.after(0, lambda: messagebox.showerror(i18n.get_text("error"), str(e)))
            
            thread = threading.Thread(target=load_async, daemon=True)
            thread.start()
    
    def populate_fields(self, client):
        """Populate the form fields with client data."""
        if client:
            self.nom_input.insert(0, client[1])
            self.prenom_input.insert(0, client[2])
            self.email_input.insert(0, client[3] or "")
            self.telephone_input.insert(0, client[4] or "")
            self.adresse_input.insert(0, client[5] or "")
            
            # Handle both old and new database structures
            if len(client) >= 9:  # New structure with devis, dinar, dette
                self.devis_input.delete(0, tk.END)
                self.devis_input.insert(0, str(client[6] or 0.0))
                self.dinar_input.delete(0, tk.END)
                self.dinar_input.insert(0, str(client[7] or 0.0))
                self.dette_input.delete(0, tk.END)
                self.dette_input.insert(0, str(client[8] or 0.0))
            elif len(client) >= 7:  # Old structure with solde, dette
                self.devis_input.delete(0, tk.END)
                self.devis_input.insert(0, str(client[6] or 0.0))  # solde becomes devis
                self.dinar_input.delete(0, tk.END)
                self.dinar_input.insert(0, "0.0")  # Default dinar value
                self.dette_input.delete(0, tk.END)
                self.dette_input.insert(0, str(client[7] or 0.0))  # dette
            else:  # Very old structure without financial fields
                self.devis_input.delete(0, tk.END)
                self.devis_input.insert(0, "0.0")
                self.dinar_input.delete(0, tk.END)
                self.dinar_input.insert(0, "0.0")
                self.dette_input.delete(0, tk.END)
                self.dette_input.insert(0, "0.0")
                
            logger.info(f"Client data loaded for ID: {self.client_id}")
    
    async def _load_client_data_async(self):
        """Async method to load client data."""
        await self.load_client_data()
            
    def get_data(self):
        return self.result_data
        
    def accept(self):
        # Validate input
        try:
            devis = float(self.devis_input.get() or 0.0)
            dinar = float(self.dinar_input.get() or 0.0)
            dette = float(self.dette_input.get() or 0.0)
        except ValueError:
            messagebox.showerror(i18n.get_text("error"), i18n.get_text("invalid_numbers"))
            return
            
        self.result_data = (
            self.nom_input.get() or "",  # Allow empty strings
            self.prenom_input.get() or "",
            self.email_input.get() or "",
            self.telephone_input.get() or "",
            self.adresse_input.get() or "",
            devis,
            dinar,
            dette
        )
        self.result = True
        self.dialog.destroy()
        
    def reject(self):
        self.result = False
        self.dialog.destroy()

class BankingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(i18n.get_text("app_title"))
        self.root.geometry(config.get_window_size())
        
        # Initialize async database
        self.db_initialized = False
        self.sql_preview = SQLPreviewWindow(self.root)
        
        # Initialize language
        i18n.set_language(config.get_language())
        
        self.setup_ui()
        
        # Initialize database in background
        self.initialize_database()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Language selector
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(pady=5)
        
        ttk.Label(lang_frame, text="Language:").pack(side="left")
        lang_var = tk.StringVar(value=i18n.get_current_language())
        lang_combo = ttk.Combobox(lang_frame, textvariable=lang_var, values=["en", "fr"], state="readonly", width=10)
        lang_combo.pack(side="left", padx=5)
        lang_combo.bind("<<ComboboxSelected>>", lambda e: self.change_language(lang_var.get()))
        
        # Connection button
        self.connect_button = ttk.Button(main_frame, text=i18n.get_text("connect_database"), 
                                       command=self.connect_database)
        self.connect_button.pack(pady=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=10)
        
        # Client management tab
        self.client_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.client_frame, text=i18n.get_text("client_management"))
        self.setup_client_tab()
        
        # SQL Preview toggle button
        self.sql_toggle_button = ttk.Button(main_frame, text=i18n.get_text("show_sql_preview"), 
                                          command=self.toggle_sql_preview)
        self.sql_toggle_button.pack(pady=10)
        
    def setup_client_tab(self):
        # Search frame
        search_frame = ttk.LabelFrame(self.client_frame, text=i18n.get_text("search_client"))
        search_frame.pack(fill="x", padx=5, pady=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search_clients)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.pack(padx=5, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self.client_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text=i18n.get_text("add_client"), command=self.add_client).pack(side="left", padx=5)
        ttk.Button(button_frame, text=i18n.get_text("edit_client"), command=self.edit_client).pack(side="left", padx=5)
        ttk.Button(button_frame, text=i18n.get_text("delete_client"), command=self.delete_client).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Account", command=self.delete_client_with_accounts).pack(side="left", padx=5)
        ttk.Button(button_frame, text=i18n.get_text("refresh"), command=self.load_clients).pack(side="left", padx=5)
        
        # Treeview for clients
        self.client_tree = ttk.Treeview(self.client_frame, 
                                       columns=("ID", "Last Name", "First Name", "Email", "Phone", "Address", "Devis (€)", "Dinar (DZD)", "Debt (€)"), 
                                       show="headings", height=15)
        
        # Configure columns
        self.client_tree.heading("ID", text=i18n.get_text("id"))
        self.client_tree.heading("Last Name", text=i18n.get_text("last_name"))
        self.client_tree.heading("First Name", text=i18n.get_text("first_name"))
        self.client_tree.heading("Email", text=i18n.get_text("email"))
        self.client_tree.heading("Phone", text=i18n.get_text("phone"))
        self.client_tree.heading("Address", text=i18n.get_text("address"))
        self.client_tree.heading("Devis (€)", text=i18n.get_text("devis"))
        self.client_tree.heading("Dinar (DZD)", text=i18n.get_text("dinar"))
        self.client_tree.heading("Debt (€)", text=i18n.get_text("debt"))
        
        self.client_tree.column("ID", width=50)
        self.client_tree.column("Last Name", width=100)
        self.client_tree.column("First Name", width=100)
        self.client_tree.column("Email", width=150)
        self.client_tree.column("Phone", width=100)
        self.client_tree.column("Address", width=150)
        self.client_tree.column("Devis (€)", width=80)
        self.client_tree.column("Dinar (DZD)", width=100)
        self.client_tree.column("Debt (€)", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.client_frame, orient="vertical", command=self.client_tree.yview)
        self.client_tree.configure(yscrollcommand=scrollbar.set)
        
        self.client_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
    def initialize_database(self):
        """Initialize database in background thread."""
        def init_db():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(async_db.initialize())
                self.db_initialized = True
                logger.info("Database initialized successfully")
            except Exception as e:
                logger.error(f"Database initialization failed: {e}")
        
        thread = threading.Thread(target=init_db, daemon=True)
        thread.start()
        
    def change_language(self, language):
        """Change application language."""
        i18n.set_language(language)
        config.update_language(language)
        logger.info(f"Language changed to: {language}")
        
        # Update UI text
        self.root.title(i18n.get_text("app_title"))
        self.connect_button.config(text=i18n.get_text("connect_database"))
        self.sql_toggle_button.config(text=i18n.get_text("show_sql_preview"))
        
        # Update tab text
        self.notebook.tab(0, text=i18n.get_text("client_management"))
        
        # Update treeview headers
        self.client_tree.heading("ID", text=i18n.get_text("id"))
        self.client_tree.heading("Last Name", text=i18n.get_text("last_name"))
        self.client_tree.heading("First Name", text=i18n.get_text("first_name"))
        self.client_tree.heading("Email", text=i18n.get_text("email"))
        self.client_tree.heading("Phone", text=i18n.get_text("phone"))
        self.client_tree.heading("Address", text=i18n.get_text("address"))
        self.client_tree.heading("Devis (€)", text=i18n.get_text("devis"))
        self.client_tree.heading("Dinar (DZD)", text=i18n.get_text("dinar"))
        self.client_tree.heading("Debt (€)", text=i18n.get_text("debt"))
        
    def connect_database(self):
        if self.db_initialized:
            messagebox.showinfo(i18n.get_text("success"), i18n.get_text("database_connection_successful"))
            self.connect_button.config(state="disabled")
            self.connect_button.config(text=i18n.get_text("connected"))
            self.load_clients()
        else:
            messagebox.showerror(i18n.get_text("error"), i18n.get_text("database_connection_failed"))
            
    def load_clients(self):
        """Load clients asynchronously."""
        if not self.db_initialized:
            return
            
        def load_async():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                clients = loop.run_until_complete(async_db.get_all_clients())
                
                # Update UI in main thread
                self.root.after(0, self.update_client_tree, clients)
                
                # Show SQL preview for manual refresh
                sql_command = "SELECT * FROM clients ORDER BY nom, prenom;"
                self.root.after(0, lambda: self.show_sql_preview(sql_command))
                
            except Exception as e:
                logger.error(f"Error loading clients: {e}")
                error_msg = str(e)
                self.root.after(0, lambda: messagebox.showerror(i18n.get_text("error"), error_msg))
        
        thread = threading.Thread(target=load_async, daemon=True)
        thread.start()
        
    def update_client_tree(self, clients):
        """Update the client treeview with new data."""
        # Clear existing items
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
            
        # Add new items
        for client in clients:
            self.client_tree.insert("", "end", values=client)
            
    def search_clients(self, *args):
        """Search clients asynchronously."""
        if not self.db_initialized:
            return
            
        search_term = self.search_var.get()
        
        def search_async():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                clients = loop.run_until_complete(async_db.search_clients(search_term))
                
                # Update UI in main thread
                self.root.after(0, self.update_client_tree, clients)
                
                # Show SQL command only for search operations (not for automatic refreshes)
                if search_term:
                    sql_command = f"SELECT * FROM clients WHERE nom LIKE '%{search_term}%' OR prenom LIKE '%{search_term}%' OR email LIKE '%{search_term}%' ORDER BY nom, prenom;"
                    self.root.after(0, lambda: self.show_sql_preview(sql_command))
                
            except Exception as e:
                logger.error(f"Error searching clients: {e}")
                error_msg = str(e)
                self.root.after(0, lambda: messagebox.showerror(i18n.get_text("error"), error_msg))
        
        thread = threading.Thread(target=search_async, daemon=True)
        thread.start()
        
    def add_client(self):
        if not self.db_initialized:
            messagebox.showerror(i18n.get_text("error"), i18n.get_text("please_connect_first"))
            return
            
        dialog = ClientDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            nom, prenom, email, telephone, adresse, devis, dinar, dette = dialog.get_data()
            
            # All fields are now optional - no validation required
            def add_async():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    client_id = loop.run_until_complete(async_db.add_client((nom, prenom, email, telephone, adresse, devis, dinar, dette)))
                    
                    sql_command = f"INSERT INTO clients (nom, prenom, email, telephone, adresse, devis, dinar, dette) VALUES ('{nom}', '{prenom}', '{email}', '{telephone}', '{adresse}', {devis}, {dinar}, {dette});"
                    self.root.after(0, lambda: self.show_sql_preview(sql_command))
                    self.root.after(0, lambda: messagebox.showinfo(i18n.get_text("success"), i18n.get_text("client_added")))
                    # No automatic refresh - user can manually refresh if needed
                    
                except Exception as e:
                    logger.error(f"Error adding client: {e}")
                    error_msg = str(e)
                    self.root.after(0, lambda: messagebox.showerror(i18n.get_text("error"), error_msg))
            
            thread = threading.Thread(target=add_async, daemon=True)
            thread.start()
            
    def edit_client(self):
        if not self.db_initialized:
            messagebox.showerror(i18n.get_text("error"), i18n.get_text("please_connect_first"))
            return
            
        selection = self.client_tree.selection()
        if not selection:
            messagebox.showwarning(i18n.get_text("warning"), i18n.get_text("select_client_to_edit"))
            return
            
        client_id = self.client_tree.item(selection[0])['values'][0]
        dialog = ClientDialog(self.root, client_id)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            nom, prenom, email, telephone, adresse, devis, dinar, dette = dialog.get_data()
            
            # All fields are now optional - no validation required
            def edit_async():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(async_db.update_client(client_id, (nom, prenom, email, telephone, adresse, devis, dinar, dette)))
                    
                    sql_command = f"UPDATE clients SET nom='{nom}', prenom='{prenom}', email='{email}', telephone='{telephone}', adresse='{adresse}', devis={devis}, dinar={dinar}, dette={dette} WHERE id={client_id};"
                    self.root.after(0, lambda: self.show_sql_preview(sql_command))
                    self.root.after(0, lambda: messagebox.showinfo(i18n.get_text("success"), i18n.get_text("client_updated")))
                    # No automatic refresh - user can manually refresh if needed
                    
                except Exception as e:
                    logger.error(f"Error editing client: {e}")
                    error_msg = str(e)
                    self.root.after(0, lambda: messagebox.showerror(i18n.get_text("error"), error_msg))
            
            thread = threading.Thread(target=edit_async, daemon=True)
            thread.start()
            
    def delete_client(self):
        if not self.db_initialized:
            messagebox.showerror(i18n.get_text("error"), i18n.get_text("please_connect_first"))
            return
            
        selection = self.client_tree.selection()
        if not selection:
            messagebox.showwarning(i18n.get_text("warning"), i18n.get_text("select_client_to_delete"))
            return
            
        client_id = self.client_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno(i18n.get_text("confirm"), i18n.get_text("confirm_delete_client")):
            def delete_async():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    # Check if client has accounts first
                    has_accounts = loop.run_until_complete(async_db.client_has_accounts(client_id))
                    if has_accounts:
                        accounts = loop.run_until_complete(async_db.get_client_accounts(client_id))
                        account_info = "\n".join([f"Account {acc[0]}: {acc[2]} (Balance: {acc[3]}€)" for acc in accounts])
                        error_msg = f"{i18n.get_text('cannot_delete_client_with_accounts')}\n\nClient has {len(accounts)} account(s):\n{account_info}"
                        
                        # Show SQL preview explaining why deletion failed
                        sql_command = f"""-- Cannot delete client {client_id} because they have accounts
-- Client has {len(accounts)} account(s):
-- {account_info.replace(chr(10), '\\n')}
-- Use 'Delete Account' button to delete client and all accounts"""
                        self.root.after(0, lambda: self.show_sql_preview(sql_command))
                        self.root.after(0, lambda: messagebox.showerror(i18n.get_text("error"), error_msg))
                        return
                    
                    loop.run_until_complete(async_db.delete_client(client_id))
                    
                    sql_command = f"DELETE FROM clients WHERE id={client_id};"
                    self.root.after(0, lambda: self.show_sql_preview(sql_command))
                    self.root.after(0, lambda: messagebox.showinfo(i18n.get_text("success"), i18n.get_text("client_deleted")))
                    # No automatic refresh - user can manually refresh if needed
                    
                except Exception as e:
                    logger.error(f"Error deleting client: {e}")
                    if "Cannot delete client because they have associated accounts" in str(e):
                        error_msg = i18n.get_text("cannot_delete_client_with_accounts")
                    else:
                        error_msg = str(e)
                    self.root.after(0, lambda: messagebox.showerror(i18n.get_text("error"), error_msg))
            
            thread = threading.Thread(target=delete_async, daemon=True)
            thread.start()
            
    def delete_client_with_accounts(self):
        """Delete a client and all their accounts."""
        if not self.db_initialized:
            messagebox.showerror(i18n.get_text("error"), i18n.get_text("please_connect_first"))
            return
            
        selection = self.client_tree.selection()
        if not selection:
            messagebox.showwarning(i18n.get_text("warning"), i18n.get_text("select_client_to_delete"))
            return
            
        client_id = self.client_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno(i18n.get_text("confirm"), i18n.get_text("confirm_delete_client_with_accounts")):
            def delete_async():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    # Delete accounts first
                    loop.run_until_complete(async_db.delete_client_accounts(client_id))
                    
                    # Then delete client
                    loop.run_until_complete(async_db.delete_client(client_id))
                    
                    # Show comprehensive SQL preview
                    sql_command = f"""-- Delete client accounts first
DELETE FROM comptes WHERE client_id={client_id};

-- Then delete the client
DELETE FROM clients WHERE id={client_id};"""
                    self.root.after(0, lambda: self.show_sql_preview(sql_command))
                    self.root.after(0, lambda: messagebox.showinfo(i18n.get_text("success"), i18n.get_text("client_and_accounts_deleted")))
                    # No automatic refresh - user can manually refresh if needed
                    
                except Exception as e:
                    logger.error(f"Error deleting client with accounts: {e}")
                    error_msg = str(e)
                    self.root.after(0, lambda: messagebox.showerror(i18n.get_text("error"), error_msg))
            
            thread = threading.Thread(target=delete_async, daemon=True)
            thread.start()
            
    def toggle_sql_preview(self):
        self.sql_preview.toggle()
        
    def show_sql_preview(self, sql_command):
        """Show SQL preview with the given command."""
        self.sql_preview.update_sql(sql_command)
        
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Application error: {e}")
            logger.error(traceback.format_exc())
        finally:
            # Cleanup
            try:
                asyncio.run(async_db.close())
            except:
                pass

def main():
    try:
        logger.info("Starting Banking Management System...")
        app = BankingApp()
        app.run()
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        logger.error(traceback.format_exc())
        messagebox.showerror("Fatal Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main() 