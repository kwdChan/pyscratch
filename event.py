class Event:
    active_events = []
    timer_event_checkers = []
    pygame_event_checkers = []

    def __init__(self, active=True):
        self.triggers = []
        self.handlers = []

        if active: 
            self.active()

    def inactive(self):
        type(self).active_events.remove(self)

    def active(self):
        assert not (self in type(self).active_events)
        type(self).active_events.append(self)


    def trigger(self, *args, **kwargs):
        self.triggers.append((args, kwargs))
    
    def add_handler(self, func):
        self.handlers.append(func)

    def handle_all(self):
        while self.handle_one():
            pass
        

    def handle_one(self):
        if not len(self.triggers): 
            return False
        
        args, kwargs = self.triggers.pop(0)

        for h in self.handlers:
            h(*args, **kwargs)

        return True
    


    def create_timer_event(period_sec):
        event = Event()
        
        period_ms = period_sec*1000
        time_ms_last = 0

        def check_trigger(time_ms_new):
            nonlocal time_ms_last

            dt = time_ms_new - time_ms_last
            if dt >= period_ms:
                event.trigger()
                time_ms_last = time_ms_new
                #print(dt)

            
        Event.timer_event_checkers.append(check_trigger)

        return event#, check_trigger
    

    def create_pygame_event(flag):
        event = Event()

        def check_trigger(pygame_event_list):
            for pygame_event in pygame_event_list:
                if pygame_event.type == flag:
                    event.trigger(pygame_event)

        Event.pygame_event_checkers.append(check_trigger)
        return event
    
    subscriptions = {} 

    def new_subscription(topic, event):
        if not (topic in Event.subscriptions):
            Event.subscriptions[topic] = []

        Event.subscriptions[topic].append(event)
        

    def create_messager_event(topic):
        event = Event()
        Event.new_subscription(topic, event)
        return event
    

    def submit_message(topic, *arg, **kwargs):
        if not topic in Event.subscriptions:
            return 
        
        for e in Event.subscriptions[topic]:
            e.trigger(*arg, **kwargs)


        


frame_start_event = Event()
keypress_event = Event()



        