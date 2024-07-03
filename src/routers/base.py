from fastapi.routing import APIRouter as BaseAPIRouter


class APIRouter(BaseAPIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_url_patterns(self, view, instance_id):
        url_list = [
            {"path": "/", "view": view.create, "method": "POST"},
            {"path": "/", "view": view.read_all, "method": "GET"},
            {"path": f"/{instance_id}", "view": view.read_one, "method": "GET"},
            {"path": f"/{instance_id}", "view": view.put, "method": "PUT"},
            {"path": f"/{instance_id}", "view": view.patch, "method": "PATCH"},
            {"path": f"/{instance_id}", "view": view.delete, "method": "DELETE"}
        ]

        for url in url_list:
            path = url.get("path")
            view = url.get("view")
            method = url.get("method")

            self.add_api_route(path, view, methods=[method])
