import os
import csv
import glob
import pickle
import re

file_dict = {}
caption_dict = {}
data_list = []

key_set = []
key_index = 0

with open('data.csv', newline='') as f:
	csv_reader = csv.reader(f)
	rows = list(csv_reader)
	for row in rows[1:]:
		try:
			key = int(row[0])
			key_set.append(key)
		except Exception as e:
			break
		caption_dict[key] = [
			{
				'question': 'What is the meaning of the car warning light?',
				'answer': f'{row[3]}',
			},
			{
				'question': 'Why does the car warning light turn on?',
				'answer': f'{row[4]}',
			},
			{
				'question': 'How can I fix the problem about that car warning light?',
				'answer': f'{row[5]}',
			},
		]

count = 0
key_set.sort()
for image_file in sorted(glob.glob('images/**/*.jpg') + glob.glob('images/**/*.png')):
	while key_index < len(key_set):
		cur_key = key_set[key_index]
		if os.path.basename(image_file).startswith(str(cur_key)):
			if cur_key in file_dict:
				file_dict[cur_key].append(image_file)
			else:
				file_dict[cur_key] = [image_file]
			count += 1
			break
		else:
			key_index += 1

print(len(glob.glob('images/**/*.jpg') + glob.glob('images/**/*.png')))
print(count)

for k, v in file_dict.items():
	for image_file in v:
		basename = os.path.basename(image_file)
		id, _ = os.path.splitext(basename)
		for caption in caption_dict[k]:
			data_list.append({
				'id': id,
				'question': caption['question'],
				'answer': caption['answer'],
				'image': os.path.join('carwarning', image_file)
			})

print(len(data_list))
with open('data.pkl', 'wb') as f:
	pickle.dump(data_list, f)

with open('data.pkl', 'rb') as f:
	load_data_list = pickle.load(f)
