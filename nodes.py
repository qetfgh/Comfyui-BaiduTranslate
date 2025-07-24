import hashlib
import random
import requests
import os
import json
import time


class BaiduTranslateNode:
    def __init__(self):
        # 使用当前目录保存配置文件
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baidu_config.json")
        self.config = self.load_config()
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            },
            "optional": {
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
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("translated_text",)
    FUNCTION = "translate"
    CATEGORY = "tools/translation"
    # 移除OUTPUT_NODE = True，因为这不是一个输出节点

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

    def translate(self, text, from_lang="auto", to_lang="en", app_id="", secret_key=""):
        # 如果提供了app_id和secret_key，则保存配置
        if app_id and secret_key:
            self.save_config(app_id, secret_key)
            # 更新当前实例的配置
            self.config = {"app_id": app_id, "secret_key": secret_key}
        # 检查是否已配置密钥
        elif not self.config.get("app_id") or not self.config.get("secret_key"):
            return ("⚠️ 请先配置百度翻译密钥！\n请在app_id和secret_key字段中输入您的百度翻译API密钥。\n\n注册地址: https://fanyi-api.baidu.com/product/113",)
        
        # 获取当前使用的配置
        current_app_id = self.config.get("app_id") or app_id
        current_secret_key = self.config.get("secret_key") or secret_key
        
        # 再次检查配置是否有效
        if not current_app_id or not current_secret_key:
            return ("⚠️ 请先配置百度翻译密钥！\n请在app_id和secret_key字段中输入您的百度翻译API密钥。\n\n注册地址: https://fanyi-api.baidu.com/product/113",)
        
        # 检查文本是否为空
        if not text.strip():
            return ("",)
        
        # 长文本分块处理（百度API限制6000字节/次）
        chunks = self.split_text(text, 2000)
        results = []
        
        for chunk in chunks:
            # 百度API签名生成
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
                    timeout=15
                )
                result = response.json()
                
                if "trans_result" in result:
                    translated = " ".join([res["dst"] for res in result["trans_result"]])
                    results.append(translated)
                else:
                    error_msg = result.get("error_msg", "未知错误")
                    return (f"翻译错误: {error_msg}",)
                
                # 遵守免费版QPS限制
                time.sleep(1.1)
                
            except Exception as e:
                return (f"翻译失败: {str(e)}",)
        
        return (" ".join(results),)
    
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


class BaiduConfigNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "app_id": ("STRING", {"default": ""}),
                "secret_key": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ()
    FUNCTION = "save_config"
    CATEGORY = "tools/translation"
    OUTPUT_NODE = True

    def save_config(self, app_id, secret_key):
        # 使用翻译节点保存配置
        translator = BaiduTranslateNode()
        translator.save_config(app_id, secret_key)
        return ()


# 节点映射
NODE_CLASS_MAPPINGS = {
    "BaiduTranslate": BaiduTranslateNode,
    "BaiduConfig": BaiduConfigNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BaiduTranslate": "🔤 百度翻译",
    "BaiduConfig": "⚙️ 百度翻译配置"
}