# Comfyui-BaiduTranslate nodes

这是一个基于百度翻译API的ComfyUI自定义节点，可以将文本翻译成多种语言，并直接连接到CLIP文本编码器节点。

## 功能特点

- 支持多种语言互译
- 自动保存配置信息
- 支持长文本分段翻译
- 翻译结果可直接连接至CLIP Text Encode节点
- 友好的用户提示界面
- 提供集成翻译和编码的一体化节点

## 安装方法

1. 进入ComfyUI的custom_nodes目录
   ```bash
   cd ComfyUI/custom_nodes
   ```
2. 克隆本项目
   ```bash
   git clone https://github.com/qetfgh/Comfyui-BaiduTranslate.git
   ```
   或者下载并解压项目文件到该目录
3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

## 获取百度翻译API密钥

1. 访问 [百度翻译开放平台](https://fanyi-api.baidu.com/)
2. 注册账号并登录
3. 在管理控制台中创建应用，获取APP ID和密钥

## 使用方法

### 方法一：在翻译节点中直接输入密钥（推荐）

1. 在ComfyUI中添加"🔤 百度翻译"节点
2. 双击节点，在`app_id`和`secret_key`字段中输入您的百度翻译API密钥
3. 输入要翻译的文本到`text`字段
4. 设置源语言和目标语言
5. 将翻译结果连接到CLIP Text Encode节点或其他需要文本输入的节点

![百度翻译连接示意图](https://github.com/user-attachments/assets/845e6576-4f53-46ec-9f53-d5337dd05e71)


### 方法二：使用专用配置节点

1. 在ComfyUI中添加"⚙️ 百度翻译配置"节点
2. 输入您的`app_id`和`secret_key`
3. 运行一次该节点以保存配置
4. 添加"🔤 百度翻译"节点，无需再次输入密钥
5. 输入要翻译的文本并设置语言选项

### 方法三：使用一体化翻译编码节点（推荐用于工作流简化）

1. 在ComfyUI中添加"CLIP文本编码(百度翻译)"节点
2. 连接模型加载节点到`clip`输入端口
3. 在`app_id`和`secret_key`字段中输入您的百度翻译API密钥
4. 输入要翻译的文本到`text`字段
5. 设置源语言和目标语言
6. 节点将直接输出CONDITIONING数据，可直接连接到KSampler等节点

![CLIP文本编码(百度翻译)](https://github.com/user-attachments/assets/343a0d26-1811-4bd8-9d98-63a182e520b8)


## 节点说明

### 🔤 百度翻译

主要翻译节点，支持以下参数：
- `text`: 要翻译的文本（多行输入）
- `from_lang`: 源语言（默认auto自动检测）
  - auto: 自动检测
  - zh: 中文
  - en: 英语
  - jp: 日语
  - kor: 韩语
  - fra: 法语
  - ru: 俄语
  - de: 德语
  - it: 意大利语
  - spa: 西班牙语
  - pt: 葡萄牙语
  - ara: 阿拉伯语
- `to_lang`: 目标语言（默认en英语）
- `app_id`: 百度翻译APP ID（可选，如果已配置则无需输入）
- `secret_key`: 百度翻译密钥（可选，如果已配置则无需输入）

### ⚙️ 百度翻译配置

专门用于配置和保存APP ID和密钥的节点。

### CLIP文本编码(百度翻译)

集成翻译和CLIP编码功能的一体化节点，支持以下参数：
- `text`: 要翻译的文本（多行输入）
- `clip`: CLIP模型输入
- `from_lang`: 源语言（默认auto自动检测）
- `to_lang`: 目标语言（默认en英语）
- `app_id`: 百度翻译APP ID
- `secret_key`: 百度翻译密钥

## 使用提示

1. 密钥配置会自动保存在插件目录下的`baidu_config.json`文件中
2. 如果未配置密钥，节点会显示友好的提示信息，指导您如何配置
3. 支持长文本翻译，系统会自动分段处理
4. 翻译结果可以直接连接到CLIP Text Encode节点用于图像生成
5. 一体化节点简化了工作流，无需单独连接翻译节点和CLIP编码节点

## 常见问题

### 为什么提示需要配置密钥？

首次使用节点时，必须配置百度翻译API的APP ID和密钥。请按照以下步骤操作：
1. 访问[百度翻译开放平台](https://fanyi-api.baidu.com/product/113)注册账号
2. 创建应用获取APP ID和密钥
3. 在节点的对应字段中输入密钥

### 翻译结果为空怎么办？

请检查以下几点：
1. 确认已正确配置API密钥
2. 检查输入的文本是否为空
3. 确保网络连接正常

## 节点连接

翻译节点返回的是标准字符串类型，可以连接到任何需要文本输入的节点，例如：
- CLIP Text Encode (Prompt)
- Save Text File
- 其他自定义文本处理节点

一体化节点直接输出CONDITIONING数据，可以连接到以下节点：
- KSampler
- ConditioningCombine
- 其他接受CONDITIONING输入的节点

## 支持语言

| 代码 | 语言   | 代码 | 语言     |
|------|--------|------|----------|
| auto | 自动检测 | fra  | 法语     |
| zh   | 中文   | ru   | 俄语     |
| en   | 英语   | de   | 德语     |
| jp   | 日语   | it   | 意大利语 |
| kor  | 韩语   | spa  | 西班牙语 |
| pt   | 葡萄牙语 | ara  | 阿拉伯语 |
