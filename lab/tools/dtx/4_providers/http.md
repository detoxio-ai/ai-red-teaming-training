# **HTTP Provider Documentation**
This document describes the supported **HTTP Providers**, their configurations, and how they can be used to send requests and process responses.

## **Overview**
The `HttpProvider` allows sending HTTP requests using either:
1. **Structured HTTP Requests** – Specify the URL, HTTP method, headers, and body.
2. **Raw HTTP Requests** – Define the full HTTP request manually as a raw string.

It also supports:
- **Request Transformations** (`transform_request`) – Modify the request before sending.
- **Response Transformations** (`transform_response`) – Extract or process the API response.

---

## **1. Structured HTTP Provider**
A structured HTTP provider defines an HTTP request using **explicit fields** such as `url`, `method`, `headers`, and `body`.

### **Configuration Fields**
| Field | Type | Required | Description |
|--------|------|----------|-------------|
| `url` | `str` | ✅ Yes | The HTTP endpoint URL. |
| `method` | `HttpMethod` | ✅ Yes | The HTTP method (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`). |
| `headers` | `dict[str, str]` | ❌ No | HTTP headers for the request (default: `{}`). |
| `body` | `Union[str, dict]` | ❌ No | Request body as **a JSON object** or **a form-urlencoded string**. |
| `transform_request` | `Union[str, dict]` | ❌ No | A **template** or **function** that modifies the request before sending. |
| `transform_response` | `Union[str, dict]` | ❌ No | A **string expression**, **function**, or **file reference** to process the response. |

### **Example Usage**
#### **1.1 JSON Request Example**
```yaml
providers:
  - id: http
    config:
      url: "https://api.example.com/chat"
      method: POST
      headers:
        "Content-Type": "application/json"
      body:
        prompt: "{{prompt}}"
        model: "gpt-4o-mini"
```

#### **1.2 Form-Encoded Request Example**
```yaml
providers:
  - id: http
    config:
      url: "https://api.example.com/submit"
      method: POST
      headers:
        "Content-Type": "application/x-www-form-urlencoded"
      body: "username={{user}}&password={{pass}}"
```

---

## **2. Raw HTTP Provider**
A raw HTTP provider allows defining the entire HTTP request manually, including headers and body, giving **full control** over the request format.

### **Configuration Fields**
| Field | Type | Required | Description |
|--------|------|----------|-------------|
| `raw_request` | `str` | ✅ Yes | The full HTTP request in raw format. |
| `use_https` | `bool` | ❌ No | Whether to use HTTPS (`true` by default). |
| `transform_response` | `Union[str, dict]` | ❌ No | A **string expression**, **function**, or **file reference** to process the response. |

### **Example Usage**
#### **2.1 Raw HTTP Request**
```yaml
providers:
  - id: http
    config:
      use_https: true
      raw_request: |
        POST /v1/chat HTTP/1.1
        Host: api.example.com
        Content-Type: application/json
        Authorization: Bearer {{api_key}}

        {
          "model": "llama3.1-405b-base",
          "prompt": "{{prompt}}",
          "max_tokens": 100
        }
      transform_response: "json.content"
```

#### **2.2 Loading Raw Request from a File**
```yaml
providers:
  - id: http
    config:
      raw_request: file://requests/chat_request.txt
      transform_response: "json.result.text"
```

---

## **3. Request Transformation (`transform_request`)**
Before sending a request, **request transformations** allow modifying the payload dynamically.

### **Supported Formats**
| Type | Example |
|------|---------|
| **String Template** | `'{"message": "{{prompt}}"}'` |
| **Python Lambda Function** | `'lambda prompt: {"text": prompt, "timestamp": 1710341825}'` |
| **External File** | `'file://transforms/request_transform.py:transform_request'` |

### **Example Usage**
#### **3.1 Using a String Template**
```yaml
providers:
  - id: http
    config:
      url: "https://api.example.com/chat"
      transform_request: '{"message": "{{prompt}}"}'
      body:
        user_message: "{{prompt}}"
```

#### **3.2 Using a Python Function**
```yaml
providers:
  - id: http
    config:
      url: "https://api.example.com/chat"
      transform_request: "lambda prompt: {'text': prompt, 'timestamp': 1710341825}"
```

#### **3.3 Loading a Request Transform from File**
```yaml
providers:
  - id: http
    config:
      url: "https://api.example.com/chat"
      transform_request: "file://transforms/request_transform.py"
```

---

## **4. Response Transformation (`transform_response`)**
After receiving a response, **response transformations** allow extracting or modifying the output before returning it.

### **Supported Formats**
| Type | Example |
|------|---------|
| **JSON Path** | `'json.choices[0].message.content'` |
| **Python Lambda Function** | `'lambda json, text, context: json["choices"][0]["message"]["content"]'` |
| **External File** | `'file://parsers/response_parser.py:parse_response'` |

### **Example Usage**
#### **4.1 Extracting JSON Data**
```yaml
providers:
  - id: http
    config:
      url: "https://api.example.com/completions"
      transform_response: "json.choices[0].message.content"
```

#### **4.2 Using a Lambda Function**
```yaml
providers:
  - id: http
    config:
      url: "https://api.example.com/generate"
      transform_response: "lambda json, text, context: json['result']['message']"
```

#### **4.3 Loading Response Transform from File**
```yaml
providers:
  - id: http
    config:
      url: "https://api.example.com/parse"
      transform_response: "file://parsers/response_parser.py"
```

---

## **5. Query Parameters**
You can **dynamically generate query parameters** using placeholders.

### **Example**
```yaml
providers:
  - id: http
    config:
      url: "https://api.example.com/search"
      method: GET
      queryParams:
        q: "{{prompt}}"
        lang: "en"
```

---

## **6. Nested JSON Objects in Request Body**
When working with **complex request payloads**, use `dump` to serialize nested objects.

### **Example**
```yaml
providers:
  - id: http
    config:
      url: "https://api.example.com/generate"
      body:
        messages: "{{messages | dump}}"
        model: "gpt-4o-mini"
```

