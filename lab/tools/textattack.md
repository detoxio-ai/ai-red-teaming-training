
### Running Textattack

```
❯ textattack attack --recipe textfooler --model bert-base-uncased-mr --num-examples 100

Attack(
  (search_method): GreedyWordSwapWIR(
    (wir_method):  delete
  )
  (goal_function):  UntargetedClassification
  (transformation):  WordSwapEmbedding(
    (max_candidates):  50
    (embedding):  WordEmbedding
  )
  (constraints): 
    (0): WordEmbeddingDistance(
        (embedding):  WordEmbedding
        (min_cos_sim):  0.5
        (cased):  False
        (include_unknown_words):  True
        (compare_against_original):  True
      )
    (1): PartOfSpeech(
        (tagger_type):  nltk
        (tagset):  universal
        (allow_verb_noun_swap):  True
        (compare_against_original):  True
      )
    (2): UniversalSentenceEncoder(
        (metric):  angular
        (threshold):  0.840845057
        (window_size):  15
        (skip_text_shorter_than_window):  True
        (compare_against_original):  False
      )
    (3): RepeatModification
    (4): StopwordModification
    (5): InputColumnModification(
        (matching_column_labels):  ['premise', 'hypothesis']
        (columns_to_ignore):  {'premise'}
      )
  (is_black_box):  True
) 

  0%|                                                                                                  | 0/100 [00:00<?, ?it/s]2025-01-08 14:55:54.925839: E external/local_xla/xla/stream_executor/cuda/cuda_driver.cc:152] failed call to cuInit: INTERNAL: CUDA error: Failed call to cuInit: UNKNOWN ERROR (303)
2025-01-08 14:55:59.249677: E tensorflow/core/util/util.cc:131] oneDNN supports DT_INT64 only on platforms with AVX-512. Falling back to the default Eigen-based implementation if present.
  1%|▉                                                                                         | 1/100 [00:20<34:23, 20.85s/it]--------------------------------------------- Result 1 ---------------------------------------------
Positive (100%) --> Negative (60%)

lovingly photographed in the manner of a golden book sprung to life , stuart little 2 manages sweetness largely without stickiness .

lovingly photographed in the manner of a golden book sprung to life , stuart little 2 administration sweetness largely without stickiness .


[Succeeded / Failed / Skipped / Total] 1 / 0 / 0 / 1:   2%|▋                                   | 2/100 [00:46<38:18, 23.46s/it]--------------------------------------------- Result 2 ---------------------------------------------
Positive (100%) --> Negative (99%)

consistently clever and suspenseful .

ceaselessly cleverer and enigmatic .


[Succeeded / Failed / Skipped / Total] 2 / 0 / 0 / 2:   3%|█                                   | 3/100 [00:47<25:32, 15.80s/it]--------------------------------------------- Result 3 ---------------------------------------------
Negative (84%) --> [SKIPPED]

it's like a " big chill " reunion of the baader-meinhof gang , only these guys are more harmless pranksters than political activists .


[Succeeded / Failed / Skipped / Total] 2 / 0 / 1 / 3:   4%|█▍                                  | 4/100 [02:19<55:37, 34.77s/it]--------------------------------------------- Result 4 ---------------------------------------------
Positive (100%) --> Negative (99%)

the story gives ample opportunity for large-scale action and suspense , which director shekhar kapur supplies with tremendous skill .

the story poses ample hazard for large-scale action and suspense , which director shekhar kapur supplies with huge jurisdictional .


[Succeeded / Failed / Skipped / Total] 3 / 0 / 1 / 4:   5%|█▊                                  | 5/100 [02:19<44:12, 27.92s/it]--------------------------------------------- Result 5 ---------------------------------------------
Negative (99%) --> [SKIPPED]

red dragon " never cuts corners .


[Succeeded / Failed / Skipped / Total] 3 / 0 / 2 / 5:   6%|██▏                                 | 6/100 [02:20<36:35, 23.35s/it]--------------------------------------------- Result 6 ---------------------------------------------
Negative (95%) --> [SKIPPED]

fresnadillo has something serious to say about the ways in which extravagant chance can distort our perspective and throw us off the path of good sense .


[Succeeded / Failed / Skipped / Total] 3 / 0 / 3 / 6:   7%|██▌                                 | 7/100 [03:10<42:15, 27.26s/it]--------------------------------------------- Result 7 ---------------------------------------------
Positive (100%) --> Negative (89%)

throws in enough clever and unexpected twists to make the formula feel fresh .

throws in enough clever and casual folds to pose the formula feel fresh .


[Succeeded / Failed / Skipped / Total] 4 / 0 / 3 / 7:   8%|██▉                                 | 8/100 [03:11<36:40, 23.92s/it]--------------------------------------------- Result 8 ---------------------------------------------
Negative (95%) --> [SKIPPED]

weighty and ponderous but every bit as filling as the treat of the title .


[Succeeded / Failed / Skipped / Total] 4 / 0 / 4 / 8:   9%|███▏                                | 9/100 [05:13<52:53, 34.87s/it]--------------------------------------------- Result 9 ---------------------------------------------
Positive (100%) --> Negative (98%)

a real audience-pleaser that will strike a chord with anyone who's ever waited in a doctor's office , emergency room , hospital bed or insurance company office .

a actual audience-pleaser that desired strike a chord with anyone who's ever waited in a doctor's office , eventuality camera , committal bed or safer venture cabinet .


[Succeeded / Failed / Skipped / Total] 5 / 0 / 4 / 9:  10%|███▌                               | 10/100 [06:28<58:19, 38.89s/it]--------------------------------------------- Result 10 ---------------------------------------------
Positive (100%) --> Negative (72%)

generates an enormous feeling of empathy for its characters .

leeds an enormous foreboding of empathy for its specs .


[Succeeded / Failed / Skipped / Total] 6 / 0 / 4 / 10:  11%|███▌                            | 11/100 [07:26<1:00:13, 40.60s/it]--------------------------------------------- Result 11 ---------------------------------------------
Positive (100%) --> Negative (100%)

exposing the ways we fool ourselves is one hour photo's real strength .

implying the ways we fool ourselves is one timing photo's real kraft .


[Succeeded / Failed / Skipped / Total] 7 / 0 / 4 / 11:  12%|████                              | 12/100 [07:50<57:27, 39.17s/it]--------------------------------------------- Result 12 ---------------------------------------------
Positive (96%) --> Negative (63%)

it's up to you to decide whether to admire these people's dedication to their cause or be repelled by their dogmatism , manipulativeness and narrow , fearful view of american life .

it's up to you to decide whether to admire these people's dedication to their cause or be adjourn by their dogmatism , manipulativeness and narrow , fearful view of american life .


[Succeeded / Failed / Skipped / Total] 8 / 0 / 4 / 12:  13%|████▍                             | 13/100 [08:14<55:07, 38.01s/it]--------------------------------------------- Result 13 ---------------------------------------------
Positive (100%) --> Negative (59%)

mostly , [goldbacher] just lets her complicated characters be unruly , confusing and , through it all , human .

mostly , [goldbacher] just lets her complicated characters be remiss , confusing and , through it all , humanistic .


[Succeeded / Failed / Skipped / Total] 9 / 0 / 4 / 13:  14%|████▊                             | 14/100 [08:29<52:11, 36.41s/it]--------------------------------------------- Result 14 ---------------------------------------------
Positive (99%) --> Negative (99%)

. . . quite good at providing some good old fashioned spooks .

. . . quite adequate at providing some good old fashioned spooks .


[Succeeded / Failed / Skipped / Total] 10 / 0 / 4 / 14:  15%|████▉                            | 15/100 [08:30<48:11, 34.02s/it]--------------------------------------------- Result 15 ---------------------------------------------
Negative (99%) --> [SKIPPED]

at its worst , the movie is pretty diverting ; the pity is that it rarely achieves its best .


[Succeeded / Failed / Skipped / Total] 10 / 0 / 5 / 15:  16%|█████▎                           | 16/100 [10:29<55:05, 39.36s/it]--------------------------------------------- Result 16 ---------------------------------------------
Positive (100%) --> Negative (99%)

scherfig's light-hearted profile of emotional desperation is achingly honest and delightfully cheeky .

scherfig's light-hearted outline of affectionate wretchedness is achingly cordial and surprisingly vulgar .


[Succeeded / Failed / Skipped / Total] 11 / 0 / 5 / 16:  17%|█████▎                         | 17/100 [12:41<1:01:56, 44.78s/it]--------------------------------------------- Result 17 ---------------------------------------------
Positive (100%) --> Negative (98%)

a journey spanning nearly three decades of bittersweet camaraderie and history , in which we feel that we truly know what makes holly and marina tick , and our hearts go out to them as both continue to negotiate their imperfect , love-hate relationship .

a displacement spanning barely two decades of bittersweet friendship and history , in which we feel that we awfully know what paid holly and marina tick , and our hearts go out to them as both ceaseless to negotiate their imperfect , love-hate relationship .


[Succeeded / Failed / Skipped / Total] 12 / 0 / 5 / 17:  18%|█████▌                         | 18/100 [13:32<1:01:43, 45.16s/it]--------------------------------------------- Result 18 ---------------------------------------------
Positive (100%) --> Negative (99%)

the wonderfully lush morvern callar is pure punk existentialism , and ms . ramsay and her co-writer , liana dognini , have dramatized the alan warner novel , which itself felt like an answer to irvine welsh's book trainspotting .

the appallingly lush morvern callar is pure punk existentialism , and ms . ramsay and her co-writer , liana dognini , have dramatization the alan warner novel , which itself felt like an answer to irvine welsh's book trainspotting .


[Succeeded / Failed / Skipped / Total] 13 / 0 / 5 / 18:  19%|██████▎                          | 19/100 [13:52<59:11, 43.84s/it]--------------------------------------------- Result 19 ---------------------------------------------
Positive (100%) --> Negative (77%)

as it turns out , you can go home again .

as it turns out , you can go homing again .


[Succeeded / Failed / Skipped / Total] 14 / 0 / 5 / 19:  20%|██████▌                          | 20/100 [14:58<59:53, 44.91s/it]--------------------------------------------- Result 20 ---------------------------------------------
Positive (99%) --> Negative (55%)

you've already seen city by the sea under a variety of titles , but it's worth yet another visit .

you've already seen suburbs by the crewman under a serial of title , but it's worth yet another visiting .


[Succeeded / Failed / Skipped / Total] 15 / 0 / 5 / 20:  21%|██████▌                        | 21/100 [17:31<1:05:54, 50.06s/it]--------------------------------------------- Result 21 ---------------------------------------------
Positive (100%) --> Negative (89%)

this kind of hands-on storytelling is ultimately what makes shanghai ghetto move beyond a good , dry , reliable textbook and what allows it to rank with its worthy predecessors .

this kind of hands-on narrator is maybe what makes shenzhen ghetto displacement beyond a buena , dry , reputable textbooks and what allows it to categorized with its laudable predecessor .


[Succeeded / Failed / Skipped / Total] 16 / 0 / 5 / 21:  22%|██████▊                        | 22/100 [17:31<1:02:09, 47.81s/it]--------------------------------------------- Result 22 ---------------------------------------------
Negative (99%) --> [SKIPPED]

making such a tragedy the backdrop to a love story risks trivializing it , though chouraqui no doubt intended the film to affirm love's power to help people endure almost unimaginable horror .


[Succeeded / Failed / Skipped / Total] 16 / 0 / 6 / 22:  23%|███████▏                       | 23/100 [18:13<1:01:01, 47.55s/it]--------------------------------------------- Result 23 ---------------------------------------------
Positive (97%) --> Negative (53%)

grown-up quibbles are beside the point here . the little girls understand , and mccracken knows that's all that matters .

grown-up quibbles are beside the point here . the little girls realising , and mccracken knew that's all that matters .


[Succeeded / Failed / Skipped / Total] 17 / 0 / 6 / 23:  23%|███████▏                       | 23/100 [18:13<1:01:01, 47.56s/it]

```


### **Explanation of the TextAttack Results**

#### **Overview**
The TextAttack run employs the **TextFooler attack recipe** on the `bert-base-uncased-mr` model (fine-tuned on the Rotten Tomatoes dataset) to test the model's robustness against adversarial attacks. Below is a breakdown of the results, with explanations and examples for succeeded, skipped, and failed cases.

---

### **Attack Configuration**
- **Model**: `bert-base-uncased-mr`  
- **Attack Recipe**: `TextFooler`  
- **Goal Function**: Untargeted classification (change the classification label of an input sentence).  
- **Transformation**: `WordSwapEmbedding` (replaces words with similar ones based on word embeddings).  
- **Constraints**:
  - **WordEmbeddingDistance**: Ensures word replacements are semantically similar.
  - **PartOfSpeech**: Maintains grammatical correctness during transformations.
  - **UniversalSentenceEncoder**: Ensures semantic similarity of the transformed sentence with the original.

---

### **Results Breakdown**
#### **Succeeded Examples**
The adversarial attack successfully changed the predicted sentiment of the input sentence.

1. **Result 1**  
   - **Original**: *"Lovingly photographed in the manner of a golden book sprung to life, Stuart Little 2 manages sweetness largely without stickiness."*  
     **Prediction**: Positive (100%)  
   - **Adversarial**: *"Lovingly photographed in the manner of a golden book sprung to life, Stuart Little 2 administration sweetness largely without stickiness."*  
     **Prediction**: Negative (60%)  
   - **Explanation**: Changing "manages" to "administration" disrupted the sentence's meaning, reducing its positivity and flipping the classification.

2. **Result 2**  
   - **Original**: *"Consistently clever and suspenseful."*  
     **Prediction**: Positive (100%)  
   - **Adversarial**: *"Ceaselessly cleverer and enigmatic."*  
     **Prediction**: Negative (99%)  
   - **Explanation**: Subtle word swaps ("consistently" → "ceaselessly", "suspenseful" → "enigmatic") altered the tone, misleading the classifier.

3. **Result 9**  
   - **Original**: *"A real audience-pleaser that will strike a chord with anyone who's ever waited in a doctor's office, emergency room, hospital bed, or insurance company office."*  
     **Prediction**: Positive (100%)  
   - **Adversarial**: *"A actual audience-pleaser that desired strike a chord with anyone who's ever waited in a doctor's office, eventuality camera, committal bed, or safer venture cabinet."*  
     **Prediction**: Negative (98%)  
   - **Explanation**: Replacing words like "real" with "actual" and introducing nonsensical replacements such as "emergency room" → "eventuality camera" confused the classifier.

---

#### **Skipped Examples**
The attack did not attempt modifications due to constraints or semantic limitations.

1. **Result 3**  
   - **Original**: *"It's like a 'Big Chill' reunion of the Baader-Meinhof gang, only these guys are more harmless pranksters than political activists."*  
     **Prediction**: Negative (84%)  
   - **Adversarial**: [SKIPPED]  
   - **Explanation**: The attack could not make changes that satisfied the semantic and grammatical constraints.

2. **Result 5**  
   - **Original**: *"Red Dragon never cuts corners."*  
     **Prediction**: Negative (99%)  
   - **Adversarial**: [SKIPPED]  
   - **Explanation**: The brevity of the sentence made it challenging to apply meaningful adversarial transformations.

---

#### **Failed Examples**
None observed in this specific run. All attempted attacks either succeeded or were skipped.

---
