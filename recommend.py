import csv
import numpy as np
import matplotlib.pyplot as plt
import random

def skill_count(arr, st, end):
	count = 0
	for ele in arr:
		if(ele<end and ele>=st):
			count += 1

	return count

def update_scr_num(inp, scr, st, end):
	skc = skill_count(inp, st, end)
	for i in range(st, end):
		scr[i] -= (skc - len(inp)/5)

	return

def get_mar(arr, res, st, end, score, diff_thr, med_thr):
	ttl_scr = 0
	max_scr = 0
	for ele, eler in zip(arr, res):
		if(ele<end and ele>=st):
			if(score[ele]<diff_thr):
				curr_scr = 3
			elif(score[ele]<med_thr):
				curr_scr = 2
			else:
				curr_scr = 1
			max_scr += curr_scr
			ttl_scr += curr_scr*eler

	if(max_scr==0):
		return 0
	return ttl_scr/max_scr

def update_scr_diff(inp_ques, inp_resp, st, end, score, diff_thr, med_thr, scrs):
	s1mar = get_mar(inp_ques, inp_resp, st, end, score, diff_thr, med_thr)
	for i in range(st, end):
		if(s1mar < diff_thr):
			if(score[i] < diff_thr):
				scrs[i] -= 2
			elif(score[i] < med_thr):
				scrs[i] -= 1
			else:
				scrs[i] -= 0
		elif(s1mar < med_thr):
			if(score[i] < diff_thr):
				scrs[i] -= 1
			elif(score[i] < med_thr):
				scrs[i] -= 0
			else:
				scrs[i] -= 1
		else:
			if(score[i] < diff_thr):
				scrs[i] -= 0
			elif(score[i] < med_thr):
				scrs[i] -= 1
			else:
				scrs[i] -= 2

	return

full_data = []

with open('alldata.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
		else:
			temp_data = []
			for ele in row[12:]:
				if(ele=='0'):
					temp_data.append(0)
				else:
					temp_data.append(1)
			full_data.append(temp_data)

full_data = np.array(full_data)

diff_thr = 0.2
med_thr = 0.4

score = np.sum(full_data, axis=0)
score = score / len(full_data)

for ele in score:
	if(ele<0.2):
		plt.plot(ele, 5, 'ro', color='red')
	elif(ele<0.38):
		plt.plot(ele, 5, 'ro', color='blue')
	else:
		plt.plot(ele, 5, 'ro', color='green')

plt.show()

exit()

inp_ques = [16, 19, 30, 7, 5, 33, 25, 42, 9, 2]
inp_resp = [ 0,  0,  1, 1, 1,  1,  1,  1, 1, 1]


new_ques = []
for ele in inp_ques:
	new_ques.append(ele)

for i in range(10):
	scrs = np.zeros((45))
	for ele in new_ques:
		scrs[ele] -= float('inf')

	update_scr_num(new_ques, scrs, 0, 10)
	update_scr_num(new_ques, scrs, 10, 20)
	update_scr_num(new_ques, scrs, 20, 30)
	update_scr_num(new_ques, scrs, 30, 40)
	update_scr_num(new_ques, scrs, 40, 45)

	update_scr_diff(inp_ques, inp_resp, 0, 10, score, diff_thr, med_thr, scrs)
	update_scr_diff(inp_ques, inp_resp, 10, 20, score, diff_thr, med_thr, scrs)
	update_scr_diff(inp_ques, inp_resp, 20, 30, score, diff_thr, med_thr, scrs)
	update_scr_diff(inp_ques, inp_resp, 30, 40, score, diff_thr, med_thr, scrs)
	update_scr_diff(inp_ques, inp_resp, 40, 45, score, diff_thr, med_thr, scrs)

	# print(scrs)

	max_val = -1*float('inf')
	for j in range(45):
		if(scrs[j]>max_val):
			max_val = scrs[j]

	max_ind = []
	for j in range(45):
		if(scrs[j]==max_val):
			max_ind.append(j)

	ans_ind = random.randint(0, len(max_ind)-1)
	new_ques.append(max_ind[ans_ind])

def get_skill(inp_arr):
	ans_arr = []
	for ele in inp_arr:
		ans_arr.append(int(ele/10))

	return ans_arr

def get_diff(inp_arr, scr):
	global diff_thr
	global med_thr

	ans_arr = []
	for ele in inp_arr:
		if(scr[ele] < diff_thr):
			ans_arr.append(2)
		elif(scr[ele] < med_thr):
			ans_arr.append(1)
		else:
			ans_arr.append(0)

	return ans_arr

print("Questions")
print(inp_ques)
print("Response")
print(inp_resp)
print("Skill Index")
print(get_skill(inp_ques))
print("Difficulty Index")
print(get_diff(inp_ques, score))
print("\n\n")
print("New Questions")
print(new_ques)
print("Skill Index")
print(get_skill(new_ques))
print("Difficulty Index")
print(get_diff(new_ques, score))