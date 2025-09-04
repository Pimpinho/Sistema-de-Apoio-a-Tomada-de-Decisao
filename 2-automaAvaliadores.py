import pandas as pd

nomeAvaliador = input("Digite o nome do avaliador: ").strip()
nome_arquivo = nomeAvaliador + ".csv"
csv_final_avaliador = "csv_final_avaliador.csv"

horarios_completos = [
    "07:30 - 08:20", "08:20 - 09:10", "09:20 - 10:10", "10:10 - 11:00",
    "11:10 - 12:00", "12:00 - 12:50", "13:30 - 14:20", "14:20 - 15:10",
    "15:20 - 16:10", "16:10 - 17:00", "17:10 - 18:00", "18:00 - 18:50",
    "19:00 - 19:50", "19:50 - 20:40", "20:50 - 21:40", "21:40 - 22:30"
]

colunas_esperadas = ["Horários", "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]

# Carregar CSV do avaliador
df = pd.read_csv(nome_arquivo)
df = df[colunas_esperadas]

# Garantir todos os horários estão presentes
df_completo = pd.DataFrame({"Horários": horarios_completos})
df = pd.merge(df_completo, df, on="Horários", how="left")
for col in colunas_esperadas[1:]:
    df[col] = df[col].fillna("---")

# Salvar CSV do avaliador atualizado
df.to_csv(nome_arquivo, index=False)

# Atualizar csv_final_avaliador
df_final = pd.read_csv(csv_final_avaliador)

for col in colunas_esperadas[1:]:
    for idx, valor in enumerate(df[col]):
        if valor.strip() == "---":
            atual = str(df_final.at[idx, col]).strip()
            if atual == "---" or atual == "":
                df_final.at[idx, col] = nomeAvaliador
            else:
                if nomeAvaliador not in atual.split("\n"):
                    df_final.at[idx, col] = atual + "\n" + nomeAvaliador

# Salvar csv_final_avaliador atualizado
df_final.to_csv(csv_final_avaliador, index=False)

print(f"Avaliador '{nomeAvaliador}' adicionado ao csv_final_avaliador com quebra de linha.")