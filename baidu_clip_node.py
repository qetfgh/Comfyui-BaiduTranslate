import hashlib
import random
import requests
import os
import json
import time


class BaiduTranslateClipTextEncodeNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "clip": ("CLIP", ),
                "from_lang": ([
                    "auto", "zh", "en", "jp", 
                    "kor", "fra", "ru", "de", 
                    "it", "spa", "pt", "ara"
                ], {"default": "auto"}),
                "to_lang": ([
                    "en", "zh", "jp", "kor", 
                    "fra", "ru", "de", "it", 
                    "spa", "pt", "ara"
                ], {"default": "en"}),
                "app_id": ("STRING", {"default": ""}),
                "secret_key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "qetfgh/txt"

    def __init__(self):
        # 使用当前目录保存配置文件
        config_file = "baidu_config.json"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(current_dir, config_file)
        self.config = self.load_config()

    def load_config(self):
        """加载百度翻译配置"""
        default_config = {"app_id": "", "secret_key": ""}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return default_config
        return default_config

    def save_config(self, app_id, secret_key):
        """保存百度翻译配置"""
        config = {"app_id": app_id, "secret_key": secret_key}
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        self.config = config
        return config

    def translate(self, text, from_lang="auto", to_lang="en", 
                  app_id="", secret_key=""):
        if app_id and secret_key:
            self.save_config(app_id, secret_key)
            self.config = {"app_id": app_id, "secret_key": secret_key}
        elif not self.config.get("app_id") or not self.config.get("secret_key"):
            error_msg = ("⚠️ 请先配置百度翻译密钥！\n请在app_id和secret_key字段中输入您的"
                         "百度翻译API密钥。\n\n注册地址: "
                         "https://fanyi-api.baidu.com/product/113")
            raise Exception(error_msg)

        current_app_id = self.config.get("app_id") or app_id
        current_secret_key = self.config.get("secret_key") or secret_key

        if not current_app_id or not current_secret_key:
            error_msg = ("⚠️ 请先配置百度翻译密钥！\n请在app_id和secret_key字段中输入您的"
                         "百度翻译API密钥。\n\n注册地址: "
                         "https://fanyi-api.baidu.com/product/113")
            raise Exception(error_msg)

        if not text.strip():
            return ""

        chunks = self.split_text(text, 2000)
        results = []

        for chunk in chunks:
            salt = str(random.randint(32768, 65536))
            sign_str = current_app_id + chunk + salt + current_secret_key
            sign = hashlib.md5(sign_str.encode()).hexdigest()

            params = {
                "q": chunk,
                "from": from_lang,
                "to": to_lang,
                "appid": current_app_id,
                "salt": salt,
                "sign": sign
            }

            try:
                response = requests.get(
                    "https://api.fanyi.baidu.com/api/trans/vip/translate",
                    params=params,
                    timeout=15,
                )
                result = response.json()

                if "trans_result" in result:
                    translated = " ".join([res["dst"] for res in result["trans_result"]])
                    results.append(translated)
                else:
                    error_msg = result.get("error_msg", "未知错误")
                    raise Exception(f"翻译错误: {error_msg}")

                time.sleep(1.1)

            except Exception as e:
                raise Exception(f"翻译失败: {str(e)}")

        return " ".join(results)

    def split_text(self, text, max_length=2000):
        """将长文本分割为适合API处理的块"""
        if len(text) <= max_length:
            return [text]

        chunks = []
        while text:
            if len(text) <= max_length:
                chunks.append(text)
                break
            # 尝试在句子边界分割
            split_index = text.rfind(".", 0, max_length)
            if split_index == -1:
                split_index = text.rfind(" ", 0, max_length)
            if split_index == -1:
                split_index = max_length

            chunks.append(text[:split_index+1])
            text = text[split_index+1:]

        return chunks

    def encode(self, text, clip, from_lang="auto", to_lang="en", 
               app_id="", secret_key=""):
        # 先进行翻译
        translated_text = self.translate(text, from_lang, to_lang, 
                                         app_id, secret_key)
        
        # 对翻译后的文本进行编码
        tokens = clip.tokenize(translated_text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]], )


# 节点映射
NODE_CLASS_MAPPINGS = {
    "BaiduTranslateClipTextEncode": BaiduTranslateClipTextEncodeNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BaiduTranslateClipTextEncode": "CLIP文本编码(百度翻译)"
}