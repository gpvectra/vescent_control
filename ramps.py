def rampdef(rampname):
    from datetime import datetime, timedelta

    if rampname == 'test':
        Temperatures =  {'Temps_ch1':[1,2,3],
                        'Temps_ch2':[1,2,3],
                         'Temps_ch3':[1,2,3],
                         'Temps_ch4':[1,2,3]}  #4 channels on vescent / only need to fill in ones you want
        Elapsed_m = [0.0,5/60,10/60]

        start_time = 'now'#
        #start_time = datetime(2023, 7, 10,18,24,0) #'now' for immediate start, or datetime y,m,d,h,m,s
        #start_time = datetime.now()+timedelta(minutes = 1)#datetime.datetime(2023, 07, 10,12,0,0) #'now' for immediate start, or datetime y,m,d,h,m,s

        repeats = 3
        repeat_interval_m = 20/60  # cycle repeat interval in minutes, 0 for no repeat



    if rampname == '87/32 retrace 20h+4h':
        Temperatures =  {'Temps1':[87, 32, 87],
                        'Temps2':[85.5, 30.5, 85.5],
                         'Temps3':[29, 29, 29],
                         'Temps4':[35.65,35.65,35.65]}  #4 channels on vescent
        Elapsed_m = [0,1,250] #elapsed minutes to initiate new temp setpoint (same length as temps1,2,3...

        start_time = 'now'# datetime.datetime(2023, 07, 10,12,0,0) #'now' for immediate start, or datetime y,m,d,h,m,s
        #start_time = datetime(2023, 7, 11, 11, 50, 0)  # 'now' for immediate start, or datetime y,m,d,h,m,s
        # start_time = datetime.now()+timedelta(minutes = 1)#datetime.datetime(2023, 07, 10,12,0,0) #'now' for immediate start, or datetime y,m,d,h,m,s

        repeats = 10
        repeat_interval_m = 24 * 60  # cycle repeat interval in minutes, 0 for no repeat


        # for T in Temperatures:  #call the dict like this
        #     print(T)
        #     print(Temperatures[T])
        # for T in Temperatures['Temps2']:
        #     print(T)

    return(Temperatures,Elapsed_m, start_time, repeats, repeat_interval_m)