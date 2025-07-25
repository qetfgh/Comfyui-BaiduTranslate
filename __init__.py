from .nodes import NODE_CLASS_MAPPINGS as BASIC_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as BASIC_DISPLAY_NAMES
from .baidu_clip_node import NODE_CLASS_MAPPINGS as CLIP_NODE_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as CLIP_DISPLAY_NAMES

# 合并所有节点映射
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 添加基础节点
NODE_CLASS_MAPPINGS.update(BASIC_NODE_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(BASIC_DISPLAY_NAMES)

# 添加CLIP集成节点
NODE_CLASS_MAPPINGS.update(CLIP_NODE_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(CLIP_DISPLAY_NAMES)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']