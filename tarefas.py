import json
import os
from datetime import datetime, timedelta

tarefas = []  
id_counter = 1  

def validar_prioridade(prioridade):
    return prioridade in ["Urgente", "Alta", "Média", "Baixa"]

def validar_origem(origem):
    return origem in ["E-mail", "Telefone", "Chamado do Sistema"]

def validar_status(status):
    return status in ["Pendente", "Fazendo", "Concluída", "Arquivado", "Excluída"]

def load_data():
    global tarefas
    try:
        if os.path.exists("tarefas.json"):
            with open("tarefas.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                tarefas = []
                for t in data:
                    t["data_criacao"] = datetime.fromisoformat(t["data_criacao"])
                    if "data_conclusao" in t and t["data_conclusao"]:
                        t["data_conclusao"] = datetime.fromisoformat(t["data_conclusao"])
                    tarefas.append(t)
                global id_counter
                if tarefas:
                    id_counter = max(t["id"] for t in tarefas) + 1
        else:
            
            with open("tarefas.json", "w", encoding="utf-8") as f:
                json.dump([], f)
    except Exception as e:
        print(f"Erro ao carregar tarefas: {e}")

def save_data():
    try:
        data = []
        for t in tarefas:
            t_copy = t.copy()
            t_copy["data_criacao"] = t["data_criacao"].isoformat()
            if "data_conclusao" in t and t["data_conclusao"]:
                t_copy["data_conclusao"] = t["data_conclusao"].isoformat()
            data.append(t_copy)
        with open("tarefas.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar tarefas: {e}")

def save_arquivadas(tarefa):
    try:
        if not os.path.exists("tarefas_arquivadas.json"):
            with open("tarefas_arquivadas.json", "w", encoding="utf-8") as f:
                json.dump([], f)
        with open("tarefas_arquivadas.json", "r", encoding="utf-8") as f:
            arquivadas = json.load(f)
        tarefa_copy = tarefa.copy()
        tarefa_copy["data_criacao"] = tarefa["data_criacao"].isoformat()
        if "data_conclusao" in tarefa and tarefa["data_conclusao"]:
            tarefa_copy["data_conclusao"] = tarefa["data_conclusao"].isoformat()
        arquivadas.append(tarefa_copy)
        with open("tarefas_arquivadas.json", "w", encoding="utf-8") as f:
            json.dump(arquivadas, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar tarefa arquivada: {e}")

def criar_tarefa():
    print("Executando criar_tarefa")
    global tarefas, id_counter
    titulo = input("Título da tarefa (obrigatório): ").strip()
    if not titulo:
        print("Título é obrigatório.")
        return
    descricao = input("Descrição da tarefa: ").strip()
    print("Prioridades possíveis: Urgente, Alta, Média, Baixa")
    while True:
        prioridade = input("Prioridade (obrigatório): ").strip()
        if validar_prioridade(prioridade):
            break
        print("Prioridade inválida. Tente novamente.")
    print("Origens possíveis: E-mail, Telefone, Chamado do Sistema")
    while True:
        origem = input("Origem (obrigatório): ").strip()
        if validar_origem(origem):
            break
        print("Origem inválida. Tente novamente.")
    tarefa = {
        "id": id_counter,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": "Pendente",
        "origem": origem,
        "data_criacao": datetime.now(),
        "data_conclusao": None
    }
    tarefas.append(tarefa)
    id_counter += 1
    print("Tarefa criada com sucesso!")

def verificar_urgencia():
    print("Executando verificar_urgencia")
    global tarefas
    prioridades = ["Urgente", "Alta", "Média", "Baixa"]
    if any(t["status"] == "Fazendo" for t in tarefas):
        print("Já existe uma tarefa em andamento.")
        return
    for prioridade in prioridades:
        for tarefa in tarefas:
            if tarefa["prioridade"] == prioridade and tarefa["status"] == "Pendente":
                tarefa["status"] = "Fazendo"
                print("Tarefa selecionada para execução:")
                print(f"ID: {tarefa['id']} | Título: {tarefa['titulo']} | Prioridade: {tarefa['prioridade']} | Status: {tarefa['status']}")
                return
    print("Não há tarefas pendentes.")

def atualizar_prioridade():
    print("Executando atualizar_prioridade")
    global tarefas
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    print("Tarefas disponíveis:")
    for t in tarefas:
        print(f"ID: {t['id']} - {t['titulo']} (Prioridade: {t['prioridade']})")
    while True:
        try:
            id_escolha = int(input("Digite o ID da tarefa para alterar prioridade: "))
            tarefa = next((t for t in tarefas if t["id"] == id_escolha), None)
            if tarefa:
                break
            print("ID inválido.")
        except ValueError:
            print("Digite um ID numérico válido.")
    print("Prioridades possíveis: Urgente, Alta, Média, Baixa")
    while True:
        nova_prioridade = input("Nova prioridade: ").strip()
        if validar_prioridade(nova_prioridade):
            tarefa["prioridade"] = nova_prioridade
            print("Prioridade atualizada com sucesso!")
            break
        print("Prioridade inválida. Tente novamente.")

def concluir_tarefa():
    print("Executando concluir_tarefa")
    global tarefas
    tarefa_fazendo = next((t for t in tarefas if t["status"] == "Fazendo"), None)
    if not tarefa_fazendo:
        print("Nenhuma tarefa em andamento para concluir.")
        return
    tarefa_fazendo["status"] = "Concluída"
    tarefa_fazendo["data_conclusao"] = datetime.now()
    print(f"Tarefa '{tarefa_fazendo['titulo']}' concluída.")

def arquivar_tarefas_antigas():
    print("Executando arquivar_tarefas_antigas")
    global tarefas
    agora = datetime.now()
    a_remover = []
    for tarefa in tarefas:
        if tarefa["status"] == "Concluída" and tarefa["data_conclusao"] and (agora - tarefa["data_conclusao"]) > timedelta(days=7):
            tarefa["status"] = "Arquivado"
            save_arquivadas(tarefa)
            a_remover.append(tarefa)
    for t in a_remover:
        tarefas.remove(t)
    if a_remover:
        print(f"{len(a_remover)} tarefa(s) arquivada(s).")
    else:
        print("Nenhuma tarefa para arquivar.")

def excluir_tarefa():
    print("Executando excluir_tarefa")
    global tarefas
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    print("Tarefas disponíveis:")
    for t in tarefas:
        print(f"ID: {t['id']} - {t['titulo']} (Status: {t['status']})")
    while True:
        try:
            id_escolha = int(input("Digite o ID da tarefa para excluir: "))
            tarefa = next((t for t in tarefas if t["id"] == id_escolha), None)
            if tarefa:
                tarefa["status"] = "Excluída"
                save_arquivadas(tarefa)
                tarefas.remove(tarefa)
                print("Tarefa excluída com sucesso!")
                break
            print("ID inválido.")
        except ValueError:
            print("Digite um ID numérico válido.")

def relatorio():
    print("Executando relatorio")
    global tarefas
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    print("Relatório de Tarefas:")
    for t in tarefas:
        tempo_execucao = ""
        if t["status"] == "Concluída" and t["data_conclusao"]:
            delta = t["data_conclusao"] - t["data_criacao"]
            tempo_execucao = f" | Tempo de Execução: {delta}"
        print(f"ID: {t['id']} | Título: {t['titulo']} | Descrição: {t['descricao']} | Prioridade: {t['prioridade']} | Status: {t['status']} | Origem: {t['origem']} | Data Criação: {t['data_criacao'].strftime('%d/%m/%Y %H:%M')}{tempo_execucao}")

def relatorio_arquivados():
    print("Executando relatorio_arquivados")
    try:
        if not os.path.exists("tarefas_arquivadas.json"):
            print("Nenhum arquivo de arquivados encontrado.")
            return
        with open("tarefas_arquivadas.json", "r", encoding="utf-8") as f:
            arquivadas = json.load(f)
        arquivadas_filtradas = [t for t in arquivadas if t["status"] == "Arquivado"]
        if not arquivadas_filtradas:
            print("Nenhuma tarefa arquivada.")
            return
        print("Relatório de Tarefas Arquivadas:")
        for t in arquivadas_filtradas:
            print(f"ID: {t['id']} | Título: {t['titulo']} | Descrição: {t['descricao']} | Prioridade: {t['prioridade']} | Status: {t['status']} | Origem: {t['origem']} | Data Criação: {t['data_criacao']}")
    except Exception as e:
        print(f"Erro ao carregar relatório arquivado: {e}")

def menu():
    while True:
        print("\nMenu de Operações:")
        print("1 - Criar Tarefa")
        print("2 - Verificar Próxima Tarefa")
        print("3 - Atualizar Prioridade")
        print("4 - Concluir Tarefa")
        print("5 - Arquivar Tarefas Antigas")
        print("6 - Excluir Tarefa")
        print("7 - Relatório")
        print("8 - Relatório Arquivados")
        print("9 - Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            criar_tarefa()
        elif escolha == "2":
            verificar_urgencia()
        elif escolha == "3":
            atualizar_prioridade()
        elif escolha == "4":
            concluir_tarefa()
        elif escolha == "5":
            arquivar_tarefas_antigas()
        elif escolha == "6":
            excluir_tarefa()
        elif escolha == "7":
            relatorio()
        elif escolha == "8":
            relatorio_arquivados()
        elif escolha == "9":
            save_data
            break
        else:
            print("Opção invalida. Tente novamente")