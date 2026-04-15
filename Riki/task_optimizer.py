#!/usr/bin/env python3
"""
重複任務優化系統
自動識別、處理同優化常見重複任務
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import os

class TaskOptimizer:
    """任務優化器"""
    
    def __init__(self, task_log_file="/data/workspace/Riki/task_optimizer.json"):
        self.task_log_file = task_log_file
        self.task_patterns = {}
        self.optimization_rules = {}
        self.performance_stats = defaultdict(list)
        
        # 載入現有數據
        self._load_data()
        
        # 初始化優化規則
        self._init_optimization_rules()
    
    def _load_data(self):
        """載任務數據"""
        try:
            if os.path.exists(self.task_log_file):
                with open(self.task_log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.task_patterns = data.get('task_patterns', {})
                    self.optimization_rules = data.get('optimization_rules', {})
                    self.performance_stats = defaultdict(list, data.get('performance_stats', {}))
                print("✅ 任務優化器數據已載入")
            else:
                print("🆕 創建新嘅任務優化器數據")
        except Exception as e:
            print(f"⚠️ 載入數據失敗: {e}")
    
    def _save_data(self):
        """保存任務數據"""
        try:
            data = {
                'task_patterns': self.task_patterns,
                'optimization_rules': self.optimization_rules,
                'performance_stats': dict(self.performance_stats),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.task_log_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ 任務優化器數據已保存")
        except Exception as e:
            print(f"⚠️ 保存數據失敗: {e}")
    
    def _init_optimization_rules(self):
        """初始化優化規則"""
        self.optimization_rules = {
            'excel_processing': {
                'pattern': 'excel.*processing|處理.*excel',
                'optimization': 'use_cached_template',
                'priority': 'high'
            },
            'invoice_handling': {
                'pattern': 'invoice.*handle|發票.*處理',
                'optimization': 'use_specialized_processor',
                'priority': 'critical'
            },
            'github_upload': {
                'pattern': 'github.*upload|上傳.*github',
                'optimization': 'batch_upload',
                'priority': 'medium'
            },
            'web_search': {
                'pattern': 'web.*search|網絡.*搜索',
                'optimization': 'cache_results',
                'priority': 'medium'
            },
            'file_management': {
                'pattern': 'file.*manage|檔案.*管理',
                'optimization': 'automate_cleanup',
                'priority': 'low'
            }
        }
    
    def _generate_task_hash(self, task_type, task_params):
        """生成任務唯一標識"""
        content = f"{task_type}:{json.dumps(task_params, sort_keys=True)}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def _analyze_pattern(self, task_type, task_params):
        """分析任務模式"""
        # 記錄任務頻率
        if task_type not in self.task_patterns:
            self.task_patterns[task_type] = {
                'count': 0,
                'last_seen': None,
                'avg_duration': 0,
                'success_rate': 1.0,
                'common_params': Counter()
            }
        
        pattern = self.task_patterns[task_type]
        pattern['count'] += 1
        pattern['last_seen'] = datetime.now().isoformat()
        
        # 記錄參數模式
        for key, value in task_params.items():
            pattern['common_params'][f"{key}:{value}"] += 1
        
        # 更新平均執行時間
        if 'execution_time' in task_params:
            self.performance_stats[task_type].append(task_params['execution_time'])
        
        # 保存更新
        self._save_data()
    
    def _optimize_task(self, task_type, task_params):
        """優化任務執行"""
        # 檢查優化規則
        for rule_name, rule in self.optimization_rules.items():
            if self._matches_pattern(task_type, rule['pattern']):
                return self._apply_optimization(rule_name, task_params)
        
        # 如果冇特定規則，使用通用優化
        return self._generic_optimization(task_type, task_params)
    
    def _matches_pattern(self, task_type, pattern):
        """檢查任務類型是否匹配模式"""
        import re
        return re.search(pattern, task_type.lower(), re.IGNORECASE)
    
    def _apply_optimization(self, rule_name, task_params):
        """應用特定優化規則"""
        print(f"🎯 應用優化規則: {rule_name}")
        
        if rule_name == 'excel_processing':
            return {
                'action': 'use_cached_template',
                'template': 'excel_optimized_template',
                'expected_saving': 30  # 預期節省30%時間
            }
        
        elif rule_name == 'invoice_handling':
            return {
                'action': 'use_specialized_processor',
                'processor': 'invoice_processor_v2',
                'expected_saving': 50  # 預期節省50%時間
            }
        
        elif rule_name == 'github_upload':
            return {
                'action': 'batch_upload',
                'batch_size': 5,
                'expected_saving': 25  # 預期節省25%時間
            }
        
        elif rule_name == 'web_search':
            return {
                'action': 'cache_results',
                'cache_ttl': 3600,  # 1小時緩存
                'expected_saving': 40  # 預期節省40%時間
            }
        
        elif rule_name == 'file_management':
            return {
                'action': 'automate_cleanup',
                'cleanup_interval': 3600,  # 1小時清理
                'expected_saving': 20  # 預期節省20%時間
            }
        
        return {'action': 'no_optimization'}
    
    def _generic_optimization(self, task_type, task_params):
        """通用優化策略"""
        print(f"🔧 應用通用優化: {task_type}")
        
        # 如果任務頻率高，建議預處理
        if task_type in self.task_patterns:
            pattern = self.task_patterns[task_type]
            if pattern['count'] > 10:  # 超過10次
                return {
                    'action': 'preprocessing_suggested',
                    'frequency': pattern['count'],
                    'suggestion': '建立專用緩存'
                }
        
        return {'action': 'no_optimization'}
    
    def process_task(self, task_type, task_params, execution_time=None):
        """處理任務（主要入口）"""
        start_time = time.time()
        
        print(f"🚀 開始處理任務: {task_type}")
        
        # 分析任務模式
        self._analyze_pattern(task_type, task_params)
        
        # 優化任務
        optimization = self._optimize_task(task_type, task_params)
        
        # 記錄執行時間
        if execution_time:
            task_params['execution_time'] = execution_time
        else:
            execution_time = time.time() - start_time
            task_params['execution_time'] = execution_time
        
        print(f"✅ 任務完成: {task_type}, 耗時: {execution_time:.2f}秒")
        print(f"💡 優化建議: {optimization}")
        
        return {
            'task_type': task_type,
            'task_params': task_params,
            'optimization': optimization,
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_optimization_report(self):
        """獲取優化報告"""
        report = {
            'total_tasks_processed': sum(pattern['count'] for pattern in self.task_patterns.values()),
            'patterns_analyzed': len(self.task_patterns),
            'optimization_rules_active': len(self.optimization_rules),
            'task_patterns': {},
            'performance_summary': {}
        }
        
        # 生成任務模式摘要
        for task_type, pattern in self.task_patterns.items():
            report['task_patterns'][task_type] = {
                'count': pattern['count'],
                'last_seen': pattern['last_seen'],
                'most_common_params': dict(pattern['common_params'].most_common(5))
            }
        
        # 生成性能摘要
        for task_type, times in self.performance_stats.items():
            if times:
                report['performance_summary'][task_type] = {
                    'avg_time': sum(times) / len(times),
                    'max_time': max(times),
                    'min_time': min(times),
                    'total_executions': len(times)
                }
        
        return report
    
    def suggest_improvements(self):
        """提出改進建議"""
        suggestions = []
        
        # 分析高頻率任務
        for task_type, pattern in self.task_patterns.items():
            if pattern['count'] > 5:  # 超過5次
                suggestions.append({
                    'type': 'high_frequency_task',
                    'task_type': task_type,
                    'frequency': pattern['count'],
                    'suggestion': f'為 {task_type} 建立專用優化處理器'
                })
        
        # 分析執行時間
        for task_type, times in self.performance_stats.items():
            if times and len(times) > 3:
                avg_time = sum(times) / len(times)
                if avg_time > 10:  # 超過10秒
                    suggestions.append({
                        'type': 'slow_task',
                        'task_type': task_type,
                        'avg_time': avg_time,
                        'suggestion': f'優化 {task_type} 嘅執行效率'
                    })
        
        return suggestions

# 全局任務優化器實例
task_optimizer = TaskOptimizer()

def process_task_with_optimization(task_type, task_params=None, execution_time=None):
    """使用優化器處理任務嘅便捷函數"""
    if task_params is None:
        task_params = {}
    
    return task_optimizer.process_task(task_type, task_params, execution_time)

def get_optimization_report():
    """獲取優化報告嘅便捷函數"""
    return task_optimizer.get_optimization_report()

def get_improvement_suggestions():
    """獲取改進建議嘅便捷函數"""
    return task_optimizer.suggest_improvements()

# 示例使用
if __name__ == "__main__":
    # 測試任務優化器
    print("=== 任務優化器測試 ===")
    
    # 模擬處理幾個任務
    task1 = process_task_with_optimization('excel_processing', {'file': 'test.xlsx'})
    task2 = process_task_with_optimization('invoice_handling', {'image': 'receipt.jpg'})
    task3 = process_task_with_optimization('excel_processing', {'file': 'data.xlsx'})
    
    # 獲取報告
    report = get_optimization_report()
    print("📊 優化報告:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # 獲取改進建議
    suggestions = get_improvement_suggestions()
    print("💡 改進建議:")
    for suggestion in suggestions:
        print(f"- {suggestion['suggestion']}")