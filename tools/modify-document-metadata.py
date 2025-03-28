from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# curl --location 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/metadata' \
# --header 'Content-Type: application/json' \
# --header 'Authorization: Bearer {api_key}' \
# --data '{
#     "operation_data":[
#         {
#             "document_id": "3e928bc4-65ea-4201-87c8-cbcc5871f525",
#             "metadata_list": [
#                     {
#                     "id": "1887f5ec-966f-4c93-8c99-5ad386022f46",
#                     "value": "dify",
#                     "name": "test"
#                 }
#             ]
#         }
#     ]
# }'


class ModifyDocumentMetadata(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = self.runtime.credentials["knowledge_api_key"]
        dataset_id = tool_parameters.get("dataset_id")
        document_id = tool_parameters.get("document_id")
        json_list_metadata = tool_parameters.get("json_list_metadata")
        url = f"{self.runtime.credentials['knowledge_api_url'].strip('/')}/datasets/{dataset_id}/documents/metadata"

        operation_data = [
            {"document_id": document_id, "metadata_list": json_list_metadata}
        ]

        resp = requests.post(
            url=url,
            json={"operation_data": operation_data},
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        print(
            f"key: {key}",
            f"url: {url}",
            f"document_id: {document_id}",
            f"json_list_metadata: {json_list_metadata}",
        )

        print(resp.json())

        yield self.create_json_message(resp.json())
