import pandas as pd

# Arquivos
candidatos_file = "csv_final_candidato.csv"
avaliadores_file = "csv_final_avaliador.csv"

# Ler CSVs
df_cand = pd.read_csv(candidatos_file, sep=",", quotechar='"')
df_av = pd.read_csv(avaliadores_file, sep=",", quotechar='"')

# Função para transformar célula com quebras de linha em lista
def parse_names(cell):
    if pd.isna(cell) or str(cell).strip() == "":
        return []
    return [name.strip() for name in str(cell).splitlines() if name.strip()]

# Criar dicionários de disponibilidade
candidatos_disp = {}
avaliadores_disp = {}

dias = df_cand.columns[1:]  # ignorando coluna "Horários"

for _, row in df_cand.iterrows():
    horario = row['Horários']
    for dia in dias:
        candidatos_disp[(horario, dia)] = parse_names(row[dia])

for _, row in df_av.iterrows():
    horario = row['Horários']
    for dia in dias:
        avaliadores_disp[(horario, dia)] = parse_names(row[dia])

# Contar avaliadores por horário
avaliadores_count = {k: len(v) for k, v in avaliadores_disp.items()}

# Ordenar horários do maior para menor número de avaliadores
horarios_ordenados = sorted(avaliadores_count.keys(), key=lambda x: -avaliadores_count[x])

# Alocar candidatos (cada candidato só pode aparecer uma vez)
candidatos_alocados = set()
resultado = []

for horario, dia in horarios_ordenados:
    candidatos_possiveis = [c for c in candidatos_disp.get((horario, dia), []) if c not in candidatos_alocados]
    if candidatos_possiveis:
        # Alocar todos os candidatos possíveis nesse horário
        resultado.append({
            "Horário": horario,
            "Dia": dia,
            "Avaliadores": "\n".join(avaliadores_disp.get((horario, dia), [])),
            "Candidatos": "\n".join(candidatos_possiveis)
        })
        # Atualiza o conjunto de candidatos já alocados
        candidatos_alocados.update(candidatos_possiveis)

# Criar DataFrame final e salvar mantendo quebras de linha
if resultado:
    df_result = pd.DataFrame(resultado)
    df_result.to_csv("tabela_final.csv", index=False, sep=",", line_terminator='\n', quoting=pd.io.common.csv.QUOTE_ALL)
    print("Tabela final gerada: tabela_final.csv")
else:
    print("Nenhum candidato foi alocado. Verifique os nomes e disponibilidade nas planilhas.")