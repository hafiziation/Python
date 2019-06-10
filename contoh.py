#========================================================
# Sample codes for Elevator Simulation using Multithreads
# by: norliza.zaini
#========================================================

import threading
import time
import random
import statistics 
  
# ================= CONTROLLER CLASS ==============================================
# Controller class: to simulate the centralized control panel of the elevator system
class Controller(threading.Thread):
    def __init__(self, name, ground_floor, top_floor, totalRequest):
        threading.Thread.__init__(self)
        self.name = name
        self.top_floor = top_floor
        self.ground_floor = ground_floor        
        self.passengers_waiting_time = []
        self.requestList = []        
        self.requestSize = totalRequest
        self.avg_waiting_time = 0
    
    # function to start the controller thread
    def run(self):                
        current_complete = 0
        while (len(self.passengers_waiting_time)<self.requestSize):
            if (current_complete < len(self.passengers_waiting_time)):
                current_complete = len(self.passengers_waiting_time)
                avg_waiting_time = round(statistics.mean(self.passengers_waiting_time),4)
                self.avg_waiting_time = avg_waiting_time
                print(self.name + ": " + str(current_complete) +  " requests completed. Avg waiting time: " + str(avg_waiting_time)) # show users' avg waiting time       
        
        print(self.name + ": ALL requests completed...")   
        #---- once all user requests are served, get the average waiting time ------------------
        avg_waiting_time = round(statistics.mean(self.passengers_waiting_time),4)
        self.avg_waiting_time = avg_waiting_time
        print(self.name + ": passenger average waiting time >> " + str(avg_waiting_time)) # show users' avg waiting time
        
    
    # function to serve reception of request from user (user push the lift button), the request list is appended
    def request(self, user, from_floor, to_floor):
        start_time = time.time()
        
        if (to_floor > from_floor): # determine the direction requested
            direction = "up"
        else:
            direction = "down"
        
        self.requestList.append([user, from_floor, to_floor, direction, start_time]) # append request to list
        print(self.name + ": received a request from User " + str(user) + " from floor " + str(from_floor) + " " + direction + " to floor " + str(to_floor))
        
        
    # function invoked by the elevator to pick up first passenger (in the elevator)
    def pickup_first_passenger(self, floor):                
        try:
            for x in range (len(controller.requestList)):
                if controller.requestList[x][1] == floor: # get passenger on the respective floor (to any direction)
                    passenger = controller.requestList[x]
                    del controller.requestList[x] # remove passenger from controller's list
                    # count waiting time from passenger start request until passenger pick up                    
                    elapsed_time = round(time.time() - passenger[4],4)
                    self.passengers_waiting_time.append(elapsed_time) # save passenger waiting time in list                    
                    return passenger # pass this passenger to elevator
        except IndexError:
            pass                
        return None
    
    # function invoked by the elevator to pick up passenger (in the elevator)
    def pickup_passenger(self, floor, direction):        
        try:
            for x in range (len(controller.requestList)):
                # get passenger on the respective floor with the same direction as the elevator
                if ((controller.requestList[x][1] == floor) and (controller.requestList[x][3] == direction)):
                    passenger = controller.requestList[x]
                    del controller.requestList[x] # remove passenger from controller's list
                    # count waiting time from passenger start request until passenger pick up                    
                    elapsed_time = round(time.time() - passenger[4],4)
                    self.passengers_waiting_time.append(elapsed_time) # save passenger waiting time in list
                    passenger[4] = elapsed_time
                    return passenger # pass this passenger to elevator
        except IndexError:
            pass
        return None
    
    # this function is invoked by the elevator if on the current floor, no passenger is found               
    # so the elevator wants to go to another floor (closest) to fetch the passenger
    def get_closest_passenger_floor(self, floor):
    
        try:
            for c_floor in range (floor,self.top_floor): # browse all floor aboves for passenger           
                for x in range (len(controller.requestList)):
                    if controller.requestList[x][1] == c_floor:                    
                        return c_floor # return the closest floor to elevator
        
            for c_floor in range (floor,self.ground_floor, -1): # browse all floors below for passenger
                for x in range (len(controller.requestList)):
                    if controller.requestList[x][1] == c_floor:                    
                        return c_floor # return the closest floor to elevator
        except IndexError:
            pass
        
        return None
        
# ================= end: CONTROLLER CLASS ==============================================                     


       
# ================= ELEVATOR CLASS ==============================================        
# Elevator class: to simulate the instance of elevator
class Elevator(threading.Thread):
    def __init__(self, name, ctroller, ground_floor, top_floor):
        threading.Thread.__init__(self)
        self.name = name        
        self.current_floor = ground_floor # elevator by default start at ground floor
        self.top_floor = top_floor # set the top floor number
        self.ground_floor = ground_floor # set the ground floor number
        self.direction = None # by default the elevator does go to any direction yet
        self.passengers = [] # initially no passengers in the elevator
        self.delay_count = 5  # to simulate lift movement to another floor
        self.max_passenger = 12 # max passengers set to 12 only at any one time
        self.controller = ctroller # reference/pointer to the centralized controller
        self.distance = 0 # this var is used to accumulate distance travelled by this elevator 
        self.stop_thread = False
    
    # -- function to start this thread ----------------
    def run(self):        
        print (self.name + ": Starting ")        
        while (True): # loop continuously
            self.pickup_passenger() 
            self.move()
            self.dropoff_passenger()   
            if (self.stop_thread and len(self.passengers)==0): #-- stop thread when simulation completes
                break            
    
    # -- function to simulate the elevator fetching passengers
    def pickup_passenger(self):
        if (len(self.passengers)==0): # --- if no passenger in elevator
            self.direction = None # reset direction to none
            # get the first passenger to go to any direction
            passenger = self.controller.pickup_first_passenger(self.current_floor) 
            
            if passenger != None: # first passenger fetched
                self.passengers.append(passenger)  # add passenger to list
                print(self.name + " [F:" + str(self.current_floor) + " P:" + str(len(self.passengers)) + "] " + ": pickup first passenger: " + self.label(passenger))
                self.set_direction(passenger[2]) # set direction of elevator based on passenger request
        
        if self.direction!= None: # if elevator is moving to a certain direction (otw to send passengers)
            while (len(self.passengers) < self.max_passenger): # loop :make sure max limit not exceeded

                # get any passenger requested to go to the same direction
                passenger = self.controller.pickup_passenger(self.current_floor, self.direction)
                
                if passenger != None: # a passenger fetched
                    self.passengers.append(passenger) # add passenger to list 
                    print(self.name + " [F:" + str(self.current_floor) + " P:" + str(len(self.passengers)) + "] " + ": pickup passenger: " + self.label(passenger))
                    self.set_direction(passenger[2]) # set direction of elevator based on passenger request
                else:
                    break
                    
        else: # if no passenger found on this floor >> get another floor (closest one) with passengers
            self.closest_floor = self.controller.get_closest_passenger_floor(self.current_floor)
            if (self.closest_floor != None): # found a floor with passengers
                self.set_direction(self.closest_floor) # set direction to move to that closest floor

            
    # function to simulate the movement of the elevator
    def move(self):       
                    
        if (len(self.passengers)==0): # if no passenger is in the elevator
            self.direction == None # reset direction to none (stay on this floor)              
    
        if (self.direction == None):            
            if (len(self.passengers)>0): # if direction is none but there are still passengers in elevator
                self.set_direction(self.passengers[0][2]) # set direction based on passenger destination
        
        if (self.direction != None): # if elevator has a certain direction to go (otw to send passenger)
            if (self.direction == "up"): # if elevator is moving up               
                if self.current_floor < self.top_floor: # as long as floor# is less than top floor
                    self.delay() # delay to simulate elevator moving up
                    self.current_floor +=1 # already arived at next floor, so update the current floor no
                    self.distance += 1 # update distance
                    print(self.name + " [F:" + str(self.current_floor) + " P:" + str(len(self.passengers)) + "] " + ": arrived at Floor " + str(self.current_floor) + " (distance: " + str(self.distance) + ")")
                else:
                    if (len(self.passengers)>0): # if already reached top floor but still has passengers in elevator
                        self.direction = "down" # bounce downward so that passengers can be sent
            
            elif (self.direction == "down"): # if elevator is moving down                           
                if self.current_floor > self.ground_floor: # as long as floor# is bigger than ground floor
                    self.delay() # delay to simulate elevator moving down
                    self.current_floor -=1 # already arived at next floor, so update the current floor no
                    self.distance += 1 # update distance
                    print(self.name + " [F:" + str(self.current_floor) + " P:" + str(len(self.passengers)) + "] " + ": arrived at Floor " + str(self.current_floor) + " (distance: " + str(self.distance) + ")")
                else:
                    if (len(self.passengers)>0): # if already reached ground floor but still has passengers in elevator
                        self.direction = "up" # bounce upward so that passengers can be sent        
        
    
    # -- function to set the direction of the elevator >> to move up or down ----------
    def set_direction(self, destination):
        if (destination > self.current_floor): # determine based on the destination & current_floor
            self.direction = "up"
        else:
            self.direction = "down"
        
                            
    # function to simulate dropping off passenger once the targeted floor is reached
    def dropoff_passenger(self):        
        
        passengers_left = [] # initialize a temporary list (for remaining passengers)
        for  x in range(len(self.passengers)):
            passenger = self.passengers[x] 
            if passenger[2] == self.current_floor:
                # -- simulate dropping off passenger on this floor if intended floor = current floor -------------
                print(self.name + " [F:" + str(self.current_floor) + " P:" + str(len(self.passengers)) + "] " + ": drop_off passenger: " + self.label(self.passengers[x]))                
            else:
                passengers_left.append(passenger) # add remaining passenger to temporary list

        self.passengers = None # reset the passengers list
        self.passengers = passengers_left # update passengers list with only the remaining ones
        
        #if (len(self.passengers)>0):
        #    print(self.name + " [F:" + str(self.current_floor) + " Psg:" + str(self.passengers) + "] " + ": updating passenger: ")
    
    # function to label the passenger details -----------
    def label(self, passenger):
        str_label = "User" + str(passenger[0]) + " Floor" + str(passenger[1]) + " --> Floor" + str(passenger[2]) + " (" +  str(passenger[3]) + ")"
        return str_label
                
    # function to simulate delay of the elevator moving from one floor to another ----------------
    def delay(self):                
        print(self.name + " [F:" + str(self.current_floor) + " P:" + str(len(self.passengers)) + "] " + ": moving " + self.direction + " from Floor " + str(self.current_floor))
        time.sleep(self.delay_count)        

# ================= end: ELEVATOR CLASS ==============================================        
     

#-- function to generate requests from users ---------------------
def generate_requests(traffic_type, top_floor, ground_floor):
    
    user_id = 1 # starts with user id 1
    requests = []
    
    if traffic_type == "low":
        total_request = 60 # 6o requests wil be genarated for low-traffic scenario
    elif traffic_type == "moderate":
        total_request = 120 # 120 requests wil be genarated for moderate-traffic scenario
    else:
        total_request = 280 # 280 requests wil be genarated for moderate-traffic scenario
      
    while (user_id <= total_request): # loop while no of requests still not enough
        from_floor = random.randint(ground_floor,top_floor) # randomly generate origin floor for a user
        to_floor = random.randint(ground_floor,top_floor) # randomly generate targeted floor for the user
        while (from_floor == to_floor): # if to and from are the same >> repeat generation of targeted floor
            to_floor = random.randint(ground_floor,top_floor)
        requests.append([user_id, from_floor, to_floor]) # add generated request to list
        user_id += 1 # update user id
    
    return requests

    
# ============= MAIN SIMUALATOR PROGRAM ===================================
top_floor = 5 #-- set top floor no
ground_floor = 1 #-- set ground floor no
traffic_type = "low" #--- can change to "low" or "moderate" or "high"

#---- generate requests from users to be simulated based on traffic type -------------
requests = generate_requests(traffic_type, top_floor, ground_floor) #-- generate requests based on traffic scenario

controller = Controller("Controller", ground_floor, top_floor, len(requests)) # create controller instance
controller.start() # start controller thread

elevator1 = Elevator("Lift-1", controller, ground_floor, top_floor) # create elevator 1 instance
elevator1.start() # start elevator 1 thread

elevator2 = Elevator("Lift-2", controller, ground_floor, top_floor) # create elevator 2 instance
elevator2.start() # start elevator 2 thread


#--- set interval delay between requests from users ----------------
if (traffic_type=="low"):
    min_delay = 3
    max_delay = 5
elif (traffic_type=="moderate"):
    min_delay = 2
    max_delay = 4
else:
    min_delay = 1
    max_delay = 2

#--- this loop simulates (user push button)/ user-requests given at different times
for x in range(len(requests)): 
    req = requests[x]
    controller.request(req[0],req[1],req[2]) #---- push request to controller == user push lift button
    rand_delay = random.randint(min_delay,max_delay) #--- simulate time elapse between user requests
    time.sleep(rand_delay)


while(len(controller.passengers_waiting_time)<len(requests) or len(elevator1.passengers)>0 or len(elevator2.passengers)>0):
    count = 0 # do nothing

print("Main: Average Users Waiting Time: " + str(controller.avg_waiting_time))
print("Main: Elevator1 total distance: " + str(elevator1.distance))
print("Main: Elevator2 total distance: " + str(elevator2.distance))
elevator1.stop_thread = True
elevator2.stop_thread = True

print("............... ELEVATOR SIMULATION COMPLETED .................")

    