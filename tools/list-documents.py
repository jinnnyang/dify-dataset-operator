from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# curl --location --request GET 'https://api.dify.ai/v1/datasets/{dataset_id}/documents' \
# --header 'Authorization: Bearer {api_key}'


class listeDocuments(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = self.runtime.credentials["knowledge_api_key"]
        dataset_id = tool_parameters.get("dataset_id")
        url = f"{self.runtime.credentials['knowledge_api_url'].strip('/')}/datasets/{dataset_id}/documents"

        resp = requests.get(
            url=url,
            headers={
                "Authorization": f"Bearer {key}",
            },
        )
        print(
            f"key: {key}",
            f"url: {url}",
        )

        print(resp.json())

        yield self.create_json_message(resp.json())
