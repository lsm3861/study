from scipy import io
import numpy as np
import csv
import os
mat_file = io.loadmat('Voxel_input.mat')
voxel_array = np.array(mat_file['BW'])
#voxel_array.shape
#new_voxel_array = np.transpose(voxel_array, (1,2,0)) #matlab의 구조가 z,x,y 순서이므로 바꿔줘야함.
#new_voxel_array = np.transpose(voxel_array, (2,1,0))
#new_voxel_array = np.transpose(voxel_array, (1,0,2))
new_voxel_array = np.transpose(voxel_array, (2,0,1))  # 이걸로 성공
#new_voxel_array = np.transpose(voxel_array, (0,2,1))
#new_voxel_array.shape --> x=67, y=191, z=191 순서
#flatten = np.ravel(new_voxel_array, order='C')

#correct_voxel = np.flip(new_voxel_array,axis=0)  # 이거까지 해줘야 Z 방향이 맞는 줄 알았는데 아니었음.. 다시 주석 처리함

flatten = np.ravel(new_voxel_array, order='C')
split_box = []
for i in range(244422):
    temp = flatten[10*i:10*(i+1)]
    temp = np.array(temp)
    temp = temp.tolist()
    split_box.append(temp)
temp = flatten[2444220:]
temp = np.array(temp)
temp = temp.tolist()
split_box.append(temp)
split_box = np.array(split_box)
with open('MC_vox.txt', 'w') as f:
    writer = csv.writer(f, delimiter = ' ')
    writer.writerows(split_box)
text = open('MC_vox.txt', 'r+')
addspace = open('spaced_MC_vox.txt', 'w')
for line in text.readlines():
    addspace.write("     "+line)
addspace.close()
os.remove('MC_vox.txt')
print("done")