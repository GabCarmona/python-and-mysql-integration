import Functions as f

def menu():
    while True:
        print()
        print('''O que deseja fazer?
              
        A - Os dez Atores com maior número de prêmios
        B - Os dez filmes mais premiados
        C - Os dez filmes com maior arrecadação
        D - Atores/atrizes nominados com melhor ator/atriz em todos os eventos existentes
        E - Dado um prêmio, encontrar atores/atrizes ou filmes nominados e premiados
        S - Sair
        ''')

        opcao = input('Digite a letra correspondente a sua opção: ').upper()

        if opcao == 'A':
            f.get_top_awarded_actors() 
        elif opcao == 'B':
            f.get_top_awarded_films() 
        elif opcao == 'C':
            f.get_top_grossing_films() 
        elif opcao == 'D': 
            f.get_best_actor_nominees()
        elif opcao == 'E':  
            print('Estes são os prêmios disponíveis:')
            print('''
        F) Melhor Ator/Atriz
        G) Melhor Protagonista
        H) Melhor Narrativa
        I) Melhor Produção ''')
            print()
            premio = input('Digite a letra correspondente ao prêmio que deseja consultar: ').upper()

            if premio == 'F':
                f.get_best_actor_awards()
            elif premio == 'G':
                f.get_best_protagonist_nominees()
            elif premio == 'H':
                f.get_best_narrative_nominees()
            elif premio == 'I':
                f.get_best_production_nominees()
            else:
                print()
                print('Prêmio inválido! Voltando ao menu...')
                print()
                print('-' * 100)
                print()
        elif opcao == 'S':
            print('Saindo do programa...')
            break
        else:
            print('Opção inválida! Tente novamente.')

menu()