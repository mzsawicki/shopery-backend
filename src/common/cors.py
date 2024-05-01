import typing


def parse_origins(origins_param: str) -> typing.List:
    return origins_param.split(",")
