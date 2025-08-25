#!/usr/bin/env python3
"""
Interface graphique pour OCR Assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import os
import sys
import json
import subprocess
import threading
from datetime import datetime
from pathlib import Path

# Ajouter le chemin parent pour les imports (gui est dans un sous-dossier)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Vérifier les dépendances au démarrage
from src.utils.dependency_checker import DependencyChecker


class OCRAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Assistant - Interface de Gestion")
        self.root.geometry("900x700")
        
        # Variables
        self.config_path = "src/config/config.json"
        self.hierarchical_config_path = "src/config/hierarchical_config.json"
        self.processing = False
        self.dependencies_ok = False
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Créer l'interface
        self.create_widgets()
        
        # Charger la configuration
        self.load_configuration()
        
        # Vérifier les dépendances
        self.check_dependencies()
        
        # Mettre à jour l'état initial
        self.update_status()
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        
        # Notebook pour les onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Onglet Principal
        self.create_main_tab()
        
        # Onglet Configuration
        self.create_config_tab()
        
        # Onglet Traitement
        self.create_processing_tab()
        
        # Onglet Révision
        self.create_review_tab()
        
        # Onglet Logs
        self.create_logs_tab()
        
        # Barre de statut
        self.status_bar = ttk.Label(self.root, text="Prêt", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_main_tab(self):
        """Onglet principal avec vue d'ensemble"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="🏠 Accueil")
        
        # Titre
        title_label = ttk.Label(main_frame, text="OCR Assistant", font=('Arial', 18, 'bold'))
        title_label.pack(pady=20)
        
        # Cadre d'informations
        info_frame = ttk.LabelFrame(main_frame, text="État du Système", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Informations système
        self.info_text = tk.Text(info_frame, height=10, width=60, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Boutons d'action rapide
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=20)
        
        ttk.Button(action_frame, text="🔧 Configuration Rapide", 
                  command=self.quick_config, width=20).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(action_frame, text="▶️ Lancer Traitement", 
                  command=self.quick_process, width=20).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(action_frame, text="📊 Voir Statistiques", 
                  command=self.show_stats, width=20).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(action_frame, text="🔄 Rafraîchir", 
                  command=self.update_status, width=20).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(action_frame, text="🔍 Vérifier Dépendances", 
                  command=self.check_dependencies_gui, width=20).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(action_frame, text="📦 Installer Dépendances", 
                  command=self.install_dependencies, width=20).grid(row=2, column=1, padx=5, pady=5)
    
    def create_config_tab(self):
        """Onglet de configuration"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuration")
        
        # Frame pour les dossiers
        folders_frame = ttk.LabelFrame(config_frame, text="Dossiers Configurés", padding=10)
        folders_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Liste des dossiers
        self.folders_listbox = tk.Listbox(folders_frame, height=10)
        self.folders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(folders_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.folders_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.folders_listbox.yview)
        
        # Boutons de gestion des dossiers
        folder_buttons = ttk.Frame(config_frame)
        folder_buttons.pack(pady=10)
        
        ttk.Button(folder_buttons, text="➕ Ajouter Dossier", 
                  command=self.add_folder).grid(row=0, column=0, padx=5)
        ttk.Button(folder_buttons, text="➖ Supprimer", 
                  command=self.remove_folder).grid(row=0, column=1, padx=5)
        ttk.Button(folder_buttons, text="📁 Ouvrir Dossier Scan", 
                  command=self.open_scan_folder).grid(row=0, column=2, padx=5)
        
        # Configuration globale
        global_frame = ttk.LabelFrame(config_frame, text="Configuration Globale", padding=10)
        global_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(global_frame, text="🌍 Configurer Global", 
                  command=self.configure_global, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(global_frame, text="📂 Config par Dossier", 
                  command=self.configure_folder, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(global_frame, text="🔄 Config Complète", 
                  command=self.run_full_config, width=25).pack(side=tk.LEFT, padx=5)
    
    def create_processing_tab(self):
        """Onglet de traitement"""
        process_frame = ttk.Frame(self.notebook)
        self.notebook.add(process_frame, text="▶️ Traitement")
        
        # Frame de contrôle
        control_frame = ttk.LabelFrame(process_frame, text="Contrôles", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Sélection du dossier à traiter
        ttk.Label(control_frame, text="Dossier à traiter:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.process_folder_var = tk.StringVar()
        self.process_folder_combo = ttk.Combobox(control_frame, textvariable=self.process_folder_var, width=30)
        self.process_folder_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Boutons de traitement
        ttk.Button(control_frame, text="▶️ Traiter", command=self.start_processing, 
                  width=15).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(control_frame, text="⏹️ Arrêter", command=self.stop_processing, 
                  width=15).grid(row=0, column=3, padx=5, pady=5)
        
        # Statistiques en temps réel
        stats_frame = ttk.LabelFrame(process_frame, text="Statistiques", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_labels = {}
        stats = ["PDFs trouvés", "En cours", "Traités", "Erreurs"]
        for i, stat in enumerate(stats):
            ttk.Label(stats_frame, text=f"{stat}:").grid(row=0, column=i*2, sticky=tk.W, padx=5)
            self.stats_labels[stat] = ttk.Label(stats_frame, text="0")
            self.stats_labels[stat].grid(row=0, column=i*2+1, sticky=tk.W, padx=5)
        
        # Console de sortie
        console_frame = ttk.LabelFrame(process_frame, text="Console", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.console_text = scrolledtext.ScrolledText(console_frame, height=15, width=80, 
                                                      bg='black', fg='green', 
                                                      font=('Consolas', 9))
        self.console_text.pack(fill=tk.BOTH, expand=True)
    
    def create_review_tab(self):
        """Onglet de révision"""
        review_frame = ttk.Frame(self.notebook)
        self.notebook.add(review_frame, text="✅ Révision")
        
        # Frame de contrôle
        control_frame = ttk.LabelFrame(review_frame, text="Révision des Résultats", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="📋 Charger Derniers Résultats", 
                  command=self.load_results, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="✅ Valider", 
                  command=self.validate_result, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="❌ Corriger", 
                  command=self.correct_result, width=15).pack(side=tk.LEFT, padx=5)
        
        # Affichage du résultat actuel
        result_frame = ttk.LabelFrame(review_frame, text="Résultat Actuel", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Labels pour les informations
        self.result_labels = {}
        fields = ["Fichier Original", "Nom Généré", "Date Extraite", "Fournisseur", "Numéro"]
        for i, field in enumerate(fields):
            ttk.Label(result_frame, text=f"{field}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=3)
            self.result_labels[field] = ttk.Label(result_frame, text="", font=('Arial', 10, 'bold'))
            self.result_labels[field].grid(row=i, column=1, sticky=tk.W, padx=5, pady=3)
        
        # Aperçu du texte OCR
        preview_frame = ttk.LabelFrame(review_frame, text="Aperçu OCR", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=8, width=80, wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
    
    def create_logs_tab(self):
        """Onglet des logs"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📊 Logs")
        
        # Contrôles
        control_frame = ttk.Frame(logs_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="🔄 Rafraîchir", 
                  command=self.refresh_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🗑️ Effacer", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="💾 Sauvegarder", 
                  command=self.save_logs).pack(side=tk.LEFT, padx=5)
        
        # Zone de texte pour les logs
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=20, width=100, wrap=tk.WORD)
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # --- Méthodes fonctionnelles ---
    
    def load_configuration(self):
        """Charge la configuration actuelle"""
        try:
            # Charger config.json
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    
                # Mettre à jour la liste des dossiers
                self.folders_listbox.delete(0, tk.END)
                for folder in self.config.get('sub_folders', []):
                    self.folders_listbox.insert(tk.END, folder)
                
                # Mettre à jour le combo de traitement
                self.process_folder_combo['values'] = ['Tous'] + self.config.get('sub_folders', [])
                if self.process_folder_combo['values']:
                    self.process_folder_combo.current(0)
            else:
                self.config = {'sub_folders': []}
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement de la configuration: {e}")
    
    def update_status(self):
        """Met à jour l'état du système"""
        self.info_text.delete(1.0, tk.END)
        
        info = []
        info.append("📊 ÉTAT DU SYSTÈME\n")
        info.append("="*50 + "\n\n")
        
        # Dossiers configurés
        folders = self.config.get('sub_folders', [])
        info.append(f"📁 Dossiers configurés: {len(folders)}\n")
        if folders:
            info.append(f"   {', '.join(folders[:5])}\n")
        
        # PDFs en attente
        total_pdfs = 0
        for folder in folders:
            scan_path = f"scan/{folder}"
            if os.path.exists(scan_path):
                pdfs = [f for f in os.listdir(scan_path) if f.lower().endswith('.pdf')]
                total_pdfs += len(pdfs)
        info.append(f"\n📄 PDFs en attente: {total_pdfs}\n")
        
        # Configuration hiérarchique
        if os.path.exists(self.hierarchical_config_path):
            info.append(f"\n✅ Configuration hiérarchique: Active\n")
        else:
            info.append(f"\n⚠️ Configuration hiérarchique: Non configurée\n")
        
        # Tesseract
        tesseract_ok = self.check_tesseract()
        if tesseract_ok:
            info.append(f"✅ Tesseract OCR: Installé\n")
        else:
            info.append(f"❌ Tesseract OCR: Non trouvé\n")
        
        self.info_text.insert(tk.END, ''.join(info))
        self.status_bar.config(text=f"Mise à jour: {datetime.now().strftime('%H:%M:%S')}")
    
    def check_tesseract(self):
        """Vérifie si Tesseract est installé"""
        paths = [
            r'C:\Tools\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        ]
        for path in paths:
            if os.path.exists(path):
                return True
        return False
    
    def quick_config(self):
        """Lance la configuration rapide"""
        self.run_script("python scripts/configure_hierarchical.py")
    
    def quick_process(self):
        """Lance le traitement rapide"""
        self.notebook.select(2)  # Aller à l'onglet traitement
        self.start_processing()
    
    def show_stats(self):
        """Affiche les statistiques"""
        try:
            from src.utils.learning_system import LearningSystem
            learning = LearningSystem()
            report = learning.generate_improvement_report()
            
            # Créer une fenêtre popup
            stats_window = tk.Toplevel(self.root)
            stats_window.title("Statistiques d'Apprentissage")
            stats_window.geometry("600x400")
            
            text_widget = scrolledtext.ScrolledText(stats_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert(tk.END, report)
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les statistiques: {e}")
    
    def add_folder(self):
        """Ajoute un nouveau dossier"""
        folder_name = simpledialog.askstring("Nouveau Dossier", 
                                                "Nom du nouveau dossier:")
        if folder_name:
            # Nettoyer le nom
            folder_clean = folder_name.replace(" ", "").replace("/", "").replace("\\", "")
            
            # Créer les dossiers
            os.makedirs(f"scan/{folder_clean}", exist_ok=True)
            os.makedirs(f"output/{folder_clean}", exist_ok=True)
            
            # Mettre à jour la config
            if 'sub_folders' not in self.config:
                self.config['sub_folders'] = []
            if folder_clean not in self.config['sub_folders']:
                self.config['sub_folders'].append(folder_clean)
                
                # Sauvegarder
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                
                # Recharger
                self.load_configuration()
                messagebox.showinfo("Succès", f"Dossier '{folder_clean}' créé!")
    
    def remove_folder(self):
        """Supprime un dossier sélectionné"""
        selection = self.folders_listbox.curselection()
        if selection:
            folder = self.folders_listbox.get(selection[0])
            if messagebox.askyesno("Confirmation", f"Supprimer le dossier '{folder}'?"):
                self.config['sub_folders'].remove(folder)
                
                # Sauvegarder
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                
                # Recharger
                self.load_configuration()
    
    def open_scan_folder(self):
        """Ouvre le dossier scan sélectionné"""
        selection = self.folders_listbox.curselection()
        if selection:
            folder = self.folders_listbox.get(selection[0])
            path = f"scan/{folder}"
            if os.path.exists(path):
                if sys.platform == "win32":
                    os.startfile(path)
                elif sys.platform == "darwin":
                    subprocess.call(["open", path])
                else:
                    subprocess.call(["xdg-open", path])
    
    def configure_global(self):
        """Configure les paramètres globaux"""
        # Créer une fenêtre de configuration
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuration Globale")
        config_window.geometry("600x500")
        
        # Charger la config hiérarchique
        hierarchical_config = {}
        if os.path.exists(self.hierarchical_config_path):
            with open(self.hierarchical_config_path, 'r', encoding='utf-8') as f:
                hierarchical_config = json.load(f)
        
        global_config = hierarchical_config.get('global', {})
        
        # Frame principal
        main_frame = ttk.Frame(config_window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Infos utilisateur
        info_frame = ttk.LabelFrame(main_frame, text="Informations Utilisateur", padding=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text="Nom:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        name_entry = ttk.Entry(info_frame, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, global_config.get('user_info', {}).get('name', ''))
        
        ttk.Label(info_frame, text="Entreprise:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        company_entry = ttk.Entry(info_frame, width=30)
        company_entry.grid(row=1, column=1, padx=5, pady=5)
        company_entry.insert(0, global_config.get('user_info', {}).get('company', ''))
        
        # Mots à ignorer
        ignore_frame = ttk.LabelFrame(main_frame, text="Mots à Ignorer (un par ligne)", padding=10)
        ignore_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ignore_text = tk.Text(ignore_frame, height=10, width=50)
        ignore_text.pack(fill=tk.BOTH, expand=True)
        ignore_words = global_config.get('ignore_words', [])
        ignore_text.insert(tk.END, '\n'.join(ignore_words))
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        def save_global_config():
            # Construire la nouvelle config
            new_global = {
                'user_info': {
                    'name': name_entry.get(),
                    'company': company_entry.get()
                },
                'ignore_words': [w.strip() for w in ignore_text.get(1.0, tk.END).strip().split('\n') if w.strip()]
            }
            
            # Mettre à jour la config hiérarchique
            hierarchical_config['global'] = new_global
            
            # Sauvegarder
            os.makedirs(os.path.dirname(self.hierarchical_config_path), exist_ok=True)
            with open(self.hierarchical_config_path, 'w', encoding='utf-8') as f:
                json.dump(hierarchical_config, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Succès", "Configuration globale sauvegardée!")
            config_window.destroy()
        
        ttk.Button(button_frame, text="💾 Sauvegarder", command=save_global_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Annuler", command=config_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def configure_folder(self):
        """Configure un dossier spécifique"""
        selection = self.folders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier")
            return
            
        folder = self.folders_listbox.get(selection[0])
        
        # Créer une fenêtre de configuration
        config_window = tk.Toplevel(self.root)
        config_window.title(f"Configuration: {folder}")
        config_window.geometry("600x500")
        
        # Charger la config hiérarchique
        hierarchical_config = {}
        if os.path.exists(self.hierarchical_config_path):
            with open(self.hierarchical_config_path, 'r', encoding='utf-8') as f:
                hierarchical_config = json.load(f)
        
        folder_config = hierarchical_config.get('folders', {}).get(folder, {})
        
        # Frame principal
        main_frame = ttk.Frame(config_window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mots à ajouter
        add_frame = ttk.LabelFrame(main_frame, text="Mots à Ajouter (+) - un par ligne", padding=10)
        add_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        add_text = tk.Text(add_frame, height=8, width=50)
        add_text.pack(fill=tk.BOTH, expand=True)
        add_words = folder_config.get('add', [])
        add_text.insert(tk.END, '\n'.join(add_words))
        
        # Mots à retirer
        remove_frame = ttk.LabelFrame(main_frame, text="Mots à Retirer (-) - un par ligne", padding=10)
        remove_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        remove_text = tk.Text(remove_frame, height=8, width=50)
        remove_text.pack(fill=tk.BOTH, expand=True)
        remove_words = folder_config.get('remove', [])
        remove_text.insert(tk.END, '\n'.join(remove_words))
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        def save_folder_config():
            # Construire la nouvelle config
            new_folder_config = {
                'add': [w.strip() for w in add_text.get(1.0, tk.END).strip().split('\n') if w.strip()],
                'remove': [w.strip() for w in remove_text.get(1.0, tk.END).strip().split('\n') if w.strip()]
            }
            
            # Mettre à jour la config hiérarchique
            if 'folders' not in hierarchical_config:
                hierarchical_config['folders'] = {}
            hierarchical_config['folders'][folder] = new_folder_config
            
            # Sauvegarder
            with open(self.hierarchical_config_path, 'w', encoding='utf-8') as f:
                json.dump(hierarchical_config, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Succès", f"Configuration du dossier '{folder}' sauvegardée!")
            config_window.destroy()
        
        ttk.Button(button_frame, text="💾 Sauvegarder", command=save_folder_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Annuler", command=config_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def run_full_config(self):
        """Lance la configuration complète"""
        self.run_script("python scripts/configure_hierarchical.py")
    
    def start_processing(self):
        """Démarre le traitement"""
        if not self.processing:
            self.processing = True
            self.console_text.delete(1.0, tk.END)
            
            # Lancer dans un thread séparé
            thread = threading.Thread(target=self.process_pdfs)
            thread.start()
    
    def stop_processing(self):
        """Arrête le traitement"""
        self.processing = False
        self.console_text.insert(tk.END, "\n⏹️ Traitement arrêté\n")
    
    def process_pdfs(self):
        """Traite les PDFs"""
        try:
            # Simuler le traitement
            self.console_text.insert(tk.END, "▶️ Démarrage du traitement...\n")
            
            # Lancer le script réel
            process = subprocess.Popen(
                ["python", "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            for line in process.stdout:
                if not self.processing:
                    process.terminate()
                    break
                self.console_text.insert(tk.END, line)
                self.console_text.see(tk.END)
                self.root.update()
            
            self.console_text.insert(tk.END, "\n✅ Traitement terminé\n")
            
        except Exception as e:
            self.console_text.insert(tk.END, f"\n❌ Erreur: {e}\n")
        finally:
            self.processing = False
    
    def load_results(self):
        """Charge les derniers résultats pour révision"""
        messagebox.showinfo("Info", "Chargement des derniers résultats...")
    
    def validate_result(self):
        """Valide le résultat actuel"""
        messagebox.showinfo("Info", "Résultat validé et enregistré pour apprentissage")
    
    def correct_result(self):
        """Corrige le résultat actuel"""
        messagebox.showinfo("Info", "Interface de correction...")
    
    def refresh_logs(self):
        """Rafraîchit les logs"""
        self.logs_text.delete(1.0, tk.END)
        
        # Chercher le dernier fichier de log
        log_dir = "logs"
        if os.path.exists(log_dir):
            log_files = sorted([f for f in os.listdir(log_dir) if f.endswith('.log')])
            if log_files:
                latest_log = os.path.join(log_dir, log_files[-1])
                try:
                    with open(latest_log, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.logs_text.insert(tk.END, content)
                except Exception as e:
                    self.logs_text.insert(tk.END, f"Erreur lecture log: {e}")
    
    def clear_logs(self):
        """Efface les logs affichés"""
        self.logs_text.delete(1.0, tk.END)
    
    def save_logs(self):
        """Sauvegarde les logs"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.logs_text.get(1.0, tk.END))
            messagebox.showinfo("Succès", f"Logs sauvegardés dans {filename}")
    
    def run_script(self, command):
        """Lance un script dans une nouvelle fenêtre"""
        if sys.platform == "win32":
            subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", command])
        else:
            # Pour Linux/Mac, lancer dans le terminal par défaut
            subprocess.Popen(command, shell=True)
    
    def check_dependencies(self):
        """Vérifie les dépendances au démarrage"""
        try:
            checker = DependencyChecker()
            installed, missing = checker.check_all_packages()
            
            if missing:
                self.dependencies_ok = False
                response = messagebox.askyesno(
                    "Dépendances Manquantes",
                    f"Des dépendances sont manquantes:\n{', '.join(missing)}\n\n"
                    "Voulez-vous les installer maintenant?"
                )
                if response:
                    self.install_dependencies()
            else:
                self.dependencies_ok = True
        except Exception as e:
            print(f"Erreur lors de la vérification des dépendances: {e}")
            self.dependencies_ok = False
    
    def check_dependencies_gui(self):
        """Vérifie les dépendances avec interface graphique"""
        # Créer une fenêtre de vérification
        check_window = tk.Toplevel(self.root)
        check_window.title("Vérification des Dépendances")
        check_window.geometry("600x400")
        
        # Zone de texte pour les résultats
        text_widget = scrolledtext.ScrolledText(check_window, wrap=tk.WORD, 
                                               font=('Consolas', 9))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bouton de fermeture
        ttk.Button(check_window, text="Fermer", 
                  command=check_window.destroy).pack(pady=10)
        
        # Lancer la vérification dans un thread
        def run_check():
            import sys
            from io import StringIO
            
            # Capturer la sortie
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                checker = DependencyChecker()
                result = checker.full_check()
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            # Afficher le résultat
            text_widget.insert(tk.END, output)
            
            if result:
                text_widget.insert(tk.END, "\n✅ Tout est prêt!")
                self.dependencies_ok = True
            else:
                text_widget.insert(tk.END, "\n⚠️ Des composants sont manquants")
                self.dependencies_ok = False
        
        thread = threading.Thread(target=run_check)
        thread.start()
    
    def install_dependencies(self):
        """Installe les dépendances manquantes"""
        # Créer une fenêtre d'installation
        install_window = tk.Toplevel(self.root)
        install_window.title("Installation des Dépendances")
        install_window.geometry("600x400")
        
        # Zone de texte pour les résultats
        text_widget = scrolledtext.ScrolledText(install_window, wrap=tk.WORD,
                                               bg='black', fg='green',
                                               font=('Consolas', 9))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Boutons
        button_frame = ttk.Frame(install_window)
        button_frame.pack(pady=10)
        
        close_btn = ttk.Button(button_frame, text="Fermer", 
                              command=install_window.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)
        
        # Lancer l'installation dans un thread
        def run_install():
            text_widget.insert(tk.END, "🚀 Démarrage de l'installation...\n\n")
            
            checker = DependencyChecker()
            installed, missing = checker.check_all_packages()
            
            if not missing:
                text_widget.insert(tk.END, "✅ Toutes les dépendances sont déjà installées!\n")
                self.dependencies_ok = True
                return
            
            text_widget.insert(tk.END, f"📦 Packages à installer: {', '.join(missing)}\n\n")
            
            for package in missing:
                text_widget.insert(tk.END, f"Installation de {package}...\n")
                text_widget.see(tk.END)
                install_window.update()
                
                if checker.install_package(package):
                    text_widget.insert(tk.END, f"✅ {package} installé\n")
                else:
                    text_widget.insert(tk.END, f"❌ Échec pour {package}\n")
                
                text_widget.insert(tk.END, "\n")
            
            # Vérifier à nouveau
            installed, still_missing = checker.check_all_packages()
            
            if not still_missing:
                text_widget.insert(tk.END, "\n✅ Installation terminée avec succès!\n")
                self.dependencies_ok = True
                messagebox.showinfo("Succès", "Toutes les dépendances ont été installées!")
            else:
                text_widget.insert(tk.END, f"\n⚠️ Packages non installés: {', '.join(still_missing)}\n")
                text_widget.insert(tk.END, "\nVeuillez les installer manuellement:\n")
                text_widget.insert(tk.END, f"pip install {' '.join(still_missing)}\n")
                self.dependencies_ok = False
        
        thread = threading.Thread(target=run_install)
        thread.start()


def main():
    """Point d'entrée principal"""
    root = tk.Tk()
    app = OCRAssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()