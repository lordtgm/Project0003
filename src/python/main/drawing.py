from math import cos, pi, radians, sin

from PIL import Image, ImageDraw

pi2 = pi / 2


def generate_timer(outer: int, inner: int, thickness: int, total: int, on: int, red: bool) -> Image.Image:
    color = (0xFF, 0x00, 0x00) if red else (0xFF, 0x91, 0x4D)
    img = Image.new("RGBA", (outer * 2, outer * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    angle = radians(360 / total)
    for i in range(total):
        inner_x = outer - cos(i * angle - pi2) * inner
        inner_y = outer + sin(i * angle - pi2) * inner
        outer_x = outer - cos(i * angle - pi2) * outer
        outer_y = outer + sin(i * angle - pi2) * outer
        if on > 0:
            draw.line((inner_x, inner_y, outer_x, outer_y), fill=color, width=thickness)
            on -= 1
        else:
            draw.line((inner_x, inner_y, outer_x, outer_y), fill=(127, 127, 127), width=thickness * 4 // 5)
    return img
