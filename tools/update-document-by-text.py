from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# curl --location --request POST 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}/update-by-text' \
# --header 'Authorization: Bearer {api_key}' \
# --header 'Content-Type: application/json' \
# --data-raw '{"name": "name","text": "text"}'


class UpdateDocumentByText(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = self.runtime.credentials["knowledge_api_key"]
        dataset_id = tool_parameters.get("dataset_id")
        document_id = tool_parameters.get("document_id")
        url = f"{self.runtime.credentials['knowledge_api_url'].strip('/')}/datasets/{dataset_id}/documents/{document_id}/update-by-text"

        document_name = tool_parameters.get("document_name")
        document_text = tool_parameters.get("document_text")

        resp = requests.post(
            url=url,
            json={"name": document_name, "text": document_text},
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        print(
            f"key: {key}",
            f"url: {url}",
            f"name: {document_name}",
            f"text: {document_text}",
        )

        print(resp.json())

        yield self.create_json_message(resp.json())
