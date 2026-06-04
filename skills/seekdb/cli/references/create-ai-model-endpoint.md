# CREATE_AI_MODEL_ENDPOINT

> **Source:** OceanBase Database Documentation — DBMS_AI_SERVICE Subprograms (MySQL Mode)
>
> https://www.oceanbase.com/docs/common-oceanbase-database-cn-1000000004479800

The `CREATE_AI_MODEL_ENDPOINT` procedure creates an access endpoint for an AI model object, specifying properties such as the endpoint URL, access key, and model provider.

## Syntax

```sql
CALL DBMS_AI_SERVICE.CREATE_AI_MODEL_ENDPOINT(
    name     VARCHAR(128),
    params   JSON
);
```

## Parameters

| Parameter | JSON key | Description | Type | Required |
|-----------|----------|-------------|------|----------|
| `name` | — | Name of the access endpoint. | VARCHAR(128) | YES |
| `params` | `ai_model_name` | Name of the AI model object previously created by `CREATE_AI_MODEL`. | JSON STRING | YES |
| | `url` | Full URL of the AI model service endpoint (the specific interface address for chat, embedding, or reranking — not the base URL). | JSON STRING | YES |
| | `access_key` | API key for authenticating with the service. | JSON STRING | YES |
| | `request_model_name` | User-defined model name placed in the request body (e.g. `big-m3-custom`). | JSON STRING | NO |
| | `provider` | Model provider identifier (see below). | JSON STRING | YES |

### Supported Providers

| Provider value | Vendor |
|----------------|--------|
| `aliyun-openAI` | Alibaba Cloud (OpenAI-compatible) |
| `aliyun-dashscope` | Alibaba Cloud DashScope |
| `deepseek` | DeepSeek |
| `siliconflow` | SiliconFlow |
| `hunyuan-openAI` | Tencent Hunyuan (OpenAI-compatible) |
| `openAI` | OpenAI |

### Provider Endpoint URLs

| Vendor | Type | URL |
|--------|------|-----|
| Alibaba Cloud (OpenAI-compatible) | completion | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` |
| | embedding | `https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings` |
| Alibaba Cloud DashScope (native) | completion | `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` |
| | embedding | `https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding` |
| | rerank | `https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank` |
| DeepSeek (OpenAI-compatible) | completion | `https://api.deepseek.com/chat/completions` |
| SiliconFlow (OpenAI-compatible) | completion | `https://api.siliconflow.cn/v1/chat/completions` |
| | embedding | `https://api.siliconflow.cn/v1/embeddings` |
| | rerank | `https://api.siliconflow.cn/v1/rerank` |
| Tencent Hunyuan (OpenAI-compatible) | completion | `https://api.hunyuan.cloud.tencent.com/v1/chat/completions` |
| | embedding | `https://api.hunyuan.cloud.tencent.com/v1/embeddings` |

## SQL Example

```sql
CALL DBMS_AI_SERVICE.CREATE_AI_MODEL_ENDPOINT(
  'my_model_endpoint1', '{
    "ai_model_name": "my_model1",
    "url": "https://api.deepseek.com/chat/completions",
    "access_key": "sk-xxxxxxxxxxxx",
    "request_model_name": "deepseek-chat",
    "provider": "deepseek"
  }');
```

## seekdb-cli Usage

```bash
seekdb ai model endpoint create <endpoint_name> <ai_model_name> \
  --url <service_url> \
  --access-key <api_key> \
  --provider <provider>

seekdb ai model endpoint delete <endpoint_name>
```

### CLI Example

```bash
seekdb ai model endpoint create my_ep my_llm \
  --url "https://api.siliconflow.cn/v1/chat/completions" \
  --access-key "sk-xxxxxxxxxxxx" \
  --provider siliconflow

seekdb ai model endpoint delete my_ep
```
