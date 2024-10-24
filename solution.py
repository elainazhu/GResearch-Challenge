class Task:
    def __init__(self, id, factor, arrival, bonus, reward, duration, time_bonus):
        totalFactor = sum(factor)
        scale = 1.0 / totalFactor
        
        self.factor = [f * scale for f in factor]
        self.arrival = arrival
        self.bonus = bonus * totalFactor
        self.reward = reward * totalFactor
        self.duration = duration
        self.time_bonus = time_bonus
        self.id = id




def evaluate(task, time, processor):
    assert time >= task.arrival
    if time <= task.arrival + task.time_bonus:
        return task.factor[processor] * ((task.bonus) + (task.reward * task.duration) / (time + task.duration - task.arrival))
    else:
        return task.factor[processor] * (task.reward * task.duration) / (time + task.duration - task.arrival)




ave_time_bonus = 0
def sorting_key(task):
    return task.reward + task.bonus * (task.time_bonus / ave_time_bonus) / 3.8 - 1.25*task.duration




def assign_tasks(factor, arrival, bonus, reward, duration, time_bonus):
    T = len(arrival)
    P = len(factor[0])
    
    global ave_time_bonus
    ave_time_bonus = sum(time_bonus) / T
    
    tasks = []
    for t in range(T):
        tasks.append(Task(t, factor[t], arrival[t], bonus[t], reward[t], duration[t], time_bonus[t]))    
        
    tasks.sort(key=sorting_key, reverse=True)
    
    inf = int(1e9)
    processors = [[(-1, -1), (inf, inf)] for _ in range(P)]
    
    ans = []
    for task in tasks:
        arr = task.arrival
        dur = task.duration
        
        candidatesPositions = [] # (scare, processor, time)
        for p in range(P):
            # find first tuple that is >= arrival time
            for i in range(len(processors[p])):
                start, end = processors[p][i]
                time = max(end+1, arr)
                nextstart, nextend = processors[p][i+1]
                if nextstart - time - 1 >= dur:
                    candidatesPositions.append((evaluate(task, time, p), p, time, i))
                    break
            else: 
                assert False
                
        assert len(candidatesPositions) == P
        
        candidatesPositions.sort(key=lambda x: x[0], reverse=True)
        score, processor, time, i = candidatesPositions[0]
        # insert the time + duration into the processors
        
        processors[processor].insert(i+1, (time, time + dur - 1))
            
        ans.append((task.id, processor, time))
        
    
    ans.sort(key=lambda x: x[0])
    ans = [(x[1], x[2]) for x in ans]
    
    return ans
