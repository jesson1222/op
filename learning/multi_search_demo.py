#!/usr/bin/env python3
"""
Multi Search Engine 简单实现示例
并行搜索多个引擎并融合结果
"""

import asyncio
import aiohttp
from typing import Dict, List, Tuple
from datetime import datetime

class MultiSearchEngine:
    """多搜索引擎融合器"""
    
    def __init__(self, engines: List[str] = None):
        self.engines = engines or ['google', 'bing', 'duckduckgo']
        self.session = None
        self.cache = {}
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        搜索多个引擎并融合结果
        
        Args:
            query: 搜索查询
            top_k: 返回结果数量
        
        Returns:
            融合后的结果列表
        """
        print(f"🔍 搜索查询：{query}")
        print(f"📊 引擎：{', '.join(self.engines)}")
        start_time = datetime.now()
        
        # 1. 并行查询所有引擎
        results = await self._query_all_engines(query)
        
        # 2. 融合结果 (使用 RRF 算法)
        fused_results = self._reciprocal_rank_fusion(results)
        
        # 3. 去重
        deduped_results = self._deduplicate(fused_results)
        
        # 4. 返回前 K 个
        final_results = deduped_results[:top_k]
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ 搜索完成：{duration:.2f}秒")
        print(f"📦 返回结果：{len(final_results)} 条")
        
        return final_results
    
    async def _query_all_engines(self, query: str) -> Dict[str, List[Tuple]]:
        """并行查询所有引擎"""
        tasks = [self._query_single_engine(engine, query) for engine in self.engines]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 整理结果
        engine_results = {}
        for engine, result in zip(self.engines, results):
            if isinstance(result, Exception):
                print(f"❌ {engine} 搜索失败：{result}")
                engine_results[engine] = []
            else:
                engine_results[engine] = result
                print(f"✅ {engine}: {len(result)} 条结果")
        
        return engine_results
    
    async def _query_single_engine(self, engine: str, query: str) -> List[Tuple]:
        """查询单个引擎（模拟实现）"""
        # 实际实现需要调用各引擎的 API
        # 这里用模拟数据演示
        
        await asyncio.sleep(0.5)  # 模拟网络延迟
        
        # 模拟结果
        mock_results = {
            'google': [
                (f'https://google-result-{i}.com', f'Google Result {i}', i+1)
                for i in range(10)
            ],
            'bing': [
                (f'https://bing-result-{i}.com', f'Bing Result {i}', i+1)
                for i in range(10)
            ],
            'duckduckgo': [
                (f'https://ddg-result-{i}.com', f'DDG Result {i}', i+1)
                for i in range(10)
            ]
        }
        
        return mock_results.get(engine, [])
    
    def _reciprocal_rank_fusion(self, results: Dict[str, List[Tuple]], k: int = 60) -> List[Tuple]:
        """
        倒数排名融合 (Reciprocal Rank Fusion)
        
        Score = Σ 1 / (k + rank)
        """
        scores = {}
        
        for engine, engine_results in results.items():
            for rank, (url, title, _) in enumerate(engine_results, 1):
                if url not in scores:
                    scores[url] = {'title': title, 'score': 0.0, 'engines': []}
                # RRF 公式
                rrf_score = 1.0 / (k + rank)
                scores[url]['score'] += rrf_score
                scores[url]['engines'].append(engine)
        
        # 按分数排序
        sorted_results = sorted(
            scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )
        
        return [
            (url, data['title'], data['score'], data['engines'])
            for url, data in sorted_results
        ]
    
    def _deduplicate(self, results: List[Tuple], threshold: float = 0.9) -> List[Tuple]:
        """基于 URL 去重"""
        from urllib.parse import urlparse
        
        unique_results = []
        seen_domains = set()
        
        for url, title, score, engines in results:
            parsed = urlparse(url)
            domain = parsed.netloc
            
            if domain in seen_domains:
                continue
            
            unique_results.append((url, title, score, engines))
            seen_domains.add(domain)
        
        return unique_results


async def main():
    """演示使用"""
    print("=" * 70)
    print("Multi Search Engine 演示")
    print("=" * 70)
    print()
    
    async with MultiSearchEngine(engines=['google', 'bing', 'duckduckgo']) as searcher:
        # 搜索示例
        results = await searcher.search("Python asyncio tutorial", top_k=5)
        
        print()
        print("=" * 70)
        print("📋 搜索结果")
        print("=" * 70)
        
        for i, (url, title, score, engines) in enumerate(results, 1):
            print(f"\n{i}. {title}")
            print(f"   URL: {url}")
            print(f"   融合分数：{score:.4f}")
            print(f"   来源引擎：{', '.join(engines)}")
        
        print()
        print("=" * 70)


if __name__ == '__main__':
    asyncio.run(main())
