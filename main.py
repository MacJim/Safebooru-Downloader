import os
import argparse


def main(images_dir: str, start_url: str):
    pass


if __name__ == '__main__':
    print(f"Working directory: {os.getcwd()}")

    parser = argparse.ArgumentParser()
    parser.add_argument("--images_dir", "-d", type=str, default="images/")
    parser.add_argument("start_url", type=str)
    args = parser.parse_args()

    main(args.images_dir, args.start_url)
