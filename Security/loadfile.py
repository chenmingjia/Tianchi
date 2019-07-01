import pandas as pd
import pickle
import numpy as np

train_path = r'./security_train.csv'
test_path = r'./security_test.csv'

def FileChunker(path):
    temp = pd.read_csv(path,engine='python',iterator=True)
    loop = True
    chunkSize = 10000
    chunks = []
    while loop:
        try:
            chunk = temp.get_chunk(chunkSize)
            chunks.append(chunk)
        except StopIteration:
            loop = False
            print("Iteration is stopped.")
    data = pd.concat(chunks, ignore_index= True,axis=0)
    return data

def read_train_file(path):
    labels = []
    files = []
    data = FileChunker(path)
    goup_fileid = data.groupby('file_id')
    for file_name, file_group in goup_fileid:
        print(file_name)
        file_labels = file_group['label'].values[0]
        result = file_group.sort_values(['tid', 'index'], ascending=True)
        api_sequence = ' '.join(result['api'])
        labels.append(file_labels)
        files.append(api_sequence)

    labels = np.asarray(labels)
    print(labels.shape)
    with open("security_train.csv.pkl", 'wb') as f:
        pickle.dump(labels, f)
        pickle.dump(files, f)


def read_test_file(path):
    names = []
    files = []
    data = FileChunker(path)
    goup_fileid = data.groupby('file_id')
    for file_name, file_group in goup_fileid:
        print(file_name)
        result = file_group.sort_values(['tid', 'index'], ascending=True)
        api_sequence = ' '.join(result['api'])
        names.append(file_name)
        files.append(api_sequence)

    with open("security_test.csv.pkl", 'wb') as f:
        pickle.dump(names, f)
        pickle.dump(files, f)

if __name__ == '__main__':
    print("read train file.....")
    read_train_file(train_path)
    print("read test file......")
    read_test_file(test_path)
