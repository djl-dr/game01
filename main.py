#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python编程基础词库工具
作者：AI助手
功能：帮助用户整理和记忆Python基础语法知识
"""

import json
import os
import sys
from typing import List, Dict, Optional

# 尝试导入语音库，如果失败则提供提示
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("提示：未安装pyttsx3库，语音朗读功能将不可用")
    print("安装命令：pip install pyttsx3")

class PythonVocabTool:
    """Python编程基础词库工具主类"""
    
    def __init__(self, data_file: str = "vocab_data.json"):
        """
        初始化词库工具
        
        Args:
            data_file: 数据文件路径
        """
        self.data_file = data_file
        self.vocab_data = []  # 存储所有词条数据
        self.categories = set()  # 存储所有分类
        
        # 预设分类
        self.default_categories = {
            "关键字", "数据类型", "循环结构", "函数与类", 
            "文件操作", "异常处理", "模块导入", "数据结构"
        }
        
        # 初始化语音引擎
        self.tts_engine = None
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)  # 默认语速
            except Exception as e:
                print(f"语音引擎初始化失败：{e}")
        
        # 加载数据
        self.load_data()
    
    def load_data(self) -> None:
        """从文件加载数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.vocab_data = data.get('vocab_data', [])
                    self.categories = set(data.get('categories', []))
                    # 确保默认分类存在
                    self.categories.update(self.default_categories)
                print(f"✅ 成功加载 {len(self.vocab_data)} 个词条")
            else:
                print("📝 数据文件不存在，将创建新的词库")
                self.categories.update(self.default_categories)
        except Exception as e:
            print(f"❌ 加载数据失败：{e}")
            self.categories.update(self.default_categories)
    
    def save_data(self) -> None:
        """保存数据到文件"""
        try:
            data = {
                'vocab_data': self.vocab_data,
                'categories': list(self.categories)
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ 数据保存成功")
        except Exception as e:
            print(f"❌ 保存数据失败：{e}")
    
    def add_entry(self) -> None:
        """添加新词条"""
        print("\n" + "="*50)
        print("📝 添加新词条")
        print("="*50)
        
        # 获取词条信息
        content = input("请输入核心内容（如：for 循环）：").strip()
        if not content:
            print("❌ 核心内容不能为空")
            return
        
        # 显示现有分类
        print(f"\n现有分类：{', '.join(sorted(self.categories))}")
        category = input("请输入分类（输入新分类名可创建新分类）：").strip()
        if not category:
            print("❌ 分类不能为空")
            return
        
        explanation = input("请输入详细解释：").strip()
        example = input("请输入示例代码：").strip()
        pronunciation = input("请输入发音提示（可选）：").strip()
        
        # 创建新词条
        entry = {
            'content': content,
            'category': category,
            'explanation': explanation,
            'example': example,
            'pronunciation': pronunciation
        }
        
        # 添加到数据中
        self.vocab_data.append(entry)
        self.categories.add(category)
        
        # 保存数据
        self.save_data()
        print(f"✅ 成功添加词条：{content}")
    
    def view_entries(self) -> None:
        """查看词条"""
        print("\n" + "="*50)
        print("📖 查看词条")
        print("="*50)
        
        if not self.vocab_data:
            print("📝 词库为空，请先添加一些词条")
            return
        
        print("选择查看方式：")
        print("1. 按分类查看")
        print("2. 按关键词搜索")
        print("3. 查看所有词条")
        
        choice = input("请选择（1-3）：").strip()
        
        if choice == "1":
            self.view_by_category()
        elif choice == "2":
            self.search_entries()
        elif choice == "3":
            self.view_all_entries()
        else:
            print("❌ 无效选择")
    
    def view_by_category(self) -> None:
        """按分类查看词条"""
        print(f"\n现有分类：{', '.join(sorted(self.categories))}")
        category = input("请输入要查看的分类：").strip()
        
        if category not in self.categories:
            print("❌ 分类不存在")
            return
        
        entries = [entry for entry in self.vocab_data if entry['category'] == category]
        if not entries:
            print(f"📝 分类 '{category}' 下没有词条")
            return
        
        print(f"\n📚 分类 '{category}' 下的词条：")
        for i, entry in enumerate(entries, 1):
            self.display_entry(entry, i)
    
    def search_entries(self) -> None:
        """搜索词条"""
        keyword = input("请输入搜索关键词：").strip()
        if not keyword:
            print("❌ 关键词不能为空")
            return
        
        results = []
        for entry in self.vocab_data:
            if (keyword.lower() in entry['content'].lower() or 
                keyword.lower() in entry['explanation'].lower()):
                results.append(entry)
        
        if not results:
            print(f"🔍 未找到包含 '{keyword}' 的词条")
            return
        
        print(f"\n🔍 找到 {len(results)} 个相关词条：")
        for i, entry in enumerate(results, 1):
            self.display_entry(entry, i)
    
    def view_all_entries(self) -> None:
        """查看所有词条"""
        print(f"\n📚 所有词条（共 {len(self.vocab_data)} 个）：")
        for i, entry in enumerate(self.vocab_data, 1):
            self.display_entry(entry, i)
    
    def display_entry(self, entry: Dict, index: int = None) -> None:
        """显示单个词条"""
        prefix = f"{index}. " if index else ""
        print(f"\n{prefix}{'='*40}")
        print(f"📝 内容：{entry['content']}")
        print(f"🏷️  分类：{entry['category']}")
        print(f"📖 解释：{entry['explanation']}")
        if entry['example']:
            print(f"💻 示例：\n{entry['example']}")
        if entry['pronunciation']:
            print(f"🔊 发音：{entry['pronunciation']}")
        print("="*40)
    
    def edit_delete_entry(self) -> None:
        """编辑或删除词条"""
        print("\n" + "="*50)
        print("✏️  编辑/删除词条")
        print("="*50)
        
        if not self.vocab_data:
            print("📝 词库为空")
            return
        
        # 显示所有词条供选择
        print("现有词条：")
        for i, entry in enumerate(self.vocab_data, 1):
            print(f"{i}. {entry['content']} ({entry['category']})")
        
        try:
            choice = int(input(f"\n请选择要操作的词条（1-{len(self.vocab_data)}）："))
            if choice < 1 or choice > len(self.vocab_data):
                print("❌ 无效选择")
                return
            
            entry_index = choice - 1
            entry = self.vocab_data[entry_index]
            
            print(f"\n当前词条：{entry['content']}")
            print("1. 编辑词条")
            print("2. 删除词条")
            
            action = input("请选择操作（1-2）：").strip()
            
            if action == "1":
                self.edit_entry(entry_index)
            elif action == "2":
                self.delete_entry(entry_index)
            else:
                print("❌ 无效选择")
                
        except ValueError:
            print("❌ 请输入有效数字")
    
    def edit_entry(self, index: int) -> None:
        """编辑词条"""
        entry = self.vocab_data[index]
        print(f"\n编辑词条：{entry['content']}")
        
        # 逐个字段编辑
        content = input(f"核心内容（当前：{entry['content']}）：").strip()
        if content:
            entry['content'] = content
        
        print(f"现有分类：{', '.join(sorted(self.categories))}")
        category = input(f"分类（当前：{entry['category']}）：").strip()
        if category:
            entry['category'] = category
            self.categories.add(category)
        
        explanation = input(f"详细解释（当前：{entry['explanation']}）：").strip()
        if explanation:
            entry['explanation'] = explanation
        
        example = input(f"示例代码（当前：{entry['example']}）：").strip()
        if example:
            entry['example'] = example
        
        pronunciation = input(f"发音提示（当前：{entry['pronunciation']}）：").strip()
        if pronunciation:
            entry['pronunciation'] = pronunciation
        
        self.save_data()
        print("✅ 词条编辑成功")
    
    def delete_entry(self, index: int) -> None:
        """删除词条"""
        entry = self.vocab_data[index]
        confirm = input(f"确定要删除词条 '{entry['content']}' 吗？（y/N）：").strip().lower()
        
        if confirm == 'y':
            del self.vocab_data[index]
            self.save_data()
            print("✅ 词条删除成功")
        else:
            print("❌ 取消删除")
    
    def text_to_speech(self) -> None:
        """语音朗读功能"""
        if not TTS_AVAILABLE or not self.tts_engine:
            print("❌ 语音朗读功能不可用")
            return
        
        print("\n" + "="*50)
        print("🔊 语音朗读")
        print("="*50)
        
        if not self.vocab_data:
            print("📝 词库为空")
            return
        
        # 显示所有词条供选择
        print("选择要朗读的词条：")
        for i, entry in enumerate(self.vocab_data, 1):
            print(f"{i}. {entry['content']}")
        
        try:
            choice = int(input(f"\n请选择词条（1-{len(self.vocab_data)}）："))
            if choice < 1 or choice > len(self.vocab_data):
                print("❌ 无效选择")
                return
            
            entry = self.vocab_data[choice - 1]
            
            print("朗读选项：")
            print("1. 仅朗读核心内容")
            print("2. 朗读完整信息")
            
            option = input("请选择（1-2）：").strip()
            
            if option == "1":
                text = entry['content']
            elif option == "2":
                text = f"{entry['content']}。{entry['explanation']}"
            else:
                print("❌ 无效选择")
                return
            
            print(f"🔊 正在朗读：{text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            print("✅ 朗读完成")
            
        except ValueError:
            print("❌ 请输入有效数字")
    
    def manage_categories(self) -> None:
        """管理分类"""
        print("\n" + "="*50)
        print("🏷️  管理分类")
        print("="*50)
        
        print("1. 查看所有分类")
        print("2. 添加新分类")
        print("3. 删除分类")
        
        choice = input("请选择操作（1-3）：").strip()
        
        if choice == "1":
            self.view_categories()
        elif choice == "2":
            self.add_category()
        elif choice == "3":
            self.delete_category()
        else:
            print("❌ 无效选择")
    
    def view_categories(self) -> None:
        """查看所有分类"""
        print(f"\n📚 所有分类（共 {len(self.categories)} 个）：")
        for i, category in enumerate(sorted(self.categories), 1):
            count = len([entry for entry in self.vocab_data if entry['category'] == category])
            print(f"{i}. {category} ({count} 个词条)")
    
    def add_category(self) -> None:
        """添加新分类"""
        category = input("请输入新分类名称：").strip()
        if not category:
            print("❌ 分类名称不能为空")
            return
        
        if category in self.categories:
            print("❌ 分类已存在")
            return
        
        self.categories.add(category)
        self.save_data()
        print(f"✅ 成功添加分类：{category}")
    
    def delete_category(self) -> None:
        """删除分类"""
        print(f"\n现有分类：{', '.join(sorted(self.categories))}")
        category = input("请输入要删除的分类：").strip()
        
        if category not in self.categories:
            print("❌ 分类不存在")
            return
        
        # 检查分类下是否有词条
        entries_in_category = [entry for entry in self.vocab_data if entry['category'] == category]
        if entries_in_category:
            print(f"❌ 分类 '{category}' 下还有 {len(entries_in_category)} 个词条，无法删除")
            print("请先删除或移动这些词条")
            return
        
        confirm = input(f"确定要删除分类 '{category}' 吗？（y/N）：").strip().lower()
        if confirm == 'y':
            self.categories.remove(category)
            self.save_data()
            print(f"✅ 成功删除分类：{category}")
        else:
            print("❌ 取消删除")
    
    def show_menu(self) -> None:
        """显示主菜单"""
        print("\n" + "="*60)
        print("🐍 Python编程基础词库工具")
        print("="*60)
        print(f"📚 当前词库：{len(self.vocab_data)} 个词条")
        print(f"🏷️  分类数量：{len(self.categories)} 个")
        print("="*60)
        print("1. 📖 查看条目（按分类/搜索）")
        print("2. 📝 添加新条目")
        print("3. ✏️  修改/删除条目")
        print("4. 🔊 语音朗读条目")
        print("5. 🏷️  管理分类（添加/删除分类）")
        print("6. 🚪 退出程序")
        print("="*60)
    
    def run(self) -> None:
        """运行主程序"""
        print("🐍 欢迎使用Python编程基础词库工具！")
        
        while True:
            self.show_menu()
            choice = input("请选择操作（1-6）：").strip()
            
            if choice == "1":
                self.view_entries()
            elif choice == "2":
                self.add_entry()
            elif choice == "3":
                self.edit_delete_entry()
            elif choice == "4":
                self.text_to_speech()
            elif choice == "5":
                self.manage_categories()
            elif choice == "6":
                print("👋 感谢使用，再见！")
                break
            else:
                print("❌ 无效选择，请输入1-6之间的数字")
            
            input("\n按回车键继续...")


def main():
    """主函数"""
    try:
        tool = PythonVocabTool()
        tool.run()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，再见！")
    except Exception as e:
        print(f"\n❌ 程序运行出错：{e}")
        print("请检查数据文件或重新运行程序")


if __name__ == "__main__":
    main() 