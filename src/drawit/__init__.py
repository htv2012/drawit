import drawtree
import click


@click.command
@click.argument("seq", nargs=-1)
def main(seq):
    seq = ["#" if token=="null" else token for token in seq]
    text = f"{{{','.join(seq)}}}"
    drawtree.draw_level_order(text)

