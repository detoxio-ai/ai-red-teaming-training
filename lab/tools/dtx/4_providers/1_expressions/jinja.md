# **Jinja Templating Tutorial: A Beginner’s Guide**

## **1. Introduction to Jinja**
Jinja is a **templating language** for dynamically generating content, commonly used in Python web frameworks like Flask and Django, as well as in **YAML files for configuration automation**.

### **Why Use Jinja?**
**Dynamic Variables** – Insert values into templates without hardcoding.  
**Conditional Logic** – Create templates that adapt based on conditions.  
**Loops & Filters** – Process lists, format data, and apply transformations.  
**Used in YAML, HTML, JSON, and more** – Supports dynamic configuration files.  

### **Basic Jinja Syntax**
Jinja expressions are enclosed in **double curly braces (`{{ }}`)** for **output**, and **curly braces with percentage signs (`{% %}`)** for **logic**.

- **Variables:** `{{ variable }}`
- **Conditions:** `{% if condition %} ... {% endif %}`
- **Loops:** `{% for item in list %} ... {% endfor %}`
- **Filters:** `{{ variable | filter }}`

---

## **2. Using Jinja in YAML Configuration Files**
Jinja is commonly used in YAML for **configuring automation, API requests, and templated configurations**.

### **Example: Inserting Variables**
```yaml
api_url: "https://{{ env.API_HOST }}/v1/detect"
```
Here, `{{ env.API_HOST }}` dynamically **retrieves the value of an environment variable**.

### **Example: Using Jinja for Dynamic API Requests**
```yaml
providers:
  - id: "http"
    config:
      raw_request: |
        POST /detect/jailbreak HTTP/1.1
        Host: {{ ENV_HOST }}
        Content-Type: application/json

        {
          "texts": [
            "{{ prompt }}"
          ]
        }
```
- `{{ ENV_HOST }}` dynamically inserts an API host from **environment variables**.
- `{{ prompt }}` injects **user input** into the request.

---

## **3. Jinja Expressions and Filters**
### **Variables in Jinja**
Jinja allows you to **store and display variables dynamically**.

#### **Example**
```yaml
greeting: "Hello, {{ user_name }}!"
```
If `user_name = "Alice"`, the output will be:
```yaml
greeting: "Hello, Alice!"
```

---

## **4. Jinja Filters**
Filters **modify variables** before they are rendered. They are applied using the `|` (pipe) symbol.

### **Common Jinja Filters**
| Filter | Description | Example | Output |
|--------|------------|---------|--------|
| **lower** | Converts to lowercase | `{{ "HELLO" | lower }}` | `"hello"` |
| **upper** | Converts to uppercase | `{{ "hello" | upper }}` | `"HELLO"` |
| **title** | Capitalizes first letter of each word | `{{ "hello world" | title }}` | `"Hello World"` |
| **replace** | Replaces part of a string | `{{ "error: 404" | replace("error", "status") }}` | `"status: 404"` |
| **default** | Provides a default value if variable is missing | `{{ undefined_var | default("N/A") }}` | `"N/A"` |
| **join** | Joins a list into a string | `{{ ["one", "two", "three"] | join(", ") }}` | `"one, two, three"` |
| **length** | Returns the length of a string or list | `{{ "Hello" | length }}` | `5` |
| **int** | Converts to an integer | `{{ "42" | int }}` | `42` |
| **round** | Rounds a number | `{{ 3.14159 | round(2) }}` | `3.14` |

#### **Example: Using Filters in YAML**
```yaml
server_name: "{{ 'myServer' | upper }}"
```
**Output:**
```yaml
server_name: "MYSERVER"
```

---

## **5. Jinja Conditionals (`if` Statements)**
Jinja allows conditional logic for **dynamic configuration**.

### **Example: Setting Different Hosts Based on Environment**
```yaml
api_host: "{% if env.ENVIRONMENT == 'production' %}api.prod.com{% else %}api.dev.com{% endif %}"
```
If `ENVIRONMENT=production`, then:
```yaml
api_host: "api.prod.com"
```
If `ENVIRONMENT=development`, then:
```yaml
api_host: "api.dev.com"
```

---

## **6. Jinja Loops (`for` Statements)**
Jinja **loops** allow you to iterate over lists and generate content dynamically.

### **Example: Iterating Over a List**
```yaml
services:
  {% for service in ["database", "cache", "api"] %}
  - "{{ service }}"
  {% endfor %}
```
**Output:**
```yaml
services:
  - "database"
  - "cache"
  - "api"
```

### **Example: Iterating with Index**
```yaml
users:
  {% for user in ["Alice", "Bob", "Charlie"] %}
  - name: "{{ user }}"
    id: "{{ loop.index }}"
  {% endfor %}
```
**Output:**
```yaml
users:
  - name: "Alice"
    id: "1"
  - name: "Bob"
    id: "2"
  - name: "Charlie"
    id: "3"
```
**`loop.index`** gives a **1-based index** for each item in the list.

---

## **7. Nested Jinja Statements**
Jinja can handle **nested loops and conditionals**.

### **Example: Dynamic Configuration for Different Environments**
```yaml
servers:
  {% for region in ["us-east", "us-west", "europe"] %}
  - region: "{{ region }}"
    host: "{% if region == 'europe' %}eu.server.com{% else %}us.server.com{% endif %}"
  {% endfor %}
```
**Output:**
```yaml
servers:
  - region: "us-east"
    host: "us.server.com"
  - region: "us-west"
    host: "us.server.com"
  - region: "europe"
    host: "eu.server.com"
```

---

## **8. Jinja in JSON (Useful for APIs)**
Jinja can be used to dynamically generate **JSON API payloads**.

### **Example: Generating JSON Using Jinja**
```json
{
  "users": [
    {% for user in ["Alice", "Bob", "Charlie"] %}
    {
      "name": "{{ user }}",
      "id": "{{ loop.index }}"
    }{% if not loop.last %},{% endif %}
    {% endfor %}
  ]
}
```
**Output:**
```json
{
  "users": [
    { "name": "Alice", "id": "1" },
    { "name": "Bob", "id": "2" },
    { "name": "Charlie", "id": "3" }
  ]
}
```

---

## **9. Combining Jinja and JQ for JSON Processing**
Jinja is **used to generate structured data**, while **JQ** is used to **filter and manipulate JSON responses**.

### **Example: Jinja JSON Request**
```yaml
providers:
  - id: "http"
    config:
      raw_request: |
        POST /api/detect HTTP/1.1
        Host: {{ ENV_HOST }}
        Content-Type: application/json

        {
          "texts": [
            "{{ prompt }}"
          ]
        }
```

### **Example: JQ Processing for Response**
```yaml
transform_response: |
  {
    "JAILBREAK": json["results"][0]["chunk_results"][0]["JAILBREAK"],
    "INJECTION": json["results"][0]["chunk_results"][0]["INJECTION"]
  }
```
This extracts:
- `JAILBREAK` and `INJECTION` scores from the first result object.

---
