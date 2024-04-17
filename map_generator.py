import arcade


def chooseblock(block):
  return print(block+'.png', end=" ")

mapa1 = '''
xxxxx
x...x
'''

print(mapa1)

def printmap(mapa):
  for i in range(len(mapa)):
    for j in range(len(mapa[i])):
        chooseblock(mapa[i][j])


print(printmap(mapa1))



def przeszkoda1(nrmodulu):
  x = nrmodulu * 16 * 12  #kazdy modul ma 12 blokow * 16px
  coordinates_list  = [[x, 12]]
  for i in range(12):
    coordinates_list = [[x, 12]]
    x+=16  #przesuniecie koordynatow bloku o 16 w osi x

  for coordinate in coordinates_list:
      wall = arcade.Sprite("brick.png", TILE_SCALING)
      wall.position = coordinate
      self.scene.add_sprite("Walls", wall)
      self.physics_engine = arcade.PhysicsEnginePlatformer(
        self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
      )


def przeszkoda1_coinsy(nrmodulu):
  x = nrmodulu * 16 * 12 #kazdy modul ma 12 blokow * 16px
  coordinates_coinsy = [[x, y]]
  for i in range(12):
    coordinates_przeszkoda = [[x, 12]]
    x+=16
    print(coordinates_przeszkoda)
  for coordinate in coordinates_coinsy:
        coin = arcade.Sprite("vote.jpg", COIN_SCALING)
        coin.center_x = x
        coin.center_y = 96
        self.scene.add_sprite("Coins", coin)


print(przeszkoda1(0))
print(przeszkoda1(1))
print(przeszkoda1(2))
print(przeszkoda1(3))
