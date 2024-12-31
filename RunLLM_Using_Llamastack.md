### Instructions to Set Up Llama Stack Locally

Follow these steps to set up the **Llama Stack** on your local machine:

---

#### **1. Install Llama Stack**
To install the Llama Stack Python library, use pip:

```bash
pip install llama-stack
```

---

#### **2. Obtain an Access Key**
1. Visit [Llama Downloads](https://www.llama.com/llama-downloads/).
2. Select the **lightweight models** category.
3. Submit your request to receive an access key.
4. The access key will be emailed to you.

---

#### **3. Download the Llama Model**
Use the following command to download the desired Llama model:

```bash
llama download --source meta --model-id meta-llama/Llama-3.2-1B-Instruct
```

**Sample Output of the Download Process**:
```plaintext
Already downloaded /home/xxx/.llama/checkpoints/Llama3.2-1B-Instruct/tokenizer.model
Already downloaded /home/xxx/.llama/checkpoints/Llama3.2-1B-Instruct/checklist.chk
Already downloaded /home/xxx/.llama/checkpoints/Llama3.2-1B-Instruct/params.json
Downloading checklist.chk               ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━           100.0%   156/156 bytes    -  0:00:00
Downloading tokenizer.model             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━           100.0%   2.2/2.2 MB       -  0:00:00
Downloading params.json                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━           100.0%   220/220 bytes    -  0:00:00
Downloading consolidated.00.pth         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━           100.0%   2.5/2.5 GB       -  0:00:00

Successfully downloaded model to /home/xxx/.llama/checkpoints/Llama3.2-1B-Instruct

View MD5 checksum files at: /home/xxx/.llama/checkpoints/Llama3.2-1B-Instruct/checklist.chk
```

---

#### **4. Verify Model Details**
To describe the model and verify the downloaded files, run the following command:

```bash
llama model describe --model-id meta-llama/Llama-3.2-1B-Instruct
```

This command provides detailed metadata about the model.


#### **4. Checking the prompt template

```bash
llama model prompt-format -m Llama3.2-1B-Instruct

                                  User and assistant conversation                                   

Here is a regular multi-turn user assistant conversation and how its formatted.                     

                                        Input Prompt Format                                         

                                                                                                    
 <|begin_of_text|><|start_header_id|>system<|end_header_id|>                                        
                                                                                                    
 You are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>                      
                                                                                                    
 Who are you?<|eot_id|><|start_header_id|>assistant<|end_header_id|>                                
                                                                                                    

```