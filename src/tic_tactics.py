import flet as ft
import random
import json
import os
import sys
import time


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# ------------------------------------------------

class LocalizationManager:
    def __init__(self, default_lang='pt_br'):
        self.file = resource_path(os.path.join("data", "strings.json"))
        self.default_lang = default_lang
        self.current_lang = default_lang
        self.strings = self.load_strings()

    def load_strings(self):
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar idioma: {e}")
            return {}

    def get_string(self, key):
        return self.strings.get(self.current_lang, {}).get(key, key)

    def set_language(self, lang_code, page, update_callback):
        self.current_lang = lang_code
        update_callback()
        page.update()

loc_manager = LocalizationManager()
def _(key):
    return loc_manager.get_string(key)

class StatsManager:
    def __init__(self):
        self.arquivo_stats = resource_path(os.path.join("data", "stats.json"))
        self.stats = self.carregar_stats()
    def carregar_stats(self):
        if not os.path.exists(self.arquivo_stats): return self._get_default_stats()
        try:
            with open(self.arquivo_stats, 'r', encoding='utf-8') as f: return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError): return self._get_default_stats()
    def salvar_stats(self):
        with open(self.arquivo_stats, 'w', encoding='utf-8') as f: json.dump(self.stats, f, indent=4, ensure_ascii=False)
    def _get_default_stats(self):
        return {"geral": {"vitorias": 0, "derrotas": 0, "empates": 0, "maior_sequencia_vitorias": 0, "sequencia_atual": 0},"vs_jogador": {"vitorias": 0, "derrotas": 0, "empates": 0},"vs_facil": {"vitorias": 0, "derrotas": 0, "empates": 0},"vs_dificil": {"vitorias": 0, "derrotas": 0, "empates": 0}}
    
    def resetar_stats(self):
        self.stats = self._get_default_stats()
        self.salvar_stats()

    def registrar_partida(self, vencedor, modo_jogo):
        if vencedor == "X":
            self.stats["geral"]["vitorias"] += 1; self.stats[modo_jogo]["vitorias"] += 1
            self.stats["geral"]["sequencia_atual"] += 1
            if self.stats["geral"]["sequencia_atual"] > self.stats["geral"]["maior_sequencia_vitorias"]: self.stats["geral"]["maior_sequencia_vitorias"] = self.stats["geral"]["sequencia_atual"]
        elif vencedor == "O":
            self.stats["geral"]["derrotas"] += 1; self.stats[modo_jogo]["derrotas"] += 1; self.stats["geral"]["sequencia_atual"] = 0
        elif vencedor == "Empate":
            self.stats["geral"]["empates"] += 1; self.stats[modo_jogo]["empates"] += 1; self.stats["geral"]["sequencia_atual"] = 0
        self.salvar_stats()
    def get_taxa_vitoria(self):
        total_jogos = self.stats["geral"]["vitorias"] + self.stats["geral"]["derrotas"]
        if total_jogos == 0: return "0.00%"
        return f"{(self.stats['geral']['vitorias'] / total_jogos) * 100:.2f}%"

class ConquistaManager:
    def __init__(self, page):
        self.page = page
        self.arquivo_conquistas = resource_path(os.path.join("data", "conquistas.json"))
        self.conquistas = self.carregar_conquistas()
        self.contadores = {"empates_seguidos": 0, "vitorias_dificil_seguidas": 0}
    def carregar_conquistas(self):
        if not os.path.exists(self.arquivo_conquistas): 
            return {"primeiro_passo":{"nome":"Primeiro Passo","descricao":"Jogue sua primeira partida.","desbloqueada":False},"primeira_vitoria":{"nome":"Primeira Vitória","descricao":"Vença sua primeira partida.","desbloqueada":False},"primeiro_empate":{"nome":"Primeiro Empate","descricao":"Empate uma partida pela primeira vez.","desbloqueada":False},"mestre_do_bot":{"nome":"Mestre do Bot","descricao":"Vença 5x seguidas contra o bot no Difícil.","desbloqueada":False},"invencivel":{"nome":"Invencível","descricao":"Vença 3 partidas seguidas (qualquer modo).","desbloqueada":False},"estrategista":{"nome":"Estrategista","descricao":"Vença uma partida ocupando o centro.","desbloqueada":False},"rei_dos_cantos":{"nome":"Rei dos Cantos","descricao":"Vença uma partida ocupando uma das quinas.","desbloqueada":False},"sequencia_de_empates":{"nome":"Sequência de Empates","descricao":"Empate 3 vezes seguidas.","desbloqueada":False},"vitoria_relampago":{"nome":"Vitória Relâmpago","descricao":"Vença em 3 jogadas (5 movimentos totais).","desbloqueada":False}}
        try:
            with open(self.arquivo_conquistas,'r',encoding='utf-8') as f: return json.load(f)
        except(json.JSONDecodeError,FileNotFoundError):
            if os.path.exists(self.arquivo_conquistas): os.remove(self.arquivo_conquistas)
            return self.carregar_conquistas()
    def salvar_conquistas(self):
        with open(self.arquivo_conquistas,'w',encoding='utf-8') as f: json.dump(self.conquistas,f,indent=4,ensure_ascii=False)
    def desbloquear(self,chave):
        if chave in self.conquistas and not self.conquistas[chave]["desbloqueada"]:
            self.conquistas[chave]["desbloqueada"]=True; self.mostrar_popup(chave); self.salvar_conquistas()
    def mostrar_popup(self, chave_conquista):
        nome_traduzido = _(f'ach_win_title_{chave_conquista}') if _(f'ach_win_title_{chave_conquista}') != f'ach_win_title_{chave_conquista}' else chave_conquista
        try:
            self.page.snack_bar.content = ft.Row([ft.Icon("emoji_events",color="amber"),ft.Text(f"Conquista: {nome_traduzido}!",weight=ft.FontWeight.BOLD)])
            self.page.snack_bar.bgcolor = "#000000e6"
            self.page.snack_bar.duration = 3000
            self.page.snack_bar.open = True
            self.page.update()
        except Exception:
            pass
    def resetar_contadores_vitoria(self): self.contadores["vitorias_dificil_seguidas"]=0
    def resetar_contadores_empate(self): self.contadores["empates_seguidos"]=0

def verificar_vencedor(tab):
    linhas=[((i,0),(i,1),(i,2))for i in range(3)]; colunas=[((0,i),(1,i),(2,i))for i in range(3)]; diagonais=[((0,0),(1,1),(2,2)),((0,2),(1,1),(2,0))]
    for linha in linhas+colunas+diagonais:
        (r1,c1),(r2,c2),(r3,c3)=linha
        if tab[r1][c1]==tab[r2][c2]==tab[r3][c3]!="" and tab[r1][c1] != "B": return tab[r1][c1],linha
    return None, None
def minimax(tab,maximizando):
    vencedor, _ = verificar_vencedor(tab)
    if vencedor:return 1 if vencedor=="O" else -1
    if all(tab[r][c]!=""for r in range(3)for c in range(3)):return 0
    melhor=-float("inf")if maximizando else float("inf")
    for r in range(3):
        for c in range(3):
            if tab[r][c]=="":
                tab[r][c]="O"if maximizando else"X"; pont=minimax(tab,not maximizando); tab[r][c]=""
                if maximizando:melhor=max(melhor,pont)
                else:melhor=min(melhor,pont)
    return melhor
def minimax_melhor_jogada(tab):
    melhor_pontuacao=-float("inf"); melhor_movimento=None; vazias=[]
    for r in range(3):
        for c in range(3):
            if tab[r][c]=="":
                vazias.append((r,c)); tab[r][c]="O"; pontuacao=minimax(tab,False); tab[r][c]=""
                if pontuacao>melhor_pontuacao:melhor_pontuacao=pontuacao; melhor_movimento=(r,c)
    return melhor_movimento if melhor_movimento is not None else random.choice(vazias)

class TicTacToeGame:
    def __init__(self, page, conquistas_manager, stats_manager):
        self.page = page
        self.conquistas = conquistas_manager
        self.stats = stats_manager
        self.ui = {}
        self.tabuleiro_logico = [["" for _ in range(3)] for _ in range(3)]
        self.jogador_atual = "X"
        self.jogo_ativo = True
        self.bot_enabled = False
        self.dificuldade = "Dificil"
        self.modo_jogo_atual = "vs_jogador"
        self.placar = {"X": 0, "O": 0, "vitorias_seguidas_X": 0}
        self.estilo_jogo = "Classico"
        self.movimentos_totais = 0 

    def vincular_controles_ui(self, ui_controls):
        self.ui = ui_controls
        for celula in self.ui["grid_cells"]:
            celula.on_click = self.jogada
        self.ui["botao_reset_placar"].on_click = self.resetar_placar
        self.ui["botao_jogar_vs_bot_facil"].on_click = lambda _: self.ui["configurar_e_avancar"](True, "Facil")
        self.ui["botao_jogar_vs_bot_dificil"].on_click = lambda _: self.ui["configurar_e_avancar"](True, "Dificil")
        self.ui["botao_jogar_vs_jogador"].on_click = lambda _: self.ui["configurar_e_avancar"](False)
        self.ui["dialogo_fim_de_jogo_novamente"].on_click = self.on_fim_de_jogo_result
        self.ui["dialogo_fim_de_jogo_menu"].on_click = self.on_fim_de_jogo_result

    def start(self, vs_bot, dificuldade="Dificil", estilo_jogo="Classico"):
        self.bot_enabled=vs_bot; self.dificuldade=dificuldade
        self.estilo_jogo = estilo_jogo
        
        if not vs_bot: self.modo_jogo_atual = "vs_jogador"
        else: self.modo_jogo_atual = "vs_facil" if dificuldade == "Facil" else "vs_dificil"
        
        self.conquistas.desbloquear("primeiro_passo")
        self.reiniciar()
        
        if self.estilo_jogo == "Minado":
            self.colocar_minas()

        self.ui["mostrar_tela"]("game")

    def reiniciar(self):
        self.tabuleiro_logico=[[""for _ in range(3)]for _ in range(3)]; self.jogador_atual="X"; self.jogo_ativo=True
        self.movimentos_totais = 0 
        for celula in self.ui["grid_cells"]:
            celula.content.name = "circle"
            celula.content.color = "transparent"
        self.ui["texto_status"].value=f"{_('game_turn')} {self.jogador_atual}"
        self.ui["texto_placar"].value=f"{_('game_score_label')} X {self.placar['X']} - {self.placar['O']} O"; self.page.update()

    def colocar_minas(self):
        celulas_vazias_indices = [i for i in range(9)]
        num_minas = random.randint(1, 2)
        minas_indices = random.sample(celulas_vazias_indices, num_minas)

        for index in minas_indices:
            celula = self.ui["grid_cells"][index]
            r, c = celula.data
            self.tabuleiro_logico[r][c] = "B"
            celula.content.name = "block"
            celula.content.color = "grey" 
        self.page.update()

    def finalizar(self,vencedor,linha_vitoria):
        self.jogo_ativo = False
        vencedor_original = vencedor
        
        texto_resultado = f"{_('word_player')} '{vencedor_original}' {_('game_win')}"

        if self.estilo_jogo == "Invertido" and vencedor not in [None, "Empate"]:
            vencedor = "O" if vencedor == "X" else "X"
            texto_resultado = f"{_('word_player')} '{vencedor_original}' {_('game_lose_inverted')} '{vencedor}'!"
        
        self.stats.registrar_partida(vencedor, self.modo_jogo_atual)

        if vencedor_original == "Empate":
            self.ui["texto_status"].value = _('game_draw')
            vencedor_final_para_placar = "Empate"
        else:
            self.ui["texto_status"].value = texto_resultado
            self.placar[vencedor] += 1
            vencedor_final_para_placar = vencedor
            if linha_vitoria:
                for r,c in linha_vitoria:
                    celula_index = r * 3 + c
                    if 0 <= celula_index < len(self.ui["grid_cells"]):
                        self.ui["grid_cells"][celula_index].content.color = "#66BB6A" 

        self._verificar_conquistas_fim_de_jogo(vencedor_final_para_placar, linha_vitoria)
        self.ui["texto_placar"].value=f"{_('game_score_label')} X {self.placar['X']} - {self.placar['O']} O"
        self.ui["fim_de_jogo_dialog"].title.value = _('dialog_end_title')
        self.page.dialog=self.ui["fim_de_jogo_dialog"];self.page.dialog.open=True;self.page.update()

    def _verificar_conquistas_fim_de_jogo(self, vencedor_final, linha_vitoria):
        
        if vencedor_final == "X":
            self.conquistas.desbloquear("primeira_vitoria")
            
            if self.tabuleiro_logico[1][1] == "X": self.conquistas.desbloquear("estrategista")

            cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
            if any(self.tabuleiro_logico[r][c] == "X" for r, c in cantos): self.conquistas.desbloquear("rei_dos_cantos")
            
            if self.movimentos_totais <= 5: self.conquistas.desbloquear("vitoria_relampago")

            if self.stats.stats["geral"]["sequencia_atual"] >= 3: self.conquistas.desbloquear("invencivel")

            if self.bot_enabled and self.dificuldade == "Dificil":
                self.conquistas.contadores["vitorias_dificil_seguidas"] += 1
                if self.conquistas.contadores["vitorias_dificil_seguidas"] >= 5: self.conquistas.desbloquear("mestre_do_bot")
            else:
                self.conquistas.resetar_contadores_vitoria()
            
            self.conquistas.resetar_contadores_empate() 
        
        elif vencedor_final == "O":
            self.conquistas.resetar_contadores_vitoria()
            self.conquistas.resetar_contadores_empate()

        elif vencedor_final == "Empate":
            self.conquistas.desbloquear("primeiro_empate")
            self.conquistas.contadores["empates_seguidos"] += 1
            if self.conquistas.contadores["empates_seguidos"] >= 3: self.conquistas.desbloquear("sequencia_de_empates")
            
            self.conquistas.resetar_contadores_vitoria() 

    def jogada_bot(self):
        self.page.splash = ft.Row([ft.ProgressRing(color="#18FFFF"), ft.Text(f"{_('game_turn')} O...")])
        self.page.update()
        time.sleep(1) 
        self.page.splash = None
        self.page.update()
        
        if self.dificuldade=="Facil":
            vazias=[(r,c)for r in range(3)for c in range(3)if self.tabuleiro_logico[r][c]==""]
            vazias = [(r, c) for r, c in vazias if self.tabuleiro_logico[r][c] != "B"]
            if not vazias: return
            bot_r,bot_c=random.choice(vazias)
        else:
            bot_r,bot_c=minimax_melhor_jogada(self.tabuleiro_logico)
        
        celula_alvo = self.ui["grid_cells"][bot_r * 3 + bot_c]
        
        evento_bot = ft.ControlEvent(
            target=celula_alvo, name="click", data=f"{bot_r},{bot_c}",
            control=celula_alvo, page=self.page
        )
        self.jogada(evento_bot)

    def jogada(self,e):
        if not self.jogo_ativo: return
        
        if isinstance(e.control.data, str):
            r_str, c_str = e.control.data.split(',')
            r, c = int(r_str), int(c_str)
        else: 
            r,c = e.control.data

        if self.tabuleiro_logico[r][c] != "": return 

        self.tabuleiro_logico[r][c]=self.jogador_atual
        self.movimentos_totais += 1 
        
        icone = "close" if self.jogador_atual == "X" else "circle_outlined"
        cor = "#FF1744" if self.jogador_atual == "X" else "#18FFFF" 
        e.control.content = ft.Icon(name=icone, color=cor, size=50)
        
        vencedor, linha = verificar_vencedor(self.tabuleiro_logico)
        if vencedor: self.finalizar(vencedor, linha); return
        if all(c!="" for r_ in self.tabuleiro_logico for c in r_): self.finalizar("Empate", None); return
        
        self.jogador_atual="O"if self.jogador_atual=="X"else"X"
        self.ui["texto_status"].value=f"{_('game_turn')} {self.jogador_atual}"; self.page.update()
        if self.bot_enabled and self.jogador_atual=="O"and self.jogo_ativo:self.jogada_bot()

    def resetar_placar(self, e):
        self.placar={"X":0,"O":0,"vitorias_seguidas_X":0}; self.reiniciar()
        try:
            self.page.snack_bar.content = ft.Text(_('snack_score_reset'))
            self.page.snack_bar.open = True
            self.page.update()
        except Exception:
            pass

    def on_fim_de_jogo_result(self, e):
        self.page.dialog.open = False
        self.page.update()
        if e.control.text == _('dialog_play_again'):
            self.start(self.bot_enabled, self.dificuldade, self.estilo_jogo)
        else:
            self.ui["mostrar_tela"]("menu")

def main(page: ft.Page):

    caminho_fonte = resource_path(os.path.join("assets", "pixel.ttf"))
    
    page.title= _('app_title') 
    page.window_width=420; page.window_height=650; page.window_resizable=False
    
    page.window_icon = "icone.png" 
    
    page.theme_mode=ft.ThemeMode.DARK
    page.snack_bar = ft.SnackBar(content=ft.Text(""))
    page.vertical_alignment=ft.MainAxisAlignment.CENTER; page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.padding=20
    
    page.fonts = {"Press Start 2P": caminho_fonte} 

    conquistas_manager = ConquistaManager(page)
    stats_manager = StatsManager()
    game = TicTacToeGame(page, conquistas_manager, stats_manager)
    partida_config = {}

    def atualizar_lista_conquistas(is_update_only=False):
        
        lista_conquistas.controls.clear()
        conquistas_manager.conquistas = conquistas_manager.carregar_conquistas()
        
        for key, dados in conquistas_manager.conquistas.items(): 
             nome_traduzido = _(f'ach_win_title_{key}') if _(f'ach_win_title_{key}') != f'ach_win_title_{key}' else dados["nome"]
             desc_traduzida = _(f'ach_win_desc_{key}') if _(f'ach_win_desc_{key}') != f'ach_win_desc_{key}' else dados["descricao"]
             
             lista_conquistas.controls.append(ft.ListTile(leading=ft.Icon("emoji_events" if dados["desbloqueada"] else "lock", color="amber" if dados["desbloqueada"] else "grey"), 
                                                          title=ft.Text(nome_traduzido,weight=ft.FontWeight.BOLD),
                                                          subtitle=ft.Text(desc_traduzida))) 
        page.update()

    def atualizar_tela_stats(is_update_only=False):
        stats = stats_manager.carregar_stats()
        stats_geral_vitorias.value = f"{_('stats_wins')} {stats['geral']['vitorias']}"
        stats_geral_derrotas.value = f"{_('stats_losses')} {stats['geral']['derrotas']}"
        stats_geral_empates.value = f"{_('stats_draws')} {stats['geral']['empates']}"
        stats_geral_taxa.value = f"{_('stats_win_rate')} {stats_manager.get_taxa_vitoria()}"
        stats_geral_sequencia.value = f"{_('stats_best_streak')} {stats['geral']['maior_sequencia_vitorias']}"
        
        modos = {"vs_jogador": _('modes_vs_player'), "vs_facil": _('modes_vs_easy'), "vs_dificil": _('modes_vs_hard')}
        stats_table.rows.clear()
        stats_table.columns = [
            ft.DataColumn(ft.Text(_('modes_title'))),
            ft.DataColumn(ft.Text(_('stats_col_v')), numeric=True),
            ft.DataColumn(ft.Text(_('stats_col_d')), numeric=True),
            ft.DataColumn(ft.Text(_('stats_col_e')), numeric=True),
        ]
        for key, nome in modos.items():
            stats_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(nome)),
                    ft.DataCell(ft.Text(str(stats[key]['vitorias']))),
                    ft.DataCell(ft.Text(str(stats[key]['derrotas']))),
                    ft.DataCell(ft.Text(str(stats[key]['empates']))),
                ])
            )
        page.update()

    def update_ui_strings():
        page.title = _('app_title')
        
        try:
            if len(menu_view.controls) > 0: menu_view.controls[0].value = _('menu_title')
            if len(menu_view.controls) > 2: menu_view.controls[2].text = _('menu_modes')
            if len(menu_view.controls) > 3: menu_view.controls[3].text = _('menu_stats')
            if len(menu_view.controls) > 4: menu_view.controls[4].text = _('menu_achievements')
            if len(menu_view.controls) > 5: menu_view.controls[5].text = _('menu_tutorial')
            if len(menu_view.controls) > 6: menu_view.controls[6].text = _('menu_options')

            if len(modos_view.controls) > 0: modos_view.controls[0].value = _('modes_title')
            if len(modos_view.controls) > 2: modos_view.controls[2].text = _('modes_vs_easy')
            if len(modos_view.controls) > 3: modos_view.controls[3].text = _('modes_vs_hard')
            if len(modos_view.controls) > 4: modos_view.controls[4].text = _('modes_vs_player')
            if len(modos_view.controls) > 6: modos_view.controls[6].text = _('button_back_menu')

            if len(selecao_estilo_view.controls) > 0: selecao_estilo_view.controls[0].value = _('style_title')
            if len(selecao_estilo_view.controls) > 2: selecao_estilo_view.controls[2].text = _('style_classic')
            if len(selecao_estilo_view.controls) > 3: selecao_estilo_view.controls[3].text = _('style_inverted')
            if len(selecao_estilo_view.controls) > 4: selecao_estilo_view.controls[4].text = _('style_mined')
            if len(selecao_estilo_view.controls) > 6: selecao_estilo_view.controls[6].text = _('button_back')

            if len(opcoes_view.controls) > 0: opcoes_view.controls[0].value = _('options_title')
            theme_button.text = _('options_theme')
            botao_reset_placar.text = _('options_reset_score')
            botao_reset_stats.text = _('options_reset_stats')
            if len(opcoes_view.controls) > 0: opcoes_view.controls[-1].text = _('button_back_menu')
            
            dialogo_reset_stats.title.value = _('dialog_reset_title')
            dialogo_reset_stats.content.value = _('dialog_reset_content')
            if len(dialogo_reset_stats.actions) > 1: dialogo_reset_stats.actions[-1].text = _('dialog_reset_confirm')
        except (IndexError, AttributeError) as ex:
            print(f"Aviso: Erro ao atualizar strings de UI: {ex}")
        
        texto_status.value = f"{_('game_turn')} {game.jogador_atual}"
        texto_placar.value = f"{_('game_score_label')} X {game.placar['X']} - {game.placar['O']} O"

        conquistas_view.controls[0].value = _('ach_title')
        stats_view.controls[0].value = _('stats_title')
        
        tutorial_view.controls[0].content.value = _('menu_tutorial')
        try:
            tutorial_pages[:] = rebuild_tutorial_pages()
            tutorial_content_area.content = tutorial_pages[0]
        except Exception:
            pass
        
        try:
            tutorial_navbar.controls[0].text = _('tut_general')
            tutorial_navbar.controls[1].text = _('tut_styles')
            tutorial_navbar.controls[2].text = _('tut_tips')
        except Exception:
            pass

        atualizar_lista_conquistas(is_update_only=True)
        atualizar_tela_stats(is_update_only=True)
        try:
            stats_view.controls[2].value = _('stats_details_by_mode')
        except Exception:
            try:
                stats_view.controls[2].text = _('stats_details_by_mode')
            except Exception:
                pass
        
        dropdown_lang.options[0].text = _('lang_name_pt')
        dropdown_lang.options[1].text = _('lang_name_en')
        dropdown_lang.options[2].text = _('lang_name_es')


        page.update()
        
    def configurar_e_avancar(vs_bot, dificuldade=None):
        partida_config["vs_bot"] = vs_bot
        if dificuldade:
            partida_config["dificuldade"] = dificuldade
        elif "dificuldade" in partida_config:
            del partida_config["dificuldade"]
        mostrar_tela("selecao_estilo")

    def criar_tabuleiro_gridview():
        celulas_clicaveis = []
        for i in range(3):
            for j in range(3):
                celulas_clicaveis.append(ft.Container(data=(i, j), border=ft.border.all(2, "outline"), border_radius=8, width=100, height=100, content=ft.Icon(name="circle", color="transparent", size=50), alignment=ft.alignment.center))
        tabuleiro_grid = ft.GridView(runs_count=3, max_extent=100, spacing=5, run_spacing=5, width=315, height=315, controls=celulas_clicaveis)
        return tabuleiro_grid, celulas_clicaveis

    def switch_language(e):
        if e.control.value:
            lang_code = e.control.value
            loc_manager.set_language(lang_code, page, update_ui_strings)
            dropdown_lang.value = lang_code
            page.update()

    def switch_tutorial_content_navbar(e):
        tutorial_content_area.content = tutorial_pages[e.control.selected_index]
        page.update()
        
    def iniciar_partida(estilo_jogo):
        game.start(vs_bot=partida_config.get("vs_bot", False), dificuldade=partida_config.get("dificuldade", "Dificil"), estilo_jogo=estilo_jogo)
        
    def mostrar_tela(nome_tela):
        for view in [menu_view, modos_view, selecao_estilo_view, game_view, opcoes_view, conquistas_view, stats_view, tutorial_view]:
            view.visible = (view.data == nome_tela)
        if nome_tela=="conquistas": atualizar_lista_conquistas()
        if nome_tela=="stats": atualizar_tela_stats()
        page.update()

    texto_status = ft.Text(f"{_('game_turn')} X", size=24, weight=ft.FontWeight.BOLD)
    texto_placar = ft.Text(f"{_('game_score_label')} X 0 - 0 O", size=18, color="grey")
    tabuleiro_visivel, grid_cells = criar_tabuleiro_gridview()
    
    botao_jogar_vs_bot_facil=ft.FilledButton(_('modes_vs_easy'),icon="smart_toy",width=280)
    botao_jogar_vs_bot_dificil=ft.FilledButton(_('modes_vs_hard'),icon="psychology",width=280)
    botao_jogar_vs_jogador=ft.FilledButton(_('modes_vs_player'),icon="people",width=280)
    
    botao_reset_placar=ft.FilledButton(_('options_reset_score'),icon="delete_sweep",width=280) 
    botao_reset_stats = ft.FilledButton(_('options_reset_stats'), icon="delete_forever", width=280, on_click=lambda e: (setattr(dialogo_reset_stats, 'open', True), page.update()))
    theme_button=ft.FilledButton(_('options_theme'),icon="light_mode",on_click=lambda e: (setattr(page, 'theme_mode', ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT), setattr(theme_button, 'icon', "dark_mode" if page.theme_mode == ft.ThemeMode.LIGHT else "light_mode"), page.update()),width=280) 
    
    dropdown_lang = ft.Dropdown(
        width=280,
        label=_('options_lang'),
        options=[
            ft.dropdown.Option("pt_br", _('lang_name_pt')),
            ft.dropdown.Option("en", _('lang_name_en')),
            ft.dropdown.Option("es", _('lang_name_es')),
        ],
        value=loc_manager.current_lang,
        on_change=switch_language,
    )
    
    dialogo_fim_de_jogo_novamente=ft.TextButton(_('dialog_play_again'))
    dialogo_fim_de_jogo_menu=ft.OutlinedButton(_('button_back_menu'))
    fim_de_jogo_dialog=ft.AlertDialog(modal=True,title=ft.Text(_('dialog_end_title'),text_align=ft.TextAlign.CENTER), actions=[dialogo_fim_de_jogo_novamente,dialogo_fim_de_jogo_menu], actions_alignment=ft.MainAxisAlignment.CENTER)

    def _on_reset_stats_confirm(e):
        stats_manager.resetar_stats()
        conquistas_manager.resetar_contadores_vitoria()
        try:
            page.snack_bar.content = ft.Text(_('snack_stats_reset'))
            page.snack_bar.open = True
        except Exception:
            pass
        dialogo_reset_stats.open = False
        page.update()

    dialogo_reset_stats=ft.AlertDialog(
        modal=True,
        title=ft.Text(_('dialog_reset_title')),
        content=ft.Text(_('dialog_reset_content')),
        actions=[
            ft.TextButton(_('button_back'), on_click=lambda e: (setattr(dialogo_reset_stats, 'open', False), page.update())),
            ft.TextButton(_('dialog_reset_confirm'), on_click=_on_reset_stats_confirm, style=ft.ButtonStyle(color="#F44336")), 
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    ui_controls={"mostrar_tela":mostrar_tela,"texto_status":texto_status,"texto_placar":texto_placar,"grid_cells":grid_cells,"fim_de_jogo_dialog":fim_de_jogo_dialog,"botao_reset_placar":botao_reset_placar,"botao_jogar_vs_bot_facil":botao_jogar_vs_bot_facil,"botao_jogar_vs_bot_dificil":botao_jogar_vs_bot_dificil,"botao_jogar_vs_jogador":botao_jogar_vs_jogador,"dialogo_fim_de_jogo_novamente":dialogo_fim_de_jogo_novamente,"dialogo_fim_de_jogo_menu":dialogo_fim_de_jogo_menu, "configurar_e_avancar": configurar_e_avancar}
    game.vincular_controles_ui(ui_controls)
    
    def _on_tutorial_nav_click(index):
        try:
            if 0 <= index < len(tutorial_pages):
                tutorial_content_area.content = tutorial_pages[index]
                page.update()
        except (IndexError, AttributeError) as ex:
            print(f"Erro ao navegar no tutorial: {ex}")

    tutorial_navbar = ft.Row(
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.OutlinedButton(_('tut_general'), on_click=lambda e, i=0: _on_tutorial_nav_click(i)),
            ft.OutlinedButton(_('tut_styles'), on_click=lambda e, i=1: _on_tutorial_nav_click(i)),
            ft.OutlinedButton(_('tut_tips'), on_click=lambda e, i=2: _on_tutorial_nav_click(i)),
        ]
    )
    
    def rebuild_tutorial_pages():
        return [
            ft.ListView(spacing=10, controls=[
                ft.Card(content=ft.ListTile(leading=ft.Icon("sports_esports", color="#66BB6A"), title=ft.Text(_('menu_modes')), subtitle=ft.Text(_('tut_intro_sub1')))),
                ft.Card(content=ft.ListTile(leading=ft.Icon("query_stats", color="#00BCD4"), title=ft.Text(_('menu_stats')), subtitle=ft.Text(_('tut_intro_sub2')))),
                ft.Card(content=ft.ListTile(leading=ft.Icon("emoji_events", color="#FFC107"), title=ft.Text(_('menu_achievements')), subtitle=ft.Text(_('tut_intro_sub3')))),
                ft.Card(content=ft.ListTile(leading=ft.Icon("settings", color="#FF9800"), title=ft.Text(_('menu_options')), subtitle=ft.Text(_('tut_intro_sub4')))),
            ], padding=ft.padding.only(top=10, bottom=10)),

            ft.ListView(spacing=10, controls=[
                ft.Card(content=ft.ListTile(leading=ft.Icon("casino", color="#9C27B0"), title=ft.Text(_('style_classic'), weight=ft.FontWeight.BOLD), subtitle=ft.Text(_('tut_styles_classic_sub')))),
                ft.Card(content=ft.ListTile(leading=ft.Icon("swap_horiz", color="#F44336"), title=ft.Text(_('style_inverted'), weight=ft.FontWeight.BOLD), subtitle=ft.Text(_('tut_styles_inverted_sub')))),
                ft.Card(content=ft.ListTile(leading=ft.Icon("landscape", color="#9E9E9E"), title=ft.Text(_('style_mined'), weight=ft.FontWeight.BOLD), subtitle=ft.Text(_('tut_styles_mined_sub')))),
            ], padding=ft.padding.only(top=10, bottom=10)),

            ft.ListView(spacing=10, controls=[
                ft.Card(content=ft.ListTile(leading=ft.Icon("center_focus_strong", color="#2196F3"), title=ft.Text(_('tut_tip_center_title')), subtitle=ft.Text(_('tut_tip_center_sub')))),
                ft.Card(content=ft.ListTile(leading=ft.Icon("block", color="#E91E63"), title=ft.Text(_('tut_tip_defensive_title')), subtitle=ft.Text(_('tut_tip_defensive_sub')))),
                ft.Card(content=ft.ListTile(leading=ft.Icon("call_split", color="#009688"), title=ft.Text(_('tut_tip_double_title')), subtitle=ft.Text(_('tut_tip_double_sub')))),
            ], padding=ft.padding.only(top=10, bottom=10)),
        ]

    tutorial_pages = rebuild_tutorial_pages()

    tutorial_content_area = ft.AnimatedSwitcher(
        content=tutorial_pages[0],
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=300,
        expand=True,
    )

    menu_view=ft.Column(data="menu", visible=True,alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=20, controls=[ft.Text(_('menu_title'),size=48,font_family="Press Start 2P"),ft.Container(height=20), ft.FilledButton(_('menu_modes'),icon="sports_esports",width=250,on_click=lambda _: mostrar_tela("modos")), ft.OutlinedButton(_('menu_stats'),icon="query_stats",width=250,on_click=lambda _: mostrar_tela("stats")), ft.OutlinedButton(_('menu_achievements'),icon="emoji_events",width=250,on_click=lambda _: mostrar_tela("conquistas")), ft.OutlinedButton(_('menu_tutorial'), icon="help_outline", width=250, on_click=lambda _: mostrar_tela("tutorial")), ft.OutlinedButton(_('menu_options'),icon="settings",width=250,on_click=lambda _: mostrar_tela("opcoes"))])
    modos_view=ft.Column(data="modos", visible=False,alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=20, controls=[ft.Text(_('modes_title'),size=32,font_family="Press Start 2P"),ft.Container(height=20), botao_jogar_vs_bot_facil, botao_jogar_vs_bot_dificil, botao_jogar_vs_jogador,ft.Container(height=20), ft.OutlinedButton(_('button_back_menu'),icon="arrow_back",width=280,on_click=lambda _: mostrar_tela("menu"))])
    
    selecao_estilo_view = ft.Column(data="selecao_estilo", visible=False, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20,
        controls=[
            ft.Text(_('style_title'), size=32, font_family="Press Start 2P"), ft.Container(height=20),
            ft.FilledButton(_('style_classic'), icon="casino", width=280, on_click=lambda _: iniciar_partida("Classico")),
            ft.FilledButton(_('style_inverted'), icon="swap_horiz", width=280, on_click=lambda _: iniciar_partida("Invertido")),
            ft.FilledButton(_('style_mined'), icon="landscape", width=280, on_click=lambda _: iniciar_partida("Minado")),
            ft.Container(height=20),
            ft.OutlinedButton(_('button_back'), icon="arrow_back", width=280, on_click=lambda _: mostrar_tela("modos"))
        ]
    )

    opcoes_view=ft.Column(data="opcoes", visible=False,alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=10, controls=[
        ft.Text(_('options_title'),size=40,weight=ft.FontWeight.BOLD,font_family="Press Start 2P"),
        ft.Container(height=20), 
        dropdown_lang, 
        ft.Container(height=10),
        theme_button, 
        botao_reset_placar, 
        botao_reset_stats, 
        ft.Container(height=10), 
        ft.OutlinedButton(_('button_back_menu'),icon="arrow_back",width=280,on_click=lambda _: mostrar_tela("menu"))])
    
    lista_conquistas=ft.ListView(expand=True,spacing=10)
    conquistas_view=ft.Column(data="conquistas", visible=False,alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=20, controls=[ft.Text(_('ach_title'),size=36,font_family="Press Start 2P"), ft.Container(lista_conquistas,border=ft.border.all(1,"grey"),border_radius=8,padding=10,height=380,width=350), ft.OutlinedButton(_('button_back_menu'),icon="arrow_back",width=250,on_click=lambda _: mostrar_tela("menu"))])

    tutorial_view = ft.Column(
        data="tutorial",
        visible=False,
        spacing=0,
        expand=True,
        controls=[
            ft.Container(
                content=ft.Text(_('menu_tutorial'), size=36, font_family="Press Start 2P", text_align=ft.TextAlign.CENTER),
                padding=ft.padding.only(top=10, bottom=10)
            ),
            ft.Divider(height=1),
            ft.Container(
                content=tutorial_content_area,
                expand=True,
            ),
            tutorial_navbar,
            ft.Container(
                content=ft.OutlinedButton(_('button_back_menu'), icon="arrow_back", width=280, on_click=lambda _: mostrar_tela("menu")),
                padding=ft.padding.only(top=5, bottom=5),
                alignment=ft.alignment.center
            )
        ]
    )


    stats_geral_vitorias = ft.Text(size=16); stats_geral_derrotas = ft.Text(size=16); stats_geral_empates = ft.Text(size=16); stats_geral_taxa = ft.Text(size=16, weight=ft.FontWeight.BOLD); stats_geral_sequencia = ft.Text(size=16)
    stats_table = ft.DataTable(columns=[
        ft.DataColumn(ft.Text(_('modes_title'))),
        ft.DataColumn(ft.Text(_('stats_col_v')), numeric=True),
        ft.DataColumn(ft.Text(_('stats_col_d')), numeric=True),
        ft.DataColumn(ft.Text(_('stats_col_e')), numeric=True),
    ], rows=[])
    
    stats_view = ft.Column(data="stats", visible=False, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, controls=[ft.Text(_('stats_title'), size=36, font_family="Press Start 2P"), ft.Container(content=ft.Column([stats_geral_taxa, stats_geral_sequencia, ft.Divider(), stats_geral_vitorias, stats_geral_derrotas, ft.Container(height=5), stats_geral_empates]), padding=15), ft.Text(_('stats_details_by_mode'), size=20), stats_table, ft.OutlinedButton(_('button_back_menu'), icon="arrow_back", width=280, on_click=lambda _: mostrar_tela("menu"))])
    
    game_view = ft.Column(data="game", visible=False,alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=25, controls=[texto_status, tabuleiro_visivel, texto_placar,ft.IconButton("home",on_click=lambda _: mostrar_tela("menu"),tooltip=_('button_back_menu'))])

    page.overlay.append(dialogo_reset_stats)

    page.add(menu_view,modos_view, selecao_estilo_view, game_view,opcoes_view,conquistas_view, stats_view, tutorial_view)

if __name__ == "__main__":
    
    ft.app(target=main, assets_dir=resource_path("assets"))