from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# curl --location 'https://api.dify.ai/v1/datasets/{dataset_id}/metadata' \
# --header 'Content-Type: application/json' \
# --header 'Authorization: Bearer {api_key}' \
# --data '{
#     "type":"string",
#     "name":"test"
# }'


class AddDatasetMetadata(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = self.runtime.credentials["knowledge_api_key"]
        dataset_id = tool_parameters.get("dataset_id")
        url = f"{self.runtime.credentials['knowledge_api_url'].strip('/')}/datasets/{dataset_id}/metadata"

        metadata_type = tool_parameters.get("metadata_type")
        metadata_name = tool_parameters.get("metadata_name")

        resp = requests.post(
            url=url,
            json={"type": metadata_type, "name": metadata_name},
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        print(
            f"key: {key}",
            f"url: {url}",
            f"type: {metadata_type}",
            f"name: {metadata_name}",
        )

        print(resp.json())

        yield self.create_json_message(resp.json())
