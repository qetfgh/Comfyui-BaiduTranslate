# ComfyUI Baidu Translate Node

This is a custom ComfyUI node based on Baidu Translate API that can translate text into multiple languages and directly connect to CLIP text encoder nodes.

## Features

- Support for multiple language translation
- Automatic configuration saving
- Long text segmentation translation
- Translation results can be directly connected to CLIP Text Encode nodes
- User-friendly prompt interface
- Integrated translation and encoding node

## Installation

1. Navigate to ComfyUI's custom_nodes directory
   ```bash
   cd ComfyUI/custom_nodes
   ```
2. Clone this repository
   ```bash
   git clone https://github.com/qetfgh/Comfyui-BaiduTranslate.git
   ```
   Or download and extract the project files to this directory
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Getting Baidu Translate API Key

1. Visit [Baidu Translate Open Platform](https://fanyi-api.baidu.com/)
2. Register an account and log in
3. Create an application in the management console to get the APP ID and secret key

## Usage

### Method 1: Enter API keys directly in the translation node (Recommended)

1. Add the "🔤 Baidu Translate" node in ComfyUI
2. Double-click the node and enter your Baidu Translate API `app_id` and `secret_key` in the fields
3. Enter the text to be translated in the `text` field
4. Set the source and target languages
5. Connect the translation result to the CLIP Text Encode node or other nodes that require text input

![百度翻译连接示意图](https://github.com/user-attachments/assets/0218e91a-d475-4346-901b-4ab5f6ffed12)


### Method 2: Use dedicated configuration node

1. Add the "⚙️ Baidu Translate Config" node in ComfyUI
2. Enter your `app_id` and `secret_key`
3. Run the node once to save the configuration
4. Add the "🔤 Baidu Translate" node without re-entering the keys
5. Enter the text to be translated and set language options

### Method 3: Use integrated translation encoding node (Recommended for workflow simplification)

1. Add the "CLIP Text Encode (Baidu Translate)" node in ComfyUI
2. Connect the CLIP model to the `clip` input port
3. Enter your Baidu Translate API `app_id` and `secret_key` in the fields
4. Enter the text to be translated in the `text` field
5. Set the source and target languages
6. The node will directly output CONDITIONING data that can be connected to KSampler and other nodes

![Uploading CLIP文本编码(百度翻译).png…]()


## Node Descriptions

### 🔤 Baidu Translate

Main translation node with the following parameters:
- `text`: Text to be translated (multi-line input)
- `from_lang`: Source language (default auto for automatic detection)
  - auto: Automatic detection
  - zh: Chinese
  - en: English
  - jp: Japanese
  - kor: Korean
  - fra: French
  - ru: Russian
  - de: German
  - it: Italian
  - spa: Spanish
  - pt: Portuguese
  - ara: Arabic
- `to_lang`: Target language (default en for English)
- `app_id`: Baidu Translate APP ID
- `secret_key`: Baidu Translate secret key

### ⚙️ Baidu Translate Config

Node specifically for configuring and saving APP ID and secret key.

### CLIP Text Encode (Baidu Translate)

Integrated node with translation and CLIP encoding functions, with the following parameters:
- `text`: Text to be translated (multi-line input)
- `clip`: CLIP model input
- `from_lang`: Source language (default auto for automatic detection)
- `to_lang`: Target language (default en for English)
- `app_id`: Baidu Translate APP ID
- `secret_key`: Baidu Translate secret key

## Usage Tips

1. Key configurations are automatically saved in the `baidu_config.json` file in the plugin directory
2. If keys are not configured, the node will display a friendly prompt guiding you on how to configure them
3. Supports long text translation with automatic segmentation
4. Translation results can be directly connected to CLIP Text Encode nodes for image generation
5. The integrated node simplifies workflow without needing to separately connect translation and CLIP encoding nodes

## FAQ

### Why does it prompt to configure API keys?

When using the node for the first time, you must configure Baidu Translate API's APP ID and secret key. Please follow these steps:
1. Visit [Baidu Translate Open Platform](https://fanyi-api.baidu.com/product/113) to register an account
2. Create an application to get the APP ID and secret key
3. Enter the keys in the corresponding fields of the node

### What if the translation result is empty?

Please check the following:
1. Confirm that the API keys are correctly configured
2. Check if the input text is empty
3. Ensure network connectivity

## Node Connections

The translation node returns a standard string type that can be connected to any node requiring text input, such as:
- CLIP Text Encode (Prompt)
- Save Text File
- Other custom text processing nodes

The integrated node directly outputs CONDITIONING data that can be connected to the following nodes:
- KSampler
- ConditioningCombine
- Other nodes accepting CONDITIONING input

## Supported Languages

| Code | Language    | Code | Language    |
|------|-------------|------|-------------|
| auto | Auto detect | fra  | French      |
| zh   | Chinese     | ru   | Russian     |
| en   | English     | de   | German      |
| jp   | Japanese    | it   | Italian     |
| kor  | Korean      | spa  | Spanish     |
| pt   | Portuguese  | ara  | Arabic      |
