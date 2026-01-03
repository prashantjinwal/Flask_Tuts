import math
import random
import threading
import multiprocessing
import itertools
import functools
import time
import sys
import os
import json
import csv
import hashlib
import queue

class Vector:
    def __init__(self, *values):
        self.values = list(values)
    def __add__(self, other):
        return Vector(*[a + b for a, b in zip(self.values, other.values)])
    def __sub__(self, other):
        return Vector(*[a - b for a, b in zip(self.values, other.values)])
    def scale(self, k):
        return Vector(*[k * v for v in self.values])
    def dot(self, other):
        return sum(a * b for a, b in zip(self.values, other.values))
    def magnitude(self):
        return math.sqrt(sum(v * v for v in self.values))
    def normalize(self):
        m = self.magnitude()
        if m == 0:
            return Vector(*self.values)
        return self.scale(1 / m)
    def __repr__(self):
        return f"Vector({','.join(str(v) for v in self.values)})"

class Matrix:
    def __init__(self, rows):
        self.rows = rows
    def shape(self):
        return len(self.rows), len(self.rows[0]) if self.rows else 0
    def transpose(self):
        return Matrix(list(map(list, zip(*self.rows))))
    def add(self, other):
        return Matrix([[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(self.rows, other.rows)])
    def multiply(self, other):
        ot = other.transpose()
        return Matrix([[sum(a * b for a, b in zip(r, c)) for c in ot.rows] for r in self.rows])
    def __repr__(self):
        return f"Matrix({self.rows})"

def fibonacci(n):
    a, b = 0, 1
    out = []
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out

def primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)

class Graph:
    def __init__(self):
        self.edges = {}
    def add_edge(self, a, b, w=1):
        self.edges.setdefault(a, []).append((b, w))
        self.edges.setdefault(b, []).append((a, w))
    def dijkstra(self, start):
        dist = {k: float("inf") for k in self.edges}
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = min(pq)
            pq.remove((d, u))
            if d > dist[u]:
                continue
            for v, w in self.edges[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    pq.append((nd, v))
        return dist

class Cache:
    def __init__(self):
        self.data = {}
    def get(self, k):
        return self.data.get(k)
    def set(self, k, v):
        self.data[k] = v

def memoize(fn):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        r = fn(*args)
        cache[args] = r
        return r
    return wrapper

@memoize
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def random_walk(steps):
    x = y = 0
    path = [(x, y)]
    for _ in range(steps):
        dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        x += dx
        y += dy
        path.append((x, y))
    return path

class Worker(threading.Thread):
    def __init__(self, q, out):
        super().__init__()
        self.q = q
        self.out = out
    def run(self):
        while True:
            try:
                item = self.q.get(timeout=0.1)
            except:
                return
            self.out.append(item * item)
            self.q.task_done()

def threaded_square(nums):
    q = queue.Queue()
    out = []
    for n in nums:
        q.put(n)
    threads = [Worker(q, out) for _ in range(4)]
    for t in threads:
        t.start()
    q.join()
    return out

def hash_text(t):
    return hashlib.sha256(t.encode()).hexdigest()

def permutations_sum(n):
    total = 0
    for p in itertools.permutations(range(n)):
        total += sum(p)
    return total

class StateMachine:
    def __init__(self):
        self.state = "INIT"
    def transition(self, event):
        if self.state == "INIT" and event == "start":
            self.state = "RUN"
        elif self.state == "RUN" and event == "stop":
            self.state = "STOP"
        elif self.state == "STOP" and event == "reset":
            self.state = "INIT"
        return self.state

def simulate():
    sm = StateMachine()
    events = ["start", "stop", "reset", "start", "stop"]
    return [sm.transition(e) for e in events]

class DataStore:
    def __init__(self, path):
        self.path = path
    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f)
    def load(self):
        with open(self.path) as f:
            return json.load(f)

def csv_roundtrip(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        for r in rows:
            w.writerow(r)
    out = []
    with open(path) as f:
        r = csv.reader(f)
        for row in r:
            out.append(row)
    return out

def statistics(nums):
    mean = sum(nums) / len(nums)
    var = sum((x - mean) ** 2 for x in nums) / len(nums)
    return mean, math.sqrt(var)

class Simulation:
    def __init__(self, size):
        self.size = size
        self.grid = [[random.random() for _ in range(size)] for _ in range(size)]
    def step(self):
        new = [[0]*self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                s = 0
                for di in (-1,0,1):
                    for dj in (-1,0,1):
                        ni = (i + di) % self.size
                        nj = (j + dj) % self.size
                        s += self.grid[ni][nj]
                new[i][j] = s / 9
        self.grid = new
    def run(self, steps):
        for _ in range(steps):
            self.step()
        return self.grid

def main():
    v1 = Vector(1,2,3)
    v2 = Vector(4,5,6)
    m1 = Matrix([[1,2],[3,4]])
    m2 = Matrix([[5,6],[7,8]])
    g = Graph()
    g.add_edge("a","b",1)
    g.add_edge("b","c",2)
    fib = fibonacci(10)
    pr = primes(50)
    arr = quicksort([random.randint(0,100) for _ in range(20)])
    dist = g.dijkstra("a")
    walk = random_walk(100)
    sq = threaded_square(list(range(20)))
    h = hash_text("python")
    fac = factorial(10)
    sm = simulate()
    stats = statistics([random.random() for _ in range(1000)])
    sim = Simulation(10).run(5)
    print(v1 + v2)
    print(m1.multiply(m2))
    print(fib)
    print(pr)
    print(arr)
    print(dist)
    print(len(walk))
    print(sum(sq))
    print(h)
    print(fac)
    print(sm)
    print(stats)
    print(sim[0][0])


