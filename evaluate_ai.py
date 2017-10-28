from beste_ki import beste_ki
from tron import tron

GAME_STEPS = 10

game = tron.TronGame(width=30, height=30)

for i in range(GAME_STEPS):
    print(game)

    player1 = beste_ki.Beste_ki(0)

    player2 = beste_ki.Beste_ki(1)

    for player in [player1, player2]:
        game_state = game.get_game_state_as_class()

        ki_action = player.predict(game_state)
        game.set_action(player.player, ki_action)

    if game.game_over():
        for player in [player1, player2]:
            game_state = game.get_game_state_as_class()

            ki_action = player.predict(game_state)
        break