from zipfile import ZipFile
import tkinter as tk
from tkinter import Listbox, filedialog
import os
from tkinter.constants import ACTIVE, END


def separar_nomearquivo(caminho):
    '''Recebe um endereço e retorna o nome do arquivo e sua extensão'''
    # apenas o nome com a extensão
    nome_arquivo = os.path.basename(caminho)
    # separa o nome e a extensão em uma tupla
    return os.path.splitext(nome_arquivo)


def selectArq(ext, caminho=''):
    return filedialog.askopenfilename(filetypes=[('APP inventor', ext)], initialfile= caminho)


def arquivoExiste(caminho: str, nome: str, extensao: str, zipFile, /) -> bool:
    """
    -> Valida se um arquivo existe.
    :param nome: (obrigatorio) Nome completo do aquivo.
    :return: Verdadeiro ou falso para a existencia do arquivo.
    """
    with ZipFile(zipFile, mode='a') as myzip:
        try:
            myzip.open(caminho + '/' + nome + '.' + extensao, 'r')
        except:
            return False
        else:
            return True


def criarArquivo(caminho: str, nome: str, extensao: str, orig: str, zipFile: str, /) -> bool:
    """
    -> Cria um arquivo.
    :param nome: (obrigatorio) Nome completo do arquivo.
    :return: Não retorna valores.
    """
    try:
        src = caminho + '/' + orig + '.' + extensao
        dest = caminho + '/' + nome + '.' + extensao

        with ZipFile(zipFile, mode='r') as myzip:
            with myzip.open(src, 'r') as myfile:
                data = myfile.read().replace(str.encode(orig), str.encode(nome))

        with ZipFile(zipFile, mode='a') as myzip:
            with myzip.open(dest, 'w') as myfile:
                myfile.write(data)
    except:
        print('Houve um ERRO na criação do arquivo!')
    else:
        print(f'Arquivo {nome + "." + extensao} criado com sucessso!')


def copyArq(escolha, zipFile):
    caminho = os.path.dirname(escolha)
    with ZipFile(zipFile) as myzip:
        arqs = [file for file in myzip.namelist() if escolha.split('.')[0] in file]

    nomes = txt_arq.get('1.0', 'end-1c').split('\n')

    for nome in nomes:
        qtdArq = 1
        if ':' in nome:
            nome, qtdArq = nome.replace(' ', '').split(':')
            nome += ' '
            qtdArq = int(qtdArq)
        for i in range(1, qtdArq + 1):
            if qtdArq > 1:
                if i == 10 or i == 100 or i == 1000:
                    nome += ' '
                nome = nome[0:-len(str(i))] + str(i)
            for a in arqs:
                orig = a.split('/')[-1].split('.')[0]
                extencao = a.split('.')[1]
                if not arquivoExiste(caminho, nome, extencao, zipFile):
                    criarArquivo(caminho, nome, extencao, orig, zipFile)
                else:
                    print(f'Arquivo {nome + "." + extencao} não foi criado, pois já existe!')
    aiaFile = zipFile.replace('.zip', '.aia')
    os.rename(zipFile, aiaFile)


def listaArq(escolha, zipFile):
    def opc():
        arquivo_escolhido = lista.get(ACTIVE)
        escolha_arq.destroy()
        copyArq(arquivo_escolhido, zipFile)


    escolha_arq = tk.Tk()
    escolha_arq.title('Paginas APP INVENTOR 2')
    escolha_arq.geometry("500x350")
    escolha_arq.resizable(width=0, height=0)
    lista = Listbox(escolha_arq, font="Corbel 14")
    lista.place(width=500, height=250)
    btn_exc = tk.Button(escolha_arq, text= 'Criar Paginas', 
                        font='Corbel 18',
                        background='#fff',
                        foreground='#212121',
                        command=opc)
    btn_exc.place(relx=.3, 
                    rely=0.8, 
                    width=200, 
                    height=50)
    for file in escolha:
        lista.insert(END, file)


def createPage():
    if txt_arq.get('1.0', 'end-1c'):
        try:
            dirFile = selectArq('.aia')
            zipFile = dirFile.replace('.aia', '.zip')
            os.rename(dirFile, zipFile)
            with ZipFile(zipFile) as myzip:
                escolha = [file for file in myzip.namelist() if '.scm' in file]
                listaArq(escolha, zipFile)
        except:
            print('Cancelado...')
            dirFile = selectArq('.zip')
            zipFile = dirFile.replace('.zip', '.aia')
    else:
        print('Sem nomes de páginas...')


def template():
    try:
        for lin in redArq(selectArq('.txt')):
            if lin.strip():
                txt_arq.insert(END, lin)
    except:
        print('cancelado...')


def redArq(file):
    for lin in open(file, 'rt'):
        yield lin





root = tk.Tk()
root.title('paginas APP INVENTOR 2')
root.geometry("300x500")
root.resizable(width=0, height=0)

txt_arq = tk.Text(root, font="Corbel 18", height=14, width=23)

btn_nome = tk.Button(root,
                    text='Template',
                    command=template,
                    font='Corbel 18',
                    background='#fff',
                    foreground='#212121'
                    )

btn_exe = tk.Button(root,
                    text='Executar',
                    command=createPage,
                    font='Corbel 18',
                    background='#fff',
                    foreground='#212121'
                    )

txt_arq.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
btn_nome.grid(row=1, column=0, padx=10, pady=10)
btn_exe.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
