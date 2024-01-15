import Connection3
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def get_top_awarded_actors():
    db = Connection3.DatabaseManager(Connection3.config)
    db.open_connection()

    # Retorna os dez atores ou atrizes com maior número de prêmios
    query = """
    SELECT 
        p.NomeArt, 
        COUNT(*) AS NumeroDePremios
    FROM 
        Pessoas_Nomeadas pn
    JOIN 
        Pessoa p ON pn.IDPessoa = p.IDPessoa
    WHERE 
        pn.Ganhou = 'S'
    GROUP BY 
        pn.IDPessoa
    ORDER BY 
        NumeroDePremios DESC
    LIMIT 10;
    """

    df = db.query(query)
    db.close_connection()

     # Criar um gráfico de barras com os dados
    plt.bar(df['NomeArt'], df['NumeroDePremios'])
    plt.ylabel('Número de Prêmios')
    plt.xlabel('Ator')
    plt.title('Os dez Atores com maior número de prêmios')
    plt.xticks(rotation=90)  # Rotacionar os nomes dos atores para melhor visualização
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Definir a escala do eixo y para inteiros
    plt.tight_layout() # Ajustar o layout do gráfico
    plt.show()
    print()
    print('-' * 100)
    print()


def get_top_awarded_films():
    db = Connection3.DatabaseManager(Connection3.config)
    db.open_connection()

    # Retorna os dez filmes com maior número de prêmios
    query = """
    SELECT 
        f.TituloOriginal,
        COUNT(*) AS NumeroDePremios
    FROM 
        Filmes_Nomeados fn
    JOIN 
        Filme f ON fn.IDFilme = f.IDFilme
    WHERE 
        fn.Premiado = 'S'
    GROUP BY 
        fn.IDFilme
    ORDER BY 
        NumeroDePremios DESC
    LIMIT 10;
    """

    df = db.query(query)
    db.close_connection()

    # Criar um gráfico de barras com os dados
    plt.figure(figsize=(8, 5))  # Aumentar o tamanho da figura
    plt.bar(df['TituloOriginal'], df['NumeroDePremios'])
    plt.ylabel('Número de Prêmios')
    plt.xlabel('Filme')
    plt.title('Os dez Filmes mais premiados')
    plt.xticks(rotation=90)  # Rotacionar os títulos dos filmes para melhor visualização
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # Definir a escala do eixo y para inteiros
    plt.tight_layout() # Ajustar o layout do gráfico
    plt.show()
    print()
    print('-' * 100)
    print()


def get_top_grossing_films():
    db = Connection3.DatabaseManager(Connection3.config)
    db.open_connection()

    # Retorna a arrecadação dos dez filmes com maior arrecadação
    query = """
    SELECT 
        TituloOriginal,
        ArrecadacaoAnoInicial
    FROM 
        Filme
    ORDER BY 
        ArrecadacaoAnoInicial DESC
    LIMIT 10;
    """

    df = db.query(query)
    db.close_connection()

    # Criar um gráfico de barras com os dados
    plt.figure(figsize=(10, 6))  # Aumentar o tamanho da figura
    bars = plt.bar(df['TituloOriginal'], df['ArrecadacaoAnoInicial'])
    plt.ylabel('Bilheteria (Dólar)')
    plt.xlabel('Filme')
    plt.title('Os dez Filmes com maior bilheteria')
    plt.xticks(rotation=90)  # Rotacionar os títulos dos filmes para melhor visualização

    # Adicionar rótulos de dados em cima das barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

    plt.tight_layout() # Ajustar o layout do gráfico
    plt.show()


def get_best_actor_nominees():
    db = Connection3.DatabaseManager(Connection3.config)
    db.open_connection()

    # Lista os atores ou atrizes nominados como melhor ator em todos os eventos existentes
    query = """
    SELECT 
        p.NomeArt
    FROM 
        Pessoa p
    JOIN 
        Pessoas_Nomeadas pn ON p.IDPessoa = pn.IDPessoa
    JOIN 
        Premio pr ON pn.IDPremio = pr.IDPremio
    JOIN 
        Edicao e ON pn.IDEdicao = e.IDEdicao
    JOIN 
        Evento ev ON e.IDEvento = ev.IDEvento
    WHERE 
        pr.Nome LIKE '%Melhor Ator%' AND pn.Ganhou = 'S'
    GROUP BY 
        p.NomeReal
    HAVING 
        COUNT(DISTINCT ev.IDEvento) = 7;
    """

    df = db.query(query)
    db.close_connection()
    print()
    
    fig, ax = plt.subplots(1, 1)
    table_data = []
    for row in df.itertuples():
        table_data.append(row[1:])
    table = ax.table(cellText=table_data, cellLoc = 'center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    ax.axis('off')

    # Adicionar um título à tabela
    plt.suptitle('Artistas Premiados em Todos os Eventos', fontsize=14, fontweight='bold')

    plt.show()

    print()
    print('-' * 100)
    print()
    


def get_best_actor_awards():
    db = Connection3.DatabaseManager(Connection3.config)
    db.open_connection()

    # Consulta para Atores Nomeados e Premiados para o prêmio de Melhor Ator
    query = """
    SELECT DISTINCT
        p.NomeArt AS NomeArtistico,
        CASE
            WHEN EXISTS (
                SELECT 1
                FROM Pessoas_Nomeadas pn2
                JOIN Premio pr2 ON pn2.IDPremio = pr2.IDPremio
                WHERE pn2.IDPessoa = pn.IDPessoa AND pr2.Nome = 'Melhor Ator' AND pn2.Ganhou = 'S'
            ) THEN 'Sim'
            ELSE 'Não'
        END AS Ganhou
    FROM 
        Pessoas_Nomeadas pn
    JOIN 
        Pessoa p ON pn.IDPessoa = p.IDPessoa
    JOIN 
        Premio pr ON pn.IDPremio = pr.IDPremio
    WHERE 
        pr.Nome = 'Melhor Ator';
    """

    df = db.query(query)
    db.close_connection()
    print()
    
    df = df.rename(columns={"NomeArtistico": "Artista"})
    fig, ax = plt.subplots(1, 1)
    table_data = []
    for row in df.itertuples():
        table_data.append(row[1:])
    table = ax.table(cellText=table_data, colLabels=df.columns, cellLoc = 'center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    ax.axis('off')

    # Colocar o título da coluna em negrito
    for (row, col), cell in table.get_celld().items():
        if (row == 0):
            cell.get_text().set_weight('bold')

    # Adicionar um título à tabela
    plt.suptitle('Artistas Premiados (ao menos uma vez) ou Indicados para Melhor Ator/Atriz', fontsize=10, fontweight='bold')

    plt.show()
    print()
    print('-' * 100)
    print()


def get_best_protagonist_nominees():
    db = Connection3.DatabaseManager(Connection3.config)
    db.open_connection()

    # Consulta para Atores Nomeados e Premiados para o prêmio de Melhor Ator
    query = """
    SELECT DISTINCT
        p.NomeArt AS NomeArtistico,
        CASE
            WHEN EXISTS (
                SELECT 1
                FROM Pessoas_Nomeadas pn2
                JOIN Premio pr2 ON pn2.IDPremio = pr2.IDPremio
                WHERE pn2.IDPessoa = pn.IDPessoa AND pr2.Nome = 'Melhor Protagonista' AND pn2.Ganhou = 'S'
            ) THEN 'Sim'
            ELSE 'Não'
        END AS Ganhou
    FROM 
        Pessoas_Nomeadas pn
    JOIN 
        Pessoa p ON pn.IDPessoa = p.IDPessoa
    JOIN 
        Premio pr ON pn.IDPremio = pr.IDPremio
    WHERE 
        pr.Nome = 'Melhor Protagonista';
    """

    df = db.query(query)
    db.close_connection()
    print()
    
    df = df.rename(columns={"NomeArtistico": "Artista"})
    fig, ax = plt.subplots(1, 1)
    table_data = []
    for row in df.itertuples():
        table_data.append(row[1:])
    table = ax.table(cellText=table_data, colLabels=df.columns, cellLoc = 'center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(0.8, 1.3)
    ax.axis('off')

    # Colocar o título da coluna em negrito
    for (row, col), cell in table.get_celld().items():
        if (row == 0):
            cell.get_text().set_weight('bold')

    # Adicionar um título à tabela
    plt.suptitle('Artistas Premiados (ao menos uma vez) ou Indicados para Melhor Protagonista', fontsize=10, fontweight='bold')

    plt.show()
    print()
    print('-' * 100)
    print()


def get_best_narrative_nominees():
    db = Connection3.DatabaseManager(Connection3.config)
    db.open_connection()

    # Consulta para filmes nomeados ou premiados para melhor narrativa
    query = """
    SELECT 
        f.TituloOriginal,
        CASE
            WHEN MAX(fn.Premiado) = 'S' THEN 'Sim'
            ELSE 'Não'
        END AS Ganhou
    FROM 
        Filmes_Nomeados fn
    JOIN 
        Filme f ON fn.IDFilme = f.IDFilme
    JOIN 
        Premio pr ON fn.IDPremio = pr.IDPremio
    WHERE 
        pr.Nome = 'Melhor Narrativa'
    GROUP BY 
        f.TituloOriginal;
    """

    df = db.query(query)
    db.close_connection()
    print()
    
    df = df.rename(columns={"TituloOriginal": "Filme"})
    fig, ax = plt.subplots(1, 1)
    table_data = []
    for row in df.itertuples():
        table_data.append(row[1:])
    table = ax.table(cellText=table_data, colLabels=df.columns, cellLoc = 'center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    ax.axis('off')

    # Colocar o título da coluna em negrito
    for (row, col), cell in table.get_celld().items():
        if (row == 0):
            cell.get_text().set_weight('bold')

    # Adicionar um título à tabela
    plt.suptitle('Filmes Premiados (ao menos uma vez) ou Indicados para Melhor Narrativa', fontsize=10, fontweight='bold')

    plt.show()
    print()
    print('-' * 100)
    print()


def get_best_production_nominees():
    db = Connection3.DatabaseManager(Connection3.config)
    db.open_connection()

    # Consulta para filmes nomeados ou premiados como melhor produção
    query = """
    SELECT 
        f.TituloOriginal,
        CASE
            WHEN MAX(fn.Premiado) = 'S' THEN 'Sim'
            ELSE 'Não'
        END AS Ganhou
    FROM 
        Filmes_Nomeados fn
    JOIN 
        Filme f ON fn.IDFilme = f.IDFilme
    JOIN 
        Premio pr ON fn.IDPremio = pr.IDPremio
    WHERE 
        pr.Nome = 'Melhor Produção'
    GROUP BY 
        f.TituloOriginal;
    """

    df = db.query(query)
    db.close_connection()
    print()
    
    df = df.rename(columns={"TituloOriginal": "Filme"})
    fig, ax = plt.subplots(1, 1)
    table_data = []
    for row in df.itertuples():
        table_data.append(row[1:])
    table = ax.table(cellText=table_data, colLabels=df.columns, cellLoc = 'center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    ax.axis('off')

    # Colocar o título da coluna em negrito
    for (row, col), cell in table.get_celld().items():
        if (row == 0):
            cell.get_text().set_weight('bold')

    # Adicionar um título à tabela
    plt.suptitle('Filmes Premiados (ao menos uma vez) ou Indicados para Melhor Produção', fontsize=10, fontweight='bold')

    plt.show()
    print()
    print('-' * 100)
    print()