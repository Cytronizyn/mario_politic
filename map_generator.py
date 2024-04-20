import arcade

def przeszkoda1(nrmodulu, scena, TILE_SCALING):
  x = nrmodulu * 16 * 12 * TILE_SCALING #kazdy modul ma 12 blokow * 16px * TILE_SCALING ABY WYMIARY SIE ZGADZALY
  coordinates_list = [[x, 24]]

  for i in range(12): # tworzenie listy 12 bloków w osi x
    coordinates_list.append([x, 24])
    x+=16 * TILE_SCALING  #przesuniecie koordynatow bloku o 16 w osi x

  for coordinate in coordinates_list: #generowanie na mapie
      wall = arcade.Sprite("brick.png", TILE_SCALING)
      wall.center_x = coordinate[0]
      wall.center_y = coordinate[1]
      scena.scene.add_sprite("Walls", wall)

