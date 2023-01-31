import tkinter as tk
from tkinter import ttk, Label, PhotoImage
from tkinter.ttk import Treeview
from tkinter import *
import json
import tkinter.messagebox as messagebox
import requests


class TASAINDODAJAULAOMONSTRO():
     

    
    def __init__(self):
        #Var principal de leitura do banco
        #Em varias funções precisei re-fazer a conexão. Preciso melhorar o conhecimento em variaveis globai e locais.
        self.base_url = 'https://filachifrudos-default-rtdb.firebaseio.com/'

        self.tela = Tk()
        self.tela.geometry('430x490')
        #self.tela.resizable(width=FALSE, height=FALSE)
        self.img = PhotoImage(file=r'C:\Users\chris\OneDrive\Área de Trabalho\waitonline\frontend_admin.png')
        
          #frames 
        
        self.frame_tela = Label(self.tela, image= self.img)
        self.frame_tela.pack()
        self.tabela_frame = Frame(self.tela)
        self.tabela_frame.pack()

         #botoes
        self.add_button = Button(text ='Add', width= 10, bd = 0, command=self.add, bg= 'black', fg= 'white')
        self.add_button.place( x= 45, y= 387, height=20)
        self.deletar_button = Button(text = 'Delete', width= 10, bd= 0, command= self.delete, bg= 'black', fg='white')
        self.deletar_button.place(x = 190, y= 387, height=20)
        self.atualiza_button = Button(text= 'Atualizar', width=10, bd= 0, command = self.att, bg = 'black', fg= 'white')
        self.atualiza_button.place( x = 333, y = 387, height=20)
        
        #Label  e entry para dados da função de Add
        self.placa_label = Label(text= 'Placa', width=10, bd=0, bg= 'black', fg = 'white')
        self.placa_label.place(x = 13, y= 422, height= 20)
        self.placa_ent = Entry(bg='black', fg='white', width=13, bd=0)
        self.placa_ent.place(x= 115, y=425, height=20 )

        self.transportadora = Label(text = 'Transp', bd=0, width=10, bg= 'black', fg= 'white')
        self.transportadora.place( x= 13, y= 457 )
        self.transp_ent = Entry(bg= 'black', fg='white',width=13, bd= 0)
        self.transp_ent.place(x =114 , y = 460, height=20 )

        self.nome_motorista = Label(text = 'Motorista', bd=0, width=10, bg= 'black', fg= 'white')
        self.nome_motorista.place( x= 228, y= 424 )
        self.nome_ent = Entry(bg= 'black', fg='white',width=13, bd= 0)
        self.nome_ent.place(x =331 , y = 425, height=20 )

        self.produto = Label(text = 'Produto', bd=0, width=10, bg= 'black', fg= 'white')
        self.produto.place( x= 227, y= 457 )
        self.produto_ent = Entry(bg= 'black', fg='white',width=13, bd= 0)
        self.produto_ent.place(x =330 , y = 457, height=20 )

        #tabelas Treeview. Tem vida própria. Não entendi o motivo mas só funciona se o frame for o usado. Não consigo movimentar ela direito.
        self.tree = Treeview(self.tela, columns=("plate", "transp", "motorista", "produto"))
        
        self.tree.heading("#0", text="ID")
        self.tree.heading("plate", text="Placa")
        self.tree.heading("transp", text="Transportadora")
        self.tree.heading("motorista", text = "Motorista")
        self.tree.heading("produto", text= "Produto")
        self.tree.column("#0", anchor= 'e',  width=5, minwidth=50, stretch=False)
        self.tree.column("plate", width=60, minwidth=50, stretch=False)
        self.tree.column("transp", width=60, minwidth=50, stretch=False)
        self.tree.column("motorista", width=90)
        self.tree.column("produto", width=60)
        self.tree.place (x = 10, y=85)
        
        self.att()
        self.tree.bind("<Double-1>", self.on_select)
        # deixa a tela sempre em primeiro plano( para ediçao de imagem) self.tela.attributes("-topmost", True)
        self.tela.mainloop()

    def att(self):
        url = "https://filachifrudos-default-rtdb.firebaseio.com/pedido.json"
        response = requests.get(url)
        data = response.json()

        for order_id, order_data in data.items():
            if not self.tree.exists(order_id):
                self.tree.insert("", "end", order_id, text=order_id)
                self.tree.set(order_id, "plate", order_data["plate"])
                self.tree.set(order_id, "transp", order_data["transp"])
                self.tree.set(order_id, "produto", order_data["produto"])
                self.tree.set(order_id, "motorista", order_data["motorista"])

   #funcao para adicionar
    def add(self):
            placa = self.placa_ent.get()
            transp = self.transp_ent.get()
            if not placa or not transp:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return
            self.save()
            self.placa_ent.delete(0, END)
            self.transp_ent.delete(0, END)
            self.att()
    # funcao de save
    def save(self):
        placa = self.placa_ent.get()
        transp = self.transp_ent.get()
        motor = self.nome_ent.get()
        prod = self.produto_ent.get()
        truck = {"plate": placa, "transp": transp, "motorista": motor, "produto":prod}
        requests.post(f'{self.base_url}/pedido.json', json=truck)
   
    #INFERNO DE FUNÇÃO DO CARALHO               
    def delete(self):
        selected_item = self.tree.selection()[0]
        base_url = 'https://filachifrudos-default-rtdb.firebaseio.com/pedido.json'
        
        # Delete, Essa merda não deleta do banco de dados, apenas da treeview! infernooooooooo
        url = f'{base_url}{selected_item}.json'
        requests.delete(url)
        self.tree.delete(selected_item)
   
    def on_select(self, event):
        self.tree.config(selectmode= 'browse') # torna a tree editável
        selected_item = self.tree.selection()[0]
        new_value = self.tree.item(selected_item)['values']
        self.tree.set(selected_item, column=0, value=new_value[0])
        self.tree.set(selected_item, column=1, value=new_value[1])
        self.tree.config(selectmode='none') # desabilita a edição  

program = TASAINDODAJAULAOMONSTRO()
