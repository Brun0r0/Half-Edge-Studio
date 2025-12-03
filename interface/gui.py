import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from interface import logica_interface
from core.modificacoes import modificar_estrutura, reflex_ponto
from interface.interface_openGL import Janela_OpenGL
from core.half_edge_funcoes import visualizar_estrutura_half_edge

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("app")
        self.resizable(False, False)
        self.configure(fg_color=("gray90", "gray12"))

        self.estruturas = []

        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame da lista de objetos
        frame_widgets = ctk.CTkFrame(main_frame)
        frame_widgets.grid(row=0, column=2, padx=10, pady=10)
        
        # Sub-frame da lista (utilizo essa só para listBox e scrollBar)
        ctk.CTkLabel(frame_widgets, text='Lista objetos', font=('Arial', 12, 'bold')).pack()
        sub_frame_widgets = ctk.CTkFrame(frame_widgets, width=150, height=100)
        sub_frame_widgets.pack_propagate(False)
        sub_frame_widgets.pack(pady=5)

        # Configurando scrollBar e listBox
        self.scrollbar_lista = tk.Scrollbar(sub_frame_widgets)
        self.listbox_lista = tk.Listbox(sub_frame_widgets, yscrollcommand=self.scrollbar_lista.set, height=10, selectmode=ctk.SINGLE)
        self.scrollbar_lista.config(command=self.listbox_lista.yview)

        self.listbox_lista.pack(side="left", fill="both", expand=True)
        self.scrollbar_lista.pack(side="right", fill="y")

        self.atualizar_listbox()

        ctk.CTkButton(frame_widgets, text='Selecionar objeto', command=self.processar_selecionado).pack(pady=10)

        ctk.CTkButton(frame_widgets, text='Limpar', command=self.limpar_tudo).pack(pady=10)

        ctk.CTkLabel(frame_widgets, text='Algoritmo', font=('Arial', 12, 'bold'))

        algoritmo_var = ctk.BooleanVar(value=True)  # True = Bresenham, False = Wu

        frame_alg = ctk.CTkFrame(frame_widgets)
        frame_alg.pack(anchor="w", padx=10)

        ctk.CTkRadioButton(frame_alg, text="Bresenham", variable=algoritmo_var, value=True,
                       command=lambda: self.openGL_view.set_algoritmo(algoritmo_var.get())).pack(anchor="w")

        ctk.CTkRadioButton(frame_alg, text="Xiaolin Wu", variable=algoritmo_var, value=False,
                       command=lambda: self.openGL_view.set_algoritmo(algoritmo_var.get())).pack(anchor="w")

        frame_trans = ctk.CTkFrame(frame_widgets)
        frame_trans.pack(anchor="w", pady=10, fill="x")

        ctk.CTkLabel(frame_trans, text="Translação", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))

        sub_trans = ctk.CTkFrame(frame_trans)
        sub_trans.grid(row=1, column=0, padx=20, sticky="w")

        ctk.CTkLabel(sub_trans, text="X:").grid(row=0, column=0, sticky="e", padx=5)
        self.CTkEntry_tx = ctk.CTkEntry(sub_trans, width=8)
        self.CTkEntry_tx.insert(0, "0")
        self.CTkEntry_tx.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(sub_trans, text="Y:").grid(row=1, column=0, sticky="e", padx=5)
        self.CTkEntry_ty = ctk.CTkEntry(sub_trans, width=8)
        self.CTkEntry_ty.insert(0, "0")
        self.CTkEntry_ty.grid(row=1, column=1, sticky="w")

        frame_esc = ctk.CTkFrame(frame_widgets)
        frame_esc.pack(anchor="w", pady=10, fill="x")

        ctk.CTkLabel(frame_esc, text="Escalar", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))

        sub_esc = ctk.CTkFrame(frame_esc)
        sub_esc.grid(row=1, column=0, padx=20, sticky="w")

        ctk.CTkLabel(sub_esc, text="X:").grid(row=0, column=0, sticky="e", padx=5)
        self.CTkEntry_sx = ctk.CTkEntry(sub_esc, width=8)
        self.CTkEntry_sx.insert(0, "0")
        self.CTkEntry_sx.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(sub_esc, text="Y:").grid(row=1, column=0, sticky="e", padx=5)
        self.CTkEntry_sy = ctk.CTkEntry(sub_esc, width=8)
        self.CTkEntry_sy.insert(0, "0")
        self.CTkEntry_sy.grid(row=1, column=1, sticky="w")

        frame_cis = ctk.CTkFrame(frame_widgets)
        frame_cis.pack(anchor="w", pady=10, fill="x")

        frame_reflex = ctk.CTkFrame(frame_widgets)
        frame_reflex.pack(anchor='w', pady=10, fill='x')

        ctk.CTkLabel(frame_reflex, text="Reflexão", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))
        
        sub_reflex = ctk.CTkFrame(frame_reflex)
        sub_reflex.grid(row=1, column=0, padx=20, sticky='w')

        self.CTkButton_ref_x = ctk.CTkButton(sub_reflex, text='Refletir x', command= self.reflex_x)
        self.CTkButton_ref_x.grid(row=0, column=1, sticky='w', pady=2)

        self.CTkButton_ref_y = ctk.CTkButton(sub_reflex, text='Refletir y', command= self.reflex_y)
        self.CTkButton_ref_y.grid(row=1, column=1, sticky='w', pady=2)

        ctk.CTkLabel(frame_cis, text="Cisalhamento", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))

        sub_cis = ctk.CTkFrame(frame_cis)
        sub_cis.grid(row=1, column=0, padx=20, sticky="w")

        ctk.CTkLabel(sub_cis, text="X:").grid(row=0, column=0, sticky="e", padx=5)
        self.CTkEntry_cisx = ctk.CTkEntry(sub_cis, width=8)
        self.CTkEntry_cisx.insert(0, "0")
        self.CTkEntry_cisx.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(sub_cis, text="Y:").grid(row=1, column=0, sticky="e", padx=5)
        self.CTkEntry_cisy = ctk.CTkEntry(sub_cis, width=8)
        self.CTkEntry_cisy.insert(0, "0")
        self.CTkEntry_cisy.grid(row=1, column=1, sticky="w")

        frame_rot = ctk.CTkFrame(frame_widgets)
        frame_rot.pack(anchor="w", pady=10, fill="x")

        ctk.CTkLabel(frame_rot, text="Rotação", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))

        sub_rot = ctk.CTkFrame(frame_rot)
        sub_rot.grid(row=1, column=0, padx=20, sticky="w")

        ctk.CTkLabel(sub_rot, text="Ângulo:").grid(row=0, column=0, sticky="e", padx=5)
        self.CTkEntry_a = ctk.CTkEntry(sub_rot, width=8)
        self.CTkEntry_a.insert(0, "0")
        self.CTkEntry_a.grid(row=0, column=1, sticky="w")

        frame_aplicar = ctk.CTkFrame(frame_widgets)
        frame_aplicar.pack(anchor="w", pady=10, fill="x")

        self.CTkButton_aplicar = ctk.CTkButton(frame_aplicar, text='Aplicar', font=('Arial', 14, 'bold'), command=self.aplicar_mods)
        self.CTkButton_aplicar.pack(pady=10)
        
        frame_openGL = ctk.CTkFrame(main_frame)
        frame_openGL.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_openGL, text="Visualização no OpenGL", font=('Arial', 12, 'bold')).pack(pady=10)

        self.openGL_view = Janela_OpenGL(frame_openGL, width=700, height=700)
        self.openGL_view.pack(fill='both', expand=True)
        self.openGL_view.animate = 1

        frame_estrutura = ctk.CTkFrame(main_frame)
        frame_estrutura.grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(frame_estrutura, text="Visualização estrutura Half-Edge", font=('Arial', 12, 'bold')).pack(pady=10)

        sub_frame_estrutura = ctk.CTkFrame(frame_estrutura)
        sub_frame_estrutura.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(sub_frame_estrutura)
        scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        self.tree = ttk.Treeview(sub_frame_estrutura, yscrollcommand=scrollbar.set, selectmode='none', height=34)
        self.tree.pack(side=ctk.LEFT, fill= ctk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

        self.tree.column("#0", width=400)

        self.update_idletasks()
        self.geometry(f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}")
        

    def atualizar_listbox(self):
        self.listbox_lista.delete(0, ctk.END)
        nomes_arquivos = logica_interface.obter_nomes_objetos()
        for nome in nomes_arquivos:
            self.listbox_lista.insert(ctk.END, nome)

    def atualizar_estrutura_lista(self):
        
        self.tree.delete(*self.tree.get_children())

        for estrutura in self.estruturas:
            estrutura_text = visualizar_estrutura_half_edge(estrutura)
            if estrutura_text:
                lista_num = self.estruturas.index(estrutura) + 1
                self.tree.insert("", "end", text=f"--- Estrutura {lista_num} ---")

                for linha in estrutura_text.split('\n'):
                    self.tree.insert("", "end", text=linha)

    def processar_selecionado(self):
        selecao = self.listbox_lista.curselection()   
        if selecao:
            indice = selecao[0]
            nome = self.listbox_lista.get(indice)
            print(f"Objeto selecionado: {nome}")

        self.resetar_configs()

        estrutura = logica_interface.ler_arquivo(nome)

        self.estruturas.append(estrutura)

        self.openGL_view.set_estrutura(estrutura)

        self.atualizar_estrutura_lista()

    def reflex_x(self):
        if self.estruturas is None:
            return
        
        reflex_ponto(self.estruturas, 'x')

        self.atualizar_estrutura_lista()

    def reflex_y(self):
        if self.estruturas is None:
            return
        
        reflex_ponto(self.estruturas, 'y')

        self.atualizar_estrutura_lista()

    def aplicar_mods(self, valor = None):
        if self.estruturas is None:
            return
        
        tx = float(self.CTkEntry_tx.get())
        ty = float(self.CTkEntry_ty.get())
        sx = float(self.CTkEntry_sx.get())
        sy = float(self.CTkEntry_sy.get())
        cis_x = float(self.CTkEntry_cisx.get())
        cis_y = float(self.CTkEntry_cisy.get())
        angulo = float(self.CTkEntry_a.get())

        modificar_estrutura(self.estruturas, tx, ty, sx, sy, cis_x, cis_y, angulo)

        self.openGL_view.redraw()

        self.resetar_configs()

        self.atualizar_estrutura_lista()

    def limpar_tudo(self):

        self.estruturas = []
        self.openGL_view.estruturas = []

        self.tree.delete(*self.tree.get_children())

        self.resetar_configs()
    
    def resetar_configs(self):

        self.CTkEntry_tx.delete(0, ctk.END)
        self.CTkEntry_tx.insert(0, "0")

        self.CTkEntry_ty.delete(0, ctk.END)
        self.CTkEntry_ty.insert(0, "0")

        self.CTkEntry_sx.delete(0, ctk.END)
        self.CTkEntry_sx.insert(0, "1")

        self.CTkEntry_sy.delete(0, ctk.END)
        self.CTkEntry_sy.insert(0, "1")

        self.CTkEntry_cisx.delete(0, ctk.END)
        self.CTkEntry_cisx.insert(0, "0")

        self.CTkEntry_cisy.delete(0, ctk.END)
        self.CTkEntry_cisy.insert(0, "0")

        self.CTkEntry_a.delete(0, ctk.END)
        self.CTkEntry_a.insert(0, "0")