import pygame


def load_animation_frames(sheet_path, frame_width, frame_height, rows=1, cols=None):
    """
    Wczytuje klatki animacji z jednego obrazka (sprite sheet).

    :param sheet_path: Ścieżka do pliku z animacją
    :param frame_width: Szerokość jednej klatki
    :param frame_height: Wysokość jednej klatki
    :param rows: Liczba wierszy (domyślnie 1)
    :param cols: Liczba kolumn (jeśli None, obliczana automatycznie z szerokości obrazka)
    :return: Lista klatek jako Surface'y
    """
    sheet = pygame.image.load(sheet_path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()

    if cols is None:
        cols = (sheet_width // frame_width)

    frames = []
    for row in range(rows):
        for col in range(cols):
            frame_rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            frame = sheet.subsurface(frame_rect)
            frames.append(frame)

    return frames
def load_single_frame(sheet_path, frame_width, frame_height, frame_index=0, row=0):
    sheet = pygame.image.load(sheet_path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()

    cols = sheet_width // frame_width
    x = (frame_index % cols) * frame_width
    y = row * frame_height

    frame_rect = pygame.Rect(x, y, frame_width, frame_height)
    return sheet.subsurface(frame_rect)
def scaleAnimationFrames(frames):
    return [pygame.transform.scale2x(frame) for frame in frames]