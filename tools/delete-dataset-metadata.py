from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# curl --location --request DELETE 'https://api.dify.ai/v1/datasets/{dataset_id}/metadata/{metadata_id}' \
# --header 'Authorization: Bearer {api_key}'


class DeleteDatasetMetadata(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = self.runtime.credentials["knowledge_api_key"]
        dataset_id = tool_parameters.get("dataset_id")
        metadata_id = tool_parameters.get("metadata_id")
        url = f"{self.runtime.credentials['knowledge_api_url'].strip('/')}/datasets/{dataset_id}/metadata/{metadata_id}"

        resp = requests.delete(
            url=url,
            headers={
                "Authorization": f"Bearer {key}",
            },
        )
        print(
            f"key: {key}",
            f"url: {url}",
        )

        print(resp.status_code)

        yield self.create_json_message(
            {
                "status": resp.status_code,
                "message": "success" if resp.status_code == 200 else "failed",
            }
        )
