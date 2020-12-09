# The area for testing this app
# 10.979953302385406, 106.11224252515844, 11.157855392546931, 106.55650216871312

import requests
import json
import multiprocessing
import ast
import sys

manager = multiprocessing.Manager()
percent = manager.list()


def CrawlJson(process_id, category, x1, y1, x2, y2, filename):

    #                      (x2,y2)
    #     ********************X
    #     *                   *
    #     *                   *
    #     *                   *
    #     X********************
    #  (x1,y1)

    # Example
    # x1 = 106.11224252515844
    # y1 = 10.979953302385406
    # x2 = 106.55650216871312
    # y2 = 11.157855392546931

    # Minimum distant between X and Y of element
    DISTANT_ELEMENT_X = 0.0073277950286865234
    DISTANT_ELEMENT_Y = 0.0027812845878827375

    # Init coordinates element
    # element is a small square of the box(x1,y1,x2,y2), it begin at the bot-left and finish at top-right
    e = {'x1': x1, 'y1': y1, 'x2': x1 +
         DISTANT_ELEMENT_X, 'y2': y1 + DISTANT_ELEMENT_Y}

    times = 0
    total_times = ((y2-y1)/DISTANT_ELEMENT_Y)*((x2-x1)/DISTANT_ELEMENT_X)

    # continue running by logger
    try:
        with open(f'log/{filename}_{process_id}.log', 'r') as f:
            data = f.read()
            json_x = ast.literal_eval(data)
            e = json_x['e']
            times = json_x['times']
    except IOError:
        pass

    if (times < total_times):
        while e['y1'] <= y2:
            while e['x1'] <= x2:
                response = None
                try:
                    response = requests.get(
                        f"https://map.coccoc.com/map/search.json?category={category}&borders={e['y1']},{e['x1']},{e['y2']},{e['x2']}")  # REMEMBER TO REVERT X & Y
                except requests.exceptions.RequestException as err:
                    print(err)

                if response.text[18] != ']':
                    with open(filename, 'a') as f:
                        s = json.loads(response.text)['result']['poi']
                        f.write(json.dumps(s) + ',')

                # logfile
                with open(f'log/{filename}_{process_id}.log', 'w') as f:
                    f.write(str({'e': e, 'times': times, 'total_time': total_times,
                                 'percent': times*100/total_times}))

                # increase x
                e['x1'] = e['x2']
                e['x2'] = e['x2'] + DISTANT_ELEMENT_X

                # logconfole:
                times = times + 1
                # percent[process_id] = times*100/total_times
                print(f'percent: {times*100/total_times}', end='\r')

            # reset x, increase y
            e['x1'] = x1
            e['x2'] = x1 + DISTANT_ELEMENT_X
            e['y1'] = e['y2']
            e['y2'] = e['y2'] + DISTANT_ELEMENT_Y


# Divide a square to number of process times to get high performace for crawling
def ShareWork(box_id, category, number_process):

    # HCM: 10.404543344158714, 106.11654053906202, 11.156072, 107.181149
    # For testing: 10.795958, 106.618704
    # 1: 22.857907350423993, 104.64321020200927, 23.34888793301606, 106.81325109163834
    # 2. 20.50098153942168, 102.10064557931051, 22.857907350423993, 108.04590526042817
    # 3. 19.035072456694454, 103.85119171540157, 20.50098153942168, 106.5725536579463
    # 4. 17.87059500178185, 104.38290892360489, 19.035072456694454, 106.57962527007327
    # 5. 15.340905609191323, 105.6093672935058, 17.87059500178185, 108.87013087576467
    # 6. 12.31679664145901, 107.29048652438634, 15.340905609191323, 109.4553821129751
    # 7. 11.06401326776402, 105.7770106909658, 12.31679664145901, 109.25284233750911
    # 8. 10.360377311574196, 104.35425865853686, 11.06401326776402, 108.52422825492937
    # 9. 8.54011246750354, 104.38472296569029, 10.360377311574196, 106.7889765688327
    # 10. 9.953655409883128, 103.82238599003524, 10.54011246750354, 104.23637092200744

    # CATEGORY
    # 1: restaurent
    # 2: coffee
    # 3: entertainment
    # 4: atm & bank
    # 5: gasstation
    # 6: hospital
    # 7: hotel & travel
    # 8: spa
    # 9: store & supermarket
    # 10: services
    # 11: places
    # 12: education
    # 13: winestore
    # 14: sport

    box_id = box_id - 1

    start_frames = [
        [22.857907350423993, 104.64321020200927],
        [20.50098153942168, 102.10064557931051],
        [19.035072456694454, 103.85119171540157],
        [17.87059500178185, 104.38290892360489],
        [15.340905609191323, 105.6093672935058],
        [12.31679664145901, 107.29048652438634],
        [11.06401326776402, 105.7770106909658],
        [10.360377311574196, 104.35425865853686],
        [8.54011246750354, 104.38472296569029],
        [9.953655409883128, 103.82238599003524],
        [0, 0],
        [10.705989, 106.547082]  # HCM
    ]
    finish_frames = [
        [23.34888793301606, 106.81325109163834],
        [22.857907350423993, 108.04590526042817],
        [20.50098153942168, 106.5725536579463],
        [19.035072456694454, 106.57962527007327],
        [17.87059500178185, 108.87013087576467],
        [15.340905609191323, 109.4553821129751],
        [12.31679664145901, 109.25284233750911],
        [11.06401326776402, 108.52422825492937],
        [10.360377311574196, 106.7889765688327],
        [10.54011246750354, 104.23637092200744],
        [3, 3],
        [10.910806, 106.799978]  # HCM
    ]

    number_cpu = multiprocessing.cpu_count()
    print(f"You have {number_cpu} core!")
    DISTANT_ELEMENT_X = (
        finish_frames[box_id][1] - start_frames[box_id][1]) / number_process
    DISTANT_ELEMENT_Y = (
        finish_frames[box_id][0] - start_frames[box_id][0]) / number_process

    # Init coordinates element
    # element is a small square of the box(x1,y1,x2,y2), it begin at the bot-left and finish at top-right
    e = [{'x1': start_frames[box_id][1], 'y1': start_frames[box_id]
          [0], 'x2': start_frames[box_id][1] + DISTANT_ELEMENT_X, 'y2': start_frames[box_id][0] + DISTANT_ELEMENT_Y}]
    jobs = []

    # create file
    with open(f'vn_{box_id+1}_{category}.json', 'a') as f:
        f.write('[')

    for i in range(0, number_process*number_process):
        percent.append('')
        p = multiprocessing.Process(target=CrawlJson, args=(
            i, category, e[i]['x1'], e[i]['y1'], e[i]['x2'], e[i]['y2'], f'vn_{box_id+1}_{category}.json'))
        jobs.append(p)
        p.start()

        #
        x = e[i].copy()
        if x['x1'] + DISTANT_ELEMENT_X < finish_frames[box_id][1]:
            x['x1'] = x['x1'] + DISTANT_ELEMENT_X
            x['x2'] = x['x2'] + DISTANT_ELEMENT_X
            e.append(x)
        else:
            if x['y1'] + DISTANT_ELEMENT_Y < finish_frames[box_id][0]:
                x['x1'] = start_frames[box_id][1]
                x['x2'] = x['x1'] + DISTANT_ELEMENT_X
                x['y1'] = x['y1'] + DISTANT_ELEMENT_Y
                x['y2'] = x['y2'] + DISTANT_ELEMENT_Y
                e.append(x)

    is_process_alive = True
    while (is_process_alive):
        jobs_check = 0
        for i in range(0, number_process):
            if not jobs[i].is_alive():
                jobs_check = jobs_check + 1
        if jobs_check == number_process-1:
            is_process_alive = False

        j = 0
        for i in range(0, number_process):
            if (jobs[j].is_alive()):
                print(f'{percent[j]} %', end='\r', flush=True)
            else:
                j = j + 1

    # close file
    with open(f'vn_{box_id+1}_{category}.json', 'a') as f:
        f.write(']')


#10.848689129464779, 106.6573182438044, 10.851470907404817, 106.66425980073494

# CrawlJson(0, 12, 106.547082, 10.705989,
#           106.799978, 10.910806, 'hcm_12.json')
if len(sys.argv) == 4:
    ShareWork(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
else:
    ShareWork(int(sys.argv[1]), int(sys.argv[2]), 2)
