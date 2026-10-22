import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


class BinomialPricerApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Binomial Options Pricer Engine | Professional Edition")
    self.root.geometry("780x680")
    self.root.minsize(720, 600)

    self.style = ttk.Style()
    self.style.theme_use("clam")

    self.create_widgets()

  def create_widgets(self):
    # En-titre
    header_frame = tk.Frame(self.root, bg="#1E293B", padx=20, pady=15)
    header_frame.pack(fill=tk.X)

    title_label = tk.Label(
        header_frame,
        text="BINOMIAL OPTIONS PRICER ENGINE",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#1E293B",
    )
    title_label.pack(anchor="w")

    subtitle_label = tk.Label(
        header_frame,
        text="Modèle Cox-Ross-Rubinstein | Moteur C++ Back-end (-O3)",
        font=("Arial", 9),
        fg="#94A3B8",
        bg="#1E293B",
    )
    subtitle_label.pack(anchor="w")

    # Conteneur principal
    main_frame = ttk.Frame(self.root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Paramètres d'entrée
    params_frame = ttk.LabelFrame(
        main_frame, text=" Paramètres du Marché & de l'Option ", padding=15
    )
    params_frame.pack(fill=tk.X, pady=5)

    fields = [
        ("Prix Spot (S) :", "100.0"),
        ("Strike (K) :", "100.0"),
        ("Taux sans risque (r) :", "0.05"),
        ("Volatilité (sigma) :", "0.20"),
        ("Maturité en années (T) :", "1.0"),
        ("Nombre d'étapes (N) :", "500"),
    ]

    self.entries = {}
    for i, (label_text, default_val) in enumerate(fields):
      row = i // 2
      col = (i % 2) * 2

      lbl = ttk.Label(params_frame, text=label_text, font=("Arial", 10))
      lbl.grid(row=row, column=col, sticky="w", padx=5, pady=8)

      ent = ttk.Entry(params_frame, width=18, font=("Arial", 10))
      ent.insert(0, default_val)
      ent.grid(row=row, column=col + 1, sticky="ew", padx=5, pady=8)
      self.entries[label_text] = ent

    params_frame.columnconfigure(1, weight=1)
    params_frame.columnconfigure(3, weight=1)

    # Boutons d'action (Calcul + Quitter)
    action_frame = ttk.Frame(main_frame, padding=5)
    action_frame.pack(fill=tk.X, pady=10)

    self.calc_btn = tk.Button(
        action_frame,
        text="Lancer le Pricing C++",
        bg="#0F172A",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=15,
        pady=8,
        relief=tk.FLAT,
        command=self.run_pricing_thread,
    )
    self.calc_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

    quit_btn = tk.Button(
        action_frame,
        text="Quitter",
        bg="#64748B",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=15,
        pady=8,
        relief=tk.FLAT,
        command=self.root.destroy,
    )
    quit_btn.pack(side=tk.RIGHT, padx=(5, 0))

    # Zone de résultats
    result_frame = ttk.LabelFrame(
        main_frame, text=" Résultats du Pricing & Grecs ", padding=15
    )
    result_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    self.result_text = tk.Text(
        result_frame,
        height=9,
        bg="#F8FAFC",
        fg="#0F172A",
        font=("Consolas", 10),
        relief=tk.SOLID,
        borderwidth=1,
    )
    self.result_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    self.result_text.insert(
        tk.END, "En attente du lancement du calcul...\n"
    )
    self.result_text.config(state=tk.DISABLED)

    # Boutons d'export institutionnel
    export_frame = ttk.Frame(main_frame)
    export_frame.pack(fill=tk.X)

    self.export_excel_btn = ttk.Button(
        export_frame,
        text="Exporter en Excel",
        command=self.export_excel_action,
        state=tk.DISABLED,
    )
    self.export_excel_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

    self.export_pdf_btn = ttk.Button(
        export_frame,
        text="Exporter en PDF",
        command=self.export_pdf_action,
        state=tk.DISABLED,
    )
    self.export_pdf_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

  def run_pricing_thread(self):
    threading.Thread(target=self.execute_cpp_engine, daemon=True).start()

  def execute_cpp_engine(self):
    self.calc_btn.config(state=tk.DISABLED, text="Calcul en cours...")

    try:
      s = self.entries["Prix Spot (S) :"].get()
      k = self.entries["Strike (K) :"].get()
      r = self.entries["Taux sans risque (r) :"].get()
      sigma = self.entries["Volatilité (sigma) :"].get()
      t = self.entries["Maturité en années (T) :"].get()
      n = self.entries["Nombre d'étapes (N) :"].get()

      if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
      else:
        base_dir = os.path.dirname(__file__)

      exe_path = os.path.join(base_dir, "Binomial Engine.exe")
      if not os.path.exists(exe_path):
        exe_path = os.path.join(base_dir, "binomial_engine.exe")

      if not os.path.exists(exe_path):
        messagebox.showerror(
            "Erreur Critique",
            f"L'exécutable C++ est introuvable dans :\n{exe_path}",
        )
        return

      process = subprocess.run(
          [exe_path, s, k, r, sigma, t, n],
          capture_output=True,
          text=True,
          timeout=5,
      )

      output = process.stdout

      self.result_text.config(state=tk.NORMAL)
      self.result_text.delete("1.0", tk.END)
      self.result_text.insert(tk.END, output)
      self.result_text.config(state=tk.DISABLED)

      self.export_excel_btn.config(state=tk.NORMAL)
      self.export_pdf_btn.config(state=tk.NORMAL)

    except Exception as e:
      messagebox.showerror(
          "Erreur d'exécution", f"Erreur lors de l'appel du moteur :\n{str(e)}"
      )

    finally:
      self.calc_btn.config(state=tk.NORMAL, text="Lancer le Pricing C++")

  def export_excel_action(self):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Fichiers texte / Rapport", "*.txt"), ("Tous les fichiers", "*.*")],
        title="Enregistrer le rapport",
    )
    if file_path:
      with open(file_path, "w", encoding="utf-8") as f:
        f.write(self.result_text.get("1.0", tk.END))
      messagebox.showinfo("Succès", "Rapport exporté avec succès !")

  def export_pdf_action(self):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")],
        title="Exporter le rapport en PDF",
    )
    if file_path:
      try:
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Heading1"],
            fontSize=16,
            textColor=colors.HexColor("#1E293B"),
            spaceAfter=15,
        )
        story.append(
            Paragraph("<b>Binomial Options Pricer Engine - Rapport</b>", title_style)
        )
        story.append(Spacer(1, 10))

        results_content = self.result_text.get("1.0", tk.END).strip()
        for line in results_content.split("\n"):
          formatted_line = (
              line.replace(" ", "&nbsp;") if line.strip() else "<br/>"
          )
          p = Paragraph(
              f"<font name='Courier' size=10>{formatted_line}</font>",
              styles["Normal"],
          )
          story.append(p)

        doc.build(story)
        messagebox.showinfo(
            "Succès", "Le rapport PDF a été généré et enregistré avec succès !"
        )
      except Exception as e:
        messagebox.showerror(
            "Erreur", f"Erreur lors de la génération du PDF :\n{str(e)}"
        )


if __name__ == "__main__":
  root = tk.Tk()
  app = BinomialPricerApp(root)
  root.mainloop()