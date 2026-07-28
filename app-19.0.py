import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from regras_engenharia import calcular_mesa_parametrica

# Importando bibliotecas de Nesting e Gráficos
try:
    from rectpack import newPacker, PackingMode, PackingBin
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    HAS_NESTING = True
except ImportError:
    HAS_NESTING = False

# Configuração visual do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ProjetistaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🛒 Projetista Virtual ERP - Gestor de Pedidos AçoNobre")
        self.geometry("1350x900")
        self.minsize(1200, 800)
        
        # ==========================================
        # CONFIGURAÇÃO DA FÁBRICA (DIMENSÕES DA CHAPA)
        # ==========================================
        self.dim_chapa_x = 3000
        self.dim_chapa_y = 1250
        
        self.carrinho = [] # Lista que guarda todos os itens do pedido
        self.pecas_temp_composto = [] # Lista temporária para o Item Composto
        self.df_lista = None
        self.df_resumo = None
        self.pecas_para_nesting_global = [] 
        
        # ==========================================
        # MOTOR DE CUSTOS (Carrega preços do Excel)
        # ==========================================
        self.custo_chapa = {"INOX 304": {}, "INOX 430": {}}
        self.custo_tubo = {}
        self.carregar_tabela_precos()

        # ==========================================
        # ESTRUTURA DA TELA (DIVISÃO PRINCIPAL)
        # ==========================================
        self.frame_esq = ctk.CTkScrollableFrame(self, width=440, corner_radius=10)
        self.frame_esq.pack(side="left", fill="y", padx=10, pady=10)

        self.frame_dir = ctk.CTkFrame(self, corner_radius=10)
        self.frame_dir.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)

        # ==========================================
        # PAINEL ESQUERDO: DADOS DO PEDIDO
        # ==========================================
        ctk.CTkLabel(self.frame_esq, text="📦 DADOS DO PEDIDO", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        self.inp_pedido = ctk.CTkEntry(self.frame_esq, placeholder_text="Nº do Pedido (Ex: 6885)", height=35)
        self.inp_pedido.pack(fill="x", padx=15, pady=5)
        
        # ==========================================
        # ABAS DE INSERÇÃO (3 OPÇÕES INTELIGENTES)
        # ==========================================
        self.abas_add = ctk.CTkTabview(self.frame_esq)
        self.abas_add.pack(fill="x", padx=15, pady=10)
        
        self.tab_param = self.abas_add.add("📐 Catálogo Paramétrico")
        self.tab_comp = self.abas_add.add("🧩 Item Composto")
        self.tab_livre = self.abas_add.add("✏️ Peça Avulsa")

        # ---------------------------------------------------------
        # ABA 1: CATÁLOGO PARAMÉTRICO (PADRÃO + OVERRIDES)
        # ---------------------------------------------------------
        f_dim = ctk.CTkFrame(self.tab_param, fg_color="transparent")
        f_dim.pack(fill="x", pady=5)
        self.inp_qtd = ctk.CTkEntry(f_dim, placeholder_text="QTD", width=60, height=35)
        self.inp_qtd.pack(side="left", padx=(0, 5))
        self.inp_comp = ctk.CTkEntry(f_dim, placeholder_text="Comp(mm)", width=90, height=35)
        self.inp_comp.pack(side="left", padx=5)
        self.inp_larg = ctk.CTkEntry(f_dim, placeholder_text="Larg(mm)", width=90, height=35)
        self.inp_larg.pack(side="left", padx=5)
        self.inp_alt = ctk.CTkEntry(f_dim, placeholder_text="Alt(mm)", height=35)
        self.inp_alt.pack(side="left", fill="x", expand=True)

        self.inp_qtd.insert(0, "1")

        f_tipos = ctk.CTkFrame(self.tab_param, fg_color="transparent")
        f_tipos.pack(fill="x", pady=5)
        self.mapa_tampo = {"Mesa Lisa": "LISA", "Mesa com Encosto": "ENCOSTO", "Pia com Cuba": "PIA"}
        self.combo_tampo = ctk.CTkComboBox(f_tipos, values=list(self.mapa_tampo.keys()), height=35)
        self.combo_tampo.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.combo_tampo.set("Mesa Lisa")

        self.mapa_base = {"Contraventamento": "CONTRAVENTAMENTO", "Prat. Lisa": "PRAT_LISA", "Prat. Gradeada": "PRAT_GRADEADA"}
        self.combo_base = ctk.CTkComboBox(f_tipos, values=list(self.mapa_base.keys()), height=35)
        self.combo_base.pack(side="left", fill="x", expand=True)
        self.combo_base.set("Contraventamento")

        # Personalização (Padrão vs Modificado)
        ctk.CTkLabel(self.tab_param, text="Personalização de Material (Opcional)", font=ctk.CTkFont(size=12, weight="bold"), text_color="#f39c12").pack(pady=(10, 0))
        
        f_mat_tampo = ctk.CTkFrame(self.tab_param, fg_color="transparent")
        f_mat_tampo.pack(fill="x", pady=2)
        ctk.CTkLabel(f_mat_tampo, text="Tampo: ", width=50).pack(side="left")
        self.cbo_mat_tampo = ctk.CTkComboBox(f_mat_tampo, values=["INOX 304", "INOX 430"], width=120)
        self.cbo_mat_tampo.pack(side="left", padx=5)
        self.cbo_esp_tampo = ctk.CTkComboBox(f_mat_tampo, values=["Esp. Padrão", "0.8", "1.0", "1.2", "1.5", "2.0"])
        self.cbo_esp_tampo.pack(side="left", fill="x", expand=True)
        self.cbo_esp_tampo.set("Esp. Padrão")

        f_mat_base = ctk.CTkFrame(self.tab_param, fg_color="transparent")
        f_mat_base.pack(fill="x", pady=2)
        ctk.CTkLabel(f_mat_base, text="Base: ", width=50).pack(side="left")
        self.cbo_mat_base = ctk.CTkComboBox(f_mat_base, values=["INOX 304", "INOX 430"], width=120)
        self.cbo_mat_base.pack(side="left", padx=5)
        self.cbo_esp_base = ctk.CTkComboBox(f_mat_base, values=["Esp. Padrão", "0.8", "1.0", "1.2", "1.5", "2.0"])
        self.cbo_esp_base.pack(side="left", fill="x", expand=True)
        self.cbo_esp_base.set("Esp. Padrão")

        self.btn_add_param = ctk.CTkButton(self.tab_param, text="➕ Adicionar ao Pedido", height=35, command=self.adicionar_item_parametrico)
        self.btn_add_param.pack(fill="x", pady=(15, 5))

        # ---------------------------------------------------------
        # ABA 2: ITEM COMPOSTO (CONSTRUTOR DE PRODUTOS)
        # ---------------------------------------------------------
        f_comp_header = ctk.CTkFrame(self.tab_comp, fg_color="transparent")
        f_comp_header.pack(fill="x", pady=5)
        self.inp_qtd_item_comp = ctk.CTkEntry(f_comp_header, placeholder_text="QTD Item", width=70, height=35)
        self.inp_qtd_item_comp.pack(side="left", padx=(0, 5))
        self.inp_qtd_item_comp.insert(0, "1")
        self.inp_nome_item_comp = ctk.CTkEntry(f_comp_header, placeholder_text="Nome do Produto (Ex: Coifa Central)", height=35)
        self.inp_nome_item_comp.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(self.tab_comp, text="Adicionar Peças a este Produto:", font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(5, 0))
        
        f_comp_p1 = ctk.CTkFrame(self.tab_comp, fg_color="transparent")
        f_comp_p1.pack(fill="x", pady=2)
        self.inp_nome_pc_comp = ctk.CTkEntry(f_comp_p1, placeholder_text="Nome Peça", height=30)
        self.inp_nome_pc_comp.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.inp_qtd_pc_comp = ctk.CTkEntry(f_comp_p1, placeholder_text="Qtd", width=50, height=30)
        self.inp_qtd_pc_comp.pack(side="left")
        
        f_comp_p2 = ctk.CTkFrame(self.tab_comp, fg_color="transparent")
        f_comp_p2.pack(fill="x", pady=2)
        self.inp_comp_pc_comp = ctk.CTkEntry(f_comp_p2, placeholder_text="Comp(mm)", width=90, height=30)
        self.inp_comp_pc_comp.pack(side="left", padx=(0, 5))
        self.inp_larg_pc_comp = ctk.CTkEntry(f_comp_p2, placeholder_text="Larg(mm)", width=90, height=30)
        self.inp_larg_pc_comp.pack(side="left", padx=(0, 5))
        self.cbo_mat_pc_comp = ctk.CTkComboBox(f_comp_p2, values=["304", "430"], width=70, height=30)
        self.cbo_mat_pc_comp.pack(side="left", padx=(0, 5))
        self.cbo_esp_pc_comp = ctk.CTkComboBox(f_comp_p2, values=["0.6","0.8","1.0","1.2","1.5","2.0"], height=30)
        self.cbo_esp_pc_comp.pack(side="left", fill="x", expand=True)
        self.cbo_esp_pc_comp.set("1.0")

        self.btn_add_pc_comp = ctk.CTkButton(self.tab_comp, text="⏬ Inserir Peça", height=28, fg_color="#34495e", command=self.adicionar_peca_composto)
        self.btn_add_pc_comp.pack(fill="x", pady=5)

        # Mini Tabela do Construtor
        self.tree_temp = ttk.Treeview(self.tab_comp, columns=("QTD", "DESC", "MAT"), show="headings", height=3)
        self.tree_temp.heading("QTD", text="QTD")
        self.tree_temp.heading("DESC", text="PEÇA (Comp x Larg)")
        self.tree_temp.heading("MAT", text="LIGA/ESP")
        self.tree_temp.column("QTD", width=40, anchor="center")
        self.tree_temp.column("DESC", width=200)
        self.tree_temp.column("MAT", width=80, anchor="center")
        self.tree_temp.pack(fill="x", pady=2)

        self.btn_finalizar_comp = ctk.CTkButton(self.tab_comp, text="✅ EMPACOTAR ITEM E ADD AO PEDIDO", height=35, fg_color="#16a085", hover_color="#1abc9c", command=self.finalizar_item_composto)
        self.btn_finalizar_comp.pack(fill="x", pady=(10, 5))

        # ---------------------------------------------------------
        # ABA 3: PEÇA AVULSA (LIVRE)
        # ---------------------------------------------------------
        f_livre1 = ctk.CTkFrame(self.tab_livre, fg_color="transparent")
        f_livre1.pack(fill="x", pady=5)
        self.inp_qtd_livre = ctk.CTkEntry(f_livre1, placeholder_text="QTD", width=60, height=35)
        self.inp_qtd_livre.pack(side="left", padx=(0, 5))
        self.inp_nome_livre = ctk.CTkEntry(f_livre1, placeholder_text="Nome (Ex: Reforço Extra)", height=35)
        self.inp_nome_livre.pack(side="left", fill="x", expand=True)

        f_livre2 = ctk.CTkFrame(self.tab_livre, fg_color="transparent")
        f_livre2.pack(fill="x", pady=5)
        self.inp_comp_livre = ctk.CTkEntry(f_livre2, placeholder_text="Comp Planif. (mm)", width=130, height=35)
        self.inp_comp_livre.pack(side="left", padx=(0, 5))
        self.inp_larg_livre = ctk.CTkEntry(f_livre2, placeholder_text="Larg Planif. (mm)", height=35)
        self.inp_larg_livre.pack(side="left", fill="x", expand=True)

        f_livre3 = ctk.CTkFrame(self.tab_livre, fg_color="transparent")
        f_livre3.pack(fill="x", pady=5)
        self.combo_mat_livre = ctk.CTkComboBox(f_livre3, values=["INOX 304", "INOX 430"], width=130, height=35)
        self.combo_mat_livre.pack(side="left", padx=(0, 5))
        self.combo_esp_livre = ctk.CTkComboBox(f_livre3, values=["0.6", "0.8", "1.0", "1.2", "1.5", "2.0"], height=35)
        self.combo_esp_livre.pack(side="left", fill="x", expand=True)
        
        self.inp_qtd_livre.insert(0, "1")
        self.combo_esp_livre.set("1.0")

        self.btn_add_livre = ctk.CTkButton(self.tab_livre, text="➕ Adicionar Peça Solta", height=35, command=self.adicionar_item_livre)
        self.btn_add_livre.pack(fill="x", pady=(20, 5))


        # ==========================================
        # ÁREA DO CARRINHO (TABELA INTERATIVA)
        # ==========================================
        ctk.CTkLabel(self.frame_esq, text="🛒 ITENS NO CARRINHO", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        
        self.tree_carrinho = ttk.Treeview(self.frame_esq, columns=("ID", "QTD", "DESC"), show="headings", height=6)
        self.tree_carrinho.heading("ID", text="Nº")
        self.tree_carrinho.heading("QTD", text="QTD")
        self.tree_carrinho.heading("DESC", text="DESCRIÇÃO DA PEÇA", anchor="w")
        
        self.tree_carrinho.column("ID", width=40, minwidth=40, stretch=False, anchor="center")
        self.tree_carrinho.column("QTD", width=45, minwidth=45, stretch=False, anchor="center")
        self.tree_carrinho.column("DESC", width=300, minwidth=250, stretch=True, anchor="w")
        self.tree_carrinho.pack(fill="x", padx=15, pady=5)

        self.btn_remover = ctk.CTkButton(self.frame_esq, text="❌ Remover Item Selecionado", fg_color="#d35400", hover_color="#e67e22", height=32, command=self.remover_item_carrinho)
        self.btn_remover.pack(fill="x", padx=15, pady=5)

        self.btn_limpar = ctk.CTkButton(self.frame_esq, text="🗑️ Limpar Todo o Carrinho", fg_color="#c0392b", hover_color="#e74c3c", height=32, command=self.limpar_carrinho)
        self.btn_limpar.pack(fill="x", padx=15, pady=(5, 15))

        self.btn_gerar = ctk.CTkButton(self.frame_esq, text="🚀 CALCULAR PEDIDO", height=45, font=ctk.CTkFont(weight="bold"), fg_color="#2980b9", command=self.calcular_pedido_completo)
        self.btn_gerar.pack(fill="x", padx=15, pady=(15, 5))

        self.btn_mapa = ctk.CTkButton(self.frame_esq, text="👁️ Ver Mapa de Corte (Nesting)", height=35, fg_color="#8e44ad", hover_color="#9b59b6", state="disabled", command=self.abrir_mapa_corte)
        self.btn_mapa.pack(fill="x", padx=15, pady=5)

        self.btn_exportar = ctk.CTkButton(self.frame_esq, text="📥 EXPORTAR EXCEL", height=35, fg_color="#27ae60", hover_color="#2ecc71", state="disabled", command=self.exportar_excel)
        self.btn_exportar.pack(fill="x", padx=15, pady=(5, 20))

        # ==========================================
        # PAINEL DIREITO: ABAS (TABS) DE RESULTADOS
        # ==========================================
        self.abas_res = ctk.CTkTabview(self.frame_dir)
        self.abas_res.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.tab_lista = self.abas_res.add("✂️ Lista de Corte (PCP)")
        self.tab_resumo = self.abas_res.add("📊 Relatório de Materiais e Custos")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=30, fieldbackground="#2b2b2b", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#1f538d", foreground="white", relief="flat", font=('Arial', 10, 'bold'))

        colunas = ("ITEM", "QTD", "CÓDIGO", "DESCRIÇÃO", "ESP", "MEDIDA", "PESO UN", "PESO TOT")
        self.tabela = ttk.Treeview(self.tab_lista, columns=colunas, show="headings")
        self.tabela.heading("ITEM", text="ITEM")
        self.tabela.heading("QTD", text="QTD")
        self.tabela.heading("CÓDIGO", text="CÓDIGO")
        self.tabela.heading("DESCRIÇÃO", text="DESCRIÇÃO DA PEÇA")
        self.tabela.heading("ESP", text="ESP")
        self.tabela.heading("MEDIDA", text="CORTE (mm)")
        self.tabela.heading("PESO UN", text="PESO UN")
        self.tabela.heading("PESO TOT", text="PESO TOT")
        
        self.tabela.column("ITEM", width=70, anchor="center")
        self.tabela.column("QTD", width=50, anchor="center")
        self.tabela.column("CÓDIGO", width=130)
        self.tabela.column("DESCRIÇÃO", width=220)
        self.tabela.column("ESP", width=50, anchor="center")
        self.tabela.column("MEDIDA", width=150, anchor="center")
        self.tabela.column("PESO UN", width=80, anchor="center")
        self.tabela.column("PESO TOT", width=80, anchor="center")

        self.tabela.pack(fill="both", expand=True, padx=5, pady=5)

        self.caixa_resumo = ctk.CTkTextbox(self.tab_resumo, font=ctk.CTkFont(size=13, family="Consolas"))
        self.caixa_resumo.pack(fill="both", expand=True, padx=5, pady=5)
        self.caixa_resumo.insert("0.0", "Calcule o pedido para ver o relatório de materiais e a estimativa de custos.")
        self.caixa_resumo.configure(state="disabled")

    # ==========================================
    # LÓGICA DE PRECIFICAÇÃO
    # ==========================================
    def carregar_tabela_precos(self):
        self.custo_chapa = {
            "INOX 304": {0.6: 29.01, 0.8: 33.16, 1.0: 30.74, 1.2: 28.66, 1.5: 29.00, 2.0: 30.96},
            "INOX 430": {0.6: 23.32, 0.8: 19.41, 1.0: 18.91, 1.2: 19.42, 1.5: 19.38, 2.0: 19.38}
        }
        self.custo_tubo = {"TUBO-RED-38": 18.47, "TUBO-RED-25": 12.08}
        try:
            df_chapas = pd.read_excel("CHAPAS.xlsx", sheet_name="CHAPAS")
            df_304 = df_chapas[df_chapas['Aisi'] == 304]
            self.custo_chapa["INOX 304"] = dict(zip(df_304['Espessura'], df_304['Custo última compra']))
            df_430 = df_chapas[df_chapas['Aisi'] == 430]
            self.custo_chapa["INOX 430"] = dict(zip(df_430['Espessura'], df_430['Custo última compra']))
            
            df_tubos = pd.read_excel("CHAPAS.xlsx", sheet_name="TUBOS")
            for index, row in df_tubos.iterrows():
                codigo = str(row['Código'])
                preco = float(row['Custo última compra'])
                if "016.201.020" in codigo: self.custo_tubo["TUBO-RED-38"] = preco
                elif "016.201.014" in codigo: self.custo_tubo["TUBO-RED-25"] = preco
        except Exception:
            pass 

    # ==========================================
    # LÓGICA DAS 3 ABAS DE INSERÇÃO
    # ==========================================
    def adicionar_item_parametrico(self):
        try:
            item = {
                "num": len(self.carrinho) + 1,
                "tipo": "parametrico",
                "qtd": int(self.inp_qtd.get()),
                "comp": float(self.inp_comp.get()),
                "larg": float(self.inp_larg.get()),
                "alt": float(self.inp_alt.get()),
                "tampo_nome": self.combo_tampo.get(),
                "tampo_cod": self.mapa_tampo[self.combo_tampo.get()],
                "base_nome": self.combo_base.get(),
                "base_cod": self.mapa_base[self.combo_base.get()],
                "mat_tampo": self.cbo_mat_tampo.get(),
                "esp_tampo": self.cbo_esp_tampo.get(),
                "mat_base": self.cbo_mat_base.get(),
                "esp_base": self.cbo_esp_base.get()
            }
            # INCLUSÃO DA ALTURA NA DESCRIÇÃO DO CARRINHO (Conforme pedido)
            txt_tampo = f"{item['mat_tampo']}/{item['esp_tampo']}" if item['esp_tampo'] != "Esp. Padrão" else f"{item['mat_tampo']}"
            txt_base = f"{item['mat_base']}/{item['esp_base']}" if item['esp_base'] != "Esp. Padrão" else f"{item['mat_base']}"
            item["desc_carrinho"] = f"{item['tampo_nome']} c/ {item['base_nome']} ({int(item['comp'])}x{int(item['larg'])}x{int(item['alt'])}) [T:{txt_tampo} | B:{txt_base}]"
            
            self.carrinho.append(item)
            self.atualizar_visor_carrinho()
            
            self.inp_qtd.delete(0, 'end')
            self.inp_comp.delete(0, 'end')
            self.inp_larg.delete(0, 'end')
            self.inp_alt.delete(0, 'end')
            self.inp_qtd.insert(0, "1")
        except ValueError:
            messagebox.showerror("Erro", "Verifique as medidas numéricas.")

    def adicionar_peca_composto(self):
        try:
            pc = {
                "nome": self.inp_nome_pc_comp.get().strip(),
                "qtd": int(self.inp_qtd_pc_comp.get()),
                "comp": float(self.inp_comp_pc_comp.get()),
                "larg": float(self.inp_larg_pc_comp.get()),
                "mat": f"INOX {self.cbo_mat_pc_comp.get()}",
                "esp": float(self.cbo_esp_pc_comp.get())
            }
            if not pc["nome"]: raise ValueError
            
            self.pecas_temp_composto.append(pc)
            self.tree_temp.insert("", "end", values=(pc['qtd'], f"{pc['nome']} ({int(pc['comp'])}x{int(pc['larg'])})", f"{pc['mat']} {pc['esp']}"))
            
            self.inp_nome_pc_comp.delete(0, 'end')
            self.inp_comp_pc_comp.delete(0, 'end')
            self.inp_larg_pc_comp.delete(0, 'end')
            self.inp_qtd_pc_comp.delete(0, 'end')
            self.inp_qtd_pc_comp.insert(0, "1")
        except ValueError:
            messagebox.showerror("Erro", "Preencha corretamente os dados da peça.")

    def finalizar_item_composto(self):
        if not self.pecas_temp_composto:
            messagebox.showwarning("Aviso", "Adicione pelo menos uma peça antes de finalizar o item.")
            return
            
        nome_item = self.inp_nome_item_comp.get().strip() or "Item Personalizado"
        try: qtd_item = int(self.inp_qtd_item_comp.get())
        except: qtd_item = 1
        
        item = {
            "num": len(self.carrinho) + 1,
            "tipo": "composto",
            "nome_item": nome_item,
            "qtd_item": qtd_item,
            "pecas": list(self.pecas_temp_composto),
            "desc_carrinho": f"🧩 [MODULAR] {nome_item} ({len(self.pecas_temp_composto)} peças)"
        }
        self.carrinho.append(item)
        self.atualizar_visor_carrinho()
        
        self.pecas_temp_composto.clear()
        for i in self.tree_temp.get_children(): self.tree_temp.delete(i)
        self.inp_nome_item_comp.delete(0, 'end')
        
    def adicionar_item_livre(self):
        try:
            item = {
                "num": len(self.carrinho) + 1,
                "tipo": "livre",
                "qtd": int(self.inp_qtd_livre.get()),
                "nome_peca": self.inp_nome_livre.get().strip(),
                "comp_pl": float(self.inp_comp_livre.get()),
                "larg_pl": float(self.inp_larg_livre.get()),
                "esp": float(self.combo_esp_livre.get()),
                "material": self.combo_mat_livre.get()
            }
            item["desc_carrinho"] = f"✏️ [SOLTA] {item['nome_peca']} - {item['material']} {item['esp']}mm ({int(item['comp_pl'])}x{int(item['larg_pl'])})"
            
            self.carrinho.append(item)
            self.atualizar_visor_carrinho()
            
            self.inp_nome_livre.delete(0, 'end')
            self.inp_comp_livre.delete(0, 'end')
            self.inp_larg_livre.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro", "Preencha as medidas da peça avulsa corretamente.")

    # ==========================================
    # GESTÃO DO CARRINHO E TABELA
    # ==========================================
    def remover_item_carrinho(self):
        selecionado = self.tree_carrinho.selection()
        if not selecionado: return
        idx = int(self.tree_carrinho.item(selecionado[0], "values")[0]) - 1
        if 0 <= idx < len(self.carrinho):
            del self.carrinho[idx]
            for i, it in enumerate(self.carrinho): it["num"] = i + 1
            self.atualizar_visor_carrinho()

    def atualizar_visor_carrinho(self):
        for item in self.tree_carrinho.get_children(): self.tree_carrinho.delete(item)
        for i in self.carrinho:
            self.tree_carrinho.insert("", "end", values=(i['num'], i.get('qtd', i.get('qtd_item', 1)), i['desc_carrinho']))

    def limpar_carrinho(self):
        self.carrinho = []
        self.atualizar_visor_carrinho()
        for item in self.tabela.get_children(): self.tabela.delete(item)
        self.caixa_resumo.configure(state="normal")
        self.caixa_resumo.delete("0.0", "end")
        self.caixa_resumo.configure(state="disabled")
        self.btn_exportar.configure(state="disabled")
        self.btn_mapa.configure(state="disabled")

    # ==========================================
    # CÁLCULO CORE (Processa os 3 Tipos de Itens)
    # ==========================================
    def calcular_pedido_completo(self):
        if not self.carrinho:
            messagebox.showwarning("Aviso", "O Carrinho está vazio!")
            return

        for item in self.tabela.get_children(): self.tabela.delete(item)
        dados_para_df = []
        self.pecas_para_nesting_global = []
        resumo_geral_chapas = {}
        resumo_geral_tubos = {}
        peso_total_pedido = 0.0
        linhas_resumo_excel = []

        # ==================================================
        # 1. PROCESSAMENTO DE TODOS OS ITENS
        # ==================================================
        texto_detalhado = f"======================================================================\n"
        texto_detalhado += f" 📝 DETALHAMENTO DE FABRICAÇÃO E CONSUMO POR ITEM\n"
        texto_detalhado += f"======================================================================\n"

        for item in self.carrinho:
            pecas_base = []
            
            if item["tipo"] == "parametrico":
                pb_cruas = calcular_mesa_parametrica(item["comp"], item["larg"], item["alt"], item["tampo_cod"], item["base_cod"])
                for p in pb_cruas:
                    e_base = any(x in p["DESC"].upper() for x in ["PRAT", "GRADE", "PERNA", "SAPATA", "CONTRA", "TRAVESSA"])
                    mat_aplicado = item["mat_base"] if e_base else item["mat_tampo"]
                    esp_aplicada = item["esp_base"] if e_base else item["esp_tampo"]
                    p["MAT_CUSTOM"] = mat_aplicado
                    
                    if "CHAPA" in p["CÓDIGO"] and esp_aplicada != "Esp. Padrão":
                        try:
                            nova_esp = float(esp_aplicada)
                            p["ESP"] = nova_esp
                            if p["LARG PL"] != "-": p["PESO UNIT"] = float(p["COMP PL"]) * float(p["LARG PL"]) * nova_esp * 0.000008
                        except: pass
                    pecas_base.append(p)
                # INCLUSÃO DA ALTURA NA IMPRESSÃO DO RELATÓRIO
                texto_detalhado += f"\n▶ ITEM {item['num']}: {item['qtd']}x {item['tampo_nome']} c/ {item['base_nome']} ({int(item['comp'])}x{int(item['larg'])}x{int(item['alt'])})\n"
            
            elif item["tipo"] == "composto":
                for pt in item["pecas"]:
                    peso_un = pt["comp"] * pt["larg"] * pt["esp"] * 0.000008
                    pecas_base.append({"CÓDIGO": "CHAPA_LIVRE", "DESC": pt["nome"], "QTD": pt["qtd"], "COMP PL": pt["comp"], "LARG PL": pt["larg"], "ESP": pt["esp"], "PESO UNIT": peso_un, "MAT_CUSTOM": pt["mat"]})
                item["qtd"] = item["qtd_item"] 
                texto_detalhado += f"\n▶ ITEM {item['num']}: {item['qtd']}x 🧩 PRODUTO MODULAR: {item['nome_item']}\n"
            
            elif item["tipo"] == "livre":
                peso_un = item["comp_pl"] * item["larg_pl"] * item["esp"] * 0.000008
                pecas_base.append({"CÓDIGO": "CHAPA_LIVRE", "DESC": item["nome_peca"], "QTD": 1, "COMP PL": item["comp_pl"], "LARG PL": item["larg_pl"], "ESP": item["esp"], "PESO UNIT": peso_un, "MAT_CUSTOM": item["material"]})
                texto_detalhado += f"\n▶ ITEM {item['num']}: {item['qtd']}x ✏️ PEÇA SOLTA: {item['nome_peca']}\n"

            resumo_item_chapas = {}
            resumo_item_tubos = {}
            peso_item_total = 0.0
            custo_unit_item_chapa = 0.0
            custo_unit_item_tubo = 0.0
            
            texto_detalhado += f"  [ COMPONENTES DA PEÇA ]\n"

            for p in pecas_base:
                qtd_final = p["QTD"] * item["qtd"]
                peso_total_final = p["PESO UNIT"] * qtd_final
                mat_peca = p.get("MAT_CUSTOM", "INOX 304")
                desc_final = p["DESC"]
                custo_peca_un = 0.0

                if "CHAPA" in p["CÓDIGO"]:
                    desc_final = f"{mat_peca} - {desc_final}"
                    if p["LARG PL"] != "-":
                        for _ in range(qtd_final): self.pecas_para_nesting_global.append({'nome': p['DESC'], 'material': f"{mat_peca} {p['ESP']}mm", 'comp': float(p["COMP PL"]), 'larg': float(p["LARG PL"])})
                    if p["ESP"] > 0:
                        custo_peca_un = p["PESO UNIT"] * self.custo_chapa.get(mat_peca, {}).get(p["ESP"], 0.0)
                        custo_unit_item_chapa += custo_peca_un * p["QTD"]
                        
                        chave = (mat_peca, p["ESP"])
                        resumo_geral_chapas[chave] = resumo_geral_chapas.get(chave, 0) + peso_total_final
                        resumo_item_chapas[chave] = resumo_item_chapas.get(chave, 0) + peso_total_final
                        
                    # Lógica de formatação para Chapas (Mostra peso)
                    linha_medida = f"{p['PESO UNIT']:>6.2f} KG un. | {peso_total_final:>6.2f} KG tot."

                elif "TUBO" in p["CÓDIGO"]:
                    metros_unit = float(p["COMP PL"]) / 1000.0
                    metros_tot = metros_unit * qtd_final
                    custo_peca_un = metros_unit * self.custo_tubo.get(p["CÓDIGO"], 0.0)
                    custo_unit_item_tubo += custo_peca_un * p["QTD"]
                    
                    resumo_geral_tubos[p["CÓDIGO"]] = resumo_geral_tubos.get(p["CÓDIGO"], 0) + (float(p["COMP PL"]) * qtd_final)
                    resumo_item_tubos[p["CÓDIGO"]] = resumo_item_tubos.get(p["CÓDIGO"], 0) + (float(p["COMP PL"]) * qtd_final)
                    
                    # NOVA LÓGICA DE FORMATAÇÃO PARA TUBOS (Mostra metros em vez de peso)
                    linha_medida = f"{metros_unit:>6.2f} M un.  | {metros_tot:>6.2f} M tot. "
                
                desc_final_str = desc_final[:28].ljust(28)
                texto_detalhado += f"   ▫ {qtd_final}x {desc_final_str} | {linha_medida} | R$ {custo_peca_un:>6.2f} un.\n".replace('.', ',')

                med = f"{p['COMP PL']} x {p['LARG PL']}" if p['LARG PL'] != "-" else f"{p['COMP PL']} mm"
                esp_str = str(p['ESP']).replace('.', ',') if p['ESP'] > 0 else "-"
                self.tabela.insert("", "end", values=(f"Item {item['num']}", qtd_final, p["CÓDIGO"], desc_final, esp_str, med, f"{p['PESO UNIT']:.2f}", f"{peso_total_final:.2f}"))
                dados_para_df.append({"ITEM": f"Item {item['num']}", "QTD FINAL": qtd_final, "CÓDIGO PEÇA": f"'{p['CÓDIGO']}", "DESCRIÇÃO": desc_final, "ESPESSURA": esp_str, "MEDIDA CORTE": med, "PESO UNIT (KG)": round(p['PESO UNIT'],2), "PESO TOTAL (KG)": round(peso_total_final,2)})
                peso_item_total += peso_total_final
                
            texto_detalhado += f"\n  [ RESUMO DO ITEM ]\n"
            for (mat, esp), peso in sorted(resumo_item_chapas.items()): 
                texto_detalhado += f"   • Chapa {mat} {esp}mm: {peso:.2f} KG\n".replace('.', ',')
            
            # MOSTRA METROS E BARRAS NO RESUMO DO ITEM
            for cod, comp in resumo_item_tubos.items(): 
                texto_detalhado += f"   • {cod}: {comp / 1000:.2f} Mts ({comp / 6000:.2f} barras)\n".replace('.', ',')
            
            c_unit = custo_unit_item_chapa + custo_unit_item_tubo
            c_tot = c_unit * item["qtd"]
            peso_unit_item = peso_item_total / item["qtd"]
            peso_total_pedido += peso_item_total
            
            texto_detalhado += f"  --------------------------------------------------------------------\n"
            if item["qtd"] > 1:
                texto_detalhado += f"   [ Peso Unit: {peso_unit_item:.2f} KG  |  Peso Total: {peso_item_total:.2f} KG ]\n".replace('.', ',')
                texto_detalhado += f"   💰 Custo Unitário : R$ {c_unit:.2f}  |  💰 Custo TOTAL ({item['qtd']}x) : R$ {c_tot:.2f}\n".replace('.', ',')
            else:
                texto_detalhado += f"   [ Peso Total: {peso_item_total:.2f} KG ]  |  💰 Custo TOTAL : R$ {c_tot:.2f}\n".replace('.', ',')

        # ==================================================
        # 2. CONSTRUÇÃO DO RELATÓRIO MASTER (ERP STYLE)
        # ==================================================
        texto_relatorio = f"██████████████████████████████████████████████████████████████████████\n"
        texto_relatorio += f"                  📊 RELATÓRIO DO PEDIDO - MATERIAIS                  \n"
        texto_relatorio += f"██████████████████████████████████████████████████████████████████████\n"
        texto_relatorio += f" 📌 PEDIDO: {self.inp_pedido.get() or 'Avulso'}\n\n"
        
        custo_tot_chapas = 0.0
        texto_relatorio += f"----------------------------------------------------------------------\n"
        texto_relatorio += f" 📦 TOTAL DE CHAPAS INOX\n"
        texto_relatorio += f"----------------------------------------------------------------------\n"
        for (mat, esp), peso in sorted(resumo_geral_chapas.items()):
            prc = self.custo_chapa.get(mat, {}).get(esp, 0.0) 
            ct = peso * prc
            custo_tot_chapas += ct
            texto_relatorio += f" > {mat} {esp}mm".ljust(25) + f" {peso:7.2f} KG  |  R$ {prc:6.2f}/kg  |  Sub: R$ {ct:8.2f}\n".replace('.', ',')
            linhas_resumo_excel.append({"TIPO": "CHAPA", "MATERIAL": f"{mat} {esp}mm", "QTD": f"{peso:.2f} KG".replace('.', ','), "CUSTO (R$)": round(ct, 2)})
            
        texto_relatorio += f"\n = PESO TOTAL CHAPA:     {peso_total_pedido:8.2f} KG\n".replace('.', ',')
        texto_relatorio += f" = CUSTO TOTAL CHAPA:    R$ {custo_tot_chapas:8.2f}\n\n".replace('.', ',')

        custo_tot_tubos = 0.0
        if resumo_geral_tubos:
            texto_relatorio += f"----------------------------------------------------------------------\n"
            texto_relatorio += f" 📏 TOTAL DE TUBOS E PERFIS\n"
            texto_relatorio += f"----------------------------------------------------------------------\n"
            for cod, c_total in resumo_geral_tubos.items():
                mts = c_total / 1000.0
                barras = mts / 6.0
                prc = self.custo_tubo.get(cod, 0.0)
                ct = mts * prc
                custo_tot_tubos += ct
                texto_relatorio += f" > {cod}".ljust(25) + f" {mts:7.2f} M   |  R$ {prc:6.2f}/m   |  Sub: R$ {ct:8.2f}\n".replace('.', ',')
                linhas_resumo_excel.append({"TIPO": "TUBO", "MATERIAL": f"{cod}", "QTD": f"{mts:.2f} M ({barras:.1f} un)".replace('.', ','), "CUSTO (R$)": round(ct, 2)})
            texto_relatorio += f"\n = CUSTO TOTAL TUBOS:    R$ {custo_tot_tubos:8.2f}\n\n".replace('.', ',')

        if HAS_NESTING and self.pecas_para_nesting_global:
            texto_relatorio += f"----------------------------------------------------------------------\n"
            texto_relatorio += f" 🧩 SIMULAÇÃO DE ENCAIXE VIRTUAL (CHAPAS {self.dim_chapa_x}x{self.dim_chapa_y})\n"
            texto_relatorio += f"----------------------------------------------------------------------\n"
            agrup_nesting = {}
            for pc in self.pecas_para_nesting_global:
                chave = pc['material']
                if chave not in agrup_nesting: agrup_nesting[chave] = []
                agrup_nesting[chave].append((pc['comp'], pc['larg']))
                
            for mat_nome, dimensoes in agrup_nesting.items():
                packer = newPacker(mode=PackingMode.Offline, bin_algo=PackingBin.Global, rotation=True)
                for idx, (c, l) in enumerate(dimensoes): packer.add_rect(width=c + 5, height=l + 5, rid=idx)
                for _ in range(50): packer.add_bin(width=self.dim_chapa_x, height=self.dim_chapa_y)
                packer.pack()
                chp_usadas = len(packer)
                area_pc = sum([c * l for c, l in dimensoes])
                area_ch = chp_usadas * (self.dim_chapa_x * self.dim_chapa_y)
                aprov = (area_pc / area_ch) * 100 if area_ch > 0 else 0
                texto_relatorio += f" > {mat_nome}".ljust(25) + f" {chp_usadas} chapa(s)   |  Aprov: {aprov:5.1f}%\n".replace('.', ',')
            texto_relatorio += f"\n"

        custo_total_geral = custo_tot_chapas + custo_tot_tubos
        texto_relatorio += f"██████████████████████████████████████████████████████████████████████\n"
        texto_relatorio += f" 💰 CUSTO TOTAL ESTIMADO (MATERIAL): R$ {custo_total_geral:10.2f}\n".replace('.', ',')
        texto_relatorio += f"██████████████████████████████████████████████████████████████████████\n\n\n"
        
        # INJEÇÃO NA TELA
        self.caixa_resumo.configure(state="normal")
        self.caixa_resumo.delete("0.0", "end")
        self.caixa_resumo.insert("0.0", texto_relatorio + texto_detalhado)
        self.caixa_resumo.configure(state="disabled")

        self.df_lista = pd.DataFrame(dados_para_df)
        self.df_resumo = pd.DataFrame(linhas_resumo_excel)
        self.btn_exportar.configure(state="normal")
        self.btn_mapa.configure(state="normal") 
        self.abas_res.set("📊 Relatório de Materiais e Custos") 

    def abrir_mapa_corte(self):
        if not HAS_NESTING or not self.pecas_para_nesting_global: return
        agrup_grafico = {}
        for pc in self.pecas_para_nesting_global:
            if pc['material'] not in agrup_grafico: agrup_grafico[pc['material']] = []
            agrup_grafico[pc['material']].append(pc)

        for mat_nome, lista_pecas in agrup_grafico.items():
            packer = newPacker(mode=PackingMode.Offline, bin_algo=PackingBin.Global, rotation=True)
            for idx, p in enumerate(lista_pecas): packer.add_rect(width=p["comp"]+5, height=p["larg"]+5, rid=idx)
            for _ in range(50): packer.add_bin(width=self.dim_chapa_x, height=self.dim_chapa_y)
            packer.pack()

            for b_idx, bin in enumerate(packer):
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.set_xlim(0, self.dim_chapa_x); ax.set_ylim(0, self.dim_chapa_y)
                ax.set_title(f"Plano de Corte - {mat_nome} | Chapa {b_idx + 1}", fontweight='bold')
                ax.add_patch(patches.Rectangle((0, 0), self.dim_chapa_x, self.dim_chapa_y, fill=True, facecolor='#ecf0f1', edgecolor='black', lw=2))

                for rect in bin:
                    w, h = rect.width, rect.height
                    pc_nome = lista_pecas[rect.rid]['nome']
                    ax.add_patch(patches.Rectangle((rect.x, rect.y), w, h, fill=True, facecolor='#2980b9', edgecolor='white', lw=1.5))
                    ax.text(rect.x + w/2, rect.y + h/2, f"{pc_nome}\n{int(w)}x{int(h)}", ha='center', va='center', fontsize=7, color='white', fontweight='bold')

                plt.gca().set_aspect('equal', adjustable='box')
                plt.tight_layout()
        plt.show()

    def exportar_excel(self):
        if self.df_lista is not None and self.df_resumo is not None:
            filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile="PCP_Pedido.xlsx", title="Salvar PCP", filetypes=[("Excel Files", "*.xlsx")])
            if filepath:
                with pd.ExcelWriter(filepath, engine='openpyxl') as w:
                    self.df_lista.to_excel(w, index=False, sheet_name='Lista_Corte_PCP')
                    self.df_resumo.to_excel(w, index=False, sheet_name='Resumo_Materiais')
                messagebox.showinfo("Sucesso", f"Excel do pedido guardado com sucesso!")

if __name__ == "__main__":
    app = ProjetistaApp()
    app.mainloop()