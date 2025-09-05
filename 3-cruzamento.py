import pandas as pd

# Configuração de horários e colunas
horarios_completos = [
    "07:30 - 08:20", "08:20 - 09:10", "09:20 - 10:10", "10:10 - 11:00",
    "11:10 - 12:00", "12:00 - 12:50", "13:30 - 14:20", "14:20 - 15:10",
    "15:20 - 16:10", "16:10 - 17:00", "17:10 - 18:00", "18:00 - 18:50",
    "19:00 - 19:50", "19:50 - 20:40", "20:50 - 21:40", "21:40 - 22:30"
]
dias_semana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]
colunas_esperadas = ["Horários"] + dias_semana

# Função auxiliar para separar nomes
def separar_nomes(celula):
    if pd.isna(celula) or str(celula).strip() in ["", "---"]:
        return []
    # divide por vírgula, ponto e vírgula ou quebra de linha
    separadores = [",", ";", "\n"]
    texto = str(celula)
    for sep in separadores:
        texto = texto.replace(sep, "\n")
    return [n.strip() for n in texto.split("\n") if n.strip()]

# 1. Ler arquivos de entrada
df_candidatos = pd.read_csv("csv_final_candidato.csv")
df_avaliadores = pd.read_csv("csv_final_avaliador.csv")


# Garantir estrutura completa (caso falte horários)
df_base = pd.DataFrame({"Horários": horarios_completos})
df_candidatos = pd.merge(df_base, df_candidatos, on="Horários", how="left")
df_avaliadores = pd.merge(df_base, df_avaliadores, on="Horários", how="left")

# 2. Calcular avaliadoresPeso
df_peso = df_base.copy()
for dia in dias_semana:
    df_peso[dia] = df_avaliadores[dia].apply(lambda x: len(separar_nomes(x)))

df_peso.to_csv("avaliadoresPeso.csv", index=False)

# 3. Criar lista de horários ordenados por prioridade
slots = []
for idx, horario in enumerate(horarios_completos):
    for dia in dias_semana:
        peso = df_peso.at[idx, dia]
        slots.append((idx, dia, peso))

slots.sort(key=lambda x: x[2], reverse=True)  # ordena por peso decrescente

# 4. Preparar controle de candidatos alocados
candidatos_alocados = set()

# 5. Criar df_final com colunas duplicadas
colunas_final = ["Horários"]
for dia in dias_semana:
    colunas_final.append(f"{dia} (Candidatos)")
    colunas_final.append(f"{dia} (Avaliadores)")

df_final = pd.DataFrame({"Horários": horarios_completos})
for col in colunas_final[1:]:
    df_final[col] = "---"

# 6. Alocação
for idx, dia, peso in slots:
    candidatos_disp = separar_nomes(df_candidatos.at[idx, dia])
    avaliadores_disp = separar_nomes(df_avaliadores.at[idx, dia])

    # Alocar candidatos (máx 2 e não repetidos)
    celula_candidatos = []
    for cand in candidatos_disp:
        if cand not in candidatos_alocados and len(celula_candidatos) < 2:
            celula_candidatos.append(cand)
            candidatos_alocados.add(cand)

    # Avaliadores: todos disponíveis
    celula_avaliadores = avaliadores_disp

    # Atualizar df_final
    col_cand = f"{dia} (Candidatos)"
    col_av = f"{dia} (Avaliadores)"
    df_final.at[idx, col_cand] = "\n".join(celula_candidatos) if celula_candidatos else "---"
    df_final.at[idx, col_av] = "\n".join(celula_avaliadores) if celula_avaliadores else "---"

# 7. Salvar resultado
df_final.to_csv("csv_final.csv", index=False)

print("Arquivos gerados com sucesso: avaliadoresPeso.csv e csv_final.csv")
