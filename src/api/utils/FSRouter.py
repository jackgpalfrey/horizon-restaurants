"""Module for managing flask routes with the file system."""
from flask import Flask, request
from typing import Callable, Any
import importlib
import os

from marshmallow import Schema, ValidationError

from src.api.utils.Result import Error, Status


class FSRouter():
    """Class for handling routes with the file system."""

    def __init__(self, app: Flask):
        """Initalised router with flask app."""
        self.app = app
        self._parent_dir: str = ""
        self._routes: dict[str, Callable] = {}

    def load_dir(self, path: str):
        """Load directory as route folder."""
        self._parent_dir = path
        self._load_dir(path)

    def _load_dir(self, path: str):
        files = os.scandir(path)
        sorted_files = sorted(files, key=lambda entry: entry.name)

        for file in sorted_files:
            if file.name.startswith("__"):
                continue
            if file.is_file():
                self._load_route_file(file.path)
            else:
                self._load_dir(file.path)

    def _load_route_file(self, path: str):
        typeless = path.replace(".py", "")
        endpoint = typeless.replace(self._parent_dir, "")
        print(f"Loading endpoint '{endpoint}' from {path}", flush=True)

        module = importlib.import_module(typeless.replace("/", "."))
        members = dir(module)
        print(members)

        methods = []
        if "get" in members:
            methods.append("GET")

        if "post" in members:
            methods.append("POST")

        schemas: dict[str, type[Schema]] = {}
        if "PostSchema" in members:
            schemas["POST"] = module.PostSchema

        for schema_name in schemas:
            schema = schemas[schema_name]
            if not issubclass(schema, Schema):
                raise Exception("Invalid Schema")

        guard_func = module.guard if "guard" in members else lambda: None

        def route_handler():
            guard_result = guard_func()
            if guard_result is not None:
                return guard_result

            match(request.method):
                case "GET":
                    return module.get()

                case "POST":
                    if "POST" in schemas:
                        json: Any = request.json

                        schema = schemas["POST"]()
                        try:
                            body = schema.load(json)
                            assert type(body) is dict
                        except ValidationError as e:
                            return Error(Status.SERVER_ERROR,
                                         "Invalid Body",
                                         e.messages)

                        return module.post(body)

                    return module.post()

            raise Exception("Unrecognised Method")

        self.app.add_url_rule(endpoint, methods=methods, endpoint=endpoint, view_func=route_handler)
