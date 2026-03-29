from collections import deque

from libcachesim import CommonCacheParams, Request


class FifoCache:
    def __init__(self, cache_size: int):
        self.queue = deque()
        self.cache_size = cache_size

    def on_hit(self, req: Request) -> None:
        pass

    def on_miss(self, req: Request) -> None:
        if req.obj_size <= self.cache_size:
            self.queue.append(req.obj_id)

    def evict(self, req: Request) -> int:
        if not self.queue:
            return 0
        return self.queue.popleft()

    def on_remove(self, obj_id: int) -> None:
        try:
            self.queue.remove(obj_id)
        except ValueError:
            pass


def cache_init_hook(common_cache_params: CommonCacheParams):
    return FifoCache(common_cache_params.cache_size)


def cache_hit_hook(data: FifoCache, req: Request):
    data.on_hit(req)


def cache_miss_hook(data: FifoCache, req: Request):
    data.on_miss(req)


def cache_eviction_hook(data: FifoCache, req: Request):
    return data.evict(req)


def cache_remove_hook(data: FifoCache, obj_id: int):
    data.on_remove(obj_id)


def cache_free_hook(data: FifoCache):
    data.queue.clear()
