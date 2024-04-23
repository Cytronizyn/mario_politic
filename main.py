import arcade
import map_generator
import time

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Mario Politic Miros"
CHARACTER_SCALING = 2
TILE_SCALING = 1
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 2
PLAYER_JUMP_SPEED = 15
COIN_SCALING = 1


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.GAME_PAUSED = False
        self.remove_msg_displayed = False
        self.generate_msg_displayed = False
        self.no_generate_msg_displayed = False
        self.current_display_image = None
        self.display_time = None
        self.collected_coins = []
        self.open_list = []
        self.background = None
        self.scene = None
        self.player_sprite = None
        self.wall_list = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None
        self.score = 0
        self.MODULE_NUMBER = 0
        self.paused_start_time = None

    def setup(self):
        self.background = arcade.load_texture("tlo.png")
        self.wall_list = arcade.SpriteList()
        self.camera = arcade.Camera(self.width, self.height)
        self.scene = arcade.Scene()
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.score = 0

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        for x in range(1250, 2500, 256):
            coin = arcade.Sprite("list_still.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.scene.add_sprite("Coins", coin)

        player_image_source = "mario.png"
        self.player_sprite = arcade.Sprite(player_image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 64
        self.scene.add_sprite("Player", self.player_sprite)

        for i in range(1):
            self.MODULE_NUMBER = 0
            map_generator.przeszkoda1(self.MODULE_NUMBER, self, TILE_SCALING)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY,
                                                             walls=self.scene["Walls"])
        arcade.schedule(self.on_update, 1 / 60)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT,
                                      self.background)
        self.clear()
        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()
        score_text = f"Vote: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)
        arcade.finish_render()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        if (self.player_sprite.center_x - self.scene["Walls"][0].center_x > 1024):
            self.scene["Walls"][0].remove_from_sprite_lists()
        if (self.player_sprite.center_x - self.scene["Walls"][-1].center_x > -1024):
            self.MODULE_NUMBER += 1
            map_generator.przeszkoda1(self.MODULE_NUMBER, self, TILE_SCALING)
        elif (self.player_sprite.center_x - self.scene["Walls"][-1].center_x < -1024):
            print(self.player_sprite.center_x - self.scene["Walls"][-1].center_x)

        self.physics_engine.update()

        # Sprawdź kolizje z monetami i zaktualizuj obrazy monet po ich zebraniu
        if not self.GAME_PAUSED:
            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Coins"])
        # Sprawdź kolizje z kopertą i zatrzymaj grę na 3 sekundy, wyświetlając obraz
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Coins"])
        for coin in coin_hit_list:
            if coin not in self.collected_coins:
                if coin not in self.open_list:
                    self.collected_coins.append(coin)  # Dodaj monetę do listy zebranych monets
                    self.open_list.append(coin)
                    self.score += 1  # Zwiększ wynik
                    self.GAME_PAUSED = True
                    self.paused_start_time = time.time()
                    self.display_image("list.png", 1)
                    time.sleep(1)# Wyświetl obrazek przez 3 sekundy

                # Zaktualizuj obrazek zebranej monet
                coin.texture = arcade.load_texture("list_open.png")
                print("Zdobyłeś monetę! Twój wynik to:", self.score)

        if not self.GAME_PAUSED:
            self.physics_engine.update()
            self.center_camera_to_player()


        if self.GAME_PAUSED:
            # Sprawdź, czy minęło wystarczająco czasu, aby wznowić grę
            if time.time() - self.paused_start_time >= 3:
                self.GAME_PAUSED = False

    def display_image(self, image_path, display_time):
        self.current_display_image = arcade.load_texture(image_path)
        self.display_time = display_time

        arcade.start_render()
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.current_display_image.width,
                                      self.current_display_image.height, self.current_display_image)
        arcade.finish_render()

        arcade.schedule(self.finish_display_image, self.display_time)

    def finish_display_image(self, delta_time):
        self.clear()
        self.on_draw()
        arcade.unschedule(self.finish_display_image)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()