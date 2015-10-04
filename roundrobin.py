

#Round Robin Logic
#I did not want to place this in the server code and mess it up for now...


round_robin = True
machine_use = 0

def allocate_server():

    global machine_use

    if len(vm_array) > 1 :
        #Round Robin Method:
        if round_robin == True and machine_use == 0:
            #code to send a request to the first vm (first vm = machine_use = 0)
            #change machine_use to 1 so the next request goes to the second vm
            machine_use = 1
        elif round_robin == True and machine_use == 1:
            #code to send a request to the second vm
            machine_use = 0

        #Priority Method:
        if round_robin == False and machine_use == 0:
            #Need to figure out this one still