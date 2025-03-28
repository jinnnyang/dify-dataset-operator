from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class ListDatasets(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = self.runtime.credentials["knowledge_api_key"]
        url = f"{self.runtime.credentials['knowledge_api_url'].strip('/')}/datasets"
        page = tool_parameters.get("page", 1)
        limit = tool_parameters.get("limit", 20)

        resp = requests.get(
            url=url,
            params={"page": page, "limit": limit},
            headers={"Authorization": f"Bearer {key}"},
        )
        print(f"key: {key}", f"url: {url}", "Resp: {resp.text}")

        yield self.create_json_message(resp.json())
