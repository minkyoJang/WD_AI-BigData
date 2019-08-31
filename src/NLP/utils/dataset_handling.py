import pandas as pd
import numpy as np


def merge_all_dataset(filename):
    '''
    데이터셋 merge 함수
    `filename (1~).csv`으로 시작하는 모든 파일을 하나로 합쳐서 저장합니다.
    comment 컬럼의 NaN 값을 'None' 텍스트로 채웁니다.
    디렉토리 경로를 입력받습니다.
    '''
    datasets = pd.DataFrame()
    i = 0
    while True:
        try:
            i += 1
            dump = pd.read_csv("{} ({}).csv".format(filename, i), engine='python')
            datasets = pd.concat([datasets, dump])
        except FileNotFoundError:
            break

    datasets.comment.fillna('None', inplace=True)
    datasets.reset_index(drop=True, inplace=True)

    return datasets


if __name__ == '__main__':
    merge_all_dataset('labeled')
