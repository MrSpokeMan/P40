import os

def rename():
    for dir in os.listdir('dataset'):
        for id, file in enumerate(os.listdir(f'dataset/{dir}')):
            os.rename(f'dataset/{dir}/{file}', f'dataset/{dir}/czw_RP7_osfi_{id}_{dir}.jpg')
        

if __name__ == '__main__':
    rename()