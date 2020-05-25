'''
This is a module file.
0. Pre-exist files: pbs_sh original file, input files(n#), MCserver_edit_run.py
1. File writing(vim, i, :wq!): pbs_sh original--(editing with "input files")--> pbs_sh_i.sh
2. Run each pbs_sh_i.sh files: "source" those pbs_sh_i.sh files
3. Making graphs
4. Sending message via Slack
'''
import os
import matplotlib.pyplot as plt
import json
import requests
import slacker

from edit_output_v1 import enumerate_frequency, savefig_LESpectrum, savefig_DDistribution

MEAN_CHORD = [0.2, 0.333, 0.667, 1.533]
COLOR = ['k', 'g', 'b', 'r']
LABEL = ['0.3um', '0.5um', '1um', '2.3um']

def vim_pbs(pbs_sh_original: str, input_file: str, input_order: int):
    forward_find = '# Run the parallel MPI executable "mg.B.8"'
    backward_find = '#/usr/local/mpich/sbin/cleanipcs'
    with open(pbs_sh_original, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if forward_find in line:
                break
        previous_block = [line for line in (lines[:i + 1])]
        backward_block = [line for line in (lines[i:])]
    for i, line in enumerate(backward_block):
        if backward_find in line:
            break
    backward_block = [line for line in (backward_block[i - 1:])]
    insert_block = 'mpirun -v -machinefile $PBS_NODEFILE -np $NPROCS mcnp6.mpi i=' \
                   + str(input_file) + '.txt o=' + str(input_file) + '.out r=' + str(input_file) + '.run'
    new_pbs_sh = 'pbs_sh_' + str(input_order) + '.sh'
    with open(new_pbs_sh, 'w') as f:
        for item in previous_block:
            f.write(item)
    with open(new_pbs_sh, 'a') as f:
        f.write(insert_block)
        f.write('\t')
    with open(new_pbs_sh, 'a') as f:
        for item in backward_block:
            f.write(item)
    return str(new_pbs_sh)


def run_shscr(new_pbs_sh: str):
    run_command = 'qsub ./' + new_pbs_sh
    os.system(run_command)
    print("its running")
    return 0


def enumerate_outputs_v1(source: str, outputs: list, tally_total: int,
                         mean_chord: list = None,
                         color: list= None,
                         label: list=None):
    # output을 하나의 list로 받아와서.
    #### beaware to check the nps number
    # v0에서의 files가 outputs과 same.
    if mean_chord is None:
        mean_chord = MEAN_CHORD
    if color is None:
        color = COLOR
    if label is None:
        label = LABEL
    energy_tot, frequency_tot, y_i_tot, ydy_i_tot, c_tot = [], [], [], [], []
    for i in range(len(outputs)):
        energy, frequency = enumerate_frequency(tally_num=tally_total,
                                                txt_path=outputs[i],
                                                mean_chord=mean_chord[i])
        energy_tot.append(energy)
        frequency_tot.append(frequency)
    LE_spectrum = savefig_LESpectrum(energy_tot, frequency_tot, color, label, source)
    D_Distribution = savefig_DDistribution(energy_tot, frequency_tot, color, label, source)
    messages = 'Finished!' + str(source)
    return LE_spectrum, D_Distribution, messages, energy_tot, frequency_tot

def send_msg(token: str, channel: str, messages: str, LE_spectrum, D_Distribution):
    # LE_spectrum, D_Distribution name including ".png"
    slack = slacker.Slacker(token)
    # send message
    slack.chat.post_message(channel, messages)
    # file upload
    slack.files.upload(file_=LE_spectrum, channels=channel)
    slack.files.upload(file_=D_Distribution, channels=channel)
    return messages

if __name__ == "__main__":
    '''
    pbs_sh_original = 'pbs_sh.sh'
    input_file = 'co_03_v3'

    for i in range(1):
        input_order = int(i)
        new_pbs_sh = vim_pbs(pbs_sh_original, input_file, input_order)
        run = run_shscr(new_pbs_sh)

    # run = run_shscr('test.sh')
    '''
    token = 'xoxb-1106300421636-1085393487431-j0WSrplKcUx6a57IBaeri8Up'
    channel = '#experiments_results'
    LE_spectrum = 'Lineal_Energy_Spectrum_Cs137.png'
    D_Distribution = 'Dose_Distribution_Cs137.png'
    messages = 'Finished!'
    #send_msg(token, channel, messages, LE_spectrum, D_Distribution)