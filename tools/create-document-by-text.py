from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# curl --location --request POST 'https://api.dify.ai/v1/datasets/{dataset_id}/document/create-by-text' \
# --header 'Authorization: Bearer {api_key}' \
# --header 'Content-Type: application/json' \
# --data-raw '{"name": "text","text": "text","indexing_technique": "high_quality","process_rule": {"mode": "automatic"}}'


class CreateDocumentByText(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = self.runtime.credentials["knowledge_api_key"]
        dataset_id = tool_parameters.get("dataset_id")
        url = f"{self.runtime.credentials['knowledge_api_url'].strip('/')}/datasets/{dataset_id}/document/create-by-text"

        document_name = tool_parameters.get("document_name")
        document_text = tool_parameters.get("document_text")
        indexing_technique = tool_parameters.get("indexing_technique", "high_quality")
        process_mode = tool_parameters.get("process_mode", "automatic")

        resp = requests.post(
            url=url,
            json={
                "name": document_name,
                "text": document_text,
                "indexing_technique": indexing_technique,
                "process_rule": {"mode": process_mode},
            },
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
            f"indexing_technique: {indexing_technique}",
        )

        print(resp.json())

        yield self.create_json_message(resp.json())


"""
{
  "text": "",
  "files": [],
  "json": [
    {
      "batch": "20250328165829543349",
      "document": {
        "archived": false,
        "created_at": 1743181110,
        "created_by": "d649e7e3-6827-4c75-964b-caa3bb45d8dd",
        "created_from": "api",
        "data_source_detail_dict": {
          "upload_file": {
            "created_at": 1743181109.626701,
            "created_by": "d649e7e3-6827-4c75-964b-caa3bb45d8dd",
            "extension": "txt",
            "id": "209341a0-bf0b-4cf0-8ec8-888a6f81fee5",
            "mime_type": "text/plain",
            "name": "超级测试数据集6",
            "size": 21
          }
        },
        "data_source_info": {
          "upload_file_id": "209341a0-bf0b-4cf0-8ec8-888a6f81fee5"
        },
        "data_source_type": "upload_file",
        "dataset_process_rule_id": "aff8e578-3ec4-42f5-815b-ede20f0e6585",
        "disabled_at": null,
        "disabled_by": null,
        "display_status": "indexing",
        "doc_form": "text_model",
        "doc_metadata": null,
        "enabled": true,
        "error": null,
        "hit_count": 0,
        "id": "024f5699-3b20-474e-94e4-01a8b491622a",
        "indexing_status": "parsing",
        "name": "超级测试数据集6",
        "position": 214,
        "tokens": 0,
        "word_count": 0
      }
    }
  ]
}
"""
