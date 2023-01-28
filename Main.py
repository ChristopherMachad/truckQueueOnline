import tkinter as tk
from tkinter import ttk, Label, PhotoImage
from tkinter.ttk import Treeview
from tkinter import *
import json
import tkinter.messagebox as messagebox
from tkinter import ttk
from turtle import width
from typing import Self
import requests


class TASAINDODAJAULAOMONSTRO():
      #----cores----
    __gray        = '#a7acb6' #cinza
    __gray_one    = '#333333' #cinza denovo

    
    def __init__(self):
        #Var principal de leitura do banco
        #Em varias funções precisei re-fazer a conexão. Preciso melhorar o conhecimento em variaveis globai e locais.
        self.base_url = 'https://filatrucks-default-rtdb.firebaseio.com/'

        self.tela = Tk()
        self.tela.geometry('430x580')
        #self.tela.resizable(width=FALSE, height=FALSE)
        self.img = PhotoImage(file=r'C:\Users\balanca.algodoeira\Desktop\waitonline\frontend.png')
        
          #frames 
        
        self.frame_tela = Label(self.tela, image= self.img)
        self.frame_tela.pack()
        self.tabela_frame = Frame(self.tela)
        self.tabela_frame.pack()

         #botoes
        self.add_button = Button(text ='Add', width= 10, bd = 0, command=self.add, bg= 'black', fg= 'white')
        self.add_button.place( x= 42, y= 486, height=20)
        self.deletar_button = Button(text = 'Delete', width= 10, bd= 0, command= self.delete, bg= 'black', fg='white')
        self.deletar_button.place(x = 188, y= 486, height=20)
        self.atualiza_button = Button(text= 'Atualizar', width=10, bd= 0, command = self.att, bg = 'black', fg= 'white')
        self.atualiza_button.place( x = 330, y = 486, height=20)

        #Label  e entry para dados da função de Add
        self.placa_label = Label(text= 'Placa', width=10, bd=0, bg= 'black', fg = 'white')
        self.placa_label.place(x = 109, y= 516, height= 20)
        self.placa_ent = Entry(bg='black', fg='white', width=20, bd=2)
        self.placa_ent.place(x= 212, y=517 )

        self.transportadora = Label(text = 'Transp', bd=0, width=10, bg= 'black', fg= 'white')
        self.transportadora.place( x= 108, y= 555 )
        self.transp_ent = Entry(bg= 'black', fg='white', bd= 2)
        self.transp_ent.place(x =211 , y = 556, height=20 )

        #tabelas Treeview. Tem vida própria. Não entendi o motivo mas só funciona se o frame for o usado. Não consigo movimentar ela direito.
        self.tree = Treeview(self.tela, columns=("plate", "transp"))
        
        self.tree.heading("#0", text="ID")
        self.tree.heading("plate", text="Placa")
        self.tree.heading("transp", text="Transportadora")
        self.tree.column("#0", anchor= 'e',  width=5, minwidth=50, stretch=False)
        self.tree.column("plate", width=100, minwidth=50, stretch=False)
        self.tree.column("transp", width=100, minwidth=50, stretch=False)
        self.tree.place (x = 0, y=10)
        
        self.att()
        self.tree.bind("<Double-1>", self.on_select)
        # deixa a tela sempre em primeiro plano( para ediçao de imagem) self.tela.attributes("-topmost", True)
        self.tela.mainloop()

     # funcao para atualizar tree

    def att(self):
        url = "https://filatrucks-default-rtdb.firebaseio.com/pedido.json"
        response = requests.get(url)
        data = response.json()

        for order_id, order_data in data.items():
            if not self.tree.exists(order_id):
                self.tree.insert("", "end", order_id, text=order_id)
                self.tree.set(order_id, "plate", order_data["plate"])
                self.tree.set(order_id, "transp", order_data["transp"])

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
    # funcao de save
    def save(self):
        placa = self.placa_ent.get()
        transp = self.transp_ent.get()
        truck = {"plate": placa, "transp": transp}
        #conexao do programa com a base_url
        response = requests.post(f'{self.base_url}/pedido.json', json=truck)
                  
        #------grande dor de cabeça, caso as informaçoes selecionadas forem de type 'int' 
        # ele vai deletar da tree, mas ao atualizar ou reiniciar o programa, as informaçoes irao voltar. meu deus eu odeio isso 
    def delete(self):
        selected_item = self.tree.selection()[0]
        plate = self.tree.item(selected_item)['values'][0]
        transp = self.tree.item(selected_item)['values'][1]
        base_url = 'https://filatrucks-default-rtdb.firebaseio.com/pedido/'

        # Delete the item from the database
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

