#!/usr/bin/env python3
import http.client
import json
import os
import pathlib
import subprocess
import sys
import urllib.request

outdir = pathlib.Path("./superslicer-releases")
outdir.mkdir(parents=True, exist_ok=True)


def human_size(bytes: int) -> str:
    suffices = ["B", "KB", "MB", "GB", "TB"]
    for s in suffices:
        if bytes < 1024:
            return f"{bytes:0.1f}{s}"
        bytes /= 1024


def report_progress(asset_file):
    def reporter(count, block_size, total_size):
        tcols = os.get_terminal_size().columns
        percent = int(count * block_size * 100 / total_size)

        print(
            f"{asset_file}: {percent:0.1f}% ({human_size(count * block_size)} / {human_size(total_size)})".ljust(
                tcols - 1, " "
            ),
            end="\r",
            file=sys.stderr,
            flush=True,
        )
        if count * block_size >= total_size:
            print("", file=sys.stderr)

    return reporter


def build_image(tag_name, asset_file):
    return subprocess.run(
        [
            "docker",
            "build",
            "--tag",
            f"kageurufu/superslicer:{tag_name}",
            "--build-arg",
            f"SUPERSLICER={asset_file.name}",
            "-f",
            "Dockerfile",
            ".",
        ],
        check=True,
    )


def tag_image(version, tag):
    return subprocess.run(
        [
            "docker",
            "tag",
            f"kageurufu/superslicer:{version}",
            f"kageurufu/superslicer:{tag}",
        ],
        check=True,
    )


releases = json.load(
    urllib.request.urlopen(
        "https://api.github.com/repos/supermerill/SuperSlicer/releases"
    )
)

nightly_version = None
latest_version = None

for idx, release in enumerate(releases):
    if idx >= 10 and nightly_version and latest_version:
        break

    tag_name = release["tag_name"]
    asset = next(
        (asset for asset in release["assets"] if "linux64" in asset["name"]), None
    )

    if not asset:
        print("\n".join(asset["name"] for asset in release["assets"]))
        continue

    asset_file: pathlib.Path = outdir / asset["name"]
    if not asset_file.is_file():
        try:
            urllib.request.urlretrieve(
                asset["browser_download_url"],
                asset_file,
                reporthook=report_progress(asset_file),
            )
        except:
            if asset_file.is_file():
                asset_file.unlink()
            raise

    if not build_image(tag_name, asset_file):
        raise ValueError("failed to build %s", tag_name)

    if not nightly_version and release["prerelease"] is True:
        nightly_version = tag_name
        print(tag_image(tag_name, "nightly"))

    elif not latest_version and release["prerelease"] is False:
        latest_version = tag_name
        print(tag_image(tag_name, "latest"))

    break