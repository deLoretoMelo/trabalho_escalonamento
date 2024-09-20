# Vamos começar simulando os quatro algoritmos de escalonamento: FCFS, SJF, RR e Priority Scheduling.
# Para isso, precisamos definir os processos e coletar os dados solicitados (tempo de espera médio, tempo de resposta médio, turnaround time médio e throughput).

import pandas as pd

# Definindo os processos com as suas características: [Processo, Tempo de Chegada, Tempo de Execução, Prioridade]
processos = [
    {"processo": "P1", "chegada": 0, "execucao": 10, "prioridade": 3},
    {"processo": "P2", "chegada": 2, "execucao": 5, "prioridade": 1},
    {"processo": "P3", "chegada": 4, "execucao": 2, "prioridade": 2},
    {"processo": "P4", "chegada": 6, "execucao": 8, "prioridade": 4}
]

# Função auxiliar para calcular métricas de escalonamento
def calcular_metricas(tempo_inicio, tempo_execucao, tempo_chegada):
    tempo_espera = tempo_inicio - tempo_chegada
    turnaround_time = tempo_execucao + tempo_espera
    return tempo_espera, turnaround_time

# Simulação do algoritmo First-Come, First-Served (FCFS)
def fcfs(processos):
    processos_fcfs = sorted(processos, key=lambda p: p["chegada"])
    tempo_atual = 0
    total_tempo_espera, total_turnaround_time = 0, 0
    inicio_execucao = []
    
    for p in processos_fcfs:
        # Verifica se o processo precisa esperar
        if tempo_atual < p["chegada"]:
            tempo_atual = p["chegada"]
        
        tempo_espera, turnaround_time = calcular_metricas(tempo_atual, p["execucao"], p["chegada"])
        inicio_execucao.append(tempo_atual - p["chegada"])
        total_tempo_espera += tempo_espera
        total_turnaround_time += turnaround_time
        tempo_atual += p["execucao"]
    
    return total_tempo_espera / len(processos), sum(inicio_execucao) / len(processos), total_turnaround_time / len(processos), len(processos) / tempo_atual

# Simulação do algoritmo Shortest Job First (SJF)
def sjf(processos):
    processos_sjf = sorted(processos, key=lambda p: (p["chegada"], p["execucao"]))
    tempo_atual = 0
    total_tempo_espera, total_turnaround_time = 0, 0
    inicio_execucao = []
    
    for p in processos_sjf:
        if tempo_atual < p["chegada"]:
            tempo_atual = p["chegada"]
        
        tempo_espera, turnaround_time = calcular_metricas(tempo_atual, p["execucao"], p["chegada"])
        inicio_execucao.append(tempo_atual - p["chegada"])
        total_tempo_espera += tempo_espera
        total_turnaround_time += turnaround_time
        tempo_atual += p["execucao"]
    
    return total_tempo_espera / len(processos), sum(inicio_execucao) / len(processos), total_turnaround_time / len(processos), len(processos) / tempo_atual

# Simulação do algoritmo Round Robin (RR)
def round_robin(processos, quantum=2):
    fila = sorted(processos, key=lambda p: p["chegada"])
    tempo_atual = 0
    total_tempo_espera, total_turnaround_time = 0, 0
    inicio_execucao = {}
    tempo_restante = {p["processo"]: p["execucao"] for p in processos}
    fila_execucao = []
    processo_atual = 0
    
    while fila:
        p = fila[processo_atual % len(fila)]
        if tempo_atual >= p["chegada"]:
            if p["processo"] not in inicio_execucao:
                inicio_execucao[p["processo"]] = tempo_atual - p["chegada"]
            tempo_a_executar = min(quantum, tempo_restante[p["processo"]])
            tempo_restante[p["processo"]] -= tempo_a_executar
            tempo_atual += tempo_a_executar

            if tempo_restante[p["processo"]] == 0:
                fila_execucao.append(p)
                fila.remove(p)
                tempo_espera, turnaround_time = calcular_metricas(tempo_atual - p["execucao"], p["execucao"], p["chegada"])
                total_tempo_espera += tempo_espera
                total_turnaround_time += turnaround_time

        processo_atual += 1
    
    return total_tempo_espera / len(processos), sum(inicio_execucao.values()) / len(processos), total_turnaround_time / len(processos), len(processos) / tempo_atual

# Simulação do algoritmo Priority Scheduling
def priority_scheduling(processos):
    processos_priority = sorted(processos, key=lambda p: (p["chegada"], p["prioridade"]))
    tempo_atual = 0
    total_tempo_espera, total_turnaround_time = 0, 0
    inicio_execucao = []
    
    for p in processos_priority:
        if tempo_atual < p["chegada"]:
            tempo_atual = p["chegada"]
        
        tempo_espera, turnaround_time = calcular_metricas(tempo_atual, p["execucao"], p["chegada"])
        inicio_execucao.append(tempo_atual - p["chegada"])
        total_tempo_espera += tempo_espera
        total_turnaround_time += turnaround_time
        tempo_atual += p["execucao"]
    
    return total_tempo_espera / len(processos), sum(inicio_execucao) / len(processos), total_turnaround_time / len(processos), len(processos) / tempo_atual

# Simulando os quatro algoritmos e gerando uma tabela de resultados
algoritmos = {
    "FCFS": fcfs(processos),
    "SJF": sjf(processos),
    "Round Robin": round_robin(processos, quantum=2),
    "Priority Scheduling": priority_scheduling(processos)
}

# Convertendo resultados para DataFrame
df_resultados = pd.DataFrame(algoritmos, index=["Tempo de Espera Médio", "Tempo de Resposta Médio", "Turnaround Time Médio", "Throughput"])
df_resultados.T
print(df_resultados.T)
