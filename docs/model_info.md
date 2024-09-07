- **name**: String
  - The identifier for the specific model or model version. Used when making API calls to select a particular model.

- **family**: String
  - Groups related models together (e.g., "GPT-4", "GPT-3.5", "DALL-E").

- **points_to**: String | null
  - If the model name is an alias, this indicates the specific version it refers to. Null for specific versions.

- **max_memory_tokens**: Integer | null
  - The maximum number of tokens the model can process in a single context window, including both input and output tokens.

- **max_request_tokens**: Integer | null
  - The maximum number of tokens that can be sent as input to the model.

- **max_response_tokens**: Integer | null
  - The maximum number of tokens the model can generate in a single response.

- **description**: String
  - A brief explanation of the model's capabilities, use cases, or distinguishing features.

- **modalities**: Array of Strings
  - The types of inputs and outputs the model can handle. Possible values include:
    - "txt-to-txt": Natural language processing tasks
    - "txt-to-cod": Generating code from natural language descriptions
    - "cod-to-cod": Code completion, refactoring, or translation
    - "img-to-txt": Describing or analyzing images
    - "txt-to-img": Generating images from text descriptions
    - "txt-to-aud": Converting text to spoken audio
    - "aud-to-txt": Transcribing spoken audio to text
    - "aud-to-txt-translation": Transcribing and translating spoken audio
    - "txt-to-emb": Generating vector embeddings from text
    - "text-moderation": Content moderation

- **is_legacy**: Boolean
  - Indicates whether the model is considered outdated or deprecated. 
  - Set to true for models with a training_end_date before June 2023.
  - Set to false for models with a training_end_date of June 2023 or later, or if the training_end_date is null.

- **training_end_date**: String (format: "MM/YYYY") | null
  - The month and year when the model's training data cutoff occurred.
  - Null for continuously updated models or when the date is not specified.

- **output_dimension**: Integer | null (only for embedding models)
  - The size of the vector representation produced by embedding models.