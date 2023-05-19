import pandas as pd


def consumo_energetico_residencial():
    path2_consumo_residencial = 'data/energy/Consumo_residencial_por_UF.csv'
    df_consumo_residencial = pd.read_csv(path2_consumo_residencial)
    df_r = pd.DataFrame(
        columns=['Timestamp', 'Estado', 'Consumo Residencial']
    )
    df_r
    for idx, row in df_consumo_residencial.iterrows():
        timestamp = []
        estado = []
        consumo_residencial = []
        for key in row.keys():
            if key == 'UF':
                pass
            else:
                timestamp.append(key)
                estado.append(row['UF'])
                consumo_residencial.append(row[key])
        data = {
            'Timestamp': timestamp,
            'Estado': estado,
            'Consumo Residencial': consumo_residencial
        }
        df_r = pd.concat([df_r, pd.DataFrame.from_dict(data)])
        df_r = df_r[1:]
        return df_r


def consumo_energetico_industrial():
    path2_consumo_industrial = 'data/energy/Consumo_industrial_por_UF.csv'
    df_consumo_industrial = pd.read_csv(path2_consumo_industrial)
    df_i = pd.DataFrame(
        columns=['Timestamp', 'Estado', 'Consumo Industrial']
    )

    for idx, row in df_consumo_industrial.iterrows():
        timestamp = []
        estado = []
        consumo_industrial = []
        for key in row.keys():
            if key == 'UF':
                pass
            else:
                timestamp.append(key)
                estado.append(row['UF'])
                consumo_industrial.append(row[key])
        data = {
            'Timestamp': timestamp,
            'Estado': estado,
            'Consumo Industrial': consumo_industrial
        }
        df_i = pd.concat([df_i, pd.DataFrame.from_dict(data)])
    df_i = df_i[1:]
    return df_i


def populacao():
    df_populacao = pd.read_csv('data/social/populacao.csv')
    df_populacao.rename(
        columns={'sigla_uf': 'Estado', 'populacao': 'Populacao'}, inplace=True)

    state_names = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins'
    }
    df_populacao['Estado'] = df_populacao['Estado'].map(state_names)

    months = months = ['jan.', 'fev.', 'mar.', 'abr.', 'mai.',
                       'jun.', 'jul.', 'ago.', 'set.', 'out.', 'nov.', 'dez.']
    # Create an empty list to store expanded rows
    expanded_rows = []

    # Iterate over each row in the original DataFrame
    for _, row in df_populacao.iterrows():
        year = row['ano']
        population = row['Populacao']

        # Iterate over each month and create a new row
        for month in months:
            expanded_rows.append(
                {'Estado': row['Estado'], 'ano': year, 'Populacao': population, 'Month': month})

    # Create a new DataFrame with the expanded rows
    df_populacao = pd.DataFrame(expanded_rows)

    # Reset the index of the new DataFrame
    df_populacao = df_populacao.reset_index(drop=True)
    df_populacao['Timestamp'] = df_populacao['Month'] + \
        ' '+df_populacao['ano'].astype(str)
    df_populacao.drop(columns=['ano', 'Month'], inplace=True)
    return df_populacao


def pib():
    df_pib = pd.read_csv('data/social/pib.csv')
    df_pib.rename(columns={'pib': 'PIB'}, inplace=True)
    state_names = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins'
    }
    df_pib['Estado'] = df_pib['Estado'].map(state_names)

    months = ['jan.', 'fev.', 'mar.', 'abr.', 'mai.', 'jun.',
              'jul.', 'ago.', 'set.', 'out.', 'nov.', 'dez.']
    # Create an empty list to store expanded rows
    expanded_rows = []

    # Iterate over each row in the original DataFrame
    for _, row in df_pib.iterrows():
        year = row['ano']
        pib = row['PIB']

        # Iterate over each month and create a new row
        for month in months:
            expanded_rows.append(
                {'Estado': row['Estado'], 'ano': year, 'PIB': pib, 'Month': month})

    # Create a new DataFrame with the expanded rows
    df_pib = pd.DataFrame(expanded_rows)

    # Reset the index of the new DataFrame
    df_pib = df_pib.reset_index(drop=True)
    df_pib['Timestamp'] = df_pib['Month']+' '+df_pib['ano'].astype(str)
    df_pib.drop(columns=['ano', 'Month'], inplace=True)
    return df_pib


def get_data():

    df = pd.DataFrame()

    # get data from source
    df_r = consumo_energetico_residencial()
    df_i = consumo_energetico_industrial()
    df_populacao = populacao()
    df_pib = pib()

    # Init dataframe
    df['Timestamp'] = df_r['Timestamp']
    df['Estado'] = df_r['Estado']

    # Add data to df
    df = pd.merge(df, df_r, on=['Timestamp', 'Estado'])
    df = pd.merge(df, df_i, on=['Timestamp', 'Estado'])
    df = pd.merge(df, df_populacao, on=['Timestamp', 'Estado'])
    df = pd.merge(df, df_pib, on=['Timestamp', 'Estado'])

    # save data as csv
    df.to_csv('./data.csv')

    return df
