import re
from typing import List, Tuple

def clean_and_truncate_text(text: str, max_length: int = 15000) -> str:
    """
    清理和截断文本内容，去除多余空白和非必要内容，提取关键信息
    
    Args:
        text: 原始文本
        max_length: 最大保留字符数
    
    Returns:
        清理并截断后的文本
    """
    # 移除多余的空白行和空格
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    # 如果文本太长，进行智能截断（保留开头和结尾部分）
    if len(text) > max_length:
        # 保留开头和结尾
        start_portion = int(max_length * 0.7)  # 70%的内容从开头取
        end_portion = max_length - start_portion  # 30%的内容从结尾取
        
        text = text[:start_portion] + "\n...[内容已截断]...\n" + text[-end_portion:]
    
    return text

def extract_key_sections(text: str, keyword_list: List[str] = None) -> str:
    """
    从文本中提取包含关键词的段落，用于减少文本量但保留重要信息
    
    Args:
        text: 原始文本
        keyword_list: 关键词列表，如果为None则使用默认关键词
    
    Returns:
        包含关键词的段落
    """
    if keyword_list is None:
        # 默认关键词列表
        keyword_list = [
            "概念", "定义", "结论", "总结", "关键", "重要", "核心",
            "特点", "特性", "原理", "方法", "技术", "流程", "步骤"
        ]
    
    # 按段落分割文本
    paragraphs = re.split(r'\n\s*\n', text)
    
    # 提取包含关键词的段落
    key_paragraphs = []
    for para in paragraphs:
        if any(keyword in para for keyword in keyword_list):
            key_paragraphs.append(para)
    
    # 如果没有找到关键段落，返回原文的一部分
    if not key_paragraphs:
        return text[:15000] if len(text) > 15000 else text
    
    return "\n\n".join(key_paragraphs)
