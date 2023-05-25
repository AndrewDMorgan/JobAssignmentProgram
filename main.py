import random

# some constants for assigning positions
maxPeopleWorking = 8
minPeopleWorking = 3
maxDaysWorking = 6
minDaysWorking = 2


# collapses the cells
def CollapseCells(requests: dict, schedule: dict) -> any:
    # returning the schedule
    if not requests:
        for day in schedule:
            if len(schedule[day]) < minDaysWorking: return False
        return schedule
    
    # finding the person with the lowest entropy
    people = [person for person in requests]
    lowestEntropy = len(requests[people[0]])
    lowestEntropyPerson = people[0]
    for person in requests:
        entropy = len(requests[person])
        if entropy < lowestEntropy:
            lowestEntropy = entropy
            lowestEntropyPerson = person

    # checking the possibilities for them
    requested = requests[lowestEntropyPerson]
        
    # getting the number of people schuled for each day
    numRequests = {day: len(schedule[day]) for day in schedule}
    
    # adding the requested days for each day to it
    for person in requests:
        for day in requests[person]:
            numRequests[day] += 1
    
    # sorting it so the items first are the least scheduled/requested (so they should be filled first)
    requested = sorted(requested, key=lambda day : numRequests[day])
    
    # looping through the number of days they can work
    days = [i for i in range(minDaysWorking, maxDaysWorking) if i <= len(requested)]
    days = sorted(days, key=lambda v : random.randint(0, 10000000))
    for numDays in days:
        # trying to see the outcome of scheduling them for those number of days
        scheduleCopy = {key: schedule[key][:] for key in schedule}
        for i in range(numDays):
            scheduleCopy[requested[i]].append(lowestEntropyPerson)
            
            # checking the schedule is valid (there aren't too many people working)
            if len(scheduleCopy[requested[i]]) > maxPeopleWorking: return False
        
        # checking if scheduling them for those days results in a valid schedule
        newRequests = {person: requests[person] for person in requests if person != lowestEntropyPerson}
        results = CollapseCells(newRequests, scheduleCopy)
        if results: return results
    
    # there aren't any valid schedules for this person
    return False


people = ["jim", "bob", "tom", "tim", "jim", "jimmy", "sam", "jerry", "bill", "billy"]
shedule = {i: [] for i in [1, 2, 11, 12, 21, 22, 30, 31, 32]}
requests = {
    people[0]: [1, 11, 12, 22, 30, 32],
    people[1]: [1, 22, 32],
    people[2]: [31, 1, 2, 12, 21],
    people[3]: [30, 31, 32, 1, 2],
    people[4]: [30, 1, 2, 12, 21],
    people[5]: [21, 22, 31, 32, 1, 11],
    people[6]: [1, 2, 11, 12, 21, 31, 32],
    people[7]: [30, 32, 11, 12, 21],
    people[8]: [2, 1, 21, 22, 31],
    people[9]: [11, 12, 31, 32]
}

print(CollapseCells(requests, shedule))

