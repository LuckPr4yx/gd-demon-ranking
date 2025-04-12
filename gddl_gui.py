import os
import json
import time
import threading
import locale
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import webbrowser
import requests
from pathlib import Path

# Detecta idioma salvo pelo instalador
idioma = "en"
try:
    with open("lang.txt", "r", encoding="utf-8") as f:
        idioma = f.read().strip()
except:
    idioma = locale.getdefaultlocale()[0][:2]

# Traduções multilíngues
traducoes = {
    'pt': {
        'titulo': 'GD DEMONS RANKING',
        'selecionar_arquivo': 'Selecionar Arquivo JSON',
        'caminho_arquivo': 'Caminho do Arquivo:',
        'botao_carregar': 'Carregar e Classificar',
        'botao_salvar': 'Salvar Ranking (.txt)',
        'botao_abrir_pasta': 'Abrir Pasta',
        'botao_instrucoes': 'Ver Instruções',
        'juntas_ou_separadas': 'Deseja ver as instruções passo a passo?',
        'juntas': 'Todas Juntas',
        'separadas': 'Passo a Passo',
        'confirmar_abrir_site': 'Abrir site agora?',
        'salvar_como_txt': 'Deseja salvar como .txt?',
        'salvar_como_csv': 'Deseja salvar como .csv?',
        'cabecalho': 'SOMENTE PARA CLASSIC DEMONS',
        'tempo_dependente': 'O tempo irá depender de quantos demons você passou.',
        'tempo_decorrido': 'Tempo decorrido:',
        'tempo_estimado': 'Tempo estimado restante:',
        'colunas': ['Nome', 'Criador', 'Dificuldade', 'Rating', 'Enjoyment'],
        'coluna_classificacao': 'Classificação',
        'salvo_em': 'Ranking salvo em:',
        'erro_json': 'Erro ao ler o arquivo JSON.',
        'erro_sem_demons': 'Nenhum demon clássico vencido encontrado.',
        'instrucoes': [
            '1º Aperte "Win + R" no teclado',
            '2º Digite "appdata" (sem as aspas)',
            '3º Abra a pasta "Local"',
            '4º Procure e abra a pasta "Geometry Dash"',
            '5º Selecione os arquivos "CCGameManager.dat" e "CCLocalLevels.dat"',
            '6º Clique nesse link para abrir o site: https://gdcolon.com/gdsave/',
            '7º Arraste os arquivos selecionados para o site',
            '8º Baixe o "Level Stats (.json)" na aba "Download"',
            '9º No aplicativo, clique em "Selecionar Arquivo JSON" e abra o arquivo',
            '10º Aperte em "Carregar e Classificar"',
            '11º Agora é só esperar!'
        ]
    },
    'en': {
        'titulo': 'GD DEMONS RANKING',
        'selecionar_arquivo': 'Select JSON File',
        'caminho_arquivo': 'File Path:',
        'botao_carregar': 'Load and Rank',
        'botao_salvar': 'Save Ranking (.txt)',
        'botao_abrir_pasta': 'Open Folder',
        'botao_instrucoes': 'View Instructions',
        'juntas_ou_separadas': 'Do you want to view the instructions step-by-step?',
        'juntas': 'All Together',
        'separadas': 'Step by Step',
        'confirmar_abrir_site': 'Open site now?',
        'salvar_como_txt': 'Do you want to save as .txt?',
        'salvar_como_csv': 'Do you want to save as .csv?',
        'cabecalho': 'ONLY FOR CLASSIC DEMONS',
        'tempo_dependente': 'Time will depend on how many demons you have beaten.',
        'tempo_decorrido': 'Elapsed time:',
        'tempo_estimado': 'Estimated time left:',
        'colunas': ['Name', 'Creator', 'Difficulty', 'Rating', 'Enjoyment'],
        'coluna_classificacao': 'Ranking',
        'salvo_em': 'Ranking saved at:',
        'erro_json': 'Error reading JSON file.',
        'erro_sem_demons': 'No beaten classic demons found.',
        'instrucoes': [
            '1st Press "Win + R" on your keyboard',
            '2nd Type "appdata" (without quotes)',
            '3rd Open the "Local" folder',
            '4th Open the "Geometry Dash" folder',
            '5th Select "CCGameManager.dat" and "CCLocalLevels.dat"',
            '6th Go to https://gdcolon.com/gdsave/',
            '7th Drag the files into the site',
            '8th Download "Level Stats (.json)" from "Download" tab',
            '9th Select the JSON file in the app',
            '10th Click "Load and Rank"',
            '11th Now just wait!'
        ]
    },
    'es': {
        'titulo': 'GD DEMONS RANKING',
        'selecionar_arquivo': 'Seleccionar Archivo JSON',
        'caminho_arquivo': 'Ruta del Archivo:',
        'botao_carregar': 'Cargar y Clasificar',
        'botao_salvar': 'Guardar Ranking (.txt)',
        'botao_abrir_pasta': 'Abrir Carpeta',
        'botao_instrucoes': 'Ver Instrucciones',
        'juntas_ou_separadas': '¿Deseas ver las instrucciones paso a paso?',
        'juntas': 'Todas Juntas',
        'separadas': 'Paso a Paso',
        'confirmar_abrir_site': '¿Abrir sitio ahora?',
        'salvar_como_txt': '¿Deseas guardar como .txt?',
        'salvar_como_csv': '¿Deseas guardar como .csv?',
        'cabecalho': 'SOLO PARA CLASSIC DEMONS',
        'tempo_dependente': 'El tiempo dependerá de cuántos demons has pasado.',
        'tempo_decorrido': 'Tiempo transcurrido:',
        'tempo_estimado': 'Tiempo estimado restante:',
        'colunas': ['Nombre', 'Creador', 'Dificultad', 'Rating', 'Disfrute'],
        'coluna_classificacao': 'Clasificación',
        'salvo_em': 'Ranking guardado en:',
        'erro_json': 'Error al leer el archivo JSON.',
        'erro_sem_demons': 'No se encontraron demons clásicos completados.',
        'instrucoes': [
            '1º Presiona "Win + R" en tu teclado',
            '2º Escribe "appdata" (sin comillas)',
            '3º Abre la carpeta "Local"',
            '4º Abre la carpeta "Geometry Dash"',
            '5º Selecciona "CCGameManager.dat" y "CCLocalLevels.dat"',
            '6º Ve a https://gdcolon.com/gdsave/',
            '7º Arrastra los archivos al sitio',
            '8º Descarga "Level Stats (.json)" desde "Download"',
            '9º Selecciona el JSON en la app',
            '10º Haz clic en "Cargar y Clasificar"',
            '¡11º ¡Ahora espera!'
        ]
    },
    'ru': {
        'titulo': 'GD DEMONS RANKING',
        'selecionar_arquivo': 'Выбрать JSON файл',
        'caminho_arquivo': 'Путь к файлу:',
        'botao_carregar': 'Загрузить и оценить',
        'botao_salvar': 'Сохранить рейтинг (.txt)',
        'botao_abrir_pasta': 'Открыть папку',
        'botao_instrucoes': 'Показать инструкции',
        'juntas_ou_separadas': 'Хотите увидеть пошаговые инструкции?',
        'juntas': 'Все вместе',
        'separadas': 'Пошагово',
        'confirmar_abrir_site': 'Открыть сайт сейчас?',
        'salvar_como_txt': 'Сохранить как .txt?',
        'salvar_como_csv': 'Сохранить как .csv?',
        'cabecalho': 'ТОЛЬКО для CLASSIC DEMONS',
        'tempo_dependente': 'Время зависит от кол-ва пройденных.',
        'tempo_decorrido': 'Прошедшее время:',
        'tempo_estimado': 'Оставшееся время:',
        'colunas': ['Название', 'Автор', 'Сложность', 'Рейтинг', 'Удовольствие'],
        'coluna_classificacao': 'Классификация',
        'salvo_em': 'Сохранёно в:',
        'erro_json': 'Ошибка чтения JSON-файла.',
        'erro_sem_demons': 'Классические демоны не найдены.',
        'instrucoes': [
            '1. Нажмите "Win + R"',
            '2. Введите "appdata"',
            '3. Откройте папку "Local"',
            '4. Перейдите в "Geometry Dash"',
            '5. Выберите "CCGameManager.dat" и "CCLocalLevels.dat"',
            '6. Откройте https://gdcolon.com/gdsave/',
            '7. Перетащите файлы на сайт',
            '8. Скачайте "Level Stats (.json)"',
            '9. Выберите файл в приложении',
            '10. Нажмите "Загрузить и ранжировать"',
            '11. Подождите...'
        ]
    }
}

# Aplica idioma selecionado
if idioma not in traducoes:
    idioma = 'en'
t = traducoes[idioma]
class DemonRankingApp:
    def __init__(self, root):
        self.root = root
        self.arquivo_json = None
        self.root.title(t['titulo'])
        self.root.configure(bg="#121212")
        self.root.geometry("1000x650")
        self.root.minsize(800, 500)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1e1e1e",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#1e1e1e",
                        font=('Segoe UI', 11))
        style.configure("Treeview.Heading",
                        font=('Segoe UI Semibold', 12),
                        background="#2a2a2a",
                        foreground="white")
        style.map("Treeview", background=[("selected", "#2e7d32")])
        style.configure("green.Horizontal.TProgressbar",
                        foreground="#2e7d32",
                        background="#2e7d32")

        self.label_cabecalho = tk.Label(root, text=t['cabecalho'], font=("Segoe UI", 14, "bold"),
                                        bg="#121212", fg="white")
        self.label_cabecalho.pack(pady=(10, 0))

        self.label_aviso = tk.Label(root, text=t['tempo_dependente'], font=("Segoe UI", 10),
                                    bg="#121212", fg="#BBBBBB")
        self.label_aviso.pack(pady=(2, 8))

        self.frame_botoes = tk.Frame(root, bg="#121212")
        self.frame_botoes.pack(pady=10)

        self.frame_superior = tk.Frame(self.frame_botoes, bg="#121212")
        self.frame_superior.pack()

        self.btn_arquivo = tk.Button(self.frame_superior, text=t['selecionar_arquivo'],
                                     command=self.abrir_arquivo,
                                     font=("Segoe UI", 11), bg="#1e1e1e", fg="white",
                                     activebackground="#2e7d32", activeforeground="white")
        self.btn_arquivo.pack(side="left", padx=8)

        self.btn_carregar = tk.Button(self.frame_superior, text=t['botao_carregar'],
                                      command=self.iniciar_thread,
                                      font=("Segoe UI", 11), bg="#1e1e1e", fg="white",
                                      activebackground="#2e7d32", activeforeground="white")
        self.btn_carregar.pack(side="left", padx=8)

        self.frame_inferior = tk.Frame(self.frame_botoes, bg="#121212")
        self.frame_inferior.pack(pady=(8, 0))

        self.btn_instrucoes = tk.Button(self.frame_inferior, text=t['botao_instrucoes'],
                                        command=self.ver_instrucoes,
                                        font=("Segoe UI", 11), bg="#1e1e1e", fg="white",
                                        activebackground="#2e7d32", activeforeground="white")
        self.btn_instrucoes.pack(side="left", padx=8)

        self.btn_salvar = tk.Button(self.frame_inferior, text=t['botao_salvar'],
                                    command=self.salvar_txt,
                                    font=("Segoe UI", 11), bg="#1e1e1e", fg="white",
                                    activebackground="#2e7d32", activeforeground="white")
        self.btn_salvar.pack(side="left", padx=8)

        self.btn_pasta = tk.Button(self.frame_inferior, text=t['botao_abrir_pasta'],
                                   command=self.abrir_pasta,
                                   font=("Segoe UI", 11), bg="#1e1e1e", fg="white",
                                   activebackground="#2e7d32", activeforeground="white")
        self.btn_pasta.pack(side="left", padx=8)

        self.label_caminho = tk.Label(self.root, text=f"{t['caminho_arquivo']} ", font=("Segoe UI", 10),
                                      bg="#121212", fg="#AAAAAA", anchor="w")
        self.label_caminho.pack(fill="x", padx=20)

        self.frame_tabela = tk.Frame(self.root, bg="#121212")
        self.frame_tabela.pack(fill="both", expand=True, padx=20, pady=(5, 5))

        colunas_com_enum = [t['coluna_classificacao']] + t['colunas']
        self.tabela = ttk.Treeview(self.frame_tabela, columns=colunas_com_enum, show="headings")

        for col in colunas_com_enum:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, anchor="center", width=100, stretch=True)

        self.tabela.pack(fill="both", expand=True)

        self.progress = ttk.Progressbar(self.root, mode="determinate", maximum=100,
                                        style="green.Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=20)

        self.label_tempo = tk.Label(self.root, text="", font=("Segoe UI", 10),
                                    bg="#121212", fg="#CCCCCC")
        self.label_tempo.pack(pady=(2, 10))
    def ver_instrucoes(self):
        sim = {"pt": "Sim", "en": "Yes", "es": "Sí", "ru": "Да"}.get(idioma, "Yes")
        nao = {"pt": "Não", "en": "No", "es": "No", "ru": "Нет"}.get(idioma, "No")
        abrir_site_msg = {
            'pt': "Abrir site agora?",
            'en': "Open site now?",
            'es': "¿Abrir sitio ahora?",
            'ru': "Открыть сайт сейчас?"
        }.get(idioma, "Open site now?")

        escolha = messagebox.askyesno(t['botao_instrucoes'], t['juntas_ou_separadas'])

        if escolha:
            for instrucao in t['instrucoes']:
                messagebox.showinfo(t['botao_instrucoes'], instrucao)
                if "https://gdcolon.com/gdsave/" in instrucao:
                    abrir = messagebox.askyesno(t['botao_instrucoes'], abrir_site_msg)
                    if abrir:
                        webbrowser.open("https://gdcolon.com/gdsave/")
        else:
            texto = "\n".join(t['instrucoes'])
            abrir_site = messagebox.askyesno(t['botao_instrucoes'], f"{texto}\n\n{abrir_site_msg}")
            if abrir_site:
                webbrowser.open("https://gdcolon.com/gdsave/")

    def abrir_arquivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.arquivo_json = file_path
            self.label_caminho.config(text=f"{t['caminho_arquivo']} {file_path}")

    def iniciar_thread(self):
        thread = threading.Thread(target=self.load_and_rank)
        thread.daemon = True
        thread.start()

    def load_and_rank(self):
        self.progress["value"] = 0
        self.label_tempo.config(text="")
        self.tabela.delete(*self.tabela.get_children())

        try:
            start_time = time.time()
            with open(self.arquivo_json, "r", encoding="utf-8") as f:
                data = json.load(f)

            demons = [lvl for lvl in data if lvl.get("demon", False) and lvl.get("percentage", 0) == 100]
            total = len(demons)
            if total == 0:
                messagebox.showerror(t['titulo'], "Nenhum demon clássico vencido encontrado.")
                return

            OFFICIAL_IDS = {14: 1, 18: 2, 20: 3}
            resultados = []

            for i, demon in enumerate(demons):
                lvl_id = OFFICIAL_IDS.get(demon["id"], demon["id"])
                try:
                    response = requests.get(f"https://gdladder.com/api/level/{lvl_id}", timeout=5)
                    if response.status_code == 200:
                        api_data = response.json()
                        resultados.append({
                            "Name": api_data["Meta"]["Name"],
                            "Creator": api_data["Meta"]["Creator"],
                            "Difficulty": api_data["Meta"]["Difficulty"],
                            "Rating": api_data.get("Rating", 0),
                            "Enjoyment": api_data.get("Enjoyment", 0)
                        })
                except:
                    continue

                self.progress["value"] = (i + 1) / total * 100
                elapsed = time.time() - start_time
                eta = (elapsed / (i + 1)) * (total - (i + 1))
                self.label_tempo.config(text=f"{t['tempo_decorrido']} {int(elapsed)}s    {t['tempo_estimado']} {int(eta)}s")
                self.root.update_idletasks()

            resultados.sort(key=lambda x: x['Rating'] if x['Rating'] is not None else -1, reverse=True)
            self.resultados = resultados

            for idx, item in enumerate(resultados, 1):
                self.tabela.insert("", "end", values=(idx, item["Name"], item["Creator"],
                                                      item["Difficulty"], item["Rating"], item["Enjoyment"]))
        except Exception as e:
            messagebox.showerror(t['titulo'], f"{t['erro_json']}\n{str(e)}")
    def salvar_txt(self):
        if not hasattr(self, 'resultados') or not self.resultados:
            return

        salvar_txt_msg = {
            'pt': "Deseja salvar como .txt?",
            'en': "Do you want to save as .txt?",
            'es': "¿Deseas guardar como .txt?",
            'ru': "Сохранить как .txt?"
        }.get(idioma, "Do you want to save as .txt?")

        salvar_csv_msg = {
            'pt': "Deseja salvar como .csv?",
            'en': "Do you want to save as .csv?",
            'es': "¿Deseas guardar como .csv?",
            'ru': "Сохранить как .csv?"
        }.get(idioma, "Do you want to save as .csv?")

        salvar_txt = messagebox.askyesno(t['titulo'], salvar_txt_msg)
        salvar_csv = messagebox.askyesno(t['titulo'], salvar_csv_msg)

        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        caminho_txt = os.path.join(downloads_path, "demon_ranking.txt")
        caminho_csv = os.path.join(downloads_path, "demon_ranking.csv")

        if salvar_txt:
            with open(caminho_txt, "w", encoding="utf-8") as f:
                for idx, item in enumerate(self.resultados, 1):
                    linha = f"{idx}. {item['Name']} - {item['Creator']} - {item['Difficulty']} - Rating: {item['Rating']} - Enjoyment: {item['Enjoyment']}"
                    f.write(linha + "\n")
            messagebox.showinfo(t['titulo'], f"{t['salvo_em']} {caminho_txt}")

        if salvar_csv:
            with open(caminho_csv, "w", encoding="utf-8") as f:
                f.write(f"{t['coluna_classificacao']},Name,Creator,Difficulty,Rating,Enjoyment\n")
                for idx, item in enumerate(self.resultados, 1):
                    linha = f"{idx},{item['Name']},{item['Creator']},{item['Difficulty']},{item['Rating']},{item['Enjoyment']}"
                    f.write(linha + "\n")
            messagebox.showinfo(t['titulo'], f"{t['salvo_em']} {caminho_csv}")

    def abrir_pasta(self):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        try:
            if os.name == "nt":
                os.startfile(downloads_path)
            elif os.name == "posix":
                os.system(f'xdg-open "{downloads_path}"')
            elif os.name == "mac":
                os.system(f'open "{downloads_path}"')
        except Exception as e:
            messagebox.showerror(t['titulo'], str(e))
if __name__ == "__main__":
    root = tk.Tk()
    app = DemonRankingApp(root)
    root.mainloop()
