import json
import sys
import pandas as pd
from tqdm import tqdm
from parse import *


def main(arg):
    if '.csv' in arg:
        df = pd.read_csv(arg)
        dlg_num = df.dlg_id.value_counts().shape[0]
        all_data = {}
        for i in tqdm(range(dlg_num)):
            dlg_id = "dlg_id"+str(i)
            dialog = Dialogue(df, i)
            corpus = dialog.get_manager_replicas()
            dlg_data = {'greeting': get_greeting(corpus)}
            dlg_data.update(get_manager_name(corpus))
            dlg_data.update({'company_name': get_company_name(corpus)})
            dlg_data.update({'farewell': get_farewell(corpus)})
            dlg_data.update({'requirement': bool(dlg_data['greeting']) and bool(dlg_data['farewell'])})
            all_data.update({dlg_id: dlg_data})

        all_data = json.dumps(all_data)
        all_data = json.loads(str(all_data))
        filename = arg.split('.')[0]+"_extracted_data.json"
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(all_data, file, indent=4, ensure_ascii=False)

        print("Done")
    else:
        sys.exit("csv-file is expected")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit("too many arguments")
    elif len(sys.argv) < 2:
        sys.exit("too few arguments")
    else:
        main(sys.argv[1])
