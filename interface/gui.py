import tkinter as tk
from tkinter import ttk
import copy
from interface import logica
from core.funcoes_modificacao import modificar_estrutura, reflex_ponto
from interface.interface_openGL import Janela_OpenGL
from core.half_edge_funcoes import visualizar_estrutura_half_edge

class App(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("app")
        self.geometry("1400x800")

        self.estrutura = None

        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame da lista de objetos
        frame_widgets = tk.Frame(main_frame)
        frame_widgets.grid(row=0, column=0, padx=10, pady=10)
        
        # Sub-frame da lista (utilizo essa só para listBox e scrollBar)
        tk.Label(frame_widgets, text='Lista objetos', font=('Arial', 12, 'bold')).pack()
        sub_frame_widgets = tk.Frame(frame_widgets, width=150, height=100)
        sub_frame_widgets.pack_propagate(False)
        sub_frame_widgets.pack(pady=5)

        # Configurando scrollBar e listBox
        self.scrollbar_lista = tk.Scrollbar(sub_frame_widgets)
        self.listbox_lista = tk.Listbox(sub_frame_widgets, yscrollcommand=self.scrollbar_lista.set, height=10, selectmode=tk.SINGLE)
        self.scrollbar_lista.config(command=self.listbox_lista.yview)

        self.listbox_lista.pack(side="left", fill="both", expand=True)
        self.scrollbar_lista.pack(side="right", fill="y")

        self.atualizar_listbox()

        tk.Button(frame_widgets, text='Selecionar objeto/Resetar', command=self.processar_selecionado).pack(pady=10)
        

        frame_trans = tk.Frame(frame_widgets)
        frame_trans.pack(anchor="w", pady=10, fill="x")

        tk.Label(frame_trans, text="Translação", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))

        sub_trans = tk.Frame(frame_trans)
        sub_trans.grid(row=1, column=0, padx=20, sticky="w")

        tk.Label(sub_trans, text="X:").grid(row=0, column=0, sticky="e", padx=5)
        self.entry_tx = tk.Entry(sub_trans, width=8)
        self.entry_tx.insert(0, "0")
        self.entry_tx.grid(row=0, column=1, sticky="w")

        tk.Label(sub_trans, text="Y:").grid(row=1, column=0, sticky="e", padx=5)
        self.entry_ty = tk.Entry(sub_trans, width=8)
        self.entry_ty.insert(0, "0")
        self.entry_ty.grid(row=1, column=1, sticky="w")

        frame_esc = tk.Frame(frame_widgets)
        frame_esc.pack(anchor="w", pady=10, fill="x")

        tk.Label(frame_esc, text="Escalar", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))

        sub_esc = tk.Frame(frame_esc)
        sub_esc.grid(row=1, column=0, padx=20, sticky="w")

        tk.Label(sub_esc, text="X:").grid(row=0, column=0, sticky="e", padx=5)
        self.entry_sx = tk.Entry(sub_esc, width=8)
        self.entry_sx.insert(0, "0")
        self.entry_sx.grid(row=0, column=1, sticky="w")

        tk.Label(sub_esc, text="Y:").grid(row=1, column=0, sticky="e", padx=5)
        self.entry_sy = tk.Entry(sub_esc, width=8)
        self.entry_sy.insert(0, "0")
        self.entry_sy.grid(row=1, column=1, sticky="w")

        frame_cis = tk.Frame(frame_widgets)
        frame_cis.pack(anchor="w", pady=10, fill="x")

        frame_reflex = tk.Frame(frame_widgets)
        frame_reflex.pack(anchor='w', pady=10, fill='x')

        tk.Label(frame_reflex, text="Reflexão", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))
        
        sub_reflex = tk.Frame(frame_reflex)
        sub_reflex.grid(row=1, column=0, padx=20, sticky='w')

        self.button_ref_x = tk.Button(sub_reflex, text='Refletir x', command= self.reflex_x)
        self.button_ref_x.grid(row=0, column=1, sticky='w', pady=2)

        self.button_ref_y = tk.Button(sub_reflex, text='Refletir y', command= self.reflex_y)
        self.button_ref_y.grid(row=1, column=1, sticky='w', pady=2)

        tk.Label(frame_cis, text="Cisalhamento", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))

        sub_cis = tk.Frame(frame_cis)
        sub_cis.grid(row=1, column=0, padx=20, sticky="w")

        tk.Label(sub_cis, text="X:").grid(row=0, column=0, sticky="e", padx=5)
        self.entry_cisx = tk.Entry(sub_cis, width=8)
        self.entry_cisx.insert(0, "0")
        self.entry_cisx.grid(row=0, column=1, sticky="w")

        tk.Label(sub_cis, text="Y:").grid(row=1, column=0, sticky="e", padx=5)
        self.entry_cisy = tk.Entry(sub_cis, width=8)
        self.entry_cisy.insert(0, "0")
        self.entry_cisy.grid(row=1, column=1, sticky="w")

        frame_rot = tk.Frame(frame_widgets)
        frame_rot.pack(anchor="w", pady=10, fill="x")

        tk.Label(frame_rot, text="Rotação", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))

        sub_rot = tk.Frame(frame_rot)
        sub_rot.grid(row=1, column=0, padx=20, sticky="w")

        tk.Label(sub_rot, text="Ângulo:").grid(row=0, column=0, sticky="e", padx=5)
        self.entry_a = tk.Entry(sub_rot, width=8)
        self.entry_a.insert(0, "0")
        self.entry_a.grid(row=0, column=1, sticky="w")

        frame_aplicar = tk.Frame(frame_widgets)
        frame_aplicar.pack(anchor="w", pady=10, fill="x")

        self.button_aplicar = tk.Button(frame_aplicar, text='Aplicar', font=('Arial', 14, 'bold'), command=self.aplicar_mods)
        self.button_aplicar.pack(pady=10)
        
        frame_openGL = tk.Frame(main_frame)
        frame_openGL.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame_openGL, text="Visualização no OpenGL", font=('Arial', 12, 'bold')).pack(pady=10)

        self.openGL_view = Janela_OpenGL(frame_openGL, width=700, height=700)
        self.openGL_view.pack(fill='both', expand=True)
        self.openGL_view.animate = 1

        frame_estrutura = tk.Frame(main_frame)
        frame_estrutura.grid(row=0, column=2, padx=10, pady=10)

        tk.Label(frame_estrutura, text="Visualização estrutura Half-Edge", font=('Arial', 12, 'bold')).pack(pady=10)

        sub_frame_estrutura = tk.Frame(frame_estrutura)
        sub_frame_estrutura.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(sub_frame_estrutura)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(sub_frame_estrutura, yscrollcommand=scrollbar.set, selectmode='none', height=20)
        self.tree.pack(side=tk.LEFT, fill= tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

        self.tree.column("#0", width=400)
        

    def atualizar_listbox(self):
        self.listbox_lista.delete(0, tk.END)
        nomes_arquivos = logica.obter_nomes_objetos()
        for nome in nomes_arquivos:
            self.listbox_lista.insert(tk.END, nome)


    def atualizar_estrutura_lista(self):

        estrutura_text = visualizar_estrutura_half_edge(self.estrutura)

        self.tree.delete(*self.tree.get_children())

        for linha in estrutura_text.split('\n'):
            self.tree.insert("", "end", text=linha)

    def processar_selecionado(self):
        selecao = self.listbox_lista.curselection()   
        if selecao:
            indice = selecao[0]
            nome = self.listbox_lista.get(indice)
            print(f"Objeto selecionado: {nome}")

        self.resetar_configs()

        self.estrutura = logica.ler_arquivo(nome)

        self.openGL_view.set_estrutura(self.estrutura)

        self.atualizar_estrutura_lista()

    def reflex_x(self):
        if self.estrutura is None:
            return
        
        reflex_ponto(self.estrutura, 'x')

        self.atualizar_estrutura_lista()

    def reflex_y(self):
        if self.estrutura is None:
            return
        
        reflex_ponto(self.estrutura, 'y')

        self.atualizar_estrutura_lista()


    def aplicar_mods(self, valor = None):
        if self.estrutura is None:
            return
        
        tx = float(self.entry_tx.get()) * 0.01
        ty = float(self.entry_ty.get()) * 0.01
        sx = float(self.entry_sx.get())
        sy = float(self.entry_sy.get())
        cis_x = float(self.entry_cisx.get()) * 0.01
        cis_y = float(self.entry_cisy.get()) * 0.01
        angulo = float(self.entry_a.get())

        modificar_estrutura(self.estrutura, tx, ty, sx, sy, cis_x, cis_y, angulo)

        if self.openGL_view.bbox_inicial is not None:
            self.openGL_view.bbox = self.openGL_view.bbox_inicial

        self.openGL_view.redraw()

        self.resetar_configs()

        self.atualizar_estrutura_lista()

    def resetar_configs(self):

        self.entry_tx.delete(0, tk.END)
        self.entry_tx.insert(0, "0")

        self.entry_ty.delete(0, tk.END)
        self.entry_ty.insert(0, "0")

        self.entry_sx.delete(0, tk.END)
        self.entry_sx.insert(0, "1")

        self.entry_sy.delete(0, tk.END)
        self.entry_sy.insert(0, "1")

        self.entry_cisx.delete(0, tk.END)
        self.entry_cisx.insert(0, "0")

        self.entry_cisy.delete(0, tk.END)
        self.entry_cisy.insert(0, "0")

        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, "0")