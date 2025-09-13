import os

import click
from win2xcur import parser
from wand.image import Image


def to_concated_image(ani_raw_data: bytes):
    ani = parser.ANIParser(ani_raw_data)
    output_image = Image()
    first_image = ani.frames[0].images[0].image
    output_image.blank(first_image.width, len(ani.frames)*first_image.height)
    for i, frame in enumerate(ani.frames):
        current_image = frame.images[0].image
        output_image.composite(current_image, 0, i * first_image.height)
    return output_image


def save_zoomed_images(image: Image, filename_prefix: str):
    image.save(filename=filename_prefix+".png")
    with image.clone() as resize:
        resize.scale(2*image.width, 2*image.height)
        resize.save(filename=filename_prefix+"_2x.png")
    with image.clone() as resize:
        resize.scale(5*image.width, 5*image.height)
        resize.save(filename=filename_prefix+"_5x.png")
    with image.clone() as resize:
        resize.scale(10*image.width, 10*image.height)
        resize.save(filename=filename_prefix+"_10x.png")


@click.command()
@click.argument("loaddir")
@click.argument("savedir")
def run(loaddir, savedir):
    if not os.path.exists(savedir):
        os.mkdir(savedir)

    for entry in os.scandir(loaddir):
        if not entry.path.endswith(".ani"):
            continue

        with open(entry.path, "rb") as f:
            image = to_concated_image(f.read())
            save_zoomed_images(image, savedir + "/" +
                               os.path.basename(entry.path)[:-4])


if __name__ == "__main__":
    run()
