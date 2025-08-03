// 全局变量
let vocabData = [];
let categories = new Set();

// 默认分类
const defaultCategories = [
    "关键字", "数据类型", "循环结构", "函数与类", 
    "文件操作", "异常处理", "模块导入", "数据结构", "内置函数"
];

// 初始化应用
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    initializeEventListeners();
    updateStats();
    renderEntries();
    renderCategories();
    updateCategoryFilter();
    updateAddEntryCategorySelect();
});

// 数据管理
function loadData() {
    const savedData = localStorage.getItem('pythonVocabData');
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            vocabData = data.vocab_data || [];
            categories = new Set(data.categories || []);
        } catch (error) {
            console.error('加载数据失败:', error);
            vocabData = [];
            categories = new Set();
        }
    }
    
    // 确保默认分类存在
    defaultCategories.forEach(cat => categories.add(cat));
}

function saveData() {
    const data = {
        vocab_data: vocabData,
        categories: Array.from(categories)
    };
    localStorage.setItem('pythonVocabData', JSON.stringify(data));
}

// 事件监听器初始化
function initializeEventListeners() {
    // 导航按钮
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.getAttribute('data-tab');
            switchTab(tab);
        });
    });

    // 添加词条表单
    document.getElementById('add-entry-form').addEventListener('submit', function(e) {
        e.preventDefault();
        addEntry();
    });

    // 分类筛选
    document.getElementById('category-filter').addEventListener('change', function() {
        filterEntries();
    });

    // 清除筛选
    document.getElementById('clear-filter').addEventListener('click', function() {
        document.getElementById('category-filter').value = '';
        filterEntries();
    });

    // 搜索功能
    document.getElementById('search-btn').addEventListener('click', function() {
        searchEntries();
    });

    document.getElementById('search-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchEntries();
        }
    });

    // 添加分类
    document.getElementById('add-category-submit').addEventListener('click', function() {
        addCategory();
    });

    // 添加词条页面的新建分类按钮
    document.getElementById('add-category-btn').addEventListener('click', function() {
        // 切换到分类管理页面
        switchTab('categories');
        // 聚焦到新建分类输入框
        setTimeout(() => {
            document.getElementById('new-category').focus();
        }, 100);
    });

    // 导出功能
    document.getElementById('export-json').addEventListener('click', function() {
        exportData('json');
    });

    document.getElementById('export-txt').addEventListener('click', function() {
        exportData('txt');
    });

    document.getElementById('export-md').addEventListener('click', function() {
        exportData('md');
    });

    // 导入功能
    document.getElementById('import-btn').addEventListener('click', function() {
        document.getElementById('import-file').click();
    });

    document.getElementById('import-file').addEventListener('change', function(e) {
        importData(e.target.files[0]);
    });

    // 清空数据
    document.getElementById('clear-data').addEventListener('click', function() {
        if (confirm('确定要清空所有数据吗？此操作不可恢复！')) {
            clearAllData();
        }
    });

    // 模态框关闭
    document.querySelector('.modal-close').addEventListener('click', function() {
        closeModal();
    });

    // 通知关闭
    document.querySelector('.notification-close').addEventListener('click', function() {
        hideNotification();
    });

    // 点击模态框背景关闭
    document.getElementById('modal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeModal();
        }
    });
}

// 标签页切换
function switchTab(tabName) {
    // 隐藏所有标签页
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // 移除所有导航按钮的active状态
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // 显示选中的标签页
    document.getElementById(tabName).classList.add('active');

    // 激活对应的导航按钮
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // 特殊处理
    if (tabName === 'home') {
        renderEntries();
    } else if (tabName === 'categories') {
        renderCategories();
    }
}

// 添加词条
function addEntry() {
    const form = document.getElementById('add-entry-form');
    const formData = new FormData(form);
    
    const entry = {
        id: Date.now(), // 使用时间戳作为ID
        content: formData.get('content'),
        category: formData.get('category'),
        explanation: formData.get('explanation'),
        example: formData.get('example'),
        pronunciation: formData.get('pronunciation')
    };

    // 验证必填字段
    if (!entry.content || !entry.category || !entry.explanation) {
        showNotification('请填写所有必填字段', 'error');
        return;
    }

    vocabData.push(entry);
    categories.add(entry.category);
    
    saveData();
    updateStats();
    renderEntries();
    renderCategories();
    
    // 重置表单
    form.reset();
    
    // 切换到首页
    switchTab('home');
    
    showNotification('词条添加成功！');
}

// 渲染词条列表
function renderEntries(filteredEntries = null) {
    const container = document.getElementById('entries-container');
    const emptyState = document.getElementById('empty-state');
    const entries = filteredEntries || vocabData;

    if (entries.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';
    
    container.innerHTML = entries.map(entry => `
        <div class="entry-card" onclick="showEntryDetail(${entry.id})">
            <div class="entry-header">
                <div>
                    <div class="entry-title">${entry.content}</div>
                    <div class="entry-category">${entry.category}</div>
                </div>
            </div>
            <div class="entry-explanation">${entry.explanation}</div>
            <div class="entry-actions">
                <button class="btn-secondary" onclick="event.stopPropagation(); editEntry(${entry.id})">
                    <i class="fas fa-edit"></i> 编辑
                </button>
                <button class="btn-danger" onclick="event.stopPropagation(); deleteEntry(${entry.id})">
                    <i class="fas fa-trash"></i> 删除
                </button>
            </div>
        </div>
    `).join('');

    // 更新分类筛选选项
    updateCategoryFilter();
    updateAddEntryCategorySelect();
}

// 显示词条详情
function showEntryDetail(entryId) {
    const entry = vocabData.find(e => e.id === entryId);
    if (!entry) return;

    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');

    modalTitle.textContent = entry.content;
    
    let exampleHtml = '';
    if (entry.example) {
        exampleHtml = `
            <div class="form-group">
                <label>示例代码：</label>
                <div class="code-block">${entry.example.replace(/\n/g, '<br>')}</div>
            </div>
        `;
    }

    let pronunciationHtml = '';
    if (entry.pronunciation) {
        pronunciationHtml = `
            <div class="form-group">
                <label>发音提示：</label>
                <p>${entry.pronunciation}</p>
            </div>
        `;
    }

    modalBody.innerHTML = `
        <div class="form-group">
            <label>分类：</label>
            <span class="entry-category">${entry.category}</span>
        </div>
        <div class="form-group">
            <label>详细解释：</label>
            <p>${entry.explanation}</p>
        </div>
        ${exampleHtml}
        ${pronunciationHtml}
        <div class="form-actions">
            <button class="btn-primary" onclick="speakText('${entry.content}')">
                <i class="fas fa-volume-up"></i> 朗读内容
            </button>
            <button class="btn-secondary" onclick="closeModal()">
                <i class="fas fa-times"></i> 关闭
            </button>
        </div>
    `;

    modal.style.display = 'block';
}

// 编辑词条
function editEntry(entryId) {
    const entry = vocabData.find(e => e.id === entryId);
    if (!entry) return;

    // 填充表单
    document.getElementById('content').value = entry.content;
    document.getElementById('category').value = entry.category;
    document.getElementById('explanation').value = entry.explanation;
    document.getElementById('example').value = entry.example;
    document.getElementById('pronunciation').value = entry.pronunciation;

    // 切换到添加页面
    switchTab('add');

    // 修改表单提交行为
    const form = document.getElementById('add-entry-form');
    form.onsubmit = function(e) {
        e.preventDefault();
        updateEntry(entryId);
    };

    // 修改提交按钮文本
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.innerHTML = '<i class="fas fa-save"></i> 更新词条';
}

// 更新词条
function updateEntry(entryId) {
    const form = document.getElementById('add-entry-form');
    const formData = new FormData(form);
    
    const entryIndex = vocabData.findIndex(e => e.id === entryId);
    if (entryIndex === -1) return;

    const updatedEntry = {
        id: entryId,
        content: formData.get('content'),
        category: formData.get('category'),
        explanation: formData.get('explanation'),
        example: formData.get('example'),
        pronunciation: formData.get('pronunciation')
    };

    vocabData[entryIndex] = updatedEntry;
    categories.add(updatedEntry.category);
    
    saveData();
    updateStats();
    renderEntries();
    renderCategories();
    
    // 重置表单
    form.reset();
    form.onsubmit = function(e) {
        e.preventDefault();
        addEntry();
    };
    
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.innerHTML = '<i class="fas fa-save"></i> 保存词条';
    
    switchTab('home');
    showNotification('词条更新成功！');
}

// 删除词条
function deleteEntry(entryId) {
    if (!confirm('确定要删除这个词条吗？')) return;

    vocabData = vocabData.filter(e => e.id !== entryId);
    saveData();
    updateStats();
    renderEntries();
    renderCategories();
    
    showNotification('词条删除成功！');
}

// 筛选词条
function filterEntries() {
    const selectedCategory = document.getElementById('category-filter').value;
    
    if (!selectedCategory) {
        renderEntries();
        return;
    }

    const filteredEntries = vocabData.filter(entry => entry.category === selectedCategory);
    renderEntries(filteredEntries);
}

// 搜索词条
function searchEntries() {
    const keyword = document.getElementById('search-input').value.trim();
    
    if (!keyword) {
        document.getElementById('search-results').innerHTML = '';
        return;
    }

    const results = vocabData.filter(entry => 
        entry.content.toLowerCase().includes(keyword.toLowerCase()) ||
        entry.explanation.toLowerCase().includes(keyword.toLowerCase())
    );

    const container = document.getElementById('search-results');
    
    if (results.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #666;">未找到相关词条</p>';
        return;
    }

    container.innerHTML = results.map(entry => `
        <div class="entry-card" onclick="showEntryDetail(${entry.id})">
            <div class="entry-header">
                <div>
                    <div class="entry-title">${entry.content}</div>
                    <div class="entry-category">${entry.category}</div>
                </div>
            </div>
            <div class="entry-explanation">${entry.explanation}</div>
            <div class="entry-actions">
                <button class="btn-secondary" onclick="event.stopPropagation(); editEntry(${entry.id})">
                    <i class="fas fa-edit"></i> 编辑
                </button>
                <button class="btn-danger" onclick="event.stopPropagation(); deleteEntry(${entry.id})">
                    <i class="fas fa-trash"></i> 删除
                </button>
            </div>
        </div>
    `).join('');
}

// 添加分类
function addCategory() {
    const input = document.getElementById('new-category');
    const categoryName = input.value.trim();
    
    if (!categoryName) {
        showNotification('请输入分类名称', 'error');
        return;
    }

    if (categories.has(categoryName)) {
        showNotification('分类已存在', 'error');
        return;
    }

    categories.add(categoryName);
    saveData();
    renderCategories();
    updateCategoryFilter();
    updateAddEntryCategorySelect();
    
    input.value = '';
    showNotification('分类添加成功！');
}

// 删除分类
function deleteCategory(categoryName) {
    const entriesInCategory = vocabData.filter(entry => entry.category === categoryName);
    
    if (entriesInCategory.length > 0) {
        showNotification(`无法删除分类"${categoryName}"，该分类下还有${entriesInCategory.length}个词条`, 'error');
        return;
    }

    if (!confirm(`确定要删除分类"${categoryName}"吗？`)) return;

    categories.delete(categoryName);
    saveData();
    renderCategories();
    updateCategoryFilter();
    updateAddEntryCategorySelect();
    
    showNotification('分类删除成功！');
}

// 渲染分类列表
function renderCategories() {
    const container = document.getElementById('categories-container');
    
    container.innerHTML = Array.from(categories).map(category => {
        const count = vocabData.filter(entry => entry.category === category).length;
        return `
            <div class="category-item">
                <div class="category-info">
                    <span class="category-name">${category}</span>
                    <span class="category-count">${count}</span>
                </div>
                <button class="btn-danger" onclick="deleteCategory('${category}')" ${count > 0 ? 'disabled' : ''}>
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
    }).join('');
}

// 更新分类筛选选项
function updateCategoryFilter() {
    const select = document.getElementById('category-filter');
    const currentValue = select.value;
    
    select.innerHTML = '<option value="">所有分类</option>';
    
    Array.from(categories).sort().forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        select.appendChild(option);
    });
    
    select.value = currentValue;
}

// 更新添加词条页面的分类选择器
function updateAddEntryCategorySelect() {
    const select = document.getElementById('category');
    const currentValue = select.value;
    
    select.innerHTML = '<option value="">选择分类</option>';
    
    Array.from(categories).sort().forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        select.appendChild(option);
    });
    
    select.value = currentValue;
}

// 更新统计信息
function updateStats() {
    document.getElementById('entry-count').textContent = vocabData.length;
    document.getElementById('category-count').textContent = categories.size;
}

// 导出数据
function exportData(format) {
    let content = '';
    let filename = `python_vocab_${new Date().toISOString().split('T')[0]}`;
    
    switch (format) {
        case 'json':
            content = JSON.stringify({
                vocab_data: vocabData,
                categories: Array.from(categories)
            }, null, 2);
            filename += '.json';
            break;
            
        case 'txt':
            content = vocabData.map(entry => 
                `${entry.content}\n分类：${entry.category}\n解释：${entry.explanation}\n${entry.example ? `示例：\n${entry.example}\n` : ''}${entry.pronunciation ? `发音：${entry.pronunciation}\n` : ''}${'='.repeat(50)}\n`
            ).join('\n');
            filename += '.txt';
            break;
            
        case 'md':
            content = '# Python编程基础词库\n\n';
            content += vocabData.map(entry => 
                `## ${entry.content}\n\n**分类：** ${entry.category}\n\n**解释：** ${entry.explanation}\n\n${entry.example ? `**示例：**\n\`\`\`python\n${entry.example}\n\`\`\`\n\n` : ''}${entry.pronunciation ? `**发音：** ${entry.pronunciation}\n\n` : ''}---\n\n`
            ).join('');
            filename += '.md';
            break;
    }
    
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
    
    showNotification(`数据已导出为${format.toUpperCase()}格式`);
}

// 导入数据
function importData(file) {
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            
            if (data.vocab_data && Array.isArray(data.vocab_data)) {
                vocabData = data.vocab_data;
                categories = new Set(data.categories || []);
                
                // 确保默认分类存在
                defaultCategories.forEach(cat => categories.add(cat));
                
                saveData();
                updateStats();
                renderEntries();
                renderCategories();
                updateCategoryFilter();
                updateAddEntryCategorySelect();
                
                showNotification(`成功导入${vocabData.length}个词条`);
            } else {
                throw new Error('数据格式不正确');
            }
        } catch (error) {
            showNotification('导入失败：文件格式不正确', 'error');
        }
    };
    reader.readAsText(file);
}

// 清空所有数据
function clearAllData() {
    vocabData = [];
    categories = new Set(defaultCategories);
    saveData();
    updateStats();
    renderEntries();
    renderCategories();
    updateCategoryFilter();
    updateAddEntryCategorySelect();
    
    showNotification('所有数据已清空');
}

// 语音朗读
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'zh-CN';
        utterance.rate = 0.8;
        speechSynthesis.speak(utterance);
    } else {
        showNotification('您的浏览器不支持语音朗读功能', 'warning');
    }
}

// 模态框控制
function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// 通知提示
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    const messageEl = document.getElementById('notification-message');
    
    messageEl.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'flex';
    
    setTimeout(() => {
        hideNotification();
    }, 3000);
}

function hideNotification() {
    document.getElementById('notification').style.display = 'none';
}

// 加载示例数据（如果词库为空）
function loadSampleData() {
    if (vocabData.length === 0) {
        const sampleData = [
            {
                id: Date.now(),
                content: "for 循环",
                category: "循环结构",
                explanation: "for循环是Python中最常用的循环结构，用于遍历可迭代对象（如列表、元组、字符串等）",
                example: "for i in range(5):\n    print(i)\n# 输出：0, 1, 2, 3, 4",
                pronunciation: "for 循环"
            },
            {
                id: Date.now() + 1,
                content: "str 字符串",
                category: "数据类型",
                explanation: "字符串是Python中的文本数据类型，用单引号或双引号包围",
                example: "name = 'Python'\nmessage = \"Hello, World!\"\nprint(name + ' ' + message)",
                pronunciation: "string 字符串"
            }
        ];
        
        vocabData = sampleData;
        saveData();
        updateStats();
        renderEntries();
        
        showNotification('已加载示例数据，开始体验吧！');
    }
}

// 页面加载完成后检查是否需要加载示例数据
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(loadSampleData, 1000);
}); 