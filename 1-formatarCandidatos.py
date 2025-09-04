import pandas as pd

nomeCandidato = "AIRTON NUNES TENORIO"
nome_arquivo = nomeCandidato + ".csv"

# Defina aqui a lista completa de horários que você quer no arquivo final
horarios_completos = [
    "07:30 - 08:20", "08:20 - 09:10", "09:20 - 10:10", "10:10 - 11:00",
    "11:10 - 12:00", "12:00 - 12:50", "13:30 - 14:20", "14:20 - 15:10",
    "15:20 - 16:10", "16:10 - 17:00", "17:10 - 18:00", "18:00 - 18:50",
    "19:00 - 19:50", "19:50 - 20:40", "20:50 - 21:40", "21:40 - 22:30"
]

# Carregue seu CSV original
df = pd.read_csv(nome_arquivo)

# Defina as colunas que deseja manter (conferir nomes, pode ajustar se necessário)
colunas_esperadas = ["Horários", "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]

# Garantir que as colunas estão corretas e na ordem certa
df = df[colunas_esperadas]

# Criar um DataFrame novo com a lista completa de horários
df_completo = pd.DataFrame({"Horários": horarios_completos})

# Fazer merge para alinhar os horários existentes com os horários completos
df = pd.merge(df_completo, df, on="Horários", how="left")

# Substituir NaN por '---' em todas as colunas, exceto "Horários"
for col in colunas_esperadas[1:]:
    df[col] = df[col].fillna("---")

# Salvar o CSV completo
df.to_csv(nome_arquivo, index=False)


