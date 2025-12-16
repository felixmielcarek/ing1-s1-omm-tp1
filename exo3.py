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

def draw_fov_cone(point, direction, distance, angle_phi, color=pr.BLUE, segments=20):
    """
    Dessine un secteur circulaire représentant le champ de vision (FOV) 2D dans la direction d'un vecteur donné.
    
    :param point: Point de départ du cône (Vector3).
    :param direction: Vecteur de direction pour le centre du cône.
    :param distance: Portée maximale du FOV.
    :param angle_phi: Angle du FOV en degrés.
    :param color: Couleur du FOV.
    :param segments: Nombre de segments pour approximer le secteur circulaire.
    """
    
    # Normalise le vecteur de direction
    direction = vector_normalize(direction)
    
    # Convertit l'angle en radians et calcule l'angle demi
    half_angle_rad = math.radians(angle_phi / 2)
    
    # Calcule les points le long de l'arc du FOV
    angle_step = (2 * half_angle_rad) / segments
    points = []
    
    for i in range(segments + 1):
        # Calcule l'angle de rotation pour chaque segment
        rotation_angle = -half_angle_rad + i * angle_step
        rotated_direction = rotate_vector_y(direction, rotation_angle)
        
        # Redimensionne la direction tournée par la distance et traduit par le point de départ
        arc_point = Vector3(
            point.x + rotated_direction.x * distance,
            point.y + rotated_direction.y * distance,
            point.z + rotated_direction.z * distance
        )
        points.append(arc_point)
    
    # Dessine des lignes du point vers chaque segment d'arc et entre les segments consécutifs
    for i in range(len(points) - 1):
        pr.draw_line_3d(point, points[i], color)
        pr.draw_line_3d(points[i], points[i + 1], color)
    
    # Dessine le dernier segment reliant l'extrémité de l'arc au point de départ
    pr.draw_line_3d(point, points[-1], color)

def draw_vector_3(start, end, color, thickness=0.05, head_size_factor=0.8):
    """Dessine un vecteur en utilisant un cylindre et un cône."""
    direction = Vector3(end.x - start.x, end.y - start.y, end.z - start.z)
    length = vector_length(direction)
    head_size = length * head_size_factor
    
    n_direction = vector_normalize(direction)
    
    arrow_start = Vector3(start.x + n_direction.x * head_size, 
                          start.y + n_direction.y * head_size, 
                          start.z + n_direction.z * head_size)
    
    pr.draw_cylinder_ex(start, end, thickness / 2, thickness / 2, 8, color)
    pr.draw_cylinder_ex(arrow_start, end, thickness * 2, thickness / 5, 8, color)

def draw_points(points):
    for point in points:
        pr.draw_sphere(point, 0.1, pr.RED)

def draw_text_if_visible_3(camera, text, position_3d, font_size=20, color=pr.BLACK):
    """
    Affiche le texte à une position 2D projetée à partir d'une coordonnée 3D si elle est dans les limites de l'écran.
    
    :param camera: La caméra utilisée pour la projection.
    :param text: Texte à afficher.
    :param position_3d: Position 3D du texte.
    :param font_size: Taille de la police du texte.
    :param color: Couleur du texte.
    """
    text_position_2d = pr.get_world_to_screen(position_3d, camera)
    if 0 <= text_position_2d.x <= pr.get_screen_width() and 0 <= text_position_2d.y <= pr.get_screen_height():
        pr.draw_text(text, int(text_position_2d.x), int(text_position_2d.y), font_size, color)
    else:
        print("La position du texte est hors des limites de l'écran :", text_position_2d)

def draw_vectors(points):
    for i in range(len(points) - 1):
        draw_vector_3(points[i], points[i + 1], pr.BLUE)

def vector_length(vector):
    # TODO : implémenter le calcul de la longueur d'un vecteur (utiliser le produit scalaire cf. dot_product(A, B))
    return math.sqrt(dot_product(vector, vector))

def vector_normalize(vector):
    #TODO : mettre en œuvre la normalisation d'un vecteur
    length = vector_length(vector)
    return Vector3(vector.x/length,vector.y/length,vector.z/length)

def dot_product(A, B):
    return A.x*B.x + A.y*B.y + A.z*B.z

def rotate_vector_y(vector, angle):
    """Fait tourner un vecteur autour de l'axe Y selon un angle donné en radians."""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return Vector3(
        vector.x * cos_a - vector.z * sin_a,
        vector.y,
        vector.x * sin_a + vector.z * cos_a
    )

def is_point_in_fov(fov_position, fov_direction, fov_distance, fov_angle, point):
    """
    Vérifie si un point est dans le champ de vision défini par une position, une direction, une distance et un angle.
    
    :param fov_position: Position du point de départ de FOV.
    :param fov_direction: Direction centrale du FOV.
    :param fov_distance: Distance maximale de portée de la FOV.
    :param fov_angle: Angle du FOV en degrés.
    :param point: Point à vérifier.
    :return: True si le point est dans le champ de vision, sinon False.
    """
    # TODO : Vecteur du FOV vers le point
    to_point = Vector3(point.x, point.y, point.z)
    
    # TODO : Calcule la distance au point et vérifie qu'elle est dans la distance FOV
    dist_to_point= math.sqrt(
        (point.x-fov_position.x)**2 +
        (point.y-fov_position.y)**2 +
        (point.z-fov_position.z)**2
    )
    if fov_distance < dist_to_point:
        return False
    
    # Normalise la direction du FOV et le vecteur vers le point
    norm_fov_direction = vector_normalize(fov_direction)
    norm_to_point = vector_normalize(to_point)
    
    # TODO: Calcule le produit scalaire
    dot_product_fov_point = dot_product(norm_fov_direction, norm_to_point)
    if dot_product_fov_point < 0:
        return False

    # TODO Calcule le cosinus de l'angle demi du FOV
    cos_half_angle = math.cos(fov_angle/2)

    # TODO Vérifie si le produit scalaire satisfait la condition du FOV
    cos_theta = dot_product_fov_point / (dist_to_point * fov_distance)
    if cos_theta < cos_half_angle:
        return True
    else:
        return False

def main():
    pr.init_window(800, 600, "FOV")
    camera = initialize_camera()
    pr.set_target_fps(60)
    grid_size = 15
    movement_speed = 0.1
    
    fov_position = Vector3(0, 0, 0)
    fov_direction = Vector3(0, 0, 1)  # Vecteur directeur du cône
    point_a = Vector3(1.5, 0, 2)
    point_b = Vector3(2, 0, 4)
    point_c = Vector3(-5, 0, 4)
    fov_distance = 5
    fov_angle = 90

    while not pr.window_should_close():
        update_camera_position(camera, movement_speed)
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)
        pr.begin_mode_3d(camera)

        pr.draw_grid(grid_size, 1)  # Dessine une grille pour référence
        draw_points([point_a, point_b, point_c])
        draw_fov_cone(fov_position, fov_direction, fov_distance, fov_angle)

        pr.end_mode_3d()

        a_point_of_fov = is_point_in_fov(fov_position, fov_direction, fov_distance, fov_angle, point_a)
        b_point_of_fov = is_point_in_fov(fov_position, fov_direction, fov_distance, fov_angle, point_b)
        c_point_of_fov = is_point_in_fov(fov_position, fov_direction, fov_distance, fov_angle, point_c)
        draw_text_if_visible_3(camera, str(a_point_of_fov) , point_a, font_size=20, color=pr.BLACK)
        draw_text_if_visible_3(camera, str(b_point_of_fov) , point_b, font_size=20, color=pr.BLACK)
        draw_text_if_visible_3(camera, str(c_point_of_fov) , point_c, font_size=20, color=pr.BLACK)

        pr.end_drawing()

    pr.close_window()

# Lancer le programme principal
if __name__ == "__main__":
    main()
