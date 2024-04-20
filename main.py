import arcade, map_generator, time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Mario Politic Miros"
CHARACTER_SCALING = 0.20
TILE_SCALING = 3
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
COIN_SCALING = 0.25

class MyGame(arcade.Window):  # trzeba zmienic na view
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        self.wall_list = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

        self.MODULE_NUMBER = 0

    def setup(self):
        # sprite list
        self.wall_list = arcade.SpriteList()

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Initialize Scene
        self.scene = arcade.Scene()

        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Keep track of the score
        self.score = 0
        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        for x in range(1250, 2500, 256):
            coin = arcade.Sprite("vote.jpg", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.scene.add_sprite("Coins", coin)

        player_image_source = "mario.jpg"
        self.player_sprite = arcade.Sprite(player_image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 96
        self.scene.add_sprite("Player", self.player_sprite)


        for i in range(1):
            self.MODULE_NUMBER = 0
            map_generator.przeszkoda1(self.MODULE_NUMBER, self, TILE_SCALING)

        # for x in range(0, 10000, 32):

        # wall = arcade.Sprite("brick.png", TILE_SCALING)

        # wall = arcade.Sprite("brick.png", TILE_SCALING)

        # wall.center_x = x
        # wall.center_y = 16
        # self.scene.add_sprite("Walls", wall)

        # coordinate_list = [[224, 64], [256, 64], [256, 96], [256, 128], [256, 160], [256, 192], [256, 224], [896, 64],
        # [896, 96], [896, 128], [896, 160], [896, 192], [896, 224], [512, 224], [720, 224]]


        # self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY,
                                                             walls=self.scene["Walls"])

    # for wall in self.scene["Walls"]:
    # print(wall.center_x)
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Vote: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

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
        """Movement and game logic"""

        if (self.player_sprite.center_x - self.scene["Walls"][0].center_x > 1000):
            print("trzeba usunac")
            self.scene["Walls"][0].remove_from_sprite_lists()
        if (self.player_sprite.center_x - self.scene["Walls"][-1].center_x > -1000):
            print("trzeba generowac")
            self.MODULE_NUMBER += 1
            map_generator.przeszkoda1(self.MODULE_NUMBER, self, TILE_SCALING)
        elif (self.player_sprite.center_x - self.scene["Walls"][-1].center_x < -1000):
            print("nie trzeba generowac")
            print(self.player_sprite.center_x - self.scene["Walls"][-1].center_x)


        # Move the player with the physics engine
        self.physics_engine.update()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            self.score += 1

        # Position the camera
        self.center_camera_to_player()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
