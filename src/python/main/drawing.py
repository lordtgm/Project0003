from math import sin, cos, radians
from PIL import Image, ImageDraw


def generate_timer(outer: int, inner: int, thickness:int, total: int, on: int) -> Image.Image:
    img = Image.new("RGBA", (outer * 2, outer * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    angle = radians(360 / total)
    for i in range(total):
        inner_x = outer - cos(i * angle) * inner
        inner_y = outer + sin(i * angle) * inner
        outer_x = outer - cos(i * angle) * outer
        outer_y = outer + sin(i * angle) * outer
        if on > 0:
            draw.line((inner_x, inner_y, outer_x, outer_y), fill=(0xFF, 0x91, 0x4D), width=thickness)
            on -= 1
        else:
            draw.line((inner_x, inner_y, outer_x, outer_y), fill=(127, 127, 127), width=thickness*4//5)
    return img


if __name__ == "__main__":
    generate_timer(1000, 500, 50, 36, 10).save(r"\Users\HOME\Desktop\image.png")
