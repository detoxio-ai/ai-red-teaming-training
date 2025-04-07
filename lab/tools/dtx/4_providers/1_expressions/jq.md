# **JQ Expressions Tutorial: A Beginner’s Guide**

## **1. Introduction to JQ**
**JQ** is a powerful **command-line JSON processor** used to **parse, filter, and transform JSON data**. It allows users to extract specific information, format data, and apply functions without writing complex scripts.

### **Why Use JQ?**
✅ **Extract specific data** from large JSON responses  
✅ **Filter and manipulate JSON** efficiently  
✅ **Transform JSON structure** for better readability  
✅ **Supports conditionals, loops, and advanced expressions**  

### **Basic JQ Syntax**
- **Extract fields:** `.field`
- **Filter arrays:** `.array[]`
- **Modify values:** `.field |= value`
- **Use pipes (`|`)** to chain operations  
- **Apply functions:** `map`, `select`, `contains`, etc.  

---

## **2. Using JQ to Extract Data**
JQ expressions can be used to **filter JSON responses** by extracting specific values.

### **Example JSON Input**
```json
{
  "results": [
    {
      "max_injection_score": 0.85,
      "max_jailbreak_score": 0.92,
      "chunk_results": [
        {
          "BENIGN": 0.05,
          "INJECTION": 0.85,
          "JAILBREAK": 0.92,
          "start": 0,
          "end": 52
        }
      ]
    }
  ]
}
```

### **Example: Extracting a Single Field**
Extract **`max_injection_score`** from the JSON:
```sh
jq '.results[0].max_injection_score' response.json
```
**Output:**
```json
0.85
```

---

## **3. Filtering JSON Data**
JQ allows **filtering specific parts** of a JSON object.

### **Example: Extract `INJECTION` and `JAILBREAK` Scores**
```sh
jq '.results[0].chunk_results[0] | {INJECTION, JAILBREAK}' response.json
```
**Output:**
```json
{
  "INJECTION": 0.85,
  "JAILBREAK": 0.92
}
```

### **Example: Extract Only High-Risk Cases**
Get responses where **INJECTION > 0.8**:
```sh
jq '.results[0].chunk_results[] | select(.INJECTION > 0.8)' response.json
```
**Output:**
```json
{
  "BENIGN": 0.05,
  "INJECTION": 0.85,
  "JAILBREAK": 0.92,
  "start": 0,
  "end": 52
}
```

---

## **4. Working with JSON Arrays**
JQ provides **array functions** to process multiple items.

### **Example: Extracting Values from an Array**
```sh
jq '.results[].chunk_results[].INJECTION' response.json
```
**Output:**
```json
0.85
```

### **Example: Listing All Scores**
```sh
jq '.results[].chunk_results[] | {BENIGN, INJECTION, JAILBREAK}' response.json
```
**Output:**
```json
{
  "BENIGN": 0.05,
  "INJECTION": 0.85,
  "JAILBREAK": 0.92
}
```

---

## **5. Using Conditionals in JQ**
JQ supports **if-else statements** to modify JSON based on conditions.

### **Example: Marking High-Risk Entries**
```sh
jq '.results[].chunk_results[] | if .JAILBREAK > 0.8 then "High Risk" else "Low Risk" end' response.json
```
**Output:**
```json
"High Risk"
```

---

## **6. Transforming JSON Structure**
JQ can **restructure JSON** to match specific output needs.

### **Example: Flattening JSON Output**
Convert nested JSON into a simpler structure:
```sh
jq '.results[].chunk_results[] | {Risk_Score: .JAILBREAK, Position: {start, end}}' response.json
```
**Output:**
```json
{
  "Risk_Score": 0.92,
  "Position": {
    "start": 0,
    "end": 52
  }
}
```

---

## **7. Working with JSON Objects**
JQ allows **modifying existing values** in JSON.

### **Example: Rounding Values**
```sh
jq '.results[].chunk_results[] | {JAILBREAK: (.JAILBREAK | round)}' response.json
```
**Output:**
```json
{
  "JAILBREAK": 1
}
```

---

## **8. Combining JQ Expressions**
Multiple JQ operations can be **chained using pipes (`|`)**.

### **Example: Extract and Transform Data**
```sh
jq '.results[].chunk_results[] | {JAILBREAK: .JAILBREAK, Status: (if .JAILBREAK > 0.8 then "Danger" else "Safe" end)}' response.json
```
**Output:**
```json
{
  "JAILBREAK": 0.92,
  "Status": "Danger"
}
```

---

## **9. Using JQ in YAML Configurations**
JQ expressions are **commonly used in YAML for JSON transformations**.

### **Example: JQ in a YAML-Based API Configuration**
```yaml
transform_response: |
  {
    "max_injection_score": json["results"][0]["max_injection_score"],
    "max_jailbreak_score": json["results"][0]["max_jailbreak_score"],
    "chunk_results": json["results"][0]["chunk_results"] | map({INJECTION, JAILBREAK})
  }
```
This extracts:
- The **max injection and jailbreak scores**.
- A **transformed list** of `INJECTION` and `JAILBREAK` scores.

---
