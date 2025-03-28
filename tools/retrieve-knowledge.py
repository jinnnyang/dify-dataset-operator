from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# curl --location --request POST 'https://api.dify.ai/v1/datasets/{dataset_id}/retrieve' \
# --header 'Authorization: Bearer {api_key}' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "query": "test",
#     "retrieval_model": {
#         "search_method": "keyword_search",
#         "reranking_enable": false,
#         "reranking_mode": null,
#         "reranking_model": {
#             "reranking_provider_name": "",
#             "reranking_model_name": ""
#         },
#         "weights": null,
#         "top_k": 1,
#         "score_threshold_enabled": false,
#         "score_threshold": null
#     }
# }'


class RetrieveKnowledge(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = self.runtime.credentials["knowledge_api_key"]
        dataset_id = tool_parameters.get("dataset_id")
        search_method = tool_parameters.get("search_method", "keyword_search")
        url = f"{self.runtime.credentials['knowledge_api_url'].strip('/')}/datasets/{dataset_id}/retrieve"

        query = tool_parameters.get("query")
        retrieval_model = tool_parameters.get(
            "retrieval_model",
            {
                "search_method": search_method,
                "reranking_enable": True,
                "reranking_mode": None,
                "reranking_model": {
                    "reranking_provider_name": "langgenius/jina/jina",
                    "reranking_model_name": "jina-reranker-v2-base-multilingual",
                },
                "weights": None,
                "top_k": 3,
                "score_threshold_enabled": False,
                "score_threshold": 0.5,
            },
        )

        resp = requests.post(
            url=url,
            json={"query": query, "retrieval_model": retrieval_model},
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        print(
            f"key: {key}",
            f"url: {url}",
            f"query: {query}",
            f"retrieval_model: {retrieval_model}",
        )

        print(resp.json())

        yield self.create_json_message(resp.json())
