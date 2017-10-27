from beste_ki.beste_ki import predict
from tron import tron

GAME_STEPS = 10

game = tron.TronGame(width=30, height=30)

for i in range(GAME_STEPS):
    print(game)
    if game.game_over():
        break
    for player in range(0, 2):

        game_state = game.get_game_state()
        is_game_over, game_field, player_pos, player_orientation, player_lost = game_state

        ki_action = predict(game_state)
        game.set_action(player, ki_action)

