import csv
from heapq import heappush, heappop
import numpy as np
import os
import matplotlib.pyplot as plt

school_dict = {}
last_id = -1

def get_data(full_row):
    global school_dict
    global last_id

    if(len(full_row[3])!=7 or int(full_row[3][0])!=5):
        school_dict[last_id]['discarded'] += 1
        return

    school_id = int(full_row[3])//1000
    student_id = int(full_row[3])%1000

    last_id = school_id

    if(school_id not in school_dict):
        school_dict[school_id] = {}
        school_dict[school_id]['data'] = [[], [], [], []]
        school_dict[school_id]['id'] = [[], [], [], []]
        school_dict[school_id]['discarded'] = 0
        school_dict[school_id]['num'] = 0
    
    lvl = int(full_row[1][6])
    school_dict[school_id]['data'][lvl].append(full_row[12:])
    school_dict[school_id]['id'][lvl].append(student_id)
    school_dict[school_id]['num'] += 1


def get_sum(arr, i, j):
    sumt = 0
    for ind in range(i, j):
        sumt += int(arr[ind])

    return sumt

def give_ran(dict_inp, i, j):
    heap = []
    for ele in dict_inp:
        heappush(heap, (0 - dict_inp[ele]['scores'][i][j], ele))

    ran = 1
    while heap:
        ele = heappop(heap)
        dict_inp[ele[1]]['ran'][i][j] = ran
        ran += 1

    return

def int_to_str(inte, leng):
    ans = str(inte)
    while(len(ans)<leng):
        ans = "0" + ans

    return ans

with open('alldata.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            get_data(row)

new_sch_dict = {}

for ele in school_dict:
    data = school_dict[ele]['data']
    if(len(data[0])<=1 and len(data[1])<=1 and len(data[2])<=1 and len(data[3])<=1):
        continue

    new_sch_dict[ele] = {}
    new_sch_dict[ele]['discarded'] = school_dict[ele]['discarded']
    new_sch_dict[ele]['data'] = [[], [], [], []]
    new_sch_dict[ele]['id'] = [[], [], [], []]
    new_sch_dict[ele]['num'] = 0
    for i in range(4):
        lvl_data = school_dict[ele]['data'][i]
        lvl_id = school_dict[ele]['id'][i]
        if(len(lvl_data)<=1):
            continue
        new_sch_dict[ele]['num'] += len(lvl_data)
        for q, idl in zip(lvl_data, lvl_id):
            temp = []
            temp.append(get_sum(q, 0, 10))
            temp.append(get_sum(q, 10, 20))
            temp.append(get_sum(q, 20, 30))
            temp.append(get_sum(q, 30, 40))
            temp.append(get_sum(q, 40, 45))
            temp.append(get_sum(q, 0, 45))
            new_sch_dict[ele]['data'][i].append(temp)
            new_sch_dict[ele]['id'][i].append(idl)
    
    ttl_scr = []
    for i in range(4):
        scr_arr = [0, 0, 0, 0, 0, 0]
        temp = new_sch_dict[ele]['data'][i]
        if(len(temp)<=1):
            ttl_scr.append(scr_arr)
            continue
        for j in range(6):
            for stu in temp:
                scr_arr[j] += stu[j]

        for j in range(6):
            scr_arr[j] = scr_arr[j]/len(temp)
        ttl_scr.append(scr_arr)

    new_sch_dict[ele]['scores'] = ttl_scr
    new_sch_dict[ele]['ran'] = np.zeros((4, 6))


aver_scr = []
for i in range(4):
    lvl_avg = []
    for j in range(6):
        temp = 0
        templen = 0
        for ele in new_sch_dict:
            datalen = len(new_sch_dict[ele]['data'][i])
            if(datalen>=1):
                temp += new_sch_dict[ele]['scores'][i][j] * datalen
                templen += datalen
        temp = temp / templen
        lvl_avg.append(temp)
    aver_scr.append(lvl_avg)

for i in range(4):
    for j in range(6):
        give_ran(new_sch_dict, i, j)


ttl_disc = 0
student_num = 0

for school in new_sch_dict:
    ttl_disc += new_sch_dict[school]['discarded']
    student_num += new_sch_dict[school]['num']

# give_ran(new_sch_dict, 'overall', 5)

for school in new_sch_dict:
    ele = new_sch_dict[school]
    os.mkdir('data/' + str(school))
    file = open('data/' + str(school) + "/data.html", "w")

    file.write("<h1>General Information</h1>\n")
    file.write("<hr />\n")

    file.write("<p><b>School ID</b> : " + str(school) + "</p>\n")
    file.write("<br />\n")

    file.write("<p><b>Number of participants:</b></p>\n")
    file.write("<table>\n")
    file.write("<tr>\n")
    file.write("<td align=\"center\">Level 0</th> <td align=\"center\">Level 1</th> <td align=\"center\">Level 2</th> <td align=\"center\">Level 3</th> <td align=\"center\">Total </th>\n")
    file.write("</tr>\n")
    file.write("<tr>\n")
    file.write("<td align=\"center\">" + str(len(ele['data'][0])) + " </td> <td align=\"center\">" + str(len(ele['data'][1])) + " </td> <td align=\"center\">" + str(len(ele['data'][2])) + " </td> <td align=\"center\">" + str(len(ele['data'][3])) + " </td> <td align=\"center\">" + str(ele['num']) + "</td>\n")
    file.write("</tr>\n")
    file.write("</table>\n")

    file.write("<br />\n<br />\n\n")

    disc = ele['discarded']
    ttl = ele['num']
    file.write("<h1>Incorrectly Filled OMR</h1>\n")
    file.write("<hr />\n")
    file.write("<p><b>Percentage of students from this school who did not fill OMR correctly : </b>" + str(int(100*disc/(disc + ttl))) + "%</p>\n")
    file.write("<p><b>Overall Percentage of students who did not fill OMR correctly : </b>" + str(int(100*ttl_disc/(ttl_disc + student_num))) + "%</p>\n")

    if(disc/(disc + ttl) > ttl_disc/(ttl_disc + student_num)):
        file.write("<p><i>Remark -> The students need practise regarding how to properly fill OMR.</i></p>\n")

    file.write("<br />\n<br />\n")

    file.write("<h1> Level Wise Analysis </h1>\n")
    file.write("<hr />\n")

    for i in range(4):
        if(len(ele['data'][i])==0):
            continue

        attn = []
        file.write("<br/>\n")
        file.write("<h2>Level " + str(i) + "</h2>\n")

        file.write("<p><b>Performance Graph (Marks Distribution) : </b></p>\n")

        extr = [0, 200]
        for dtp in ele['data'][i]:
            if(dtp[5] > extr[0]):
                extr[0] = dtp[5]
            if(dtp[5] < extr[1]):
                extr[1] = dtp[5]

        y = np.zeros((extr[0] - extr[1])//5 + 2)
        for dtp in ele['data'][i]:
            y[(dtp[5]-extr[1])//5] += 1

        x = range(extr[1]//5, extr[0]//5)
        nar = []
        for xe in x:
            nar.append(5*xe)

        while(len(nar)!=len(y)):
            nar.append(nar[-1]+5)
        
        mpl_fig = plt.figure()
        ax = mpl_fig.add_subplot(111)
        ax.set_ylabel('Number of Students')
        ax.set_xlabel('Score')

        width = 4
        plt.bar(nar, y, width, color="blue")
        file_name = str(school) + "/chart" + str(i) + ".png"
        plt.savefig('data/' + file_name)

        plt.clf()

        file.write("<img src=\"../chart" + str(i) + ".png\" height=300 width=300>\n")

        lim = int(len(ele['data'][i])*0.05)
        if(lim>=3):
            file.write("<p><b>Star Performers (Top 5%) : </b></p>\n")
        else:
            lim = 3
            file.write("<p><b>Star Performers (Top 3) : </b></p>\n")

        file.write("<table>\n")
        file.write("<tr>\n")
        file.write("<td align=\"center\"> <i>Student ID</i> </td><td align=\"center\"> <i>Overall Score</i> </td>\n")
        file.write("</tr>\n")
        heap2 = []
        for ind in range(len(ele['data'][i])):
            temp = ele['data'][i][ind][5]
            heappush(heap2, (0-temp, ele['id'][i][ind]))

        for j in range(lim):
            file.write("<tr>\n")
            star = heappop(heap2)
            file.write("<td align=\"center\">" + int_to_str(star[1], 3) + "</td> <td align=\"center\">" + str(0 - star[0]) + "</td>\n")
            file.write("</tr>\n")

        file.write("</table>")

        file.write("\n\n")

        file.write("<p><b>Average Scores and School ranking : </p></b>\n")
        file.write("<table>\n")
        file.write("<tr>\n")
        file.write("<td align=\"center\"> <i>Skill Number</i> </td> <td align=\"center\"> <i>School Average</i> </td> <td align=\"center\"> <i>Olympiad Average</i> </td> <td align=\"center\"> <i>Rank</i> </td>\n")
        file.write("</tr>\n")
        for j in range(5):
            file.write("<tr>\n")
            file.write("<td align=\"center\">" + str(j+1) + "</td> <td align=\"center\">" + str(round(ele['scores'][i][j], 2)) + "</td> <td align=\"center\">" + str(round(aver_scr[i][j], 2)) + "</td> <td align=\"center\">" + str(int(ele['ran'][i][j])) + "</td>\n")
            if(ele['scores'][i][j] < aver_scr[i][j]):
                attn.append(j)
            file.write("</tr>\n")

        file.write("<tr>")
        file.write("<td align=\"center\"> Overall </td> <td align=\"center\">" + str(round(ele['scores'][i][5], 2)) + "</td> <td align=\"center\">" + str(round(aver_scr[i][5], 2)) + "</td> <td align=\"center\">" + str(int(ele['ran'][i][5])) + "</td>\n")
        file.write("</tr>")

        file.write("</table>\n")
        file.write("<br />\n")
        
        if(len(attn)>0):
            file.write("<p><i>Remark -> The students need attention in skill number : ")
            for at in attn:
                file.write(str(at+1) + " ")
            file.write("(below average performance) </i></p>\n")

        file.write("\n\n")