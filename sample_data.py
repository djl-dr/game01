#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例数据生成器
用于创建Python编程基础词库的示例数据
"""

import json

def create_sample_data():
    """创建示例数据"""
    sample_vocab_data = [
        {
            "content": "for 循环",
            "category": "循环结构",
            "explanation": "for循环是Python中最常用的循环结构，用于遍历可迭代对象（如列表、元组、字符串等）",
            "example": "for i in range(5):\n    print(i)\n# 输出：0, 1, 2, 3, 4",
            "pronunciation": "for 循环"
        },
        {
            "content": "while 循环",
            "category": "循环结构",
            "explanation": "while循环在条件为真时重复执行代码块，直到条件变为假",
            "example": "count = 0\nwhile count < 5:\n    print(count)\n    count += 1",
            "pronunciation": "while 循环"
        },
        {
            "content": "str 字符串",
            "category": "数据类型",
            "explanation": "字符串是Python中的文本数据类型，用单引号或双引号包围",
            "example": "name = 'Python'\nmessage = \"Hello, World!\"\nprint(name + ' ' + message)",
            "pronunciation": "string 字符串"
        },
        {
            "content": "list 列表",
            "category": "数据类型",
            "explanation": "列表是Python中最常用的数据类型，可以存储多个元素，支持增删改查操作",
            "example": "fruits = ['apple', 'banana', 'orange']\nfruits.append('grape')\nprint(fruits[0])",
            "pronunciation": "list 列表"
        },
        {
            "content": "dict 字典",
            "category": "数据类型",
            "explanation": "字典是键值对的数据结构，通过键来访问值，键必须是不可变类型",
            "example": "person = {'name': 'Alice', 'age': 25}\nprint(person['name'])\nperson['city'] = 'Beijing'",
            "pronunciation": "dictionary 字典"
        },
        {
            "content": "def 函数定义",
            "category": "函数与类",
            "explanation": "def关键字用于定义函数，函数是一段可重用的代码块",
            "example": "def greet(name):\n    return f'Hello, {name}!'\n\nresult = greet('World')\nprint(result)",
            "pronunciation": "define 函数定义"
        },
        {
            "content": "class 类定义",
            "category": "函数与类",
            "explanation": "class关键字用于定义类，类是面向对象编程的基础，可以创建对象",
            "example": "class Person:\n    def __init__(self, name):\n        self.name = name\n    \n    def greet(self):\n        return f'Hello, I am {self.name}'",
            "pronunciation": "class 类定义"
        },
        {
            "content": "if 条件语句",
            "category": "关键字",
            "explanation": "if语句用于条件判断，根据条件是否为真执行不同的代码块",
            "example": "age = 18\nif age >= 18:\n    print('成年人')\nelif age >= 12:\n    print('青少年')\nelse:\n    print('儿童')",
            "pronunciation": "if 条件语句"
        },
        {
            "content": "try-except 异常处理",
            "category": "异常处理",
            "explanation": "try-except语句用于捕获和处理程序运行时的异常，提高程序的健壮性",
            "example": "try:\n    number = int(input('请输入数字：'))\n    result = 10 / number\n    print(result)\nexcept ValueError:\n    print('输入的不是有效数字')\nexcept ZeroDivisionError:\n    print('不能除以零')",
            "pronunciation": "try except 异常处理"
        },
        {
            "content": "import 模块导入",
            "category": "模块导入",
            "explanation": "import语句用于导入Python模块，使用模块中的函数、类或变量",
            "example": "import math\nprint(math.pi)\nprint(math.sqrt(16))\n\nfrom datetime import datetime\nprint(datetime.now())",
            "pronunciation": "import 模块导入"
        },
        {
            "content": "open() 文件操作",
            "category": "文件操作",
            "explanation": "open()函数用于打开文件，支持读取、写入、追加等操作模式",
            "example": "# 读取文件\nwith open('file.txt', 'r', encoding='utf-8') as f:\n    content = f.read()\n\n# 写入文件\nwith open('output.txt', 'w', encoding='utf-8') as f:\n    f.write('Hello, World!')",
            "pronunciation": "open 文件操作"
        },
        {
            "content": "range() 范围函数",
            "category": "内置函数",
            "explanation": "range()函数用于生成一个数字序列，常用于for循环中",
            "example": "# 生成0到4的序列\nfor i in range(5):\n    print(i)\n\n# 生成2到10的序列，步长为2\nfor i in range(2, 11, 2):\n    print(i)",
            "pronunciation": "range 范围函数"
        }
    ]
    
    # 预设分类
    categories = {
        "关键字", "数据类型", "循环结构", "函数与类", 
        "文件操作", "异常处理", "模块导入", "数据结构", "内置函数"
    }
    
    # 创建数据字典
    data = {
        'vocab_data': sample_vocab_data,
        'categories': list(categories)
    }
    
    # 保存到文件
    with open('vocab_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 示例数据创建成功！")
    print(f"📚 创建了 {len(sample_vocab_data)} 个示例词条")
    print(f"🏷️  包含 {len(categories)} 个分类")
    print("📁 数据已保存到 vocab_data.json 文件")

if __name__ == "__main__":
    create_sample_data() 