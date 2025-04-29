def answer_question(data, question):
    # Exemplo mínimo: artilheiro
    if "artilheiro" in question.lower():
        artilheiros = {}
        for jogo in data["jogos"]:
            for gol in jogo.get("gols", []):
                jogador = gol["jogador"]
                artilheiros[jogador] = artilheiros.get(jogador, 0) + 1
        if artilheiros:
            max_gols = max(artilheiros.values())
            lideres = [j for j, g in artilheiros.items() if g == max_gols]
            return f"Artilheiro(s): {', '.join(lideres)} com {max_gols} gols."
    return "Pergunta ainda não reconhecida nesta versão."