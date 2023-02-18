import click
import requests


@click.command(help="Downloads the file from the url to the specified filename")
@click.option('--name', type=click.Path(), help="Name of the file with extension")
@click.argument('url_of_file', type=click.Path())
def download_file(url_of_file, name):
    r = requests.head(url_of_file)
    if name:
        file_name = name
    else:
        file_name = url_of_file.split("/")[-1]

    r = requests.get(url_of_file, stream=True)
    with open(file_name, "w+b") as f:
        f.write(r.content)


if __name__ == "__main__":
    download_file(obj={})
