import pyray as pr
import math
from pyray import Vector3

def initialize_camera():
    """Initialise la caméra 3D."""
    camera = pr.Camera3D(
        Vector3(0, 10, 10),  # position
        Vector3(0, 0, 0),    # cible
        Vector3(0, 1, 0),    # haut
        45,                  # fovy (champ de vision dans la direction y)
        pr.CAMERA_PERSPECTIVE
    )
    return camera

def update_camera_position(camera, movement_speed):
    """Met à jour la position de la caméra en fonction des touches pressées."""
    if pr.is_key_down(pr.KEY_W):
        camera.position.z -= movement_speed
    if pr.is_key_down(pr.KEY_S):
        camera.position.z += movement_speed
    if pr.is_key_down(pr.KEY_A):
        camera.position.x -= movement_speed
    if pr.is_key_down(pr.KEY_D):
        camera.position.x += movement_speed
    if pr.is_key_down(pr.KEY_Q):
        camera.position.y += movement_speed
    if pr.is_key_down(pr.KEY_E):
        camera.position.y -= movement_speed

def rotate_vector_y(vector, angle):
    """Fait tourner un vecteur autour de l'axe Y selon un angle donné en radians."""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return Vector3(
        vector.x * cos_a - vector.z * sin_a,
        vector.y,
        vector.x * sin_a + vector.z * cos_a
    )
    
def draw_xyz(xyz):
    for c in xyz:
        pr.draw_sphere(c, 0.1, pr.RED)

def write_c(text, c, camera, font_size=20, color=pr.BLACK):
    text_position_2d = pr.get_world_to_screen(c, camera)
    if 0 <= text_position_2d.x <= pr.get_screen_width() and 0 <= text_position_2d.y <= pr.get_screen_height():
        pr.draw_text(text, int(text_position_2d.x), int(text_position_2d.y), font_size, color)
    else:
        print("La position du texte est hors des limites de l'écran :", text_position_2d)

def write_xyz(xyz, camera):
    write_c("X", xyz[0], camera)
    write_c("Y", xyz[1], camera)
    write_c("Z", xyz[2], camera)

def vector_length(vector):
    # TODO : implémenter le calcul de la longueur d'un vecteur (utiliser le produit scalaire cf. dot_product(A, B))
    return math.sqrt(dot_product(vector, vector))

def dot_product(A, B):
    return A.x*B.x + A.y*B.y + A.z*B.z

def draw_parallelogram(vector1, vector2):
    v0 = Vector3(0,0,0)
    v1_2 = pr.vector3_add(vector1, vector2)
    pr.draw_line_3d(v0, vector1, pr.RED)
    pr.draw_line_3d(v0, vector2, pr.RED)
    pr.draw_line_3d(vector1, v1_2, pr.RED)
    pr.draw_line_3d(vector2, v1_2, pr.RED)

    pr.draw_triangle_3d(v0, vector2, vector1, pr.BLUE)
    pr.draw_triangle_3d(vector1, vector2, v1_2, pr.BLUE)

def main():
    pr.init_window(800, 600, "FOV")
    camera = initialize_camera()
    pr.set_target_fps(60)
    grid_size = 15
    movement_speed = 0.1
    
    vector1 = Vector3(1, 0, 0)
    vector2 = Vector3(1, 1, 1)

    xyz = [Vector3(1, 0, 0),Vector3(0, 1, 0),Vector3(0, 0, 1)]

    while not pr.window_should_close():
        update_camera_position(camera, movement_speed)
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_3d(camera)

        draw_parallelogram(vector1, vector2)
        #draw_xyz(xyz)
        pr.draw_grid(grid_size, 1)  # Dessine une grille pour référence

        pr.end_mode_3d()

        #write_xyz(xyz, camera)

        pr.end_drawing()

    pr.close_window()

# Lancer le programme principal
if __name__ == "__main__":
    main()
